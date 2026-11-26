"""Coma run forward with nothing set from Coma (Keith, 25 Nov 20:02, "Run it").
Each Coma galaxy's eddy carries the load an isolated galaxy with the same stars carries, read
from stacked lensing of isolated galaxies (Mistele et al. 2024): Eq. (15) out to the isolated
reach R_iso (0.5-1 Mpc, the lensing range), with an optional mass factor f for the isolated
galaxy's own gas and the lensing excess (1 to 1.5; spirals need 1.0, ellipticals 1.3-1.8).
In Coma the eddy holds its own region only (no overlap) and takes in the hot gas there out to
its reach; its reach is where its load reaches that budget (the build carries what it was
given, it does not fill room). If the whole region cannot hold the budget, the eddy fills its
region. Then the turning against what the hot gas needs, as in coma_sdss.py.
Usage: python3 coma_budget.py <sdss csv> <2MRS asu.tsv>
"""
import sys, os, io, contextlib, runpy, numpy as np
from scipy.spatial import cKDTree
os.environ["CAPS"] = "250"
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "coma_sdss.py"), run_name="lib")
c = g["c"]; kpc = c.kpc; G = c.G
vol, dvol, gas_xyz, mparcel = g["vol"], g["dvol"], g["gas_xyz"], g["mparcel"]
RR, need, gas2, rng = g["RR"], g["need"], g["gas2"], g["rng"]
eddy_load = lambda M, R: c.g_eddy(G * M / R**2) * R**2 / G
Rgrid = np.geomspace(5, 3000, 300) * kpc

def run(Ms, xyz, Riso, f):
    n = len(xyz); tree = cKDTree(xyz)
    dv, jv = tree.query(vol); dg, jg = tree.query(gas_xyz)
    budget = eddy_load(f * Ms, Riso * kpc)
    Re = np.empty(n); Me = np.empty(n); full = 0
    ov = np.argsort(jv); jv_s = jv[ov]; dv_s = dv[ov]; vs = np.searchsorted(jv_s, np.arange(n + 1))
    og = np.argsort(jg); jg_s = jg[og]; dg_s = dg[og]; gs = np.searchsorted(jg_s, np.arange(n + 1))
    for i in range(n):
        dvi = np.sort(dv_s[vs[i]:vs[i+1]]); dgi = np.sort(dg_s[gs[i]:gs[i+1]])
        Vc = np.searchsorted(dvi, Rgrid) * dvol
        Rq = np.maximum((3 * Vc / (4 * np.pi)) ** (1 / 3), 1 * kpc)
        Mq = Ms[i] + np.searchsorted(dgi, Rgrid) * mparcel
        L = eddy_load(Mq, Rq)
        k = np.argmax(L >= budget[i]) if (L >= budget[i]).any() else -1
        if k < 0: full += 1
        Re[i], Me[i] = Rq[k], L[k]
    ed2 = np.zeros(len(RR)); nn = 200
    for (x0, y0, _), M_, R_ in zip(xyz, Me, Re):
        rr = rng.uniform(0, R_, nn); u = rng.normal(size=(nn, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
        Rp = np.hypot(x0 + rr * u[:, 0], y0 + rr * u[:, 1]); ed2 += M_ * np.array([(Rp < R).mean() for R in RR])
    Rp_all = np.hypot(xyz[:, 0], xyz[:, 1])
    st2 = np.array([Ms[Rp_all < R].sum() for R in RR])
    core = Rp_all < c.Mpc
    return (gas2 + st2 + ed2) / need, np.median(Re[core]) / kpc, np.median(Re[~core]) / kpc, full / n

if __name__ == "__main__":
    print("share of the turning the hot gas needs, cylinders 0.5, 1, 1.5, 2 Mpc")
    for name, logM in (("Bell", g["logM_bell"]), ("Taylor", g["logM_taylor"])):
        Ms = np.r_[10**logM, 0.8 * g["LK_extra"]] * c.Msun
        for f in (1.0, 1.5):
            for Riso in (500, 700, 1000):
                outs = []
                for k in range(2):
                    xyz = np.c_[g["Rall"] * np.sin(g["PAall"]), g["Rall"] * np.cos(g["PAall"]), [g["los"](R) for R in g["Rall"]]]
                    outs.append(run(Ms, xyz, Riso, f))
                o = np.mean([x[0] for x in outs], axis=0)
                print(f"stars {name:6s} f {f}, isolated reach {Riso:4d} kpc: " + " ".join(f"{a:4.2f}" for a in o) +
                      f" | reach in Coma: median {np.mean([x[1] for x in outs]):.0f} kpc inside 1 Mpc, {np.mean([x[2] for x in outs]):.0f} outside;"
                      f" eddies filling their whole region {np.mean([x[3] for x in outs])*100:.0f}%")
