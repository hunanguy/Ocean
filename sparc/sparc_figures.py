"""The paper's SPARC figures (Section 6), as vector PDFs in figures/.

  fig_sparc.pdf       (a) DDO 154 with the radial acceleration relation, the eddy set by the total mass
                          alone (Equation 15 of versions 3.13-3.15) and the eddy of Section 6, all with
                          the limit 1.20; (b) each galaxy's own best limit against its mass of stars and
                          gas, with running medians.
  fig_free_share.pdf  the share of Ocean left free to build the eddy, read off the measured speeds,
                          against the second relation of Equation 15.

Run after sparc_fit.py, sparc_report.py, sparc_fit.py cored and sparc_report.py cored.
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import sparc_data as S
import sparc_fit as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"      # categorical slots 1, 2, 3
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"


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


def load(form):
    tag = "" if form == F.DEFAULT_FORM else "_" + form.replace("/", "_over_")
    d = np.load(os.path.join(HERE, "results", "profiles" + tag + ".npz"))
    s = json.load(open(os.path.join(HERE, "results", "summary" + tag + ".json")))
    return d, s


def curve_through_points(g, d, model, form, k):
    """Model rotation speed at the measured radii, in the measurement's distance and tilt."""
    i = list(d["names"]).index(g["name"])
    th = d[model + "_TH"][i, k][:4 if g["has_bul"] else 3]
    F.FORM = form
    gobs, sig, gm = F.model_g(g, th, F.LGRID[k], model)
    lud, lub, D, inc = F.unpack(g, th)
    return np.sqrt(np.maximum(gm * g["R"] * D / g["D"], 0)) * np.sin(np.radians(inc)) / np.sin(np.radians(g["inc"]))


def fig_sparc(G):
    dl, sl = load(F.DEFAULT_FORM)
    dc, sc = load("cored")
    runs = (("rar", F.DEFAULT_FORM, BLUE, "radial acceleration relation", dl, sl),
            ("eddy", "cored", ORANGE, "eddy set by the total mass alone", dc, sc),
            ("eddy", F.DEFAULT_FORM, AQUA, "eddy of Equation 15", dl, sl))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.75))
    g = G["DDO154"]
    a1.errorbar(g["R"], g["Vobs"], yerr=g["eV"], fmt="o", ms=3, color=INK, ecolor=INK2, elinewidth=0.8,
                capsize=0, label="measured", zorder=3)
    for model, form, col, lab, dd, ss in runs:
        V = curve_through_points(g, dd, model, form, F.I0)
        chinu = ss[model]["per_galaxy"]["DDO154"]["chi2nu_120"]
        a1.plot(g["R"], V, color=col, lw=1.6, label=f"{lab}, $\\chi^2_\\nu$ {chinu:.1f}")
    a1.set_xlabel("radius (kpc)"); a1.set_ylabel("rotation speed (km s$^{-1}$)")
    a1.set_ylim(0, 58); a1.grid(color=GRID, lw=0.6)
    a1.legend(fontsize=6.8, loc="lower right", handlelength=1.6)
    a1.text(0.02, 0.97, "(a) DDO 154, limit 1.20", transform=a1.transAxes, va="top", fontsize=8.5)
    for model, form, col, lab, dd, ss in runs:
        xs, ys = [], []
        for nm, v in ss[model]["per_galaxy"].items():
            gg = G[nm]
            if not v["sel"] or np.isnan(v["lo"]) or np.isnan(v["hi"]):
                continue
            xs.append(np.log10(0.5 * gg["Ldisk"] + 0.7 * gg["Lbul"] + gg["Mgas"])); ys.append(v["lg"])
        xs, ys = np.array(xs), np.array(ys)
        a2.scatter(xs, 10 ** ys, s=6, color=col, alpha=0.35, edgecolors="none")
        b = np.quantile(xs, np.linspace(0, 1, 7))
        mx = [np.median(xs[(xs >= b[j]) & (xs <= b[j + 1])]) for j in range(6)]
        my = [10 ** np.median(ys[(xs >= b[j]) & (xs <= b[j + 1])]) for j in range(6)]
        a2.plot(mx, my, color=col, lw=2.0, label=lab)
    a2.axhline(1.20, color=INK2, lw=0.8, ls="--")
    a2.text(7.75, 1.32, "measured 1.20", color=INK2, fontsize=7, ha="left")
    a2.set_yscale("log"); a2.set_ylim(0.05, 20)
    a2.set_xlabel(r"stars and gas, $\log_{10}(M_b/M_\odot)$")
    a2.set_ylabel(r"galaxy's own best $g_\dagger$ ($10^{-10}$ m s$^{-2}$)")
    a2.grid(color=GRID, lw=0.6)
    a2.text(0.02, 0.97, "(b) each galaxy's own limit", transform=a2.transAxes, va="top", fontsize=8.5)
    a2.legend(fontsize=6.8, loc="lower right", handlelength=1.6)
    fig.tight_layout(pad=0.4, w_pad=1.2)
    fig.savefig(os.path.join(OUT, "fig_sparc.pdf"))
    plt.close(fig)


