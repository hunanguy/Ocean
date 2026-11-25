"""Fit the settled Ocean held fixed, the shortfall (two thinning rules) and the
survey's two-number form to DESI DR2 BAO, alone and with each supernova sample;
write results.json, which the paper's check reads."""
import json, numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.stats import chi2 as CHI2, norm
from model import model_E, chi2_of, weff
from supernovae import Sample, DIRS

H0_KMS = 70.0           # only to turn redshift and rates into years; nothing is fitted to it
def lookback_gyr(z, Om=0.31):
    from scipy.integrate import quad
    return quad(lambda x: 1/((1+x)*np.sqrt(Om*(1+x)**3 + 1 - Om)), 0, z)[0]*977.8/H0_KMS

def sigma(d, k): return float(norm.isf(CHI2.sf(d, k)/2))

def analyse(sample):
    tot = (lambda z, E: chi2_of(z, E)[0]) if sample is None else (lambda z, E: chi2_of(z, E)[0] + sample.chi2(z, E))
    def fit(kind, starts, bounds):
        best = None
        for s in starts:
            r = minimize(lambda p: tot(*model_E(p, kind)[:2]), s, method='Nelder-Mead', bounds=bounds,
                         options=dict(xatol=1e-6, fatol=1e-7, maxiter=6000))
            if best is None or r.fun < best.fun: best = r
        return best
    rl = fit('lcdm', [[0.3]], [(0.05, 0.7)])
    z, E, Om, _ = model_E(rl.x, 'lcdm'); s = chi2_of(z, E)[1]
    out = dict(held_fixed=dict(chi2=rl.fun, Om=Om, h_rd=299792.458/s/100))
    rc = fit('cpl', [[0.3, -0.85, -0.5], [0.33, -0.7, -1.0], [0.3, -0.9, 0.0], [0.32, -0.75, -0.8]], [(0.05, 0.7), (-2, 0), (-4, 2)])
    out['form'] = dict(dchi2=rc.fun - rl.fun, sigma=sigma(rl.fun - rc.fun, 2), Om=rc.x[0], w0=rc.x[1], wa=rc.x[2], w_z15=rc.x[1] + rc.x[2]*1.5/2.5)
    zmax = 0.70 if sample is not None else 1.20
    for w_u in (0, 1):
        res = []
        for zon in np.arange(0.01, zmax + 1e-9, 0.01):
            aon = 1/(1+zon)
            r = minimize_scalar(lambda x: tot(*model_E((x, aon), 'ocean', w_u)[:2]), bounds=(0.1, 1.5),
                                method='bounded', options=dict(xatol=1e-7))
            res.append((zon, r.fun, r.x))
        res = np.array(res); i = np.argmin(res[:, 1]); zb, cb, xb = res[i]
        ok = res[res[:, 1] <= cb + 1][:, 0]; worse = res[(res[:, 1] > rl.fun) & (res[:, 0] > zb)][:, 0]
        z, E, Om, ex = model_E((xb, 1/(1+zb)), 'ocean', w_u)
        w = weff(1/(1+z), ex['eps'])
        out[f'shortfall_wu{w_u}'] = dict(dchi2=cb - rl.fun, sigma=sigma(rl.fun - cb, 1), onset_z=round(zb, 2),
            onset_1sigma=[round(ok.min(), 2), round(ok.max(), 2)], onset_gyr=lookback_gyr(zb), Om=Om, w_today=w[0],
            settled_today=ex['eps'][0], K_over_H0=ex['K']/np.sqrt(xb + ex['eps'][0]),
            K_over_Hdefault=ex['K'], worse_than_fixed_beyond_z=(round(worse.min(), 2) if len(worse) else None),
            scan=[[round(a, 2), b - rl.fun] for a, b, _ in res])
    return out

if __name__ == '__main__':
    results = {'DESI DR2 alone': analyse(None)}; missing = []
    for name in DIRS:
        try:
            results[name] = analyse(Sample(name)); results[name]['n_sn'] = len(Sample(name).mu)
        except OSError as ex:
            print(f'{name}: data not found ({ex}); skipped'); missing.append(name)
    # results.json is what the paper's check reads; never overwrite it with a partial run
    out = 'results_partial.json' if missing else 'results.json'
    json.dump(results, open(out, 'w'), indent=1, default=float)
    if missing: print(f'Supernova samples missing ({", ".join(missing)}): wrote {out}; results.json left as it was (see README, Data).')
    for k, v in results.items():
        print(k, {kk: (round(vv['dchi2'], 2) if isinstance(vv, dict) and 'dchi2' in vv else None) for kk, vv in v.items()})
