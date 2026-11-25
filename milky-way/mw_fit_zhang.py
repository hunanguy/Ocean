"""The vertical test on Lisanti et al. 2023's own data: rotation curve (Eilers et al. 2019), the stars and gas
constraints, and the vertical densities and dispersions of Zhang et al. 2013's three K-dwarf populations at the Sun,
read from Lisanti et al. 2023, Fig. A1 (fig_a1.json, extracted from the PDF's vector drawing by extract/fig_a1.py).
Vertical Jeans equation as Lisanti et al. Eq. (11): sigma^2(z) = -(1/n) int_z^inf n a_z dz', n = n~ exp(-z/h).
The normalizations n~ are fitted analytically for each population; the scale heights h are free."""
import json, sys, os, numpy as np
from scipy.optimize import minimize
import mw_fit as F, mw_data as D

Z = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig_a1.json')))
PANELS = {p['panel']: p['points'] for p in Z}
POPS = ['rich', 'int', 'poor']
NDAT = {k: np.array([[q['z'], q['y'], q['err_up']] for q in PANELS['n_' + k] if abs((q['z'] - 0.05)/0.1 - round((q['z'] - 0.05)/0.1)) < 0.05]) for k in POPS}
SDAT = {k: np.array([[q['z'], q['y'], q['err_up']] for q in PANELS['s_' + k]]) for k in POPS}
NOBS = sum(len(v) for v in NDAT.values()) + sum(len(v) for v in SDAT.values())

ZG = np.concatenate([np.linspace(0.3, 2.0, 70), np.linspace(2.05, 6.0, 40), np.linspace(6.2, 12.0, 20)])
R0A = np.array([D.R0])
from scipy.special import j0, j1
K2 = np.linspace(1e-4, 60.0, 6000); W2 = np.full(K2.size, K2[1] - K2[0]); W2[0] = W2[-1] = W2[0]/2
J0R, J1RK = j0(K2*D.R0)*W2, j1(K2*D.R0)*W2*K2
EKZ = np.exp(-K2[None, :]*ZG[:, None])          # fixed: heights >= 0.3 kpc, so k up to 60/kpc suffices

def disk_az_grid(rho0, hR, hz):
    a = 1.0/hz; k = K2[None, :]; z = ZG[:, None]
    ekz, eaz = EKZ, np.exp(-a*z); d = k - a; ds = np.where(np.abs(d) < 1e-6, 1.0, d)
    dB = np.where(np.abs(d) < 1e-6, ekz*(1 - k*z), (-a*eaz + k*ekz)/ds)
    dI = (-k*ekz/(a + k) + dB - a*eaz/(k + a))/(2*hz)
    St = 2*rho0*hz*hR**2/(1 + (K2*hR)**2)**1.5
    return 2*np.pi*F.G*((dI*St[None, :]) @ J0R)

def disk_aR_grid(rho0, hR, hz):
    a = 1.0/hz; k = K2[None, :]; z = ZG[:, None]
    ekz, eaz = EKZ, np.exp(-a*z); d = k - a; ds = np.where(np.abs(d) < 1e-6, 1.0, d)
    B = np.where(np.abs(d) < 1e-6, z*ekz, (eaz - ekz)/ds)
    I = (ekz/(a + k) + B + eaz/(k + a))/(2*hz)
    St = 2*rho0*hz*hR**2/(1 + (K2*hR)**2)**1.5
    return -2*np.pi*F.G*((I*St[None, :]) @ J1RK)

def az_column(model, th, form=F.DEFAULT_FORM):
    """Total a_z (<0) on ZG at R0, and a_R there (for the parallel force's magnitude)."""
    p = dict(zip(F.BARYON_KEYS, th[:6])); extra = th[6:]
    az = disk_az_grid(p['rs']*1e9, p['hR'], p['hz']) + disk_az_grid(p['rg']*1e9, 2*p['hR'], p['hgz'])
    r = np.hypot(D.R0, ZG); Mb = p['Mb']*1e10; gb = F.G*Mb/(r + 0.6)**2
    az = az - gb*ZG/r
    if model == 'cdm':
        g = F.nfw_g(*extra); az = az - g(r)*ZG/r
    elif model == 'parallel':
        aR = disk_aR_grid(p['rs']*1e9, p['hR'], p['hz']) + disk_aR_grid(p['rg']*1e9, 2*p['hR'], p['hgz']) - gb*D.R0/r
        az = az*F.rar_nu(np.hypot(aR, az)/(extra[0]*F.GDAG_UNIT))
    elif model.startswith('eddy'):
        gd = 1.20 if model == 'eddy_fixed' else extra[0]
        g = F.eddy_g(sum(F.masses(p)), gd, form, p)[0]; az = az - g(r)*ZG/r
    return az

