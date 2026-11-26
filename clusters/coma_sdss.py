"""Coma with its measured members: SDSS spectroscopic galaxies (812, r < ~17.8) plus 2MRS
galaxies with no SDSS counterpart. Each eddy is its own pattern, filling the region nearer
its galaxy than any other (capped at the isolated edge), holding the stars and hot gas
there; its load is Eq. (15) at that size.

Usage: python3 coma_sdss.py <sdss csv> <2MRS asu.tsv>
Stars' mass from g, r, i light by two standard colour rules (Bell et al. 2003; Taylor et
al. 2011) - stellar-population models, not the Ocean.
"""
import sys, io, contextlib, importlib.util
import numpy as np
from scipy.spatial import cKDTree
spec = importlib.util.spec_from_file_location("coma", __file__.replace("coma_sdss.py", "coma.py"))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)

sd = np.genfromtxt(sys.argv[1], delimiter=",", skip_header=2)
ra, de, z, g, r, i, pr = sd.T
ok = (r < 18.5) & (g - i > -0.5) & (g - i < 2.0)          # drop three rows with broken photometry
ra, de, z, g, r, i = ra[ok], de[ok], z[ok], g[ok], r[ok], i[ok]
D = 100.0 * c.Mpc; dmod = 35.0
Mi = i - dmod; gi = g - i
logM_bell = -0.152 + 0.518 * gi + (-0.4) * (Mi - 4.56)      # log(M/L_i) + log L_i
logM_taylor = 1.15 + 0.70 * gi - 0.4 * Mi
ra0, de0 = 194.9468, 27.9388
def proj(ra_, de_):
    cosang = (np.sin(np.radians(de_)) * np.sin(np.radians(de0)) +
              np.cos(np.radians(de_)) * np.cos(np.radians(de0)) * np.cos(np.radians(ra_ - ra0)))
    return D * np.arccos(np.clip(cosang, -1, 1)), np.degrees(np.arctan2(
        np.cos(np.radians(de_)) * np.sin(np.radians(ra_ - ra0)),
        np.cos(np.radians(de0)) * np.sin(np.radians(de_)) - np.sin(np.radians(de0)) * np.cos(np.radians(de_)) * np.cos(np.radians(ra_ - ra0))))
Rs, PAs = proj(ra, de)

# 2MRS members without an SDSS counterpart within 15 arcsec
with contextlib.redirect_stdout(io.StringIO()):
    rows, Rm2, LK2, tm2, fa = c.main(sys.argv[2])
lines = [l.rstrip("\n") for l in open(sys.argv[2], encoding="utf-8", errors="replace") if not l.startswith("#") and l.strip()]
head = lines[0].split("\t"); ix = {k: n for n, k in enumerate(head)}
mr, md, mk = [], [], []
for l in lines[3:]:
    p = l.split("\t")
    try:
        a, b_, v, k = float(p[ix["RAJ2000"]]), float(p[ix["DEJ2000"]]), float(p[ix["cz"]]), float(p[ix["Ktmag"]])
    except ValueError:
        continue
    if abs(v - 6925) < 3000:
        mr.append(a); md.append(b_); mk.append(k)
mr, md, mk = map(np.array, (mr, md, mk))
R2, PA2 = proj(mr, md); sel = R2 < 3.05 * c.Mpc
mr, md, mk, R2, PA2 = mr[sel], md[sel], mk[sel], R2[sel], PA2[sel]
xy_s = np.c_[ra * np.cos(np.radians(de0)), de]; xy_2 = np.c_[mr * np.cos(np.radians(de0)), md]
d, _ = cKDTree(xy_s).query(xy_2)
extra = d > 15 / 3600
print(f"SDSS members used: {len(ra)}; 2MRS members within the same field: {len(mr)}, of which without an SDSS match: {extra.sum()}")
LK_extra = 10 ** (-0.4 * (mk[extra] - dmod - 3.28))

