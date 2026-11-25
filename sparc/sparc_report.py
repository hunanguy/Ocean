"""Summarize results/profiles.npz: one shared limit, the limit free galaxy by galaxy,
residual scatter, and trends of the per-galaxy limit with the galaxy's properties.
Writes results/summary.json and prints a report.  Run:  python3 sparc_report.py
(a comparison form: python3 sparc_report.py cored, after python3 sparc_fit.py cored)
"""
import os
import json
import numpy as np
from scipy.stats import spearmanr
import sparc_data as S
import sparc_fit as F

HERE = os.path.dirname(os.path.abspath(__file__))


def interval(lg, P):
    """Profile minimum and the Delta(-2 ln P) = 1 interval on the grid (linear interpolation)."""
    k = int(np.argmin(P)); m = P[k]
    def cross(rng):
        for j in rng:
            if P[j] - m >= 1:
                j0 = j - 1 if rng.step > 0 else j + 1
                t = (m + 1 - P[j0]) / (P[j] - P[j0])
                return lg[j0] + t * (lg[j] - lg[j0])
        return np.nan                       # open at the grid's edge
    return lg[k], cross(range(k + 1, len(lg), 1)), cross(range(k - 1, -1, -1)), k


def main(form=F.DEFAULT_FORM):
    tag_ = "" if form == F.DEFAULT_FORM else "_" + form.replace("/", "_over_")
    models = ("rar", "eddy") if form == F.DEFAULT_FORM else ("eddy",)
    F.FORM = form
    d = np.load(os.path.join(HERE, "results", "profiles" + tag_ + ".npz"))
    lg, names = d["lgrid"], list(d["names"])
    gals = {g["name"]: g for g in S.load()}
    G = [gals[n] for n in names]
    sel = np.array([g["Q"] < 3 and g["inc"] >= 30 for g in G])
    npar = np.array([4 if g["has_bul"] else 3 for g in G])
    npt = np.array([len(g["R"]) for g in G])
    summary = {"n_all": len(G), "n_sel": int(sel.sum()), "points_sel": int(npt[sel].sum())}

    for model in models:
        P, C, TH = d[model + "_P"], d[model + "_C"], d[model + "_TH"]
        s = {}
        # one shared limit
        tot = P[sel].sum(axis=0)
        lb, hi, lo, kb = interval(lg, tot)
        s["shared_lg"] = [float(lb), float(lo), float(hi)]
        s["shared_gdag"] = float(10 ** lb)
        for tag, k in (("at_1.20", F.I0), ("at_shared", kb)):
            chinu = C[:, k] / np.maximum(npt - npar, 1)
            s[tag] = dict(
                chi2_total=float(C[sel, k].sum()), dof=int((npt - npar)[sel].sum()),
                chi2nu_median=float(np.median(chinu[sel])),
                frac_chi2nu_lt_1_5=float(np.mean(chinu[sel] < 1.5)),
                frac_chi2nu_lt_3=float(np.mean(chinu[sel] < 3)),
                frac_chi2nu_gt_10=float(np.mean(chinu[sel] > 10)))
        # residual rms in dex on points with dV/V < 0.1 (as Li et al.), at the limit 1.20,
        # at the shared best limit, and with each galaxy at its own best limit
        kown = np.argmin(P, axis=1)
        def resid(kk):
            res, gb = [], []
            for i, g in enumerate(G):
                if not sel[i]:
                    continue
                k = kk if np.isscalar(kk) else kk[i]
                th = TH[i, k][:npar[i]]
                gobs, sig, gm = F.model_g(g, th, lg[k], model)
                lud, lub, D, inc = F.unpack(g, th)
                fD = D / g["D"]
                gbar = (g["Vgas"] * np.abs(g["Vgas"]) + 10 ** lud * g["Vdisk"] * np.abs(g["Vdisk"])
                        + 10 ** lub * g["Vbul"] * np.abs(g["Vbul"])) / g["R"]
                ok = (g["eV"] / g["Vobs"] < 0.1) & (gm > 0) & (gobs > 0) & (gbar > 0)
                res.append(np.log10(gobs[ok]) - np.log10(gm[ok])); gb.append(np.log10(gbar[ok] / S.GDAG_UNIT * 1e-10))
            return np.concatenate(res), np.concatenate(gb)
        res, gb = resid(F.I0)
        s["resid_points"] = int(res.size)
        s["resid_rms_dex"] = float(np.sqrt(np.mean(res ** 2)))
        s["resid_mean_dex"] = float(np.mean(res))
        s["resid_rms_dex_shared"] = float(np.sqrt(np.mean(resid(kb)[0] ** 2)))
        s["resid_rms_dex_own"] = float(np.sqrt(np.mean(resid(kown)[0] ** 2)))
        # mean residual in bins of log g_bar (m/s^2), at the limit 1.20
        edges = np.arange(-12.5, -8.49, 0.5)
        s["resid_by_gbar_1.20"] = [[float(edges[j]), float(edges[j + 1]), int(np.sum((gb >= edges[j]) & (gb < edges[j + 1]))),
                                    float(np.mean(res[(gb >= edges[j]) & (gb < edges[j + 1])])) if np.any((gb >= edges[j]) & (gb < edges[j + 1])) else None]
                                   for j in range(len(edges) - 1)]
        chinu_own_all = C[np.arange(len(G)), kown] / np.maximum(npt - npar - 1, 1)
        s["own_limit"] = dict(chi2_total=float(C[np.arange(len(G)), kown][sel].sum()),
                              chi2nu_median=float(np.median(chinu_own_all[sel])),
                              frac_chi2nu_lt_1_5=float(np.mean(chinu_own_all[sel] < 1.5)))
        # the limit free galaxy by galaxy
        per = [interval(lg, P[i]) for i in range(len(G))]
        best = np.array([p[0] for p in per]); up = np.array([p[1] for p in per]); dn = np.array([p[2] for p in per])
        kmin = np.array([p[3] for p in per])
        half = np.where(np.isnan(up) | np.isnan(dn), np.nan, (up - dn) / 2)
        edge = (kmin == 0) | (kmin == len(lg) - 1)
        dP = P[np.arange(len(G)), kb] - P.min(axis=1)            # per galaxy, shared vs own limit
        chinu_own = C[np.arange(len(G)), kmin] / np.maximum(npt - npar - 1, 1)
        dP_scaled = dP / np.maximum(chinu_own, 1.0)
        n = int(sel.sum())
        s["free"] = dict(
            lg_median=float(np.median(best[sel])), lg_std=float(np.std(best[sel])),
            lg_p16_p84=[float(np.percentile(best[sel], 16)), float(np.percentile(best[sel], 84))],
            at_grid_edge=int(edge[sel].sum()),
            dchi2_shared_vs_free=float(dP[sel].sum()), dof=n - 1,
            dchi2_scaled=float(dP_scaled[sel].sum()),
            n_off_2sigma=int(np.sum(dP[sel] > 4)), n_off_2sigma_scaled=int(np.sum(dP_scaled[sel] > 4)),
            n_off_3sigma_scaled=int(np.sum(dP_scaled[sel] > 9)),
        )
        # intrinsic scatter of the per-galaxy limit, from galaxies with closed intervals
        ok = sel & ~np.isnan(half) & ~edge
        x, e = best[ok], half[ok]
        def nll(t):
            mu, tau = t
            v = e ** 2 + tau ** 2
            return 0.5 * np.sum((x - mu) ** 2 / v + np.log(v))
        from scipy.optimize import minimize
        r = minimize(nll, [np.median(x), 0.1], bounds=[(-2, 2), (0, 2)])
        s["free"]["intrinsic_scatter_dex"] = float(r.x[1]); s["free"]["intrinsic_mean_lg"] = float(r.x[0])
        s["free"]["n_closed"] = int(ok.sum())
        # trends of the per-galaxy limit with the galaxy
        Mb = np.array([0.5 * g["Ldisk"] + 0.7 * g["Lbul"] + g["Mgas"] for g in G])
        fgas = np.array([g["Mgas"] for g in G]) / Mb
        SB = np.array([g["L"] / (2 * np.pi * (1e3 * g["Rdisk"]) ** 2) for g in G])
        tr = {}
        for key, v in (("log_Mb", np.log10(Mb)), ("log_SBdisk", np.log10(SB)), ("gas_fraction", fgas)):
            rho, p = spearmanr(v[ok], x)
            tr[key] = dict(spearman=float(rho), p=float(p))
            # median limit in low and high halves
            m = np.median(v[ok])
            tr[key]["lg_low_half"] = float(np.median(x[v[ok] <= m]))
            tr[key]["lg_high_half"] = float(np.median(x[v[ok] > m]))
        s["trends"] = tr
        s["per_galaxy"] = {names[i]: dict(lg=float(best[i]), lo=float(dn[i]), hi=float(up[i]),
                                          chi2nu_120=float(C[i, F.I0] / max(npt[i] - npar[i], 1)),
                                          sel=bool(sel[i])) for i in range(len(G))}
        summary[model] = s

    summary["form"] = form
    with open(os.path.join(HERE, "results", "summary" + tag_ + ".json"), "w") as fh:
        json.dump(summary, fh, indent=1)

    print(f"{summary['n_sel']} galaxies (Q<3, i>=30), {summary['points_sel']} points; eddy form {form}")
    for model in models:
        s = summary[model]; f = s["free"]
        print(f"\n== {model} ==")
        print("  shared limit: g_dagger = %.3f (lg %.3f, 1 sigma %.3f..%.3f)" % (s["shared_gdag"], *s["shared_lg"]))
        for tag in ("at_1.20", "at_shared"):
            a = s[tag]
            print(f"  {tag:10s} chi2 {a['chi2_total']:.0f} / {a['dof']}  median chi2nu {a['chi2nu_median']:.2f}"
                  f"  <1.5: {a['frac_chi2nu_lt_1_5']:.0%}  <3: {a['frac_chi2nu_lt_3']:.0%}  >10: {a['frac_chi2nu_gt_10']:.0%}")
        print(f"  residual rms {s['resid_rms_dex']:.3f} dex at 1.20 (mean {s['resid_mean_dex']:+.3f}) on {s['resid_points']} points;"
              f" {s['resid_rms_dex_shared']:.3f} at the shared best; {s['resid_rms_dex_own']:.3f} with each galaxy's own limit")
        o = s["own_limit"]
        print(f"  own limit: chi2 {o['chi2_total']:.0f}, median chi2nu {o['chi2nu_median']:.2f}, <1.5: {o['frac_chi2nu_lt_1_5']:.0%}")
        print("  mean residual by log g_bar at 1.20: " + "  ".join(
            f"[{a:.1f},{b:.1f}) {m:+.3f} (n={n})" for a, b, n, m in s["resid_by_gbar_1.20"] if m is not None))
        print(f"  free limit: median lg {f['lg_median']:+.2f}, std {f['lg_std']:.2f}, 16-84% {f['lg_p16_p84'][0]:+.2f}..{f['lg_p16_p84'][1]:+.2f},"
              f" {f['at_grid_edge']} at grid edge")
        print(f"  shared vs free: dchi2 {f['dchi2_shared_vs_free']:.0f} for {f['dof']} dof; errors rescaled {f['dchi2_scaled']:.0f};"
              f" off >2 sigma: {f['n_off_2sigma']} ({f['n_off_2sigma_scaled']} rescaled), >3 sigma rescaled {f['n_off_3sigma_scaled']}")
        print(f"  intrinsic scatter of the limit: {f['intrinsic_scatter_dex']:.3f} dex about lg {f['intrinsic_mean_lg']:+.3f}"
              f" ({f['n_closed']} galaxies with closed intervals)")
        for k, t in s["trends"].items():
            print(f"  trend with {k:12s}: Spearman {t['spearman']:+.2f} (p={t['p']:.1e}); median lg low half {t['lg_low_half']:+.2f}, high half {t['lg_high_half']:+.2f}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else F.DEFAULT_FORM)
