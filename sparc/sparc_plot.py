"""Figure for the SPARC test: (a) DDO 154 with the radial acceleration relation, the eddy of Eq. 15
and the eddy shaped by the mass inside each radius, all at the limit 1.20; (b) each galaxy's own
best limit against how far its stars spread beyond the eddy's core R_t.  Writes results/sparc_test.png.
Run after sparc_fit.py (plain and "enclosed") and sparc_report.py (the same):  python3 sparc_plot.py
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sparc_data as S
import sparc_fit as F

HERE = os.path.dirname(os.path.abspath(__file__))
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"   # categorical slots 1, 2 and 3
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def main():
    d = np.load(os.path.join(HERE, "results", "profiles.npz"))
    s = json.load(open(os.path.join(HERE, "results", "summary.json")))
    de = np.load(os.path.join(HERE, "results", "profiles_enclosed.npz"))
    se = json.load(open(os.path.join(HERE, "results", "summary_enclosed.json")))
    RUNS = (("rar", "cored", BLUE, "radial acceleration relation", d, s),
            ("eddy", "cored", ORANGE, "eddy, Eq. 15 (total mass)", d, s),
            ("eddy", "enclosed", AQUA, "eddy, mass inside each radius", de, se))
    G = {g["name"]: g for g in S.load()}
    plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                         "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.4), facecolor="#fcfcfb")

    # (a) DDO 154, each model at its fit with the limit 1.20, drawn through the measured radii
    n = "DDO154"; g = G[n]
    a1.errorbar(g["R"], g["Vobs"], yerr=g["eV"], fmt="o", ms=4, color=INK, ecolor=INK2, elinewidth=1,
                capsize=0, label="measured", zorder=3)
    for model, form, col, lab, dd, ss in RUNS:
        i = list(dd["names"]).index(n)
        nb = 4 if g["has_bul"] else 3
        th = dd[model + "_TH"][i, F.I0][:nb]
        F.FORM = form
        gobs, sig, gm = F.model_g(g, th, F.LGRID[F.I0], model)
        lud, lub, D, inc = F.unpack(g, th)
        Vm = np.sqrt(np.maximum(gm * g["R"] * D / g["D"], 0)) * np.sin(np.radians(inc)) / np.sin(np.radians(g["inc"]))
        chinu = ss[model]["per_galaxy"][n]["chi2nu_120"]
        a1.plot(g["R"], Vm, color=col, lw=2, label=f"{lab}, $\\chi^2_\\nu$ = {chinu:.1f}")
    a1.set_xlabel("radius (kpc)"); a1.set_ylabel("rotation speed (km/s)")
    a1.set_title("DDO 154, gas-rich dwarf, all at $g_\\dagger$ = 1.20", color=INK, fontsize=10, loc="left")
    a1.grid(color=GRID, lw=0.8); a1.set_ylim(0, None); a1.legend(frameon=False, fontsize=8.5, loc="lower right")

    # (b) each galaxy's own limit against R_disk / R_t
    for model, form, col, lab, dd, ss in RUNS:
        xs, ys = [], []
        for nm, v in ss[model]["per_galaxy"].items():
            gg = G[nm]
            if not v["sel"] or np.isnan(v["lo"]) or np.isnan(v["hi"]):
                continue
            Mb = 0.5 * gg["Ldisk"] + 0.7 * gg["Lbul"] + gg["Mgas"]
            Rt = np.sqrt(S.G * Mb / (1.2 * S.GDAG_UNIT))
            xs.append(np.log10(gg["Rdisk"] / Rt)); ys.append(v["lg"])
        xs, ys = np.array(xs), np.array(ys)
        a2.scatter(xs, 10 ** ys, s=12, color=col, alpha=0.45, edgecolors="none", label=lab)
        # running median
        b = np.quantile(xs, np.linspace(0, 1, 7))
        mx = [np.median(xs[(xs >= b[k]) & (xs <= b[k + 1])]) for k in range(6)]
        my = [10 ** np.median(ys[(xs >= b[k]) & (xs <= b[k + 1])]) for k in range(6)]
        a2.plot(mx, my, color=col, lw=2.5)
    a2.axhline(1.20, color=INK2, lw=1, ls="--")
    a2.text(0.55, 1.28, "measured 1.20", color=INK2, fontsize=9, ha="right")
    a2.set_yscale("log"); a2.set_ylim(0.03, 30)
    a2.set_xlabel("log (disk scale length / eddy core $R_t$)")
    a2.set_ylabel("galaxy's own best $g_\\dagger$ ($10^{-10}$ m/s$^2$)")
    a2.set_title("Each galaxy's own limit, about 150 galaxies; lines are running medians",
                 color=INK, fontsize=10, loc="left")
    a2.grid(color=GRID, lw=0.8, which="major"); a2.legend(frameon=False, fontsize=9, loc="upper right")
    fig.tight_layout()
    out = os.path.join(HERE, "results", "sparc_test.png")
    fig.savefig(out, dpi=150, facecolor=fig.get_facecolor())
    print("wrote", out)


if __name__ == "__main__":
    main()
