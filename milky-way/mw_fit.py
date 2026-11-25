"""The vertical test: the eddy of Section 6 against cold dark matter and a force parallel to the
baryons' own (the class superfluid dark matter belongs to), on the same Milky Way data.

Units: kpc, km/s, Msun. G = 4.30091e-6 kpc (km/s)^2 / Msun. 1 (km/s)^2/kpc = 3.2408e-14 m/s^2.
Baryons as Lisanti et al. 2023: Hernquist bulge (scale radius 0.6 kpc, mass free), double-exponential
stellar and gas disks (stellar scale length, both scale heights and both normalizations free; gas scale
length twice the stellar). Disk forces from the exact Bessel-integral form for a double-exponential disk.
"""
import numpy as np, sys
from scipy.special import j0, j1
from scipy.optimize import minimize
import mw_data as D

G = 4.30091e-6
ACC = 3.2408e-14                      # m/s^2 per (km/s)^2/kpc
GDAG_UNIT = 1e-10/ACC                 # 1e-10 m/s^2 in (km/s)^2/kpc  (= 3085.7)

K = np.linspace(1e-4, 160.0, 24000)   # wavenumber grid, 1/kpc
DK = K[1] - K[0]
W = np.full(K.size, DK); W[0] = W[-1] = DK/2

def _vert(k, z, h):
    """I(k,z) and dI/dz for the unit-normalized exponential layer e^{-|z|/h}/(2h), z >= 0."""
    a = 1.0/h
    ekz, eaz = np.exp(-k*z), np.exp(-a*z)
    d = k - a
    small = np.abs(d) < 1e-6
    ds = np.where(small, 1.0, d)
    B = np.where(small, z*ekz, (eaz - ekz)/ds)
    dB = np.where(small, ekz*(1 - k*z), (-a*eaz + k*ekz)/ds)
    A, dA = ekz/(a + k), -k*ekz/(a + k)
    C, dC = eaz/(k + a), -a*eaz/(k + a)
    return (A + B + C)/(2*h), (dA + dB + dC)/(2*h)

_JCACHE = {}
def _bessel(R):
    key = (R.tobytes(),)
    if key not in _JCACHE:
        _JCACHE[key] = (j0(np.outer(R, K))*W, j1(np.outer(R, K))*W*K)
    return _JCACHE[key]

def disk_acc(R, z, rho0, hR, hz):
    """(a_R, a_z) in (km/s)^2/kpc for rho = rho0 exp(-R/hR - |z|/hz), rho0 in Msun/kpc^3, at points R
    sharing one height z >= 0. a_R < 0 points inward, a_z < 0 points toward the plane."""
    R = np.atleast_1d(np.asarray(R, float)); z = float(np.atleast_1d(z)[0])
    J0w, J1wk = _bessel(R)
    St = 2*rho0*hz*hR**2/(1 + (K*hR)**2)**1.5               # Hankel transform of the surface density
    I, dI = _vert(K, z, hz)
    return -2*np.pi*G*(J1wk @ (St*I)), 2*np.pi*G*(J0w @ (St*dI))

def sph_acc(R, z, gfun):
    r = np.hypot(R, z); g = gfun(r)
    return -g*R/r, -g*z/r

def baryons(p):
    """p: dict with rs (stellar disk rho at center, Msun/pc^3), hR, hz, rg, hgz, Mb (1e10 Msun)."""
    return p

def acc_baryon(R, z, p):
    aR1, az1 = disk_acc(R, z, p['rs']*1e9, p['hR'], p['hz'])
    aR2, az2 = disk_acc(R, z, p['rg']*1e9, 2*p['hR'], p['hgz'])
    Mb = p['Mb']*1e10
    aR3, az3 = sph_acc(R, z, lambda r: G*Mb/(r + 0.6)**2)
    return aR1 + aR2 + aR3, az1 + az2 + az3

def masses(p):
    Md = 4*np.pi*p['rs']*1e9*p['hR']**2*p['hz']
    Mg = 4*np.pi*p['rg']*1e9*(2*p['hR'])**2*p['hgz']
    return Md, Mg, p['Mb']*1e10

def baryon_obs(p):
    R0 = D.R0
    rs_loc = p['rs']*np.exp(-R0/p['hR']); rg_loc = p['rg']*np.exp(-R0/(2*p['hR']))
    sig_s = 2*rs_loc*p['hz']*1e3*(1 - np.exp(-1.1/p['hz']))
    sig_g = 2*rg_loc*p['hgz']*1e3*(1 - np.exp(-1.1/p['hgz']))
    return dict(hR=p['hR'], hz=p['hz'], rho_g=rg_loc, sig_s=sig_s, sig_g=sig_g)

# ---------------------------------------------------------------- models
def nfw_g(rho, gam, rs):
    x = np.logspace(-5, 3, 4000)
    m = np.concatenate([[0], np.cumsum(0.5*(x[1:]**(2-gam)*(1+x[1:])**(gam-3) + x[:-1]**(2-gam)*(1+x[:-1])**(gam-3))*np.diff(x))])
    m += x[0]**(3-gam)/(3-gam)
    M = lambda r: 4*np.pi*rho*1e9*rs**3*np.interp(r/rs, x, m)
    return lambda r: G*M(r)/r**2

