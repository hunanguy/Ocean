"""The eddy's edge from stacked weak lensing around isolated galaxies (Mistele et al. 2024,
ApJL 969 L3, Table 1 machine-readable; Mb,eff from their Table 2).
Ocean model: the galaxy's stars and gas as a point mass (R >= 50 kpc, as the authors use),
plus the eddy of Eq. (15) out to an edge Re; beyond Re everything inside the edge acts as
one mass. Free: Re, and a mass factor f on Mb (their M/L systematic is 0.1 dex).
Errors: statistical and systematic (ESD -> g_obs) in quadrature; covariances not public, so
neighbouring radii are treated as independent (chi^2 values are indicative).
Borrowed steps: their distances (H0 = 73), star masses from population models, gas from
scaling relations, photometric redshifts in the isolation cut.
"""
import sys, numpy as np
G = 4.30091e-6; GD = 1.2e-10 / 3.2408e-14       # kpc (km/s)^2 / Msun ; g† in (km/s)^2/kpc
def g_tot(R, M):
    gN = G * M / R**2; c = (gN / GD) / np.sqrt(3); B = c*c + c*np.sqrt(c*c + 1)
    return gN + np.sqrt(gN * GD) / (1 + B)
def vc(R, M, Re):
    g = np.where(R <= Re, g_tot(R, M), g_tot(Re, M) * Re**2 / R**2)
    return np.sqrt(R * g)
rows = {}
for l in open(sys.argv[1]):
    if l[:3] not in ("All", "LTG", "ETG"): continue
    s = l[:24].strip(); R = float(l[25:32])
    for b in range(4):
        f = l[33 + 21*b: 33 + 21*b + 20].split()
        if len(f) == 3: rows.setdefault((s, b), []).append((R, *map(float, f)))
Mb = {"All": [10.10, 10.66, 10.96, 11.29], "LTG": [10.08, 10.66, 10.95, 11.23], "ETG": [None, 10.68, 10.97, 11.30]}
Re_grid = np.r_[np.geomspace(60, 5000, 120), 1e9]
fgrid = 10**np.linspace(-0.4, 0.6, 101)
rmax = float(sys.argv[2]) if len(sys.argv) > 2 else 1000
print(f"fit range 50 kpc to {rmax:.0f} kpc")
for (s, b), d in sorted(rows.items()):
    if s not in Mb or Mb[s][b] is None: continue
    d = np.array(d); d = d[(d[:, 0] >= 50) & (d[:, 0] <= rmax * 1.01)]
    R, V, es, ey = d.T; e = np.hypot(es, ey); M0 = 10**Mb[s][b]
    chi = np.array([[np.sum(((vc(R, f*M0, Re) - V) / e)**2) for f in fgrid] for Re in Re_grid])
    best_f_noedge = fgrid[np.argmin(chi[-1])]
    prof = chi.min(axis=1); c0 = prof[-1]          # mass factor profiled
    fixed = chi[:, 50]                              # f = 1 (index of 10**0)
    lim = lambda c: Re_grid[np.argmax(c - c.min() <= 4)] if (c - c.min() <= 4).any() else np.nan
    print(f"{s} bin {b+1} (log Mb {Mb[s][b]}): n={len(R)}; no edge: chi2 {c0:5.1f}, mass factor {best_f_noedge:.2f} "
          f"(V {vc(np.array([300.]), best_f_noedge*M0, 1e9)[0]:.0f}, Eq.15 at f=1 {vc(np.array([300.]), M0, 1e9)[0]:.0f}); "
          f"best edge {Re_grid[np.argmin(prof)]:.0f} (chi2 better than no edge by {c0-prof.min():.1f}); 95% lower limit on edge {lim(prof):.0f} kpc (mass free), {lim(fixed):.0f} (mass fixed)")
