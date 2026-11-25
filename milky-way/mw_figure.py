"""The paper's Milky Way figure (Section 6), as a vector PDF in figures/fig_milky_way.pdf:
(a) the rotation curve (Eilers et al. 2019) and (b)-(d) the vertical speed spread of Zhang et al.'s three
populations of stars (via Lisanti et al. 2023), with the three accounts fitted to the same data:
cold dark matter, a force parallel to the baryons' own (the superfluid class) and the eddy of Section 6.
Reads best_fits.json (Lisanti et al.'s data fits). Run after mw_fit_zhang.py.
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import mw_fit as F
import mw_fit_zhang as Z
import mw_data as D

HERE = os.path.dirname(os.path.abspath(__file__))
BLUE, AQUA, INK, INK2, GRID = "#2a78d6", "#1baf7a", "#0b0b0b", "#52514e", "#e4e3df"
MODELS = (("cdm", INK2, "--", "cold dark matter"), ("parallel", BLUE, "-", "force parallel to the baryons"),
          ("eddy", AQUA, "-", "eddy of Equation 15"))


def style():
    for f in font_manager.findSystemFonts():
        if "texgyretermes" in f.lower():
            font_manager.fontManager.addfont(f)
    fams = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": "serif",
                         "font.serif": (["TeX Gyre Termes"] if "TeX Gyre Termes" in fams else []) + ["DejaVu Serif"],
                         "mathtext.fontset": "stix", "font.size": 9, "axes.edgecolor": INK2,
                         "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 3,
                         "legend.frameon": False})


def vcirc(model, th, R):
    p = dict(zip(F.BARYON_KEYS, th[:6])); extra = th[6:]
    aR, _ = F.acc_baryon(R, np.zeros_like(R), p)
    if model == "cdm":
        aR = aR + F.sph_acc(R, 0 * R, F.nfw_g(*extra))[0]
    elif model == "parallel":
        aR = aR * F.rar_nu(np.abs(aR) / (extra[0] * F.GDAG_UNIT))
    else:
        g = F.eddy_g(sum(F.masses(p)), extra[0], F.DEFAULT_FORM, p)[0]
        aR = aR + F.sph_acc(R, 0 * R, g)[0]
    return np.sqrt(np.maximum(-aR * R, 0))


def main():
    style()
    best = json.load(open(os.path.join(HERE, "best_fits.json")))
    fig, axs = plt.subplots(1, 4, figsize=(6.6, 2.3), gridspec_kw=dict(width_ratios=[1.35, 1, 1, 1]))
    R = np.linspace(4.8, 18.5, 120); zz = np.linspace(0.33, 1.18, 40)
    axs[0].errorbar(D.RC_R, D.RC_V, D.RC_ERR, fmt="o", ms=2.4, color=INK, elinewidth=0.7, label="measured")
    for m, col, ls, lab in MODELS:
        x = np.array(best["lisanti_" + m]); th = x[:-3]
        chi = Z.chi2(x, m)
        z = 4 if m == "cdm" else 3
        axs[0].plot(R, vcirc(m, th, R), color=col, ls=ls, lw=1.4, zorder=z, label=f"{lab} ($\\chi^2$ {chi:.0f})")
        az = Z.az_column(m, th)
        for a, (k, h) in zip(axs[1:], zip(Z.POPS, x[-3:])):
            a.plot(zz, Z.sigma_model(az, zz, h), color=col, ls=ls, lw=1.4, zorder=z)
    axs[0].set_xlabel("radius (kpc)"); axs[0].set_ylabel("rotation speed (km s$^{-1}$)")
    axs[0].set_ylim(185, 245); axs[0].grid(color=GRID, lw=0.6)
    axs[0].legend(fontsize=5.6, loc="lower left", handlelength=1.6)
    axs[0].text(0.03, 0.97, "(a)", transform=axs[0].transAxes, va="top", fontsize=8.5)
    names = {"rich": "metal-rich", "int": "intermediate", "poor": "metal-poor"}
    for a, k, lab in zip(axs[1:], Z.POPS, "bcd"):
        zs, s, e = Z.SDAT[k].T
        a.errorbar(zs, s, e, fmt="o", ms=2.4, color=INK, elinewidth=0.7)
        a.set_xlabel("height $z$ (kpc)"); a.grid(color=GRID, lw=0.6)
        a.text(0.04, 0.97, f"({lab}) {names[k]}", transform=a.transAxes, va="top", fontsize=7.5)
    axs[1].set_ylabel(r"vertical speed spread $\sigma_z$ (km s$^{-1}$)")
    fig.tight_layout(pad=0.3, w_pad=0.6)
    os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
    fig.savefig(os.path.join(HERE, "figures", "fig_milky_way.pdf"))
    print("wrote figures/fig_milky_way.pdf")


if __name__ == "__main__":
    main()
