"""For the eddy of Section 6: at each galaxy's fit with one shared limit, is the eddy's central
pushback the same in every galaxy, and its core's load per area?

Central pushback: the eddy held up by pushback alone, summed from far out to the center,
p_c = integral of (load density x the eddy's turning) dr. For Eq. (15) as written this is
g_dagger^2/(4 pi G), about 1.7e-11 Pa, for any mass (checked first).
Core load per area: Burkert-equivalent rho0*r0 of the eddy's load inside 0.1-2 R_t, as in
claude/eddy_core.py (Donato et al. 2009 measure 140 +80/-30 Msun/pc^2).

The mass inside r is built from SPARC, continued inside the first and beyond the last measured
point: the stellar disk from its surface brightness (inward on the slope of the first two points,
outward on the SPARC scale length); the bulge as a round body (M ~ r^2 inside the first point);
the gas as its round stand-in, never above 1.33 M_HI, approaching it beyond the last point.
Disks have thickness: inside about their scale height the sphere holds less than the cylinder,
M_sph = M_cyl (1 - exp(-r / 1.5 h_z)), with h_z = 0.196 R_d^0.633 kpc (the relation SPARC uses).
Run after sparc_fit.py and sparc_report.py:  python3 sparc_pushback.py
(a comparison form: python3 sparc_pushback.py enclosed_p2, after fitting and reporting that form).
"""
import os
import json
import numpy as np
from scipy.optimize import least_squares
import sparc_data as S
import sparc_fit as F

HERE = os.path.dirname(os.path.abspath(__file__))
MSUN, KPC, PC = 1.989e30, 3.0857e19, 3.0857e16
ACC = 3.24078e-14                          # m/s^2 per (km/s)^2/kpc
GSI = 6.674e-11
RG = np.logspace(-4, 3.5, 6000)            # kpc


def pushback_Pa(g):
    """Central pushback for a round load whose turning is g(r) on RG, in pascals."""
    r = RG
    m = r * r * g                           # G M_load(<r), (km/s)^2 kpc
    rho = np.gradient(m, r) / (4 * np.pi * S.G * r * r)        # Msun/kpc^3
    rho_SI = rho * MSUN / KPC ** 3
    integrand = rho_SI * g * ACC
    return float(np.trapezoid(integrand, r * KPC))


def burkert_mu(g, Rt):
    """Burkert-equivalent rho0*r0 (Msun/pc^2) of the load inside 0.1-2 Rt."""
    r = np.linspace(0.1, 2.0, 60) * Rt
    Me = np.interp(r, RG, RG * RG * g) / S.G
    def Mb(r, rho0, r0):
        y = r / r0
        return 2 * np.pi * rho0 * r0 ** 3 * (np.log(1 + y) + 0.5 * np.log(1 + y * y) - np.arctan(y))
    f = lambda p: np.log(Mb(r, 10 ** p[0], 10 ** p[1] * Rt) / Me)
    s = least_squares(f, [np.log10(Me[-1] / Rt ** 3), 0.0])
    rho0, r0 = 10 ** s.x[0], 10 ** s.x[1] * Rt          # Msun/kpc^3, kpc
    return rho0 * r0 / 1e6, float(np.sqrt(np.mean(s.fun ** 2)))


def eddy_turning(Mr, gd, form=F.DEFAULT_FORM):
    gN = S.G * Mr / RG ** 2
    return np.sqrt(gN * gd) * F.free_share(gN / gd, form)


def mass_inside(g, th):
    """M(<r) on RG (Msun) at the fitted parameters th."""
    lud, lub, D, inc = F.unpack(g, th)
    Ud, Ub, fD = 10 ** lud, 10 ** lub, D / g["D"]
    R = g["R"] * fD
    hz = 0.196 * (g["Rdisk"] * fD) ** 0.633
    thick = 1 - np.exp(-RG / (1.5 * hz))
    # stellar disk: surface brightness (Lsun/pc^2, distance-free) carried in and out
    SB = np.maximum(S.read_models()[g["name"]][:, 7], 0)
    s0 = max(SB[0], 1e-9); s1 = max(SB[1], 1e-9) if len(SB) > 1 else s0
    hin = (R[1] - R[0]) / np.log(s0 / s1) if len(SB) > 1 and s0 > s1 else np.inf
    hout = g["Rdisk"] * fD
    Sig = np.where(RG < R[0], s0 * np.exp(-(RG - R[0]) / hin) if np.isfinite(hin) else s0,
                   np.where(RG > R[-1], max(SB[-1], 1e-9) * np.exp(-(RG - R[-1]) / hout),
                            np.interp(RG, R, SB)))
    ring = 2 * np.pi * RG * 1e6 * Sig                         # Lsun/kpc
    Mdisk = Ud * np.concatenate([[0], np.cumsum(0.5 * (ring[1:] + ring[:-1]) * np.diff(RG))]) * thick
    # bulge, round
    if g["has_bul"]:
        Mb_pts = Ub * g["Menc_bul"] * fD ** 2
        Mbul = np.where(RG < R[0], Mb_pts[0] * (RG / R[0]) ** 2, np.interp(RG, R, Mb_pts))
    else:
        Mbul = 0 * RG
    # gas, round stand-in, capped at the whole gas, approaching it beyond the last point
    Mg_tot = g["Mgas"] * fD ** 2
    Mg_pts = g["Menc_gas"] * fD ** 2
    Mg_last = Mg_pts[-1]
    Mgas = np.where(RG < R[0], Mg_pts[0] * (RG / R[0]) ** 2 * thick / max(thick[np.searchsorted(RG, R[0])], 1e-9),
                    np.where(RG > R[-1], Mg_tot - (Mg_tot - Mg_last) * np.exp(-(RG - R[-1]) / (R[-1] / 3)),
                             np.interp(RG, R, Mg_pts)))
    M = np.maximum.accumulate(Mdisk + Mbul + Mgas)
    Mtot = Ud * g["Ldisk"] * fD ** 2 + Ub * g["Lbul"] * fD ** 2 + Mg_tot
    return M, Mtot