DEFAULT_FORM = "loans"     # the eddy of Section 6: see eddy_g

def eddy_g(Mtot, gdag, form=DEFAULT_FORM, p=None):
    """The eddy's turning g(r). "loans" (Section 6, Equation 15): at each radius the eddy answers to the
    galaxy's pull averaged over the sphere there, g_N = G M(<r)/r^2, and is built only from the Ocean the
    galaxy's own loans leave free: g = sqrt(g_N g_dag)/(1 + rho), rho/sqrt(1 + 2 rho) = y/sqrt(3), y = g_N/g_dag.
    "cored": Equation 15 of versions 3.13-3.15, set by the total mass alone. Other forms: comparisons."""
    gd = gdag*GDAG_UNIT
    if form == "loans":
        form = "enclosed_compound_third"
    if form.startswith("enclosed"):
        # the eddy at each radius answers to the stars and gas inside that radius: Eq. (15), cored,
        # with the total mass replaced by the mass inside the sphere of radius r. "enclosed_p<k>": the
        # share of Ocean left free to build the eddy is 1/(1 + (g_N/g_dag)^k); "enclosed" is k = 1
        # "enclosed_reach": share left free 1/(1 + y + y^2), y = g_N/g_dag (see sparc/sparc_fit.py)
        k = float(form.split("_p")[1]) if "_p" in form else 1.0
        rg = np.logspace(-3, 3, 600); Mr = enclosed_mass(rg, p)
        def g(r):
            M = np.interp(np.log(r), np.log(rg), Mr)
            gN = G*M/r**2; y = gN/gd
            if form == "enclosed_reach": free = 1/(1 + y + y*y)
            elif form == "enclosed_compound": free = 1/(1 + y*y + y*np.sqrt(1 + y*y))
            elif form == "enclosed_compound_half": c = y/2; free = 1/(1 + c*c + c*np.sqrt(1 + c*c))
            elif form == "enclosed_compound_third": c = y/np.sqrt(3); free = 1/(1 + c*c + c*np.sqrt(1 + c*c))
            else: free = 1/(1 + y**k)
            return np.sqrt(gN*gd)*free
        return g, (G*Mtot*gd)**0.25, np.sqrt(G*Mtot/gd)
    V2 = np.sqrt(G*Mtot*gd); Rt = np.sqrt(G*Mtot/gd)
    S = {"cored": lambda x: x*x/(1 + x*x), "x/(1+x)": lambda x: x/(1 + x), "1-exp(-x)": lambda x: 1 - np.exp(-x)}[form]
    return (lambda r: V2/r*S(r/Rt)), np.sqrt(V2), Rt

_GLX, _GLW = np.polynomial.legendre.leggauss(64)

def _disk_sph_mass(r, rho0, hR, hz):
    """Mass of rho0 exp(-R/hR - |z|/hz) inside the sphere of radius r (r an array, kpc)."""
    r = np.asarray(r, float)[:, None]
    zt = np.minimum(r, 40*hz)                                  # beyond 40 scale heights nothing is left
    z = 0.5*zt*(_GLX + 1); w = 0.5*zt*_GLW                    # z in [0, min(r, 40 hz)]
    a = np.sqrt(np.maximum(r*r - z*z, 0))
    ring = 2*np.pi*hR**2*(1 - np.exp(-a/hR)*(1 + a/hR))       # integral of 2 pi R e^{-R/hR} dR from 0 to a
    return 2*rho0*np.sum(w*np.exp(-z/hz)*ring, axis=1)

def enclosed_mass(r, p):
    Mb = p['Mb']*1e10
    return (_disk_sph_mass(r, p['rs']*1e9, p['hR'], p['hz']) + _disk_sph_mass(r, p['rg']*1e9, 2*p['hR'], p['hgz'])
            + Mb*r**2/(r + 0.6)**2)

def rar_nu(y): return 1.0/(1.0 - np.exp(-np.sqrt(y)))

BARYON_KEYS = ['rs', 'hR', 'hz', 'rg', 'hgz', 'Mb']
BOUNDS_B = [(0.01, 5), (1, 5), (0.05, 0.6), (0.0, 5), (0.02, 0.6), (0.0, 2)]   # Lisanti et al.'s prior ranges