def fig_free(G):
    d, s = load(F.DEFAULT_FORM)
    F.FORM = F.DEFAULT_FORM
    lg, names = d["lgrid"], list(d["names"])
    kb = int(np.argmin(np.abs(lg - s["eddy"]["shared_lg"][0]))); gd = 10 ** lg[kb] * S.GDAG_UNIT
    Y, FR = [], []
    for i, n in enumerate(names):
        g = G[n]
        if not (g["Q"] < 3 and g["inc"] >= 30):
            continue
        th = d["eddy_TH"][i, kb][:4 if g["has_bul"] else 3]
        gobs, sig, gm = F.model_g(g, th, lg[kb], "eddy")
        lud, lub, D, inc = F.unpack(g, th); fD = D / g["D"]; R = g["R"] * fD
        gbar = (g["Vgas"] * np.abs(g["Vgas"]) + 10 ** lud * g["Vdisk"] * np.abs(g["Vdisk"])
                + 10 ** lub * g["Vbul"] * np.abs(g["Vbul"])) * fD / R
        Mr = 10 ** lud * g["Menc_disk"] + 10 ** lub * g["Menc_bul"] + g["Menc_gas"]
        gN = S.G * Mr * fD ** 2 / R ** 2
        ok = (g["eV"] / g["Vobs"] < 0.1) & (gN > 0)
        Y += list(gN[ok] / gd); FR += list(((gobs - gbar) / np.sqrt(gN * gd))[ok])
    Y, FR = np.array(Y), np.array(FR)
    edges = 10 ** np.arange(-1.75, 1.51, 0.25)
    xc, med, lo, hi = [], [], [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (Y >= a) & (Y < b)
        if m.sum() < 20:
            continue
        xc.append(np.sqrt(a * b)); q = np.percentile(FR[m], [16, 50, 84]); lo.append(q[0]); med.append(q[1]); hi.append(q[2])
    y = np.logspace(-2, 1.7, 300)
    fig, ax = plt.subplots(figsize=(3.3, 2.5))
    ax.fill_between(xc, lo, hi, color=INK2, alpha=0.15, lw=0, label="measured, middle 68%")
    ax.plot(xc, med, "o", ms=3.2, color=INK, label="measured, median")
    ax.plot(y, F.free_share(y, F.DEFAULT_FORM), color=AQUA, lw=1.8, label="Equation 15")
    ax.axvline(1, color=INK2, lw=0.6, ls=":"); ax.axhline(0.5, color=INK2, lw=0.6, ls=":")
    ax.set_xscale("log"); ax.set_xlim(0.015, 40); ax.set_ylim(-0.25, 1.25)
    ax.set_xlabel(r"galaxy's own turning over the limit, $g_N/g_\dagger$")
    ax.set_ylabel("share of Ocean left free")
    ax.grid(color=GRID, lw=0.6); ax.legend(fontsize=6.8, loc="lower left")
    fig.tight_layout(pad=0.4)
    fig.savefig(os.path.join(OUT, "fig_free_share.pdf"))
    plt.close(fig)
    return float(10 ** lg[kb]), int(Y.size)


def main():
    os.makedirs(OUT, exist_ok=True)
    style()
    G = {g["name"]: g for g in S.load()}
    fig_sparc(G)
    lim, n = fig_free(G)
    print(f"wrote figures/fig_sparc.pdf and figures/fig_free_share.pdf (shared limit {lim:.2f}, {n} points)")


if __name__ == "__main__":
    main()
