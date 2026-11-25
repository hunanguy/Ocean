"""Fit every SPARC galaxy with the eddy (Section 6, Equation 15) and with the radial acceleration relation.

Follows Li, Lelli, McGaugh & Schombert 2018 (A&A 615, A3; arXiv:1803.00022):
  * per galaxy: disk and bulge mass-to-light ratios, distance and inclination, with
    Gaussian priors: log Ydisk about log 0.5 and log Ybul about log 0.7, 0.1 dex;
    D about the SPARC distance with its error; i about the SPARC inclination with its error;
  * the fit is on g_obs = V_obs^2/R with error 2 V_obs dV_obs / R;
  * distance scales radii as D and baryon V^2 as D; inclination scales V_obs as 1/sin i.
Li et al. sample the posterior with emcee and report the maximum; we find the maximum
directly (emcee is not installed here). Each galaxy's posterior is profiled over the limit
g_dagger on a grid, so the same run gives the fit at one shared limit and with the limit
free galaxy by galaxy.

Models
  rar   : g = g_bar / (1 - exp(-sqrt(g_bar/g_dagger)))
  eddy, "loans" (Section 6, Equation 15; the default):
          g = g_bar + g_e,  g_e = sqrt(g_N g_dagger) / (1 + rho),
          g_N = G M(<r)/r^2, the galaxy's pull averaged over the sphere of radius r,
          rho/sqrt(1 + 2 rho) = y/sqrt(3),  y = g_N/g_dagger
          (the share of Ocean the galaxy's own loans tie up, rho/(1 + rho), compounding inward from
          one build's worth at the outskirts to the loan's energy deep inside, half where g_N = g_dagger)
  eddy, "cored": Equation 15 of versions 3.13-3.15, set by the total mass alone,
          g_e = (V^2/r) x^2/(1+x^2), x = r/R_t, V^4 = G M_b g_dagger, R_t = sqrt(G M_b/g_dagger),
          M_b = Ydisk L_disk + Ybul L_bul + 1.33 M_HI (all scaled by (D/D0)^2)
  other forms (comparisons, eddy only): "x/(1+x)", "1-exp(-x)", "enclosed" (power 1),
          "enclosed_p<k>", "enclosed_reach", "enclosed_compound", "enclosed_compound_half", "enclosed_v"

Run:  python3 sparc_fit.py          (the RAR and the eddy; writes results/profiles.npz)
      python3 sparc_fit.py cored    (one comparison form, eddy only; writes results/profiles_<form>.npz)
"""
import os
import zlib
import numpy as np
from multiprocessing import Pool
from scipy.optimize import minimize
import sparc_data as S

HERE = os.path.dirname(os.path.abspath(__file__))
LGRID = np.round(np.arange(-1.5, 1.5001, 0.025), 4)   # log10(g_dagger / 1e-10 m s^-2)
I0 = int(np.argmin(np.abs(LGRID - np.log10(1.20))))    # grid point nearest 1.20
LG_UD, LG_UB, SIG_U = np.log10(0.5), np.log10(0.7), 0.1
SHAPES = {"cored": lambda x: x * x / (1 + x * x), "x/(1+x)": lambda x: x / (1 + x),
          "1-exp(-x)": lambda x: -np.expm1(-x)}
DEFAULT_FORM = "loans"      # the eddy of Section 6 (Equation 15); see free_share
ALIAS = {"loans": "enclosed_compound_third"}
FORM = DEFAULT_FORM
MODELS = ("rar", "eddy")


def free_share(y, form):
    form = ALIAS.get(form, form)
    """Share of Ocean left free to build the eddy, y = g_N/g_dag. "enclosed_p<k>": 1/(1 + y^k).
    "enclosed_reach": a loan holds its Ocean for a time growing with its energy (y) and draws on one
    build's worth of Ocean plus as many more as its extra energy needs (1 + y), so it is tied up
    y(1 + y) of the time: 1/(1 + y + y^2)."""
    if form == "enclosed_reach":
        return 1 / (1 + y + y * y)
    if form == "enclosed_compound":
        # tie-up compounding inward: the local power d ln(rho)/d ln(y) is 1 + (share tied up),
        # 1 outside (random loans, one build's worth) rising to 2 deep inside (the pull's energy);
        # integrated, rho/sqrt(1 + 2 rho) = y, so rho = y^2 + y sqrt(1 + y^2)
        rho = y * y + y * np.sqrt(1 + y * y)
        return 1 / (1 + rho)
    if form == "enclosed_compound_third":
        # the same compounding with c = 1/sqrt(3): half the Ocean tied up (rho = 1) exactly where
        # the pull equals the limit, the same g_dag that sets the outer speed (V^4 = G M g_dag)
        c = y / np.sqrt(3)
        rho = c * c + c * np.sqrt(1 + c * c)
        return 1 / (1 + rho)
    if form == "enclosed_compound_half":
        # the same compounding, with loans at the outside tying up half as much: rho/sqrt(1 + 2 rho) = y/2,
        # so rho = c^2 + c sqrt(1 + c^2) with c = y/2 (the 1/2 read off SPARC, not derived)
        c = y / 2
        rho = c * c + c * np.sqrt(1 + c * c)
        return 1 / (1 + rho)
    k = float(form.split("_p")[1]) if "_p" in form else 1.0
    return 1 / (1 + y ** k)


def unpack(g, th):
    if g["has_bul"]:
        lud, lub, D, inc = th
    else:
        lud, D, inc = th
        lub = LG_UB
    return lud, lub, D, inc