# gas
T, b, rcg, ne0 = c.GAS["Sanders 2003 / Reiprich 2001"]
rc = rcg * c.kpc; rt = 3 * c.Mpc
rho0 = c.mu_e * c.mp * ne0 * 1e6
rho_gas = lambda x: rho0 * (1 + (x / rc) ** 2) ** (-1.5 * b)
A = 3 * b * T * c.keV / (c.mu * c.mp)
rho_tot = lambda x: A / (4 * np.pi * c.G) * (x**2 + 3 * rc**2) / (x**2 + rc**2) ** 2
RR = np.array([0.5, 1.0, 1.5, 2.0]) * c.Mpc
need = np.array([c.project_density(rho_tot, R, rt) for R in RR])
gas2 = np.array([c.project_density(rho_gas, R, rt) for R in RR])
Mgas_tot = c.M_gas(rt, b, rcg, ne0)
rng = np.random.default_rng(3)
def sample_radial(n, rho, rmax):
    rg = np.linspace(0, rmax, 4001); cdf = np.cumsum(4 * np.pi * rg**2 * rho(rg)); cdf /= cdf[-1]
    rr = np.interp(rng.uniform(size=n), cdf, rg)
    u = rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1)[:, None]; return rr[:, None] * u
gas_xyz = sample_radial(300000, rho_gas, rt); mparcel = Mgas_tot / 300000
vol = rng.uniform(-rt, rt, size=(800000, 3)); vol = vol[np.linalg.norm(vol, axis=1) < rt][:400000]
dvol = 4 / 3 * np.pi * rt**3 / len(vol)
def los(R):
    zmax = np.sqrt(max(rt**2 - R**2, 0)); zz = np.linspace(-zmax, zmax, 2001)
    w = rho_gas(np.sqrt(R**2 + zz**2)); return rng.choice(zz, p=w / w.sum())

def packed(Ms_all, xyz_all, Rcap):
    tree = cKDTree(xyz_all); n = len(xyz_all)
    dv, jv = tree.query(vol); dg, jg = tree.query(gas_xyz)
    Re = np.clip((3 * np.bincount(jv[dv < Rcap], minlength=n) * dvol / (4 * np.pi)) ** (1 / 3), 1 * c.kpc, Rcap)
    M = Ms_all + np.bincount(jg[dg < Rcap], minlength=n) * mparcel
    Me = c.g_eddy(c.G * M / Re**2) * Re**2 / c.G
    ed2 = np.zeros(len(RR)); nn = 200
    for (x0, y0, _), Mi_, Ri in zip(xyz_all, Me, Re):
        rr = rng.uniform(0, Ri, nn); u = rng.normal(size=(nn, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
        Rp = np.hypot(x0 + rr * u[:, 0], y0 + rr * u[:, 1])
        ed2 += Mi_ * np.array([(Rp < R).mean() for R in RR])
    Rp_all = np.hypot(xyz_all[:, 0], xyz_all[:, 1])
    st2 = np.array([Ms_all[Rp_all < R].sum() for R in RR])
    return (gas2 + st2 + ed2) / need, np.median(Re[Rp_all < c.Mpc]) / c.kpc, st2

Rall = np.r_[Rs, R2[extra]]; PAall = np.radians(np.r_[PAs, PA2[extra]])
print("needed (1e14 suns, cylinders 0.5,1,1.5,2 Mpc):", " ".join(f"{x/c.Msun/1e14:.2f}" for x in need))
if __name__ == "__main__":
    for name, logM in (("Bell 2003", logM_bell), ("Taylor 2011", logM_taylor)):
        for ups_k in (0.6, 1.0):
            Ms = np.r_[10 ** logM, ups_k * LK_extra] * c.Msun
            for Rcap in [float(x) for x in __import__("os").environ.get("CAPS", "150,230").split(",")]:
                outs, meds = [], []
                for k in range(4):
                    xyz = np.c_[Rall * np.sin(PAall), Rall * np.cos(PAall), [los(R) for R in Rall]]
                    o, m, st2 = packed(Ms, xyz, Rcap * c.kpc); outs.append(o); meds.append(m)
                o = np.mean(outs, axis=0); s = np.std(outs, axis=0)
                print(f"stars {name}, 2MRS extras M/L_K {ups_k}, edge cap {Rcap:.0f} kpc: stars in 1 Mpc {st2[1]/c.Msun:.2e}; "
                      f"share of needed " + " ".join(f"{a:4.2f}±{e:.2f}" for a, e in zip(o, s)) + f"; median eddy in core {np.mean(meds):.0f} kpc")