def predict(model, th, form=DEFAULT_FORM):
    p = dict(zip(BARYON_KEYS, th[:6])); extra = th[6:]
    Rr, zr = D.RC_R, np.zeros_like(D.RC_R); Rk, zk = D.KZ_R, np.full_like(D.KZ_R, D.KZ_Z)
    aRb, _ = acc_baryon(Rr, zr, p); aRk, azk = acc_baryon(Rk, zk, p)
    Vs = 0.0
    if model == "cdm":
        g = nfw_g(*extra); aR = aRb + sph_acc(Rr, zr, g)[0]; az = azk + sph_acc(Rk, zk, g)[1]
    elif model == "parallel":
        a0 = extra[0]*GDAG_UNIT
        aR = aRb*rar_nu(np.abs(aRb)/a0)
        az = azk*rar_nu(np.hypot(aRk, azk)/a0)
    elif model.startswith("eddy"):
        gd = 1.20 if model == "eddy_fixed" else extra[0]
        Mtot = sum(masses(p)); g, V, Rt = eddy_g(Mtot, gd, form, p)
        aR = aRb + sph_acc(Rr, zr, g)[0]; az = azk + sph_acc(Rk, zk, g)[1]
        if model == "eddy_s": Vs = extra[1]
    vc = 0.5*(Vs + np.sqrt(Vs**2 + 4*Rr*np.maximum(-aR, 0)))      # co-rotating: v^2/R = -a_R + v V_s/R
    kz = -az/(2*np.pi*G)/1e6
    return vc, kz, baryon_obs(p)

def chi2_parts(model, th, form=DEFAULT_FORM):
    vc, kz, b = predict(model, th, form)
    c_rc = np.sum(((vc - D.RC_V)/D.RC_ERR)**2)
    c_kz = np.sum(((kz - D.KZ)/D.KZ_ERR)**2)
    c_b = (((b['hR'] - D.HSTAR_R[0])/D.HSTAR_R[1])**2 + ((b['hz'] - D.HSTAR_Z[0])/D.HSTAR_Z[1])**2
           + ((b['rho_g'] - D.RHO_GAS0[0])/D.RHO_GAS0[1])**2 + ((b['sig_s'] - D.SIG_STAR[0])/D.SIG_STAR[1])**2
           + ((b['sig_g'] - D.SIG_GAS[0])/D.SIG_GAS[1])**2)
    c_p = 0.0
    if model in ("parallel", "eddy", "eddy_s"):
        c_p = ((th[6] - D.GDAG[0])/D.GDAG[1])**2
    return c_rc, c_kz, c_b, c_p

def chi2(th, model, form=DEFAULT_FORM):
    bounds = BOUNDS_B + MODELS[model]['extra']
    if any(not (lo <= x <= hi) for x, (lo, hi) in zip(th, bounds)): return 1e9
    return sum(chi2_parts(model, th, form))

MODELS = {
    "cdm":      dict(extra=[(0.0, 10.0), (0.0, 2.5), (1.0, 100.0)], start=[0.01, 1.0, 19.0]),   # Lisanti et al. 2023 ranges: gamma [0, 10] cut to < 3 (finite mass)   # rho_DM tilde (Msun/pc^3), gamma, r_s
    "parallel": dict(extra=[(0.3, 3.0)], start=[1.2]),                                       # a0 (1e-10 m/s^2)
    "eddy":     dict(extra=[(0.3, 3.0)], start=[1.2]),                                       # g_dagger (1e-10 m/s^2)
    "eddy_fixed": dict(extra=[], start=[]),                                                 # g_dagger held at 1.20
    "eddy_s":   dict(extra=[(0.3, 3.0), (0.0, 19.0)], start=[1.2, 10.0]),                     # g_dagger, V_s (km/s)
}
B_STARTS = [[1.0, 2.6, 0.31, 0.15, 0.13, 0.9], [0.6, 3.0, 0.3, 0.1, 0.15, 1.5], [1.5, 2.2, 0.28, 0.2, 0.1, 0.5]]

def fit(model, form=DEFAULT_FORM):
    m = MODELS[model]; bounds = BOUNDS_B + m['extra']; best = None
    for bs in B_STARTS:
        x0 = np.array(bs + m['start'])
        r = minimize(chi2, x0, args=(model, form), method="Powell", bounds=bounds, options=dict(maxiter=20000, xtol=1e-5, ftol=1e-7))
        r = minimize(chi2, r.x, args=(model, form), method="Nelder-Mead", options=dict(maxiter=8000, xatol=1e-6, fatol=1e-7, adaptive=True))
        if best is None or r.fun < best.fun: best = r
    return best

if __name__ == "__main__":
    import os
    FORM = os.environ.get("EDDY_FORM", DEFAULT_FORM)
    models = sys.argv[1:] or list(MODELS)
    for mdl in models:
        r = fit(mdl, FORM)
        parts = chi2_parts(mdl, r.x, FORM); n = 26 + 43 + 5 + (1 if mdl in ("parallel", "eddy", "eddy_s") else 0)
        k = len(r.x)
        print(f"{mdl:9s} chi2 = {r.fun:7.2f}  [RC {parts[0]:.1f}, Kz {parts[1]:.1f}, baryons {parts[2]:.1f}, prior {parts[3]:.1f}]  "
              f"params {k}, BIC = {r.fun + k*np.log(n):.1f}", flush=True)
        print("          ", np.round(r.x, 4).tolist(), flush=True)
        if FORM == DEFAULT_FORM:                 # keep the saved best fits current (read by mw_report.py and the check)
            import json
            bf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_fits.json")
            d = json.load(open(bf)) if os.path.exists(bf) else {}
            d["bovyrix_" + mdl] = r.x.tolist(); json.dump(d, open(bf, "w"), indent=1)
