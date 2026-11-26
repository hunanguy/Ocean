"""Any cluster run forward the way Coma was (coma_budget.py), with nothing set from the cluster:
each member galaxy's eddy carries the load an isolated galaxy with the same stars carries (Eq. 15
out to the isolated reach R_iso, mass factor f; from stacked lensing, Mistele et al. 2024); in the
cluster it holds its own region and takes in the hot gas there until its load reaches that amount.
Compared with the turning the hot gas needs (isothermal beta model, hydrostatic balance).

Usage: python3 cluster_budget.py <members csv with columns cl,ra,dec,z,g,r,i,petro_r> [cluster ...]
Gas: Chen et al. 2007 Table 1 (single beta model; rc and n0 converted from h50 to h70), centers and
redshifts from Reiprich & Bohringer 2002 Table 3. Coma uses Sanders 2003 / Reiprich 2001 (h70).
Borrowed steps: stars' mass from population models (Taylor 2011 x1.4 to the lensing paper's scale for
ellipticals; Bell 2003), no k-corrections (z < 0.08), distances cz/H0 with H0 = 70, single isothermal
beta models (cool-core clusters A1795, A2029, A2199 are fitted better by double beta models), galaxy
depths placed as the gas, SDSS spectroscopic limit r < 17.77 (shallower in absolute terms for the
more distant clusters).
"""
import sys, os, importlib.util, numpy as np
from scipy.spatial import cKDTree
spec = importlib.util.spec_from_file_location("coma", os.path.join(os.path.dirname(os.path.abspath(__file__)), "coma.py"))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
kpc, Mpc, Msun, G = c.kpc, c.Mpc, c.Msun, c.G
h50to70_r, h50to70_n = 0.5 / 0.7, (0.7 / 0.5) ** 0.5
# name: ra, dec, z (RB02 Table 3); T keV, beta, rc kpc (h70), n_e0 cm^-3 (h70)
CL = {
 "COMA":  (194.9468, 27.9388, 0.0232, 8.21, 0.705, 275.0, 3.64e-3),
 "A1367": (176.1903, 19.7030, 0.0216, 3.55, 0.695, 383 * h50to70_r, 0.15e-2 * h50to70_n),
 "A2199": (247.1586, 39.5477, 0.0302, 4.10, 0.655, 139 * h50to70_r, 0.83e-2 * h50to70_n),
 "A2147": (240.5628, 15.9586, 0.0351, 4.91, 0.444, 237 * h50to70_r, 0.17e-2 * h50to70_n),
 "A1795": (207.2201, 26.5944, 0.0616, 6.00, 0.596, 78 * h50to70_r, 2.88e-2 * h50to70_n),
 "A2029": (227.7331, 5.7450, 0.0767, 8.70, 0.582, 83 * h50to70_r, 3.90e-2 * h50to70_n),
}
rng = np.random.default_rng(7)
eddy_load = lambda M, R: c.g_eddy(G * M / R**2) * R**2 / G
Rgrid = np.geomspace(5, 3000, 300) * kpc
RR = np.array([0.5, 1.0, 1.5, 2.0]) * Mpc
rt = 3 * Mpc

def setup(name):
    ra0, de0, z0, T, b, rcg, ne0 = CL[name]
    rc = rcg * kpc
    rho_gas = lambda x: c.mu_e * c.mp * ne0 * 1e6 * (1 + (x / rc) ** 2) ** (-1.5 * b)
    A = 3 * b * T * c.keV / (c.mu * c.mp)
    rho_tot = lambda x: A / (4 * np.pi * G) * (x**2 + 3 * rc**2) / (x**2 + rc**2) ** 2
    need = np.array([c.project_density(rho_tot, R, rt) for R in RR])
    gas2 = np.array([c.project_density(rho_gas, R, rt) for R in RR])
    Mg = c.M_gas(rt, b, rcg, ne0)
    rg = np.linspace(0, rt, 4001); cdf = np.cumsum(4 * np.pi * rg**2 * rho_gas(rg)); cdf /= cdf[-1]
    n = 200000; rr = np.interp(rng.uniform(size=n), cdf, rg)
    u = rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
    gas_xyz = rr[:, None] * u
    vol = rng.uniform(-rt, rt, size=(600000, 3)); vol = vol[np.linalg.norm(vol, axis=1) < rt][:300000]
    wz = lambda R: (lambda zz: rng.choice(zz, p=(w := rho_gas(np.sqrt(R**2 + zz**2))) / w.sum()))(
        np.linspace(-np.sqrt(max(rt**2 - R**2, 0)), np.sqrt(max(rt**2 - R**2, 0)), 1001))
    return dict(need=need, gas2=gas2, gas_xyz=gas_xyz, mparcel=Mg / n, vol=vol, dvol=4 / 3 * np.pi * rt**3 / len(vol),
                los=wz, z0=z0, ra0=ra0, de0=de0, Mgas=Mg)

