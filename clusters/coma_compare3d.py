"""Coma, forward model (coma_budget.py) as 3D enclosed load M(<r), against the measured sides:
hot gas isothermal (beta model), hot gas with Planck SZ pressure (coma_need_planck.py), and galaxy
motions (Lokas & Mamon 2003: 1.4e15 within 2.9 Mpc, +-30%, Jeans analysis of 355 E-S0s; their
extrapolation 1.6e15 +-0.5 within 3.6 Mpc; caustics, Geller et al. 1999, 1.7e15 +-0.4 within 3.6 Mpc).
Stars: Taylor x1.4 (the lensing paper's mass scale for ellipticals) and Bell, as in coma_budget.
"""
import os, sys, io, contextlib, runpy, numpy as np
if len(sys.argv) < 3: sys.argv = [sys.argv[0], "/home/claude/rawsdss/coma_sdss.csv", "/home/claude/raw2mrs/asu.tsv"]
from scipy.spatial import cKDTree
here = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    B = runpy.run_path(os.path.join(here, "coma_budget.py"), run_name="lib")
g = B["g"]; c = g["c"]; kpc, Mpc, Msun, G = c.kpc, c.Mpc, c.Msun, c.G
vol, dvol, gas_xyz, mparcel, eddy_load, Rgrid = B["vol"], B["dvol"], B["gas_xyz"], B["mparcel"], B["eddy_load"], B["Rgrid"]
rq = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 2.9]) * Mpc
def model3d(Ms, xyz, Riso, f):
    n = len(xyz); tree = cKDTree(xyz); dv, jv = tree.query(vol); dg, jg = tree.query(gas_xyz)
    budget = eddy_load(f * Ms, Riso * kpc)
    ov = np.argsort(jv); jvs, dvs = jv[ov], dv[ov]; vs = np.searchsorted(jvs, np.arange(n + 1))
    og = np.argsort(jg); jgs, dgs = jg[og], dg[og]; gs = np.searchsorted(jgs, np.arange(n + 1))
    Re = np.empty(n); Me = np.empty(n)
    for i in range(n):
        dvi = np.sort(dvs[vs[i]:vs[i+1]]); dgi = np.sort(dgs[gs[i]:gs[i+1]])
        Rq = np.maximum((3 * np.searchsorted(dvi, Rgrid) * dvol / (4 * np.pi)) ** (1/3), kpc)
        L = eddy_load(Ms[i] + np.searchsorted(dgi, Rgrid) * mparcel, Rq)
        k = np.argmax(L >= budget[i]) if (L >= budget[i]).any() else -1
        Re[i], Me[i] = Rq[k], L[k]
    rng = np.random.default_rng(5); out = np.zeros(len(rq)); nn = 300
    for p, M_, R_ in zip(xyz, Me, Re):
        u = rng.normal(size=(nn, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
        pts = p + (R_ * rng.uniform(size=nn) ** (1/3))[:, None] * u     # eddy load spread over its sphere
        rr = np.linalg.norm(pts, axis=1); out += M_ * np.array([(rr < R).mean() for R in rq])
    rgal = np.linalg.norm(xyz, axis=1); rgas = np.linalg.norm(gas_xyz, axis=1)
    return out + np.array([Ms[rgal < R].sum() for R in rq]) + np.array([(rgas < R).sum() for R in rq]) * mparcel
# measured sides
T, b, rcg, ne0 = c.GAS["Sanders 2003 / Reiprich 2001"]
M_iso = c.g_obs(rq, T, b, rcg) * rq**2 / G
with contextlib.redirect_stdout(io.StringIO()):
    P = runpy.run_path(os.path.join(here, "coma_need_planck.py"), run_name="lib")
M_sz = np.interp(rq, P["r"], P["g_sz"]) * rq**2 / G
print("3D enclosed (1e14 suns) at r =", " ".join(f"{x/Mpc:.1f}" for x in rq), "Mpc")
print("  hot gas, isothermal          ", " ".join(f"{x/Msun/1e14:5.2f}" for x in M_iso))
print("  hot gas, Planck SZ pressure  ", " ".join(f"{x/Msun/1e14:5.2f}" for x in M_sz))
print("  galaxy motions (Lokas&Mamon) at 2.9 Mpc: 14.0 +- 4.2")
for name, logM in (("Taylor x1.4", g["logM_taylor"] + np.log10(1.4)), ("Bell", g["logM_bell"])):
    Ms = np.r_[10**logM, 0.8 * g["LK_extra"]] * Msun
    for f, Riso in ((1.0, 700), (1.5, 700), (1.5, 1000)):
        xyz = np.c_[g["Rall"] * np.sin(g["PAall"]), g["Rall"] * np.cos(g["PAall"]), [g["los"](R) for R in g["Rall"]]]
        m = model3d(Ms, xyz, Riso, f)
        print(f"  eddies: stars {name:11s} f {f} R_iso {Riso:4d}", " ".join(f"{x/Msun/1e14:5.2f}" for x in m))
