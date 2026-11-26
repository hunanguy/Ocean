"""Coma, second pass: each galaxy's eddy answers to everything inside it, stars and
the hot gas around it (Eq. 15 with M(<r) = stars + gas inside r of the galaxy).

Usage: python3 coma_gas.py <2MRS asu.tsv>
Two ways to count the gas: (a) shared out, each parcel of gas belongs to the
nearest galaxy whose edge reaches it; (b) every eddy counts all gas inside it
(overlapping eddies count the same gas again; an upper bound).
"""
import sys, io, contextlib, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location("coma", __file__.replace("coma_gas.py", "coma.py"))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
from scipy.spatial import cKDTree

with contextlib.redirect_stdout(io.StringIO()):
    rows, Rm, LK, tm, fa = c.main(sys.argv[1])
T, b, rcg, ne0 = c.GAS["Sanders 2003 / Reiprich 2001"]
rc = rcg * c.kpc; rt = 3 * c.Mpc
rho0 = c.mu_e * c.mp * ne0 * 1e6
rho_gas = lambda r: rho0 * (1 + (r / rc) ** 2) ** (-1.5 * b)
A = 3 * b * T * c.keV / (c.mu * c.mp)
rho_tot = lambda r: A / (4 * np.pi * c.G) * (r**2 + 3 * rc**2) / (r**2 + rc**2) ** 2
RR = np.array([0.5, 1.0, 1.5, 2.0]) * c.Mpc
need = np.array([c.project_density(rho_tot, R, rt) for R in RR])
gas2 = np.array([c.project_density(rho_gas, R, rt) for R in RR])
Mgas_tot = c.M_gas(rt, b, rcg, ne0)

rng = np.random.default_rng(7)

def sample_radial(n, rho, rmax):
    """3D points drawn from a spherical density rho(r) inside rmax."""
    rgrid = np.linspace(0, rmax, 4001)
    cdf = np.cumsum(4 * np.pi * rgrid**2 * rho(rgrid)); cdf /= cdf[-1]
    r = np.interp(rng.uniform(size=n), cdf, rgrid)
    u = rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
    return r[:, None] * u

# gas parcels
Np = 300000
gas_xyz = sample_radial(Np, rho_gas, rt); mparcel = Mgas_tot / Np

def los_depth(R):
    """Line-of-sight depth for a galaxy at projected R, galaxies taken to follow the gas."""
    zmax = np.sqrt(max(rt**2 - R**2, 0))
    z = np.linspace(-zmax, zmax, 2001); w = rho_gas(np.sqrt(R**2 + z**2))
    return rng.choice(z, p=w / w.sum())

for ups in (0.6, 1.0):
    Ms = ups * LK * c.Msun
    for Re in (100, 150, 230):
        Re_m = Re * c.kpc
        ratios = {"shared": [], "every": []}
        for real in range(4):
            phi = rng.uniform(0, 2 * np.pi, len(Rm))
            gal = np.c_[Rm * np.cos(phi), Rm * np.sin(phi), [los_depth(R) for R in Rm]]
            gtree = cKDTree(gal)
            # (a) shared: each parcel to the nearest galaxy, if within its edge
            d, j = gtree.query(gas_xyz)
            Mshared = np.bincount(j[d < Re_m], minlength=len(gal)) * mparcel
            # (b) every eddy counts all gas inside its edge
            ptree = cKDTree(gas_xyz)
            Mevery = np.array([len(x) for x in ptree.query_ball_point(gal, Re_m)]) * mparcel
            # stars inside each eddy (own plus neighbours')
            Mst = np.array([Ms[idx].sum() for idx in gtree.query_ball_point(gal, Re_m)])
            for key, Mg in (("shared", Mshared + Ms), ("every", Mevery + Mst)):
                gN = c.G * Mg / Re_m**2
                Me = c.g_eddy(gN) * Re_m**2 / c.G
                # project each eddy (load ~ 1/r^2 inside its edge) into cylinders
                n = 300; ed2 = np.zeros(len(RR))
                for (x0, y0, _), Mi in zip(gal, Me):
                    rr = rng.uniform(0, Re_m, n)
                    u = rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
                    Rp = np.hypot(x0 + rr * u[:, 0], y0 + rr * u[:, 1])
                    ed2 += Mi * np.array([(Rp < R).mean() for R in RR])
                stars2 = np.array([Ms[Rm < R].sum() for R in RR])
                ratios[key].append((gas2 + stars2 + ed2) / need)
        for key in ratios:
            r = np.mean(ratios[key], axis=0); s = np.std(ratios[key], axis=0)
            print(f"M/L {ups}, edge {Re:3d} kpc, gas {key:>6}: total/needed at 0.5,1,1.5,2 Mpc " +
                  "  ".join(f"{a:4.2f}±{e:.2f}" for a, e in zip(r, s)))