def members(path, name, s, Mr_lim=None):
    d = np.genfromtxt(path, delimiter=",", names=True, dtype=None, encoding="utf-8")
    cols = d.dtype.names
    lab = np.array([str(x).strip().strip("'").upper() for x in d[cols[0]]])
    m = lab == name
    ra, de, z = d["ra"][m], d["dec"][m], d["z"][m]
    g_, r_, i_ = d[cols[4]][m], d[cols[5]][m], d[cols[6]][m]
    ok = (r_ < 18.5) & (g_ - i_ > -0.5) & (g_ - i_ < 2.0)
    ra, de, z, g_, r_, i_ = ra[ok], de[ok], z[ok], g_[ok], r_[ok], i_[ok]
    z0 = s["z0"]; Dc = c.Mpc * 2.998e5 * z0 / 70.0
    DA, DL = Dc / (1 + z0), Dc * (1 + z0)
    dmod = 5 * np.log10(DL / (10 * 3.0857e16))
    cosang = (np.sin(np.radians(de)) * np.sin(np.radians(s["de0"])) +
              np.cos(np.radians(de)) * np.cos(np.radians(s["de0"])) * np.cos(np.radians(ra - s["ra0"])))
    R = DA * np.arccos(np.clip(cosang, -1, 1))
    PA = np.arctan2(np.cos(np.radians(de)) * np.sin(np.radians(ra - s["ra0"])),
                    np.cos(np.radians(s["de0"])) * np.sin(np.radians(de)) - np.sin(np.radians(s["de0"])) * np.cos(np.radians(de)) * np.cos(np.radians(ra - s["ra0"])))
    Mi, Mr, gi = i_ - dmod, r_ - dmod, g_ - i_
    keep = (np.abs(z - z0) * 2.998e5 / (1 + z0) < 3000) & (R < 3 * Mpc)
    if Mr_lim is not None: keep &= Mr < Mr_lim
    logT = 1.15 + 0.70 * gi - 0.4 * Mi
    logB = -0.152 + 0.518 * gi - 0.4 * (Mi - 4.56)
    return R[keep], PA[keep], logT[keep], logB[keep], Mr[keep].max() if keep.any() else np.nan

def run(s, Ms, R, PA, Riso, f):
    xyz = np.c_[R * np.sin(PA), R * np.cos(PA), [s["los"](x) for x in R]]
    n = len(xyz); tree = cKDTree(xyz)
    dv, jv = tree.query(s["vol"]); dg, jg = tree.query(s["gas_xyz"])
    budget = eddy_load(f * Ms, Riso * kpc)
    ov = np.argsort(jv); jvs, dvs = jv[ov], dv[ov]; vs = np.searchsorted(jvs, np.arange(n + 1))
    og = np.argsort(jg); jgs, dgs = jg[og], dg[og]; gs = np.searchsorted(jgs, np.arange(n + 1))
    Re = np.empty(n); Me = np.empty(n)
    for k in range(n):
        dvi = np.sort(dvs[vs[k]:vs[k+1]]); dgi = np.sort(dgs[gs[k]:gs[k+1]])
        Rq = np.maximum((3 * np.searchsorted(dvi, Rgrid) * s["dvol"] / (4 * np.pi)) ** (1 / 3), kpc)
        L = eddy_load(Ms[k] + np.searchsorted(dgi, Rgrid) * s["mparcel"], Rq)
        j = np.argmax(L >= budget[k]) if (L >= budget[k]).any() else -1
        Re[k], Me[k] = Rq[j], L[j]
    ed2 = np.zeros(len(RR)); nn = 200
    for (x0, y0, _), M_, R_ in zip(xyz, Me, Re):
        rr = rng.uniform(0, R_, nn); u = rng.normal(size=(nn, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
        Rp = np.hypot(x0 + rr * u[:, 0], y0 + rr * u[:, 1]); ed2 += M_ * np.array([(Rp < X).mean() for X in RR])
    Rp = np.hypot(xyz[:, 0], xyz[:, 1])
    st2 = np.array([Ms[Rp < X].sum() for X in RR])
    return (s["gas2"] + st2 + ed2) / s["need"], np.median(Re) / kpc

if __name__ == "__main__":
    path = sys.argv[1]
    names = [a.upper() for a in sys.argv[2:]] or list(CL)
    Mr_lim = float(os.environ["MRLIM"]) if "MRLIM" in os.environ else None
    for name in names:
        s = setup(name)
        R, PA, logT, logB, faint = members(path, name, s, Mr_lim)
        print(f"{name}: z {s['z0']}, members {len(R)} (faintest M_r {faint:.1f}); hot gas within 3 Mpc {s['Mgas']/Msun:.2e}; "
              f"needed in cylinders 0.5-2 Mpc (1e14): " + " ".join(f"{x/Msun/1e14:.2f}" for x in s["need"]))
        for lab, logM in (("Taylor x1.4", logT + np.log10(1.4)), ("Bell", logB)):
            Ms = 10**logM * Msun
            for f, Riso in ((1.0, 700), (1.5, 700), (1.5, 1000)):
                o, med = run(s, Ms, R, PA, Riso, f)
                print(f"   stars {lab:11s} f {f} R_iso {Riso:4d}: share " + " ".join(f"{a:4.2f}" for a in o) + f"  (median reach {med:.0f} kpc)")
