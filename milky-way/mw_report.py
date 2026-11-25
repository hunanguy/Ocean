"""Turning at the Sun and fit quality for the saved best fits (best_fits.json).
Usage: python3 mw_report.py   (from inside milky-way/)"""
import json, os, numpy as np
import mw_fit as F, mw_data as D, mw_fit_zhang as Z
HERE = os.path.dirname(os.path.abspath(__file__))
BEST = json.load(open(os.path.join(HERE, "best_fits.json")))

def turning(model, th):
    p = dict(zip(F.BARYON_KEYS, th[:6])); R0 = np.array([D.R0]); out = {}
    for z in (0.0, 0.5, 1.0):
        aRb, azb = F.acc_baryon(R0, z, p)
        if model == "parallel":
            nu = F.rar_nu(np.hypot(aRb, azb)/(th[6]*F.GDAG_UNIT)); aRx, azx = aRb*(nu - 1), azb*(nu - 1)
        else:
            g = F.nfw_g(*th[6:]) if model == "cdm" else F.eddy_g(sum(F.masses(p)), 1.20 if model == "eddy_fixed" else th[6], F.DEFAULT_FORM, p)[0]
            aRx, azx = F.sph_acc(R0, np.array([z]), g)
        out[z] = (aRb[0], azb[0], aRx[0], azx[0])
    return (out[0.0][0] + out[0.0][2])/out[0.0][0], 100*out[0.5][3]/out[0.5][1], 100*out[1.0][3]/out[1.0][1]

def chi2_bovyrix(model, th): return sum(F.chi2_parts(model, np.array(th)))
def chi2_lisanti(model, x): return Z.chi2(np.array(x), model)

if __name__ == "__main__":
    for data, fn, strip in (("Bovy & Rix 2013 vertical force", chi2_bovyrix, 0), ("Lisanti et al. 2023 (Zhang et al.) vertical data", chi2_lisanti, 3)):
        print(data)
        for m in ("cdm", "parallel", "eddy", "eddy_fixed"):
            x = BEST[("bovyrix_" if strip == 0 else "lisanti_") + m]; th = x[:len(x) - strip]
            r, v05, v10 = turning(m, th)
            print(f"  {m:10s} chi2 {fn(m, x):7.2f}   at the Sun: radial x{r:.2f}, vertical +{v05:.1f}% (0.5 kpc), +{v10:.1f}% (1 kpc)")