def model_g(g, th, lgd, model):
    """Return g_obs, sigma_g, g_model (all (km/s)^2/kpc) at parameters th."""
    lud, lub, D, inc = unpack(g, th)
    Ud, Ub, fD = 10 ** lud, 10 ** lub, D / g["D"]
    s = np.sin(np.radians(g["inc"])) / np.sin(np.radians(inc))
    R = g["R"] * fD
    V, eV = g["Vobs"] * s, g["eV"] * s
    gobs, sig = V * V / R, 2 * V * eV / R
    Vb2 = (g["Vgas"] * np.abs(g["Vgas"]) + Ud * g["Vdisk"] * np.abs(g["Vdisk"])
           + Ub * g["Vbul"] * np.abs(g["Vbul"])) * fD
    gbar = Vb2 / R
    gd = 10 ** lgd * S.GDAG_UNIT
    if model == "rar":
        y = np.maximum(gbar, 1e-12) / gd
        gm = np.where(gbar > 0, gbar / (-np.expm1(-np.sqrt(y))), gbar)
    elif ALIAS.get(FORM, FORM).startswith("enclosed"):
        # the eddy at each radius answers to the stars and gas inside that radius (Eq. 15, cored,
        # with M_b replaced by M(<r)); "enclosed_v" takes every part as its round stand-in R V|V|/G.
        # "enclosed_p<k>": the share of Ocean left free to build the eddy is 1/(1 + (g_N/g_dag)^k)
        # (k = 1 is "enclosed"; k = 2 when the time a loan holds its Ocean goes with the energy
        # the pull holds there, which grows as the pull squared); "enclosed_reach": see free_share
        if FORM == "enclosed_v":
            Mr = Ud * g["Menc_disk_v"] + Ub * g["Menc_bul"] + g["Menc_gas_v"]
        else:
            Mr = Ud * g["Menc_disk"] + Ub * g["Menc_bul"] + g["Menc_gas"]
        gN = S.G * Mr * fD ** 2 / R ** 2
        gm = gbar + np.sqrt(gN * gd) * free_share(gN / gd, FORM)
    else:
        M = (Ud * g["Ldisk"] + Ub * g["Lbul"] + g["Mgas"]) * fD ** 2
        Rt = np.sqrt(S.G * M / gd)
        x = R / Rt
        gm = gbar + np.sqrt(S.G * M * gd) / R * SHAPES[FORM](x)
    return gobs, sig, gm


def chi2(g, th, lgd, model):
    gobs, sig, gm = model_g(g, th, lgd, model)
    return float(np.sum(((gobs - gm) / sig) ** 2))


def prior2(g, th):
    lud, lub, D, inc = unpack(g, th)
    p = ((lud - LG_UD) / SIG_U) ** 2 + ((D - g["D"]) / g["e_D"]) ** 2 + ((inc - g["inc"]) / g["e_inc"]) ** 2
    if g["has_bul"]:
        p += ((lub - LG_UB) / SIG_U) ** 2
    return p


def bounds(g):
    b = [(-2.0, 1.5)] + ([(-2.0, 1.5)] if g["has_bul"] else [])
    return b + [(max(0.05 * g["D"], 0.05), 5 * g["D"]), (1.0, 90.0)]


def start(g):
    return np.array([LG_UD] + ([LG_UB] if g["has_bul"] else []) + [g["D"], g["inc"]])


def m2lnp(th, g, lgd, model):
    return chi2(g, th, lgd, model) + prior2(g, th)


def best(g, lgd, model, x0s):
    out = None
    for x0 in x0s:
        r = minimize(m2lnp, x0, args=(g, lgd, model), method="L-BFGS-B", bounds=bounds(g))
        if out is None or r.fun < out.fun:
            out = r
    return out


def fit_galaxy(g):
    res = {}
    for model in MODELS:
        # several starts at the grid point nearest 1.20, then sweep out both ways warm-started
        b = bounds(g)
        rng = np.random.default_rng(zlib.crc32(g["name"].encode()))   # same starts on every run
        x0s = [start(g)] + [np.array([rng.uniform(lo, hi) for lo, hi in b]) for _ in range(6)]
        n = len(LGRID)
        P, C, TH = np.zeros(n), np.zeros(n), np.zeros((n, len(b)))
        r = best(g, LGRID[I0], model, x0s)
        P[I0], C[I0], TH[I0] = r.fun, chi2(g, r.x, LGRID[I0], model), r.x
        for rng_ in (range(I0 + 1, n), range(I0 - 1, -1, -1)):
            prev = r.x
            for k in rng_:
                rk = best(g, LGRID[k], model, [prev, start(g)])
                P[k], C[k], TH[k] = rk.fun, chi2(g, rk.x, LGRID[k], model), rk.x
                prev = rk.x
        res[model] = dict(P=P, C=C, TH=TH)
    return g["name"], res


def init(form, models):
    global FORM, MODELS
    FORM, MODELS = form, models


def main(form=DEFAULT_FORM):
    models = ("rar", "eddy") if form == DEFAULT_FORM else ("eddy",)
    init(form, models)
    gals = S.load()
    with Pool(max(os.cpu_count(), 1), initializer=init, initargs=(form, models)) as pool:
        out = dict(pool.map(fit_galaxy, gals, chunksize=1))
    names = [g["name"] for g in gals]
    save = dict(lgrid=LGRID, names=np.array(names))
    for model in models:
        save[model + "_P"] = np.array([out[n][model]["P"] for n in names])
        save[model + "_C"] = np.array([out[n][model]["C"] for n in names])
        save[model + "_TH"] = np.array([np.pad(out[n][model]["TH"], ((0, 0), (0, 4 - out[n][model]["TH"].shape[1])),
                                               constant_values=np.nan) for n in names], dtype=float)
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    fn = "profiles.npz" if form == DEFAULT_FORM else "profiles_" + form.replace("/", "_over_") + ".npz"
    np.savez(os.path.join(HERE, "results", fn), **save)
    print("wrote results/" + fn)


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FORM)