def sigma_model(az, z, h):
    """sigma^2(z) = int_z^inf exp(-(z'-z)/h) (-a_z(z')) dz' on the grid, for each data height z."""
    out = []
    for zz in z:
        zs = np.concatenate([[zz], ZG[ZG > zz]]); a = np.interp(zs, ZG, -az)
        w = np.exp(-(zs - zz)/h)*a
        out.append(np.sum(0.5*(w[1:] + w[:-1])*np.diff(zs)))
    return np.sqrt(np.maximum(out, 0))

def chi2_vertical(model, th, hs, form=F.DEFAULT_FORM):
    az = az_column(model, th, form); c_n = c_s = 0.0
    for k, h in zip(POPS, hs):
        zn, ln, en = NDAT[k].T
        w = 1/en**2; lnt = np.sum(w*(ln + zn/h))/np.sum(w)            # best ln n~ for this h
        c_n += np.sum(((lnt - zn/h - ln)/en)**2)
        zs, s, es = SDAT[k].T
        c_s += np.sum((((sigma_model(az, zs, h)) - s)/es)**2)
    return c_n, c_s

H_BOUNDS = [(0.1, 1.0)]*3
def chi2(x, model, form=F.DEFAULT_FORM):
    th, hs = x[:-3], x[-3:]
    bounds = F.BOUNDS_B + F.MODELS[model]['extra'] + H_BOUNDS
    if any(not (lo <= v <= hi) for v, (lo, hi) in zip(x, bounds)): return 1e9
    c_rc, _, c_b, c_p = F.chi2_parts(model, th, form)
    c_n, c_s = chi2_vertical(model, th, hs, form)
    return c_rc + c_b + c_p + c_n + c_s

def parts(model, x, form=F.DEFAULT_FORM):
    th, hs = x[:-3], x[-3:]; c_rc, _, c_b, c_p = F.chi2_parts(model, th, form); c_n, c_s = chi2_vertical(model, th, hs, form)
    return dict(rc=c_rc, n=c_n, sigma=c_s, baryons=c_b, prior=c_p)

def fit(model, form=F.DEFAULT_FORM, starts=None):
    m = F.MODELS[model]; best = None
    if starts is None:
        starts = [bs + m['start'] + [0.26, 0.46, 0.9] for bs in F.B_STARTS[:1]]
        bf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_fits.json")
        if os.path.exists(bf) and ("bovyrix_" + model) in json.load(open(bf)):
            starts.insert(0, json.load(open(bf))["bovyrix_" + model] + [0.26, 0.46, 0.9])
    for x0 in starts:
        r = minimize(chi2, np.array(x0, float), args=(model, form), method="Nelder-Mead", options=dict(maxiter=30000, xatol=1e-6, fatol=1e-6, adaptive=True))
        r = minimize(chi2, r.x, args=(model, form), method="Nelder-Mead", options=dict(maxiter=30000, xatol=1e-7, fatol=1e-7, adaptive=True))
        if best is None or r.fun < best.fun: best = r
    return best

if __name__ == "__main__":
    FORM = os.environ.get("EDDY_FORM", F.DEFAULT_FORM)
    for mdl in sys.argv[1:]:
        r = fit(mdl, FORM); P = parts(mdl, r.x, FORM)
        nobs = 26 + NOBS + 5 + (1 if mdl in ("parallel", "eddy", "eddy_s") else 0); k = len(r.x) + 3    # + the three n~
        print(f"{mdl:10s} chi2 = {r.fun:7.2f}  " + ", ".join(f"{a} {b:.1f}" for a, b in P.items()) +
              f"  | obs {nobs}, params {k}, dof {nobs - k}, BIC {r.fun + k*np.log(nobs):.1f}", flush=True)
        print("           ", np.round(r.x, 4).tolist(), flush=True)
        if FORM == F.DEFAULT_FORM:               # keep the saved best fits current (read by mw_report.py and the check)
            import json
            bf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_fits.json")
            d = json.load(open(bf)) if os.path.exists(bf) else {}
            d["lisanti_" + mdl] = r.x.tolist(); json.dump(d, open(bf, "w"), indent=1)
