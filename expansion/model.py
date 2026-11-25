"""The settled Ocean's shortfall (Section 5.1): the model and DESI DR2 BAO distances.

Model (22 Nov 2026, the §5.1 candidate made quantitative):
  - the settled Ocean holds its default energy per volume eps_def while the
    drive supplied by what is gathered meets the need;
  - the drive per volume is K * rho_m (proportional to what is gathered);
  - the need, to hold eps at eps_def, is 3(1 + w_u) H eps;
  - after the onset (drive < need) eps evolves as
        d eps / d ln a = -3 (1 + w_u) eps + K rho_m / H ,
    capped at eps_def (the build builds settled Ocean and no more);
  - w_u is how the settled Ocean thins when not made up:
        w_u = 0 : its energy is merely spread over the growing volume,
        w_u = 1 : its current thins (the paper's "thinning of the current",
                  Eq. 39 with no supply), energy per volume as a^-6.
Units: eps_def = 1, H^2 = rho_m + eps (8 pi G / 3 absorbed). One unknown, K,
traded for the onset scale factor a_on.  Flat; radiation neglected (< 0.1%
at z <= 2.33).  BAO: D/r_d = s * (dimensionless distance), s = c/(H0 r_d)
free and minimized analytically, so no early-universe input enters.
"""
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.optimize import minimize

# DESI DR2, Table IV of arXiv:2503.14738 (DESI Collaboration, Abdul-Karim et al. 2025)
BGS = (0.295, 7.942, 0.075)                       # z, D_V/r_d, err
ANISO = [  # z, D_M/r_d, err, D_H/r_d, err, r_MH
    (0.510, 13.588, 0.167, 21.863, 0.425, -0.459),
    (0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
    (0.934, 21.576, 0.152, 17.641, 0.193, -0.416),
    (1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
    (1.484, 30.512, 0.760, 12.817, 0.516, -0.500),
    (2.330, 38.988, 0.531, 8.632, 0.101, -0.431),
]

def data_vectors():
    zs, vals, kinds = [BGS[0]], [BGS[1]], ['V']
    C = [[BGS[2]**2]]
    blocks = [np.array([[BGS[2]**2]])]
    for z, dm, edm, dh, edh, r in ANISO:
        zs += [z, z]; vals += [dm, dh]; kinds += ['M', 'H']
        blocks.append(np.array([[edm**2, r*edm*edh], [r*edm*edh, edh**2]]))
    n = len(vals); cov = np.zeros((n, n)); i = 0
    for b in blocks:
        k = b.shape[0]; cov[i:i+k, i:i+k] = b; i += k
    return np.array(zs), np.array(vals), kinds, np.linalg.inv(cov)

ZS, VALS, KINDS, ICOV = data_vectors()

def eps_history(x, a_on, w_u, a_grid):
    """eps(a) on a_grid (ascending, ending at 1); x = rho_m0/eps_def."""
    if a_on >= 1.0:
        return np.ones_like(a_grid), np.nan
    g = 3*(1 + w_u)
    H_on = np.sqrt(x*a_on**-3 + 1.0)
    K = g*H_on/(x*a_on**-3)                       # onset: K rho_m = g H eps_def
    def rhs(lna, y):
        a = np.exp(lna); e = y[0]; rm = x*a**-3
        H = np.sqrt(rm + e)
        d = -g*e + K*rm/H
        if e >= 1.0 and d > 0: d = 0.0
        return [d]
    sol = solve_ivp(rhs, [np.log(a_on), 0.0], [1.0], dense_output=True,
                    rtol=1e-9, atol=1e-12)
    eps = np.ones_like(a_grid)
    m = a_grid > a_on
    eps[m] = sol.sol(np.log(a_grid[m]))[0]
    return eps, K

def model_E(params, kind, w_u=0):
    """Returns (z grid, E(z)=H/H0, Om0, extra)."""
    z = np.linspace(0, 2.5, 2501); a = 1/(1+z)
    if kind == 'ocean':
        x, a_on = params
        ag = a[::-1]
        eps, K = eps_history(x, a_on, w_u, ag)
        eps = eps[::-1]
        H2 = x*a**-3 + eps
        E = np.sqrt(H2/H2[0])
        Om = x/(x + eps[0])
        return z, E, Om, dict(K=K, eps=eps)
    if kind == 'lcdm':
        (Om,) = params
        return z, np.sqrt(Om*(1+z)**3 + 1 - Om), Om, {}
    if kind == 'cpl':
        Om, w0, wa = params
        de = (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))
        return z, np.sqrt(Om*(1+z)**3 + (1-Om)*de), Om, {}

def predict(z, E):
    DM = np.concatenate([[0], cumulative_trapezoid(1/E, z)])
    DH = 1/E
    out = []
    for zz, k in zip(ZS, KINDS):
        dm = np.interp(zz, z, DM); dh = np.interp(zz, z, DH)
        out.append({'M': dm, 'H': dh, 'V': (zz*dm**2*dh)**(1/3)}[k])
    return np.array(out)

def chi2_of(z, E):
    t = predict(z, E)
    s = (t @ ICOV @ VALS)/(t @ ICOV @ t)          # best c/(H0 r_d)
    r = VALS - s*t
    return float(r @ ICOV @ r), s

def fit(kind, x0, bounds, w_u=0):
    def f(p):
        try:
            z, E, Om, _ = model_E(p, kind, w_u)
            if not np.all(np.isfinite(E)): return 1e9
            return chi2_of(z, E)[0]
        except Exception:
            return 1e9
    best = None
    for start in x0:
        r = minimize(f, start, method='Nelder-Mead', bounds=bounds,
                     options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000))
        if best is None or r.fun < best.fun: best = r
    return best

def weff(a, eps):
    lna = np.log(a); d = np.gradient(np.log(eps), lna)
    return -1 - d/3