def main(form=F.DEFAULT_FORM):
    gd0 = 1.20 * S.GDAG_UNIT
    # check: Eq. (15) as written gives g_dag^2/(4 pi G) and 264 Msun/pc^2 at any mass
    target = (1.2e-10) ** 2 / (4 * np.pi * GSI)
    for Mb in (1e8, 1e11):
        V2 = np.sqrt(S.G * Mb * gd0); Rt = np.sqrt(S.G * Mb / gd0); x = RG / Rt
        g = V2 / RG * x * x / (1 + x * x)
        print(f"check, Eq. 15 at M = {Mb:.0e}: pushback {pushback_Pa(g):.4e} Pa (expected {target:.4e});"
              f" core load per area {burkert_mu(g, Rt)[0]:.0f}")

    tag = "" if form == F.DEFAULT_FORM else "_" + form
    d = np.load(os.path.join(HERE, "results", "profiles" + tag + ".npz"))
    summ = json.load(open(os.path.join(HERE, "results", "summary" + tag + ".json")))
    lg, names = d["lgrid"], list(d["names"])
    kb = int(np.argmin(np.abs(lg - summ["eddy"]["shared_lg"][0])))
    gd = 10 ** lg[kb] * S.GDAG_UNIT
    F.FORM = form
    gals = {g["name"]: g for g in S.load()}
    rows = []
    for i, n in enumerate(names):
        g = gals[n]
        if not (g["Q"] < 3 and g["inc"] >= 30):
            continue
        nb = 4 if g["has_bul"] else 3
        th = d["eddy_TH"][i, kb][:nb]
        M, Mtot = mass_inside(g, th)
        ge = eddy_turning(M, gd, form)
        Rt = np.sqrt(S.G * Mtot / gd)
        mu, rms = burkert_mu(ge, Rt)
        rows.append(dict(name=n, logMb=float(np.log10(Mtot)), p_Pa=pushback_Pa(ge), mu=mu, fit_rms=rms,
                         fgas=float(g["Mgas"] / Mtot * (th[-2] / g["D"]) ** 2)))
    p = np.array([r["p_Pa"] for r in rows]); mu = np.array([r["mu"] for r in rows])
    lm = np.array([r["logMb"] for r in rows])
    from scipy.stats import spearmanr
    ref = (10 ** lg[kb] * 1e-10) ** 2 / (4 * np.pi * GSI)
    out = dict(gdag_shared=float(10 ** lg[kb]), pushback_ref_Pa=ref,
               pushback_median_Pa=float(np.median(p)), pushback_p16_p84=[float(np.percentile(p, 16)), float(np.percentile(p, 84))],
               pushback_dex_scatter=float(np.std(np.log10(p))),
               pushback_vs_mass=dict(zip(("rho", "p"), map(float, spearmanr(lm, np.log10(p))))),
               mu_median=float(np.median(mu)), mu_p16_p84=[float(np.percentile(mu, 16)), float(np.percentile(mu, 84))],
               mu_dex_scatter=float(np.std(np.log10(mu))),
               mu_vs_mass=dict(zip(("rho", "p"), map(float, spearmanr(lm, np.log10(mu))))),
               n=len(rows), rows=rows)
    json.dump(out, open(os.path.join(HERE, "results", "pushback" + tag + ".json"), "w"), indent=1)
    print(f"{len(rows)} galaxies, form {form}, shared limit {10 ** lg[kb]:.2f}")
    print(f"central pushback: median {np.median(p):.3e} Pa (Eq. 15 at this limit: {ref:.3e}); 16-84% "
          f"{np.percentile(p, 16):.2e}..{np.percentile(p, 84):.2e}; scatter {np.std(np.log10(p)):.2f} dex;"
          f" Spearman with mass {out['pushback_vs_mass']['rho']:+.2f} (p {out['pushback_vs_mass']['p']:.1e})")
    print(f"core load per area: median {np.median(mu):.0f} Msun/pc^2; 16-84% {np.percentile(mu, 16):.0f}..{np.percentile(mu, 84):.0f};"
          f" scatter {np.std(np.log10(mu)):.2f} dex; Spearman with mass {out['mu_vs_mass']['rho']:+.2f} (p {out['mu_vs_mass']['p']:.1e})"
          f"  [Donato: 140 +80/-30, scatter about 0.2 dex]")
    for lo, hi in ((7, 9), (9, 10), (10, 10.7), (10.7, 12)):
        m = (lm >= lo) & (lm < hi)
        if m.any():
            print(f"  log M_b {lo}-{hi}: n={m.sum():3d}  pushback median {np.median(p[m]):.2e} Pa  core load {np.median(mu[m]):.0f}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else F.DEFAULT_FORM)
