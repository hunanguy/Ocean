"""Coma, second pass continued: the visible galaxies with stars only, and with
galaxies too faint for 2MRS added from the K-band luminosity function down to
M_K = -19 (about 10^9 suns of stars), each eddy counting the stars and the
hot gas around it, the gas shared out (each parcel to the nearest galaxy whose
edge reaches it).  Usage: python3 coma_gas2.py <2MRS asu.tsv>
"""
import sys, io, contextlib, importlib.util
import numpy as np
from scipy.spatial import cKDTree
spec = importlib.util.spec_from_file_location("coma", __file__.replace("coma_gas2.py", "coma.py"))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
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
rng = np.random.default_rng(11)

def sample_radial(n, rho, rmax):
    rgrid = np.linspace(0, rmax, 4001)
    cdf = np.cumsum(4 * np.pi * rgrid**2 * rho(rgrid)); cdf /= cdf[-1]
    r = np.interp(rng.uniform(size=n), cdf, rgrid)
    u = rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
    return r[:, None] * u

Np = 300000
gas_xyz = sample_radial(Np, rho_gas, rt); mparcel = Mgas_tot / Np

def los(R):
    zmax = np.sqrt(max(rt**2 - R**2, 0)); z = np.linspace(-zmax, zmax, 2001)
    w = rho_gas(np.sqrt(R**2 + z**2)); return rng.choice(z, p=w / w.sum())

def schechter_draw(n_bright, alpha, Lmin, Lcut, Lstar):
    """Number of galaxies between Lcut and Lmin for n_bright above Lmin, and their L."""
    from scipy.integrate import quad
    phi = lambda x: x**alpha * np.exp(-x)
    n_above = quad(phi, Lmin / Lstar, 50)[0]
    n_faint_rel = quad(phi, Lcut / Lstar, Lmin / Lstar)[0]
    nf = rng.poisson(n_bright * n_faint_rel / n_above)
    xs = np.geomspace(Lcut / Lstar, Lmin / Lstar, 4000)
    w = phi(xs) * xs; w /= w.sum()
    return rng.choice(xs, size=nf, p=w) * Lstar

def total_ratio(Ms_all, xyz_all, Re_m, gas_on=True):
    gtree = cKDTree(xyz_all)
    if gas_on:
        d, j = gtree.query(gas_xyz)
        Mg = np.bincount(j[d < Re_m], minlength=len(xyz_all)) * mparcel
    else:
        Mg = 0.0
    M = Ms_all + Mg
    Me = c.g_eddy(c.G * M / Re_m**2) * Re_m**2 / c.G
    n = 200; ed2 = np.zeros(len(RR))
    for (x0, y0, _), Mi in zip(xyz_all, Me):
        rr = rng.uniform(0, Re_m, n)
        u = rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
        Rp = np.hypot(x0 + rr * u[:, 0], y0 + rr * u[:, 1])
        ed2 += Mi * np.array([(Rp < R).mean() for R in RR])
    Rp_all = np.hypot(xyz_all[:, 0], xyz_all[:, 1])
    stars2 = np.array([Ms_all[Rp_all < R].sum() for R in RR])
    return (gas2 + stars2 + ed2) / need, len(xyz_all)

Lstar = 10 ** (-0.4 * (-24.2 - 3.28)); Lmin = 10 ** (-0.4 * (-23.25 - 3.28))
Lcut = 10 ** (-0.4 * (-19.0 - 3.28))
ups = 0.8
for Re in (100, 150, 230):
    Re_m = Re * c.kpc
    phi = rng.uniform(0, 2 * np.pi, len(Rm))
    vis = np.c_[Rm * np.cos(phi), Rm * np.sin(phi), [los(R) for R in Rm]]
    Ms = ups * LK * c.Msun
    r0, n0 = total_ratio(Ms, vis, Re_m, gas_on=False)
    r1, n1 = total_ratio(Ms, vis, Re_m, gas_on=True)
    print(f"edge {Re} kpc, M/L {ups}: visible 117, stars only: " + " ".join(f"{x:4.2f}" for x in r0)
          + " | with gas around them: " + " ".join(f"{x:4.2f}" for x in r1))
    for alpha in (-1.0, -1.3):
        out = []
        for k in range(3):
            Lf = schechter_draw(len(Rm), alpha, Lmin, Lcut, Lstar)
            xyz_f = sample_radial(len(Lf), rho_gas, rt)
            xyz = np.r_[vis, xyz_f]; Mall = np.r_[Ms, ups * Lf * c.Msun]
            r2, n2 = total_ratio(Mall, xyz, Re_m, gas_on=True); out.append(r2)
        r2 = np.mean(out, axis=0)
        print(f"      + faint galaxies to M_K -19, slope {alpha} ({n2} galaxies): with gas: "
              + " ".join(f"{x:4.2f}" for x in r2))
