"""Coma: the turning its hot gas shows, against the eddies of the Ocean.

Usage: python3 coma.py <2mrs asu.tsv>

Measured side (no cosmological model): the hot gas's beta-model and temperature
(Sanders 2003 Table 1, from Reiprich 2001, h = 0.7; cross-check Reiprich & Bohringer
2002 Table 4), read as hydrostatic balance: the inward turning that holds the gas
at each radius.  Ocean side: stars from 2MRS K-band light; the eddy of Eq. (15).
"""
import sys
import numpy as np
from scipy.integrate import quad
from scipy.special import gammaincc, gamma as Gamma

G = 6.674e-11; Msun = 1.989e30; kpc = 3.0857e19; Mpc = 1e3 * kpc
mp = 1.6726e-27; keV = 1.602e-16
gdag = 1.20e-10

# ---------------------------------------------------------------- gas (measured)
GAS = {  # name: T keV, beta, rc kpc, n_e0 cm^-3   (h = 0.7)
    "Sanders 2003 / Reiprich 2001": (8.21, 0.705, 275.0, 3.64e-3),
    "Reiprich & Bohringer 2002":    (8.38, 0.654, 344.0 * 50 / 70, None),
}
mu, mu_e = 0.61, 1.17


def g_obs(r, T, beta, rc):
    """Turning that holds isothermal beta-model gas at radius r (m/s^2)."""
    return 3 * beta * T * keV / (mu * mp) * r / (r**2 + (rc * kpc)**2)


def M_gas(r, beta, rc, ne0):
    rho0 = mu_e * mp * ne0 * 1e6
    f = lambda x: 4 * np.pi * x**2 * rho0 * (1 + (x / (rc * kpc))**2) ** (-1.5 * beta)
    return quad(f, 0, r, limit=200)[0]


# ------------------------------------------------------------- eddy of Eq. (15)
def B_of_y(y):
    """Solve B / sqrt(1+2B) = y / sqrt(3)."""
    c = y / np.sqrt(3.0)
    # B^2 = c^2 (1 + 2B)  ->  B = c^2 + c sqrt(c^2 + 1)
    return c**2 + c * np.sqrt(c**2 + 1)


def g_eddy(gN):
    gN = np.maximum(gN, 1e-30)
    return np.sqrt(gN * gdag) / (1 + B_of_y(gN / gdag))


def main(path):
    # ---------------- 1. measured turning from the gas
    print("=== 1. Coma's hot gas (measured), turning that holds it ===")
    radii = np.array([250, 500, 1000, 1450, 2000]) * kpc
    Tg, bg, rcg, ne0 = GAS["Sanders 2003 / Reiprich 2001"]
    rows = {}
    for r in radii:
        go = g_obs(r, Tg, bg, rcg)
        go2 = g_obs(r, *GAS["Reiprich & Bohringer 2002"][:3])
        Mg = M_gas(r, bg, rcg, ne0)
        rows[r] = (go, go2, Mg)
        print(f"r = {r/kpc:5.0f} kpc  g_obs = {go:.2e} ({go2:.2e} RB02) m/s^2 = {go/gdag:5.2f} gdag;"
              f"  as load {go*r**2/G/Msun:.2e} Msun;  gas {Mg/Msun:.2e} Msun")

    # ---------------- 2. galaxies from 2MRS
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")
             if not l.startswith("#") and l.strip()]
    head = lines[0].split("\t"); ix = {k: i for i, k in enumerate(head)}
    ra, de, cz, kt, typ = [], [], [], [], []
    for l in lines[3:]:
        p = l.split("\t")
        try:
            vals = (float(p[ix["RAJ2000"]]), float(p[ix["DEJ2000"]]),
                    float(p[ix["cz"]]), float(p[ix["Ktmag"]]))
        except ValueError:
            continue
        ra.append(vals[0]); de.append(vals[1]); cz.append(vals[2]); kt.append(vals[3])
        typ.append(p[ix["type"]].strip())
    ra, de, cz, kt = map(np.array, (ra, de, cz, kt)); typ = np.array(typ)
    ra0, de0, cz0 = 194.9468, 27.9388, 6925.0
    D = 100.0 * Mpc          # Coma's distance: cz_CMB ~ 7,200 km/s over H0 = 70-73 (Sec. 6)
    cosang = (np.sin(np.radians(de)) * np.sin(np.radians(de0)) +
              np.cos(np.radians(de)) * np.cos(np.radians(de0)) * np.cos(np.radians(ra - ra0)))
    R = D * np.arccos(np.clip(cosang, -1, 1))
    mem = (np.abs(cz - cz0) < 3000) & (R < 3 * Mpc)
    print(f"\n=== 2. 2MRS galaxies within 3 Mpc of Coma's center and 3,000 km/s of its redshift: {mem.sum()} ===")
    dmod = 5 * np.log10(D / (10 * 3.0857e16))
    MK = kt[mem] - dmod
    LK = 10 ** (-0.4 * (MK - 3.28))                      # solar K luminosities
    Rm = R[mem]; tm = typ[mem]
    print(f"distance modulus {dmod:.2f}; faintest included M_K = {MK.max():.2f} (survey limit 11.75 -> {11.75-dmod:.2f})")
    print(f"K light of these galaxies: {LK.sum():.2e} Lsun; within 1 Mpc {LK[Rm<Mpc].sum():.2e}")

    # correction for galaxies below the survey limit: Schechter K-band function
    # (field values, M*_K = -24.2 for h = 0.7; alpha -1.0 and -1.3 bracket clusters)
    Lmin = 10 ** (-0.4 * (11.75 - dmod - 3.28))
    Lstar = 10 ** (-0.4 * (-24.2 - 3.28))
    xmin = Lmin / Lstar

    def frac_above(alpha, power):
        """Share of sum(L^power) carried by galaxies above Lmin."""
        a = alpha + 1 + power
        tot = Gamma(a) if a > 0 else None
        if tot is None:
            return np.nan
        return gammaincc(a, xmin)  # regularized upper incomplete gamma
    for alpha in (-1.0, -1.3):
        print(f"alpha {alpha}: share of light above the limit {frac_above(alpha, 1):.2f};"
              f" share of sum L^(1/2) (eddy load ~ V^2 ~ sqrt(M)) {frac_above(alpha, 0.5):.2f}")
    return rows, Rm, LK, tm, frac_above




