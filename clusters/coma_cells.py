"""Coma, third pass: each eddy a spinning pattern rebuilt as its own, holding its own
region. Eddies do not overlap: each galaxy's eddy fills the region nearer to it than to
any other galaxy (its cell), out to at most the isolated edge; it holds the stars and the
hot gas in that region; its load is Eq. (15) at the cell's size, spread as 1/r^2.
Usage: python3 coma_cells.py <2MRS asu.tsv>
"""
import sys, io, contextlib, importlib.util
import numpy as np
from scipy.spatial import cKDTree
spec = importlib.util.spec_from_file_location("coma", __file__.replace("coma_cells.py", "coma.py"))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
spec2 = importlib.util.spec_from_file_location("cg2", __file__.replace("coma_cells.py", "coma_gas2.py"))
with contextlib.redirect_stdout(io.StringIO()):
    sys.argv = [sys.argv[0], sys.argv[1]]
    g2 = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(g2)
rng = np.random.default_rng(5)
rt = g2.rt
Nv = 400000
vol_xyz = rng.uniform(-rt, rt, size=(Nv * 2, 3)); vol_xyz = vol_xyz[np.linalg.norm(vol_xyz, axis=1) < rt][:Nv]
dvol = 4 / 3 * np.pi * rt**3 / len(vol_xyz)

def packed(Ms_all, xyz_all, Rcap):
    tree = cKDTree(xyz_all)
    dv, jv = tree.query(vol_xyz)
    dg, jg = tree.query(g2.gas_xyz)
    n = len(xyz_all)
    # cell volume within the cap, as an equivalent radius
    Vc = np.bincount(jv[dv < Rcap], minlength=n) * dvol
    Re = np.minimum((3 * Vc / (4 * np.pi)) ** (1 / 3), Rcap)
    Re = np.maximum(Re, 1 * c.kpc)
    Mg = np.bincount(jg[dg < Rcap], minlength=n) * g2.mparcel
    M = Ms_all + Mg
    Me = c.g_eddy(c.G * M / Re**2) * Re**2 / c.G
    nn = 200; ed2 = np.zeros(len(g2.RR))
    for (x0, y0, _), Mi, Ri in zip(xyz_all, Me, Re):
        rr = rng.uniform(0, Ri, nn)
        u = rng.normal(size=(nn, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
        Rp = np.hypot(x0 + rr * u[:, 0], y0 + rr * u[:, 1])
        ed2 += Mi * np.array([(Rp < R).mean() for R in g2.RR])
    Rp_all = np.hypot(xyz_all[:, 0], xyz_all[:, 1])
    stars2 = np.array([Ms_all[Rp_all < R].sum() for R in g2.RR])
    inner = Rp_all < 1 * c.Mpc
    return (g2.gas2 + stars2 + ed2) / g2.need, np.median(Re[inner]) / c.kpc

ups = 0.8
Ms = ups * g2.LK * c.Msun
for Rcap in (150, 230):
    Rcap_m = Rcap * c.kpc
    phi = rng.uniform(0, 2 * np.pi, len(g2.Rm))
    vis = np.c_[g2.Rm * np.cos(phi), g2.Rm * np.sin(phi), [g2.los(R) for R in g2.Rm]]
    r, med = packed(Ms, vis, Rcap_m)
    print(f"isolated edge {Rcap} kpc: 117 visible: " + " ".join(f"{x:4.2f}" for x in r) + f"  (median eddy size inside 1 Mpc {med:.0f} kpc)")
    for alpha in (-1.0, -1.3):
        for Mcut in (-19.0, -17.0):
            Lcut = 10 ** (-0.4 * (Mcut - 3.28))
            out = []; meds = []
            for k in range(3):
                Lf = g2.schechter_draw(len(g2.Rm), alpha, g2.Lmin, Lcut, g2.Lstar)
                xyz = np.r_[vis, g2.sample_radial(len(Lf), g2.rho_gas, rt)]
                rr_, med = packed(np.r_[Ms, ups * Lf * c.Msun], xyz, Rcap_m); out.append(rr_); meds.append(med)
            print(f"   + faint to M_K {Mcut}, slope {alpha} (~{len(xyz)} galaxies): " +
                  " ".join(f"{x:4.2f}" for x in np.mean(out, axis=0)) + f"  (median eddy size inside 1 Mpc {np.mean(meds):.0f} kpc)")