# ======================================================================= part 2
def project_density(rho, R, rt):
    """Mass inside a cylinder of radius R, for a sphere truncated at rt."""
    def Sigma(Rp):
        f = lambda z: rho(np.sqrt(Rp**2 + z**2))
        zmax = np.sqrt(max(rt**2 - Rp**2, 0))
        return 2 * quad(f, 0, zmax, limit=200)[0]
    return quad(lambda Rp: 2 * np.pi * Rp * Sigma(Rp), 0, min(R, rt), limit=100)[0]


def eddy_load(M, r):
    """Load of one galaxy's eddy inside radius r (stars M treated as a point)."""
    gN = G * M / r**2
    return g_eddy(gN) * r**2 / G


def run(path):
    rows, Rm, LK, tm, frac_above = main(path)
    Tg, bg, rcg, ne0 = GAS["Sanders 2003 / Reiprich 2001"]
    rt = 3.0 * Mpc
    # total load density the gas balance needs (isothermal beta model)
    A = 3 * bg * Tg * keV / (mu * mp)
    rc = rcg * kpc
    rho_tot = lambda r: A / (4 * np.pi * G) * (r**2 + 3 * rc**2) / (r**2 + rc**2) ** 2
    rho0 = mu_e * mp * ne0 * 1e6
    rho_gas = lambda r: rho0 * (1 + (r / rc) ** 2) ** (-1.5 * bg)
    RR = np.array([0.5, 1.0, 1.5, 2.0]) * Mpc
    Mtot2 = np.array([project_density(rho_tot, R, rt) for R in RR])
    Mgas2 = np.array([project_density(rho_gas, R, rt) for R in RR])

    rng = np.random.default_rng(1)
    print("\n=== 3. Inside cylinders around Coma's center (10^14 suns), sphere cut at 3 Mpc ===")
    print("R (Mpc):                          " + "  ".join(f"{R/Mpc:6.1f}" for R in RR))
    print("needed by the gas balance:        " + "  ".join(f"{m/Msun/1e14:6.2f}" for m in Mtot2))
    print("hot gas:                          " + "  ".join(f"{m/Msun/1e14:6.2f}" for m in Mgas2))
    results = {}
    for ups in (0.6, 1.0):
        Ms = ups * LK * Msun
        stars2 = np.array([Ms[Rm < R].sum() for R in RR])
        for alpha in (-1.0, -1.3):
            fstar = frac_above(alpha, 1.0)
            stars_c = stars2 / fstar
            for edge_rule in ("fixed 100", "fixed 230", "scaled 100", "scaled 230"):
                kind, Re0 = edge_rule.split(); Re0 = float(Re0) * kpc
                V = (G * Ms * gdag) ** 0.25
                Re = Re0 * (V / 176e3 if kind == "scaled" else np.ones_like(V))
                power = 0.5 if kind == "fixed" else 0.75
                ftot = frac_above(alpha, power)
                Me = eddy_load(Ms, Re)
                # project each eddy (load density ~ 1/r^2 inside Re) into the cylinders
                ed2 = np.zeros(len(RR))
                n = 400
                for Mi, Rei, Ri in zip(Me, Re, Rm):
                    rr = rng.uniform(0, Rei, n)      # 1/r^2 density: r uniform
                    u = rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
                    phi = rng.uniform(0, 2 * np.pi)
                    x = Ri + rr * u[:, 0]; y = rr * u[:, 1]
                    Rp = np.hypot(x, y)
                    ed2 += Mi * np.array([(Rp < R).mean() for R in RR])
                ed_c = ed2 / ftot
                tot = Mgas2 + stars_c + ed_c
                results[(ups, alpha, edge_rule)] = (stars_c, ed_c, tot)
    for key, (s, e, t) in results.items():
        print(f"M/L {key[0]}, faint slope {key[1]}, edge {key[2]:>10} kpc: stars " +
              " ".join(f"{x/Msun/1e14:5.2f}" for x in s) + " | eddies " +
              " ".join(f"{x/Msun/1e14:5.2f}" for x in e) + " | total/needed " +
              " ".join(f"{x/m:5.2f}" for x, m in zip(t, Mtot2)))
    return RR, Mtot2, Mgas2, results


if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "run":
    run(sys.argv[1])
