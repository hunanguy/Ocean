#!/usr/bin/env python3
"""
check_ocean_math.py
-------------------
Consistency and accuracy checks for the mathematics of the Ocean formalism draft.

Every check names the place in the paper it tests and carries an "anchor": a short
piece of the paper's own LaTeX that states the claim. If the paper's wording or
number changes, the anchor is no longer found and the check fails, so the checks
cannot silently drift away from the text.

Kinds of check
  FORMULA      an equation is re-derived or tested numerically (identities at
               random points, Euler-Lagrange equations from a discretized action,
               dispersion relations from a numerically expanded Lagrangian)
  NUMBER       a numerical statement is recomputed from physical constants
  SIMULATION   a numerical experiment reported in the paper is re-run
  CONSISTENCY  the paper is checked against itself (symbols, references,
               citations, repeated values)
Outcomes
  PASS  agrees within the stated tolerance
  FAIL  disagrees, or the anchor is missing
  NOTE  agrees only with a stated caveat, or cannot be decided from the text

Usage:  python3 check_ocean_math.py [--build PATH] [--quick] [--report FILE]
Requires numpy and scipy. Exit status is 1 if any check fails.
"""
import argparse, importlib.util, re, sys, math
from pathlib import Path
import numpy as np

# ----------------------------------------------------------------- constants
# CODATA 2018 unless noted; c exact by the SI definition of the metre.
c = 299792458.0; G = 6.67430e-11; hbar = 1.054571817e-34; h = 2*math.pi*hbar
me = 9.1093837015e-31; e = 1.602176634e-19; eps0 = 8.8541878128e-12
alpha = 7.2973525693e-3; kB = 1.380649e-23; eV = e; MeV = 1e6*eV
Msun = 1.98847e30; GMsun = 1.32712440018e20; kpc = 3.0857e19; AU = 1.495978707e11
yr = 3.15576e7; mp = 1.67262192369e-27; u_amu = 1.66053906660e-27
lP = math.sqrt(hbar*G/c**3)

# ----------------------------------------------------------------- framework
RESULTS = []
def norm(s): return " ".join(s.split())

class Paper:
    def __init__(self, path):
        spec = importlib.util.spec_from_file_location("ocean_build", path)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        body = mod.BODY.replace("@@APPENDIX_A@@", getattr(mod, "APPENDIX_A", ""))
        self.body = body; self.n = norm(body); self.version = mod.VERSION
    def has(self, anchor): return norm(anchor) in self.n

def check(where, kind, what, anchor=None):
    """Decorator: register a check. The function returns (status, detail)."""
    def deco(fn):
        RESULTS.append(dict(where=where, kind=kind, what=what, anchor=anchor, fn=fn))
        return fn
    return deco

def close(x, target, rel):
    return abs(x - target) <= rel*abs(target)

def verdict(ok, detail, note=False):
    return ("PASS" if ok and not note else "NOTE" if ok else "FAIL"), detail

# ================================================================ FORMULAS
# --- Section 3: equations of motion, by varying a discretized action --------
def functional_derivative_check(L, fields, analytic, nx=40, nt=40, dx=0.05, dt=0.05):
    """Compare dS/d(field at a grid point), by finite differences of the discretized
    action, with the analytic Euler-Lagrange expression, at interior points."""
    t = np.arange(nt)*dt; x = np.arange(nx)*dx; T, X = np.meshgrid(t, x, indexing="ij")
    F = [f(T, X) for f in fields]
    def S(F):
        d = []
        for f in F:
            ft = (np.roll(f, -1, 0) - np.roll(f, 1, 0))/(2*dt)
            fx = (np.roll(f, -1, 1) - np.roll(f, 1, 1))/(2*dx)
            d.append((f, ft, fx))
        dens = L(d)[2:-2, 2:-2]
        return dens.sum()*dt*dx
    errs = []
    rng = np.random.default_rng(1)
    pts = [(rng.integers(6, nt-6), rng.integers(6, nx-6)) for _ in range(6)]
    for k in range(len(F)):
        A = analytic(T, X, F)[k]
        for (i, j) in pts:
            eps = 1e-6
            Fp = [f.copy() for f in F]; Fm = [f.copy() for f in F]
            Fp[k][i, j] += eps; Fm[k][i, j] -= eps
            num = (S(Fp) - S(Fm))/(2*eps)/(dt*dx)
            errs.append(abs(num - A[i, j])/(abs(A[i, j]) + 1e-3))
    return max(errs)

def _derivs(f, dt, dx):
    ft = np.gradient(f, dt, axis=0); fx = np.gradient(f, dx, axis=1)
    ftt = np.gradient(ft, dt, axis=0); fxx = np.gradient(fx, dx, axis=1)
    return ft, fx, ftt, fxx

@check("§3, Eq. (13)", "FORMULA",
       "Amount and phase equations follow from the minimal law, Eq. (29), by varying the action",
       anchor=r"\Box\rho = \tfrac{1}{2}\lambda\,\rho\left(\rho^{2} - v^{2}\right) - \rho\,\mu^{2},")
def _():
    lam, v = 1.3, 0.8; dt = dx = 0.05
    def L(d):   # flat 1+1, signature (-,+): (d rho)^2 = -rho_t^2 + rho_x^2; mu^2 = theta_t^2 - theta_x^2
        (r, rt, rx), (th, tht, thx) = d
        return -(-rt**2 + rx**2) + r**2*(tht**2 - thx**2) - lam/4*(r**2 - v**2)**2
    rho = lambda T, X: 1.0 + 0.1*np.sin(1.3*T + 0.7*X)
    th = lambda T, X: 0.6*T + 0.2*np.sin(0.9*X - 0.5*T)
    def analytic(T, X, F):
        r, t_ = F
        rt, rx, rtt, rxx = _derivs(r, dt, dx); tt, tx, ttt, txx = _derivs(t_, dt, dx)
        box_r = -rtt + rxx; mu2 = tt**2 - tx**2
        dS_dr = 2*box_r + 2*r*mu2 - lam*r*(r**2 - v**2)          # = 0  <=>  box rho = lam/2 rho(rho^2-v^2) - rho mu^2
        div = -np.gradient(r**2*tt, dt, axis=0) + np.gradient(r**2*tx, dx, axis=1)
        dS_dth = 2*div                                            # = 0  <=>  nabla_mu(rho^2 nabla^mu theta) = 0
        return [dS_dr, dS_dth]
    err = functional_derivative_check(L, [rho, th], analytic, dt=dt, dx=dx)
    return verdict(err < 2e-2, f"largest relative mismatch between varied action and Eq. (13): {err:.1e}")

@check("§3, Eq. (12)", "FORMULA",
       "Canonical case: L = X - V gives box(phi) = dV/dphi",
       anchor=r"\Box \phi \;=\; \frac{\partial \Veff}{\partial \phi} \;+\; C ,")
def _():
    lam, v = 0.9, 0.7; dt = dx = 0.05
    V = lambda p: lam/4*(p**2 - v**2)**2; dV = lambda p: lam*p*(p**2 - v**2)
    def L(d):
        (p, pt, px), = d
        return 0.5*(pt**2 - px**2) - V(p)                         # X = -1/2 (grad phi)^2
    ph = lambda T, X: 0.5 + 0.2*np.cos(0.8*T - 1.1*X)
    def analytic(T, X, F):
        p, = F; pt, px, ptt, pxx = _derivs(p, dt, dx)
        return [(-ptt + pxx) - dV(p)]                             # dS/dphi = box(phi) - V'
    err = functional_derivative_check(L, [ph], analytic, dt=dt, dx=dx)
    return verdict(err < 2e-2, f"largest relative mismatch: {err:.1e}")

@check("§3 and §11.4", "CONSISTENCY",
       "Uniform steady amount from Eq. (13) equals the value stated in §11.4",
       anchor=r"$\bar{\rho}^{2} = v^{2} + 2\mu^{2}/\lambda$, the value used in")
def _():
    lam, v, mu = 1.7, 0.9, 0.3
    from scipy.optimize import brentq
    r = brentq(lambda r: 0.5*lam*r*(r*r - v*v) - r*mu*mu, v, 3*v)
    target = math.sqrt(v*v + 2*mu*mu/lam)
    return verdict(close(r, target, 1e-10), f"root {r:.10f} vs sqrt(v^2+2mu^2/lam) {target:.10f}")

# --- §11.4: the minimal law, pressure, sound speed, gamma, dispersion ---------
def P_of(mu2, lam, v): return v*v*mu2 + mu2**2/lam

@check("§11.4", "FORMULA", "Integrating out the amount gives P(mu^2) = v^2 mu^2 + mu^4/lambda and P' = rho_bar^2",
       anchor=r"P(\mu^{2}) = v^{2}\mu^{2} +")
def _():
    lam, v = 1.4, 0.8; worst = 0
    for mu2 in [0.01, 0.1, 0.5]:
        rb2 = v*v + 2*mu2/lam
        Lval = rb2*mu2 - lam/4*(rb2 - v*v)**2
        worst = max(worst, abs(Lval - P_of(mu2, lam, v)))
        d = 1e-6; Pp = (P_of(mu2+d, lam, v) - P_of(mu2-d, lam, v))/(2*d)
        worst = max(worst, abs(Pp - rb2))
    return verdict(worst < 1e-8, f"largest difference {worst:.1e}")

def cs2_from_P(a, lam=1.0, v=1.0):
    mu2 = a*lam*v*v/2; d = 0.1*mu2
    P1 = (P_of(mu2+d, lam, v) - P_of(mu2-d, lam, v))/(2*d)
    P2 = (P_of(mu2+d, lam, v) - 2*P_of(mu2, lam, v) + P_of(mu2-d, lam, v))/d**2
    return P1/(P1 + 2*mu2*P2), P1

def dispersion_eq32(k, lam, v, mu):
    """Roots omega^2 of (w^2-k^2)(w^2-k^2-omega_rho^2) = 4 mu^2 w^2, omega_rho^2 = lam rho_bar^2."""
    M2 = lam*(v*v + 2*mu*mu/lam)
    # w^4 - w^2 (2k^2 + M^2 + 4mu^2) + k^2(k^2 + M^2) = 0
    b = 2*k*k + M2 + 4*mu*mu; cc = k*k*(k*k + M2)
    disc = math.sqrt(b*b - 4*cc)
    return (b - disc)/2, (b + disc)/2

def dispersion_from_lagrangian(k, lam, v, mu):
    """Expand the minimal law, Eq. (29), to second order about rho_bar, theta = mu t,
    numerically, and solve det(A^H H A) = 0 for omega^2 (flat 1+1, signature -+)."""
    rb = math.sqrt(v*v + 2*mu*mu/lam)
    def L(q):  # q = (r, r_t, r_x, phi_t, phi_x)
        r, rt, rx, pt, px = q
        rho = rb + r; tht = mu + pt; thx = px
        return (rt**2 - rx**2) + rho**2*(tht**2 - thx**2) - lam/4*(rho**2 - v*v)**2
    q0 = np.zeros(5); H = np.zeros((5, 5)); d = 1e-4
    for i in range(5):
        for j in range(5):
            e1 = np.eye(5)[i]*d; e2 = np.eye(5)[j]*d
            H[i, j] = (L(q0+e1+e2) - L(q0+e1-e2) - L(q0-e1+e2) + L(q0-e1-e2))/(4*d*d)
    def det(w):
        A = np.array([[1, -1j*w, 1j*k, 0, 0], [0, 0, 0, -1j*w, 1j*k]]).T
        D = A.conj().T @ H @ A
        return np.linalg.det(D).real
    from scipy.optimize import brentq
    ws = np.linspace(1e-6, 6, 6000); vals = [det(w) for w in ws]
    roots = [brentq(det, ws[i], ws[i+1]) for i in range(len(ws)-1) if vals[i]*vals[i+1] < 0]
    return sorted(r*r for r in roots)

@check("§11.4, Eq. (32)", "FORMULA",
       "The disturbance equation (32) follows from the minimal law expanded numerically",
       anchor=r"\left(\omega^{2} - k^{2}\right)\left(\omega^{2} - k^{2} - \omega_{\rho}^{2}\right) = 4\mu^{2}\omega^{2}")
def _():
    lam, v, mu = 1.0, 1.0, 0.35; worst = 0
    for k in [0.3, 0.9, 2.0]:
        a = dispersion_eq32(k, lam, v, mu); b = dispersion_from_lagrangian(k, lam, v, mu)
        worst = max(worst, max(abs(x - y)/y for x, y in zip(a, b)))
    return verdict(worst < 1e-4, f"largest relative difference in omega^2: {worst:.1e}")

@check("§11.4, Eq. (30)", "CONSISTENCY",
       "Sound speed three ways: from P, from the small-k slope of Eq. (32), and the stated (1+a)/(1+3a)",
       anchor=r"$c_{s}^{2} = (1 + a)/(1 + 3a)$")
def _():
    worst = 0
    for a in [1e-3, 0.1, 1.0, 10.0]:
        lam = v = 1.0; mu = math.sqrt(a*lam*v*v/2)
        fromP, _ = cs2_from_P(a); k = 1e-3*math.sqrt(1 + 3*a)
        w2, _ = dispersion_eq32(k, lam, v, mu); slope = w2/k**2 - 4*a*a/(1 + 3*a)**3*k*k   # remove the known k^4 term
        stated = (1 + a)/(1 + 3*a)
        worst = max(worst, abs(fromP - stated)/stated, abs(slope - stated)/stated)
    return verdict(worst < 1e-5, f"largest relative difference: {worst:.1e}")

@check("§11.4, Eq. (31)", "FORMULA",
       "gamma = -(2+3a)/(3a) from |g00| = P' c_s and g_ij = P'/c_s; below -1 for all a; -> -1 at large a",
       anchor=r"\gamma = -\frac{2 + 3a}{3a},")
def _():
    worst = 0; below = True
    for a in [1e-3, 0.05, 0.5, 2.0, 50.0]:
        def logs(a):
            cs2, P1 = cs2_from_P(a); cs = math.sqrt(cs2)
            return math.log(P1*cs), math.log(P1/cs)
        d = 1e-4*a
        g00p, gijp = logs(a+d); g00m, gijm = logs(a-d)
        gam = -(gijp - gijm)/(g00p - g00m)          # gamma = - dln g_ij / dln |g00|
        stated = -(2 + 3*a)/(3*a)
        worst = max(worst, abs(gam - stated)/abs(stated)); below &= stated < -1
    big = -(2 + 3*1e6)/(3*1e6)
    return verdict(worst < 1e-4 and below and abs(big + 1) < 1e-6,
                   f"largest relative difference {worst:.1e}; always below -1: {below}; a=1e6 gives {big:.7f}")

@check("§11.4", "NUMBER", "Gapped rest rhythm omega_0^2 = lambda v^2 + 6 mu^2 from Eq. (32) at k = 0",
       anchor=r"\omega_{0}^{2} = \lambda v^{2} + 6\mu^{2}")
def _():
    lam, v, mu = 1.3, 0.7, 0.4
    _, w2 = dispersion_eq32(0.0, lam, v, mu)
    return verdict(close(w2, lam*v*v + 6*mu*mu, 1e-12), f"{w2:.12f} vs {lam*v*v+6*mu*mu:.12f}")

@check("§11.4", "NUMBER", "At high k both branches approach omega = k +/- mu",
       anchor=r"approach $\omega = k \pm \mu$")
def _():
    lam, v, mu = 1.0, 1.0, 0.3; k = 2000.0
    w2a, w2b = dispersion_eq32(k, lam, v, mu)
    da, db = math.sqrt(w2a) - k, math.sqrt(w2b) - k
    return verdict(abs(abs(da) - mu) < 1e-3 and abs(abs(db) - mu) < 1e-3,
                   f"omega - k = {da:+.5f}, {db:+.5f} (mu = {mu})")

@check("§11.4", "NUMBER", "1 - c_s ~ a for small a",
       anchor=r"Since $1 - c_{s} \approx a$ for small $a$")
def _():
    a = 1e-4; cs = math.sqrt((1 + a)/(1 + 3*a))
    return verdict(close(1 - cs, a, 2e-3), f"1 - c_s = {1-cs:.6e} vs a = {a:.1e}")

@check("§7.7(3), §11.1", "FORMULA",
       "Gapless branch of Eq. (32): omega^2 = c_s^2 k^2 + B k^4 with B about 4a^2 (in units of 1/M^2)",
       anchor=r"the coefficient of the $k^{4}$ term is about $4a^{2}$")
def _():
    # Series of the lower root of Eq. (32): B = (S - M^2)^2 / S^3 with S = M^2 + 4 mu^2, i.e. B M^2 = 4a^2(1+a)/(1+3a)^3.
    out = []
    for a in [0.3, 0.05]:
        lam = v = 1.0; mu = math.sqrt(a/2); M2 = 1 + a; cs2 = (1 + a)/(1 + 3*a)
        ks = np.array([0.02, 0.04, 0.06, 0.08])
        w2 = np.array([dispersion_eq32(k, lam, v, mu)[0] for k in ks])
        fit = np.polyfit(ks**2, (w2 - cs2*ks**2)/ks**2, 2)[1]
        exact = 4*a*a/(1 + 3*a)**3
        out.append((a, fit/exact, exact*M2/(4*a*a)))
    ok = all(abs(r - 1) < 1e-3 for _, r, _ in out)
    return verdict(ok, "; ".join(f"a={a:g}: numerical/series {r:.5f}, B M^2 / 4a^2 = {q:.3f}" for a, r, q in out)
                   + "; positive, and -> 4a^2 as a -> 0")

@check("§7.7(3)", "NUMBER", "k^4 coefficient 4a^2 with a ~ 1e-23", anchor=r"$4a^{2} \lesssim 4 \times 10^{-46}$")
def _():
    val = 4*(1e-23)**2
    return verdict(abs(val - 4e-46) < 1e-50, f"4a^2 = {val:.0e} for a = 1e-23")

# --- §9.1 ---------------------------------------------------------------------
@check("§9.1, Eq. (27)", "FORMULA", "V'' = lambda(3 phi^2 - v^2), negative for |phi| < v/sqrt(3)",
       anchor=r"\Veff''(\phi) = \lambda\left(3\phi^{2} - v^{2}\right),")
def _():
    lam, v = 1.1, 0.9; V = lambda p: lam/4*(p*p - v*v)**2; worst = 0
    for p in [0.1, 0.4, 0.9, 1.5]:
        d = 1e-4; num = (V(p+d) - 2*V(p) + V(p-d))/d**2
        worst = max(worst, abs(num - lam*(3*p*p - v*v)))
    z = v/math.sqrt(3); sign_ok = lam*(3*(z*0.99)**2 - v*v) < 0 < lam*(3*(z*1.01)**2 - v*v)
    return verdict(worst < 1e-5 and sign_ok, f"largest difference {worst:.1e}; sign changes at v/sqrt(3): {sign_ok}")

# --- §11.6, §11.7: strong field ------------------------------------------------
def iso(r, M=1.0):
    psi = 1 + M/(2*r); U = (1 - M/(2*r))/(1 + M/(2*r)); return psi, U

@check("§11.7, Eq. (35)", "FORMULA",
       "psi and U satisfy rule (a) div(psi^2 grad U) = 0 and rule (b) lap psi = 0",
       anchor=r"\psi = 1 + \frac{GM}{2rc_{0}^{2}}, \qquad")
def _():
    r = np.linspace(1.0, 20.0, 20001); dr = r[1] - r[0]
    psi, U = iso(r)
    a = np.gradient(r**2*psi**2*np.gradient(U, dr), dr)/r**2          # radial divergence
    b = np.gradient(r**2*np.gradient(psi, dr), dr)/r**2
    scale = np.abs(np.gradient(U, dr)).max()
    return verdict(np.abs(a[5:-5]).max() < 1e-5*scale and np.abs(b[5:-5]).max() < 1e-5,
                   f"max |rule (a)| = {np.abs(a[5:-5]).max():.1e}, max |rule (b)| = {np.abs(b[5:-5]).max():.1e}")

@check("§11.7", "NUMBER", "Point of no return at isotropic radius GM/2c^2, areal radius 2GM/c^2",
       anchor=r"isotropic radius $GM/2c_{0}^{2}$, areal radius $2GM/c_{0}^{2}$")
def _():
    from scipy.optimize import brentq
    r0 = brentq(lambda r: iso(r)[1], 0.1, 5.0); psi, _ = iso(r0)
    return verdict(close(r0, 0.5, 1e-12) and close(r0*psi**2, 2.0, 1e-12), f"U = 0 at r = {r0:.6f} M, areal {r0*psi**2:.6f} M")

@check("§11.7", "NUMBER", "Light orbits at areal 3GM/c^2; shadow radius 3 sqrt(3) GM/c^2",
       anchor=r"Light orbits at areal radius $3GM/c_{0}^{2}$")
def _():
    from scipy.optimize import minimize_scalar
    b = lambda r: r*iso(r)[0]**2/iso(r)[1]                                # impact parameter of a circular light orbit
    res = minimize_scalar(b, bounds=(0.6, 10), method="bounded", options=dict(xatol=1e-12))
    areal = res.x*iso(res.x)[0]**2
    return verdict(close(areal, 3.0, 1e-6) and close(res.fun, 3*math.sqrt(3), 1e-9),
                   f"areal {areal:.6f} M, shadow {res.fun:.6f} M vs {3*math.sqrt(3):.6f}")

@check("§11.7", "FORMULA", "U agrees with exp(-u) to second order, so beta = 1",
       anchor=r"To second order $U$ agrees with $e^{-u}$")
def _():
    u = np.array([1e-3, 2e-3, 4e-3]); U = (1 - u/2)/(1 + u/2)
    diff = np.abs(U - np.exp(-u)); p = np.polyfit(np.log(u), np.log(diff), 1)[0]
    return verdict(2.8 < p < 3.2, f"difference scales as u^{p:.2f} (third order)")

@check("§11.6(v)", "NUMBER", "U = 1 - u gives beta = 1/2 and perihelion factor 7/6; U = exp(-u) gives beta = 1",
       anchor=r"$(2 + 2\gamma - \beta)/3 = 7/6$")
def _():
    u = 1e-3
    beta_lin = ((1 - u)**2 - 1 + 2*u)/(2*u*u)            # |g00| = U^2 = 1 - 2u + 2 beta u^2
    beta_exp = (math.exp(-2*u) - 1 + 2*u)/(2*u*u)
    fac = (2 + 2*1 - beta_lin)/3
    return verdict(close(beta_lin, 0.5, 1e-7) and close(beta_exp, 1.0, 1e-2) and close(fac, 7/6, 1e-7),
                   f"beta(1-u) = {beta_lin:.6f}, beta(exp) = {beta_exp:.4f}, factor = {fac:.6f}")

@check("§11.6(vi)", "NUMBER", "Exponential metric: no point of no return; shadow 4.6 per cent larger than GR",
       anchor=r"would be $4.6$ per cent larger than")
def _():
    from scipy.optimize import minimize_scalar
    b = lambda r: r*math.exp(2/r)                         # r e^{u} (areal) / e^{-u} (clock), u = M/r, M = 1
    res = minimize_scalar(b, bounds=(0.5, 10), method="bounded", options=dict(xatol=1e-12))
    ratio = res.fun/(3*math.sqrt(3))
    return verdict(abs((ratio - 1)*100 - 4.6) < 0.05, f"shadow ratio {ratio:.5f} ({(ratio-1)*100:.2f} per cent); clock rate exp(-M/r) > 0 everywhere")

@check("§11.6(v)", "FORMULA", "'Rulers set by the amount looks fixed from afar would give gamma = -1/3' (and fail light bending)",
       anchor=r"changes by $(1 + 3\gamma)u$; holding it fixed gives $\gamma = -\tfrac{1}{3}$")
def _():
    # Reading: the Ocean's conserved amount is the time part of the current rho^2 grad(theta) of Eq. (13).
    # With rho fixed (rule iv) and theta = -mu_inf t (rule iii), the amount per unit coordinate volume is
    # J^0 sqrt(-g) = rho^2 mu_inf sqrt(g_space)/U, with |g00| = U^2 = 1 - 2u, g_ij = (1 + 2 gamma u) delta_ij.
    from scipy.optimize import brentq
    def amount(u, gam):
        U = math.sqrt(1 - 2*u); g = np.diag([-U*U] + [1 + 2*gam*u]*3)
        J0 = -np.linalg.inv(g)[0, 0]*1.0          # rho = mu_inf = 1
        return J0*math.sqrt(-np.linalg.det(g))
    u = 1e-6
    slope = lambda gam: (amount(u, gam) - amount(0, gam))/u
    gam = brentq(slope, -2, 2); bend = (1 + gam)/2
    return verdict(abs(gam + 1/3) < 1e-4, f"amount fixed to first order only for gamma = {gam:.5f}; light then bends "
                   f"{bend:.3f} of the observed amount (the paper: 'a third as much'); amount = time part of the current of Eq. (13)")

# --- §11.9: the phase at the point of no return -----------------------------------
@check("§11.9, Eq. (38)", "FORMULA",
       "theta = mu(t + f) solves the wave equation; only 4M^2 keeps it finite for a falling traveler; far away f' -> 4M^2/r^2",
       anchor=r"r^{2}\left(1 - \frac{2M}{r}\right) f'(r) = 4M^{2} .")
def _():
    M = 1.0
    def fp(r, C): return C/(r*r*(1 - 2*M/r))
    # wave operator for stationary theta: (1/r^2) d/dr [r^2 (1-2M/r) dtheta/dr] = 0
    r = np.linspace(2.5, 30, 20001); dr = r[1] - r[0]
    box = np.gradient(r**2*(1 - 2*M/r)*fp(r, 4*M*M), dr)/r**2
    # falling traveler: compare with ingoing coordinate v = t + r*, dr*/dr = 1/(1-2M/r)
    rr = 2*M*(1 + np.array([1e-3, 1e-5, 1e-7]))
    reg = [fp(x, 4*M*M) - 1/(1 - 2*M/x) for x in rr]; bad = [fp(x, 3*M*M) - 1/(1 - 2*M/x) for x in rr]
    far = fp(1e6, 4*M*M)*(1e6)**2/(4*M*M)
    ok = np.abs(box[5:-5]).max() < 1e-8 and abs(reg[-1] + 2) < 1e-5 and abs(bad[-1]) > 1e5 and close(far, 1, 1e-5)
    return verdict(ok, f"wave equation residual {np.abs(box[5:-5]).max():.1e}; at the edge f' - dr*/dr -> {reg[-1]:.4f} "
                       f"with 4M^2, {bad[-1]:.1e} with 3M^2; far-field ratio {far:.6f}")

@check("§11.9, Eq. (38) with Eq. (6)", "CONSISTENCY", "With u = -grad(theta)/mu, the phase of Eq. (38) gives a flow forward in time and inward at every radius",
       anchor=r"\theta = \mu_{\infty}\left[t + f(r)\right], \qquad")
def _():
    M = 1.0; bad = []
    for r in [10.0, 3.0, 2.2, 2.01]:
        fp = 4*M*M/(r*r*(1 - 2*M/r)); dt_, dr_ = 1.0, fp            # theta = +mu_inf [t + f]
        gtt, grr = -1/(1 - 2*M/r), (1 - 2*M/r); mu = math.sqrt(-(gtt*dt_**2 + grr*dr_**2))
        ut, ur = gtt*(-dt_/mu), grr*(-dr_/mu)
        if not (ut > 0 and ur < 0): bad.append(r)
    return verdict(not bad, "future-directed inflow at r = 10M, 3M, 2.2M, 2.01M" if not bad else f"fails at {bad}")

# --- §2.5: light bending from the refractive index ---------------------------------
@check("§2.5, Eq. (10)", "FORMULA", "n = 1 + 2GM/(rc^2) bends light by 4GM/(bc^2), twice the slowing-only value",
       anchor=r"n(r) \;\simeq\; 1 + \frac{2GM}{rc_{0}^{2}} .")
def _():
    from scipy.integrate import quad
    M, b = 1.0, 1e4
    integrand = lambda z: 2*M*b/(b*b + z*z)**1.5           # transverse gradient of n along the straight path
    dfl = quad(integrand, -np.inf, np.inf)[0]
    return verdict(close(dfl, 4*M/b, 1e-8), f"deflection {dfl*b:.6f} GM/(b c^2)")

# ================================================================ NUMBERS
@check("§7.5, Eq. (22)", "NUMBER", "hbar c / 0.511 MeV = 386 femtometers", anchor=r"\approx 386\ \text{femtometers},")
def _():
    xi = hbar*c/(0.51099895*MeV)
    return verdict(close(xi*1e15, 386, 0.002), f"{xi*1e15:.2f} fm")

@check("§7.7(5), Eq. (25)", "NUMBER", "alpha_G = G m_e^2/(hbar c) = (l_P/xi_0)^2 ~ 1.75e-45",
       anchor=r"\;\approx\; 1.75 \times 10^{-45},")
def _():
    aG = G*me**2/(hbar*c); xi = hbar/(me*c)
    return verdict(close(aG, 1.75e-45, 0.003) and close((lP/xi)**2, aG, 1e-9), f"{aG:.4e}; (l_P/xi_0)^2 = {(lP/xi)**2:.4e}")

@check("§7.7(5)", "NUMBER", "Planck length ~1.6e-35 m, about 1e22 below the electron's localization length xi_e",
       anchor=r"\approx 1.6 \times 10^{-35}$~m about $10^{22}$ below $\xi_{e}$")
def _():
    xi = hbar/(me*c)
    return verdict(close(lP, 1.6e-35, 0.02) and 1e22 <= xi/lP < 1e23, f"l_P = {lP:.3e} m; xi_0/l_P = {xi/lP:.2e}")

@check("Preface", "NUMBER", "Electric force between two electrons ~4e42 times their gravity",
       anchor=r"about $4 \times 10^{42}$ times stronger")
def _():
    r = e**2/(4*math.pi*eps0*G*me**2)
    return verdict(close(r, 4e42, 0.1), f"{r:.3e}")

@check("Preface", "NUMBER", "Hurricane ~1e14 times the spacing of air molecules",
       anchor=r"$10^{14}$ times wider than the spacing of air molecules")
def _():
    spacing = (kB*273.15/101325)**(1/3); lo, hi = 160e3/spacing, 800e3/spacing
    return verdict(3e13 < lo and hi < 3e14, f"'hundreds of miles' (100-500 miles) / {spacing*1e9:.2f} nm = {lo:.1e} to {hi:.1e}")

@check("Preface, §7.7(5)", "NUMBER", "A kiloparsec is about 1e55 times the dent's width (Planck length / 3.5): more than fifty orders",
       anchor=r"A galaxy really is about $10^{55}$ times")
def _():
    w = lP/3.54; r = kpc/w
    return verdict(3e54 < r < 3e55, f"kpc / dent width = {r:.1e}")

@check("§7.7(7)", "NUMBER", "Electron size limit 1e-18 m is several hundred thousand times below xi_0",
       anchor=r"several hundred thousand times smaller")
def _():
    xi = hbar/(me*c); r = xi/1e-18
    return verdict(1e5 < r < 1e6, f"{r:.2e}")

@check("§11.8", "FORMULA", "Circulation per line from the paper's flow u = -grad(theta)/mu: one turn of the phase gives 2 pi/mu (hc^2/mu in SI)",
       anchor=r"with circulation $hc_{0}^{2}/\mu$ \cite{andersson2021}")
def _():
    mu0 = 3.0; out = []
    for R in [20.0, 200.0]:
        ph = np.linspace(0, 2*np.pi, 4000, endpoint=False); tot = tot_mu = 0.0
        for p_ in ph:
            x, y = R*np.cos(p_), R*np.sin(p_); g = np.array([-mu0, -y/(x*x+y*y), x/(x*x+y*y)])
            mu = math.sqrt(g[0]**2 - g[1]**2 - g[2]**2); u = -g[1:]/mu
            dl = np.array([-np.sin(p_), np.cos(p_)])*R*2*np.pi/4000
            tot += u @ dl; tot_mu += (mu*u) @ dl
        out.append((tot, tot_mu))
    ok = abs(out[-1][0] + 2*np.pi/mu0) < 1e-4 and all(abs(m_ + 2*np.pi) < 1e-9 for _, m_ in out)
    return verdict(ok, f"loop of mu u = {out[-1][1]:.6f} (exactly -2 pi); loop of u -> {out[-1][0]:.6f} (-2 pi/mu = {-2*np.pi/mu0:.6f})")

@check("§7.6", "NUMBER", "G-dot/G = (-5.0 +/- 9.6)e-15 per year: G changed by less than four parts in 1e4 over 13.8 Gyr",
       anchor=r"$G$ has changed by less than four parts in $10^{4}$")
def _():
    stated = 4e-4; c0, s0, age = -5.0e-15, 9.6e-15, 13.8e9
    two = max(abs(c0 - 2*s0), abs(c0 + 2*s0))*age        # largest change allowed at two standard deviations
    return verdict(two <= stated, f"two-standard-deviation bound {two:.2e} against the stated {stated:.0e} (strict: no margin)")

@check("§10.3, Eq. (28)", "NUMBER", "Lambda = G^2 m_e^6/(alpha^6 hbar^4) ~ 1.36e-52 m^-2",
       anchor=r"\approx 1.36 \times 10^{-52}\,\mathrm{m}^{-2},")
def _():
    L = G**2*me**6/(alpha**6*hbar**4)
    return verdict(close(L, 1.36e-52, 0.005), f"{L:.4e} m^-2")

@check("§12", "NUMBER", "G = alpha^3 hbar^2 sqrt(Lambda)/m_e^3 within ~10 per cent with measured Lambda, a few per cent with local H0",
       anchor=r"comes within about ten per cent of the measured $G$")
def _():
    Lp = 3*(67.36e3/3.0857e22)**2*0.6847/c**2; Ll = 3*(73.0e3/3.0857e22)**2*0.6847/c**2
    g1 = alpha**3*hbar**2*math.sqrt(Lp)/me**3/G; g2 = alpha**3*hbar**2*math.sqrt(Ll)/me**3/G
    return verdict(abs(g1 - 1) < 0.12 and abs(g2 - 1) < 0.05,
                   f"Planck 2018 Lambda: G ratio {g1:.3f}; H0 = 73 km/s/Mpc: {g2:.3f} (inputs: Planck 2018 H0 and Omega_Lambda)")

@check("§8.1", "NUMBER", "Hawking temperature of a solar-mass black hole ~60 nK; mass loss ~1e-45 kg/s",
       anchor=r"the Hawking temperature is about $60$~nK")
def _():
    T = hbar*c**3/(8*math.pi*G*Msun*kB); dm = hbar*c**4/(15360*math.pi*G**2*Msun**2)
    return verdict(close(T*1e9, 60, 0.05) and 0.5e-45 < dm < 2e-45, f"T = {T*1e9:.1f} nK; photon-only mass loss {dm:.1e} kg/s")

@check("§8.1, §8.2", "NUMBER", "Evaporation: about 1e67 years for a solar mass (Page 2e66 with massless neutrinos); about 1e87 years for Sgr A*",
       anchor=r"over about $10^{87}$ years for Sagittarius~A*")
def _():
    t_ph = 5120*math.pi*G**2*Msun**3/(hbar*c**4)/yr
    sgr = 1e67*(4.3e6)**3
    return verdict(1e66 < t_ph < 1e68 and 0.3e87 < sgr < 3e87,
                   f"photon-only estimate {t_ph:.1e} years for a solar mass; 1e67 x (4.3e6)^3 = {sgr:.1e} years")

@check("§8.1", "NUMBER", "Accretion efficiency about 6% (non-rotating), up to about 40% (rapidly rotating); fusion 0.7%",
       anchor=r"Accretion converts about $6$ per cent")
def _():
    schw = 1 - math.sqrt(8/9); kerr = 1 - 1/math.sqrt(3)
    fusion = (4*1.00782503223 - 4.00260325413)/(4*1.00782503223)
    return verdict(abs(schw - 0.06) < 0.005 and abs(kerr - 0.42) < 0.01 and abs(fusion - 0.007) < 0.0005,
                   f"{schw*100:.2f}%, {kerr*100:.1f}% (extreme spin), fusion {fusion*100:.2f}%")

@check("§8.2", "NUMBER", "10 solar masses: tidal difference ~10 g at 3800 km; horizon ~30 km",
       anchor=r"some $3800$~km out, while the horizon lies at about $30$~km")
def _():
    M = 10*GMsun; dA = 2*M*2.0/(3.8e6)**3; rs = 2*M/c**2
    return verdict(abs(dA/9.81 - 10) < 1 and close(rs/1e3, 30, 0.05), f"{dA/9.81:.1f} g over 2 m; horizon {rs/1e3:.1f} km")

@check("§8.2", "NUMBER", "Sagittarius A*: horizon radius ~12.7 million km; tidal difference at the horizon ~1e-4 g; lethal ~280 000 km",
       anchor=r"horizon radius about $12.7$ million km")
def _():
    M = 4.3e6*GMsun; rs = 2*M/c**2; dh = 2*M*2.0/rs**3/9.81; dl = 2*M*2.0/(2.8e8)**3/9.81
    return verdict(close(rs/1e9, 12.7, 0.01) and 0.5e-4 < dh < 2e-4 and abs(dl - 10) < 1.5,
                   f"horizon {rs/1e9:.2f} million km; {dh:.1e} g at the horizon; {dl:.1f} g at 280 000 km (same 10 g criterion as above)")

@check("§8.2", "NUMBER", "Longest time horizon to center pi GM/c^3: ~66 s Sgr A*, ~28 h M87*",
       anchor=r"about $66$ seconds for Sagittarius~A*")
def _():
    t1 = math.pi*4.3e6*GMsun/c**3; t2 = math.pi*6.5e9*GMsun/c**3/3600
    return verdict(close(t1, 66, 0.02) and close(t2, 28, 0.02), f"{t1:.1f} s; {t2:.1f} h")

@check("§11.9", "NUMBER", "Crossing to turnaround (falling from rest far away): ~1e-4 s (10 Msun), 28 s (Sgr A*), 12 h (M87*)",
       anchor=r"is about $10^{-4}$~s for a black hole")
def _():
    f = lambda m: 4*m*GMsun/(3*c**3)                      # proper time from r = 2GM/c^2 to r -> 0, marginally bound dust
    a, b, cc = f(10), f(4.3e6), f(6.5e9)/3600
    return verdict(0.5e-4 < a < 2e-4 and close(b, 28, 0.02) and close(cc, 12, 0.02),
                   f"{a:.1e} s; {b:.1f} s; {cc:.1f} h (turnaround density far above the horizon density)")

@check("§11.9", "NUMBER", "rho_c >~ 2.4e23 kg/m^3 (J0337) with rho_c c^2 ~ hbar c/l^4 gives l <~ 0.035 fm, ~1e4 below the electron's 386 fm",
       anchor=r"then $\ell \lesssim 0.035$~femtometers, some ten thousand times finer than the electron's")
def _():
    l = (hbar/(2.4e23*c))**0.25; xi = hbar/(me*c)
    return verdict(close(l*1e15, 0.035, 0.03) and 0.8e4 < xi/l < 1.3e4, f"l = {l*1e15:.4f} fm; xi_e/l = {xi/l:.0f}")

@check("§11.9", "NUMBER", "q = 1 return: five solar masses merging after ten billion years needs l <~ 6e-19 m; Sgr A* return ~1e22 years",
       anchor=r"taking five solar masses and ten billion years, with $q = 1$ the step must be $\ell \lesssim 6 \times 10^{-19}$~m")
def _():
    lmax = (5*GMsun/c**2)**2/(c*10e9*yr); tau = (4.3e6*GMsun/c**2)**2/(c*6e-19)/yr
    return verdict(close(lmax, 6e-19, 0.1) and 1e21 < tau < 1e23, f"l < {lmax:.1e} m; Sgr A* {tau:.1e} years")

@check("§11.9", "CONSISTENCY", "Turnaround half a minute after crossing for Sgr A* (§8.2) matches 28 s (§11.9)",
       anchor=r"turning it around about half a minute after the crossing")
def _():
    return verdict(close(4*4.3e6*GMsun/(3*c**3), 30, 0.1), "28 s is about half a minute")

# --- §6: the swirl ------------------------------------------------------------------
def swirl_accel(vc, V, dVdR, R):
    """Radial acceleration from Eq. (15) for a circular orbit at speed vc in a swirl V(R) phi_hat (no baryon term)."""
    conv = -V*V/R                               # (v.grad)v, radial
    curl = V/R + dVdR                           # z-component of curl v
    w = vc - V                                  # travel relative to the Ocean, azimuthal
    lorentz = -w*curl                           # -(w phi_hat) x (curl z_hat) = -w curl r_hat
    return conv + lorentz

@check("§6, Eq. (15)", "FORMULA", "Flat swirl turns a circular orbit inward by v_c V/R, with a term (v_c - V) dV/dR when V varies; nothing at rest",
       anchor=r"inward by a further $v_{c}V/R$")
def _():
    R, vc, V = 8.0, 229.0, 118.0
    a_flat = swirl_accel(vc, V, 0.0, R); a_var = swirl_accel(vc, V, 3.0, R); a_rest = swirl_accel(0.0, V, 0.0, R) + V*V/R*0
    # a pattern at rest relative to the galaxy: (v.grad)v - (-v) x curl v = grad(v^2/2) = 0 for a flat swirl
    rest = -V*V/R + V*(V/R)
    ok = close(-a_flat, vc*V/R, 1e-12) and close(-(a_var - a_flat), (vc - V)*3.0, 1e-12) and abs(rest) < 1e-12
    return verdict(ok, f"flat: {-a_flat:.4f} = v_c V/R; variable: extra {-(a_var-a_flat):.4f} = (v_c-V) dV/dR; at rest: {rest:.1e}")

@check("§6", "NUMBER", "159 km/s from baryons against 229 observed at 8.1 kpc needs a swirl of about 118 km/s",
       anchor=r"a swirl of about")
def _():
    V = (229**2 - 159**2)/229
    return verdict(abs(V - 118) < 1.0, f"V = (229^2 - 159^2)/229 = {V:.1f} km/s")

@check("§6", "SIMULATION", "Model Milky Way (flattened disk 6e10 Msun, a = 3.0, b = 0.28 kpc): 159 km/s at 8.1 kpc; star launched at 30 km/s rises 583 vs 574 pc; a swirl falling off over 0.5 kpc throws it ~10 kpc",
       anchor=r"a star launched from the midplane at $30\,\mathrm{km\,s^{-1}}$ rises to within two per cent of its height in the baryons-only case ($583$ against $574$~pc)")
def _():
    from scipy.integrate import solve_ivp
    Gk = 4.30091e-6; a, b, Mb, R0, V = 3.0, 0.28, 6e10, 8.1, 118.0; GMk = Gk*Mb
    def acc_b(x):
        zb = math.sqrt(x[2]**2 + b*b); D = (x[0]**2 + x[1]**2 + (a + zb)**2)**1.5
        return -GMk*np.array([x[0]/D, x[1]/D, x[2]*(a + zb)/(zb*D)])
    def run(swirl, falloff=None, T=0.5):
        def flow(x):
            R = math.hypot(x[0], x[1]); Vh = V*(math.exp(-abs(x[2])/falloff) if falloff else 1.0)
            return Vh*np.array([-x[1]/R, x[0]/R, 0.0])
        def rhs(t, y):
            x, u = y[:3], y[3:]; acc = acc_b(x)
            if swirl:
                hh = 1e-5; v = flow(x); Jm = np.zeros((3, 3))
                for k in range(3):
                    e_ = np.zeros(3); e_[k] = hh; Jm[:, k] = (flow(x + e_) - flow(x - e_))/(2*hh)
                cu = np.array([Jm[2, 1] - Jm[1, 2], Jm[0, 2] - Jm[2, 0], Jm[1, 0] - Jm[0, 1]])
                acc = acc + Jm @ v - np.cross(u - v, cu)
            return np.r_[u, acc]
        vb = math.sqrt(-acc_b(np.array([R0, 0, 0]))[0]*R0)
        vc = (V + math.sqrt(V*V + 4*vb*vb))/2 if swirl else vb
        sol = solve_ivp(rhs, [0, T], [R0, 0, 0, 0, vc, 30.0], rtol=1e-9, atol=1e-11, max_step=0.002)
        return vb, vc, np.abs(sol.y[2]).max()
    vb, _, z0 = run(False); _, vc, z1 = run(True); _, _, zf = run(True, falloff=0.5, T=0.25)
    ok = abs(vb - 159) < 1 and abs(vc - 229) < 1 and abs(z0*1e3 - 574) < 3 and abs(z1*1e3 - 583) < 3 and 9 < zf < 12
    return verdict(ok, f"v_bar {vb:.1f} km/s, v_c {vc:.1f}; heights {z0*1e3:.0f} and {z1*1e3:.0f} pc ({(z1/z0-1)*100:+.1f}%); falling-off swirl: {zf:.1f} kpc")

@check("§6", "NUMBER", "A galaxy's own travel tilts the Ocean by about its potential/c^2 times the orbital speed: a few times 1e-4 km/s, against 118",
       anchor=r"a few times $10^{-4}\,\mathrm{km\,s^{-1}}$")
def _():
    kpc = 3.0857e19; Ms = 1.989e30
    u = G*6e10*Ms/(c**2*8.1*kpc); s_self = 4*u*229.0
    return verdict(1e-4 < s_self < 1e-3, f"u = {u:.2e}; (2 + 2 gamma) u v_c = {s_self:.1e} km/s, {118/s_self:.0e} times short")

@check("§6", "NUMBER", "A swirl the same at every height needs, at the Sun's radius, a momentum about 4e4 times the model's stars and gas",
       anchor=r"a momentum about $4 \times 10^{4}$")
def _():
    kpc = 3.0857e19; Ms = 1.989e30; M = 6e10*Ms; a, b, R = 3*kpc, 0.28*kpc, 8.1*kpc
    # first-order law: lap s = -(16 pi G / c^2) p ; vector Laplacian of V phi_hat (V const) is -V/R^2 phi_hat
    p_need = c**2*118.2e3/(16*math.pi*G*R**2)
    rho = b*b*M/(4*math.pi)*(a*R*R + (a + 3*b)*(a + b)**2)/((R*R + (a + b)**2)**2.5*b**3)   # Miyamoto-Nagai, z = 0
    ratio = p_need/(rho*229e3)
    return verdict(3e4 < ratio < 5e4, f"needed {p_need:.2e} kg m^-2 s^-1; stars and gas {rho*229e3:.2e} ({rho/Ms*(kpc/1e3)**3:.3f} Msun/pc^3 at 229 km/s); ratio {ratio:.1e}")

@check("§6", "FORMULA", "A source-free tilt flat in the plane grows as V(1 + z^2/2R^2) and gains a radial turning -V z/R^2",
       anchor=r"as $V(1 + z^{2}/2R^{2})$")
def _():
    # azimuthal field s_phi(R, z); vector Laplacian lap = s_RR + s_R/R - s/R^2 + s_zz, by finite differences
    V = 118.0; h = 1e-3
    def s_phi(R, z): return V*(1 + z*z/(2*R*R))
    def lap(R, z):
        return ((s_phi(R+h, z) - 2*s_phi(R, z) + s_phi(R-h, z))/h**2 + (s_phi(R+h, z) - s_phi(R-h, z))/(2*h*R)
                - s_phi(R, z)/R**2 + (s_phi(R, z+h) - 2*s_phi(R, z) + s_phi(R, z-h))/h**2)
    worst = max(abs(lap(R, 0.0))/(V/R**2) for R in (4.0, 8.1, 15.0))          # source-free in the plane
    flat = abs(lap(8.1, 0.0)) ; const = -V/8.1**2                               # a swirl the same at every height instead
    BR = -(s_phi(8.1, 0.5+h) - s_phi(8.1, 0.5-h))/(2*h); ok = worst < 1e-5 and abs(BR + V*0.5/8.1**2) < 1e-6
    return verdict(ok, f"residual in the plane {worst:.1e} of V/R^2 (a constant swirl leaves {const:.3f}); radial turning at z = 0.5 kpc {BR:.4f} = -V z/R^2")

@check("§6", "SIMULATION", "Source-free swirl in the model Milky Way: vertical pull +9% at 0.5 kpc, +15% at 1 kpc; star at 30 km/s rises 558 vs 574 pc",
       anchor=r"rises to $558$~pc against $574$")
def _():
    from scipy.integrate import solve_ivp
    Gk = 4.30091e-6; a, b, Mb, R0, V = 3.0, 0.28, 6e10, 8.1, 118.0; GMk = Gk*Mb
    def acc_b(x):
        zb = math.sqrt(x[2]**2 + b*b); D = (x[0]**2 + x[1]**2 + (a + zb)**2)**1.5
        return -GMk*np.array([x[0]/D, x[1]/D, x[2]*(a + zb)/(zb*D)])
    def tilt(x):
        R = math.hypot(x[0], x[1]); Vh = V*(1 + x[2]**2/(2*R*R))
        return Vh*np.array([-x[1]/R, x[0]/R, 0.0])
    def rhs(t, y):
        x, u = y[:3], y[3:]; hh = 1e-5; v = tilt(x); Jm = np.zeros((3, 3))
        for k in range(3):
            e_ = np.zeros(3); e_[k] = hh; Jm[:, k] = (tilt(x + e_) - tilt(x - e_))/(2*hh)
        cu = np.array([Jm[2, 1] - Jm[1, 2], Jm[0, 2] - Jm[2, 0], Jm[1, 0] - Jm[0, 1]])
        return np.r_[u, acc_b(x) + Jm @ v - np.cross(u - v, cu)]
    vb = math.sqrt(-acc_b(np.array([R0, 0, 0]))[0]*R0); vc = (V + math.sqrt(V*V + 4*vb*vb))/2
    zs = np.abs(solve_ivp(rhs, [0, 0.5], [R0, 0, 0, 0, vc, 30.0], rtol=1e-9, atol=1e-11, max_step=0.002).y[2]).max()
    fr = [(vc - V)*V*zz/R0**2/(-acc_b(np.array([R0, 0, zz]))[2]) for zz in (0.5, 1.0)]
    ok = abs(zs*1e3 - 558) < 3 and abs(fr[0] - 0.09) < 0.01 and abs(fr[1] - 0.15) < 0.01
    return verdict(ok, f"height {zs*1e3:.0f} pc; vertical pull +{fr[0]*100:.1f}% at 0.5 kpc, +{fr[1]*100:.1f}% at 1 kpc; radial x{(vc/vb)**2:.2f}")

# --- §11.8: frame dragging ----------------------------------------------------------
J_earth = 0.3307*5.9722e24*6.371e6**2*7.2921e-5
def tilt_swirl(p, J=J_earth, k=2.0):
    return k*G*np.cross([0, 0, J], p)/(c**2*np.linalg.norm(p)**3)
def curl(f, p, hh=1.0):
    d = np.zeros((3, 3))
    for j in range(3):
        e_ = np.zeros(3); e_[j] = hh; d[:, j] = (f(p + e_) - f(p - e_))/(2*hh)
    return np.array([d[2, 1] - d[1, 2], d[0, 2] - d[2, 0], d[1, 0] - d[0, 1]])

@check("§11.8, Eq. (36)", "FORMULA", "A boost of the resting mass's geometry gives the sideways tilt (2 + 2 gamma) u V",
       anchor=r"\mathbf{s} = (2 + 2\gamma)\, u\, \mathbf{V}, \qquad u = \frac{G m}{c_{0}^{2}\, d},")
def _():
    out = []
    for gam in [1.0, 0.5]:
        Vb = 1e-3; gL = 1/math.sqrt(1 - Vb*Vb); U = 1e-6
        h = np.diag([2*U, 2*gam*U, 2*gam*U, 2*gam*U])                    # rest frame: h00 = 2U, hij = 2 gamma U
        Lam = np.array([[gL, -gL*Vb, 0, 0], [-gL*Vb, gL, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])  # dx_rest/dx_moving
        hp = Lam.T @ h @ Lam
        out.append((gam, -hp[0, 1]/(U*Vb)))
    ok = all(close(k, 2 + 2*g, 1e-5) for g, k in out)
    return verdict(ok, "; ".join(f"gamma={g}: tilt coefficient {k:.6f} (rule {2+2*g})" for g, k in out))

@check("§11.8, Eq. (37)", "SIMULATION", "Summed tilts of a spinning two-layer Earth equal 2G (J x r)/(c^2 r^3)",
       anchor=r"\mathbf{s} = \frac{2G}{c_{0}^{2}}\,\frac{\mathbf{J}\times\mathbf{r}}{r^{3}},")
def _():
    om = 7.2921e-5; R = 6.371e6; Rc = 3.48e6
    nr, nt, nph = 60, 45, 45
    r = (np.arange(nr) + 0.5)/nr*R; th = (np.arange(nt) + 0.5)/nt*np.pi; ph = (np.arange(nph) + 0.5)/nph*2*np.pi
    Rr, Tt, Pp = np.meshgrid(r, th, ph, indexing="ij")
    dm = np.where(Rr < Rc, 10.9e3, 4.45e3)*(R/nr)*(np.pi/nt)*(2*np.pi/nph)*Rr**2*np.sin(Tt)
    x = Rr*np.sin(Tt)*np.cos(Pp); y = Rr*np.sin(Tt)*np.sin(Pp); z = Rr*np.cos(Tt)
    u = np.stack([-om*y, om*x, 0*z]); J = (dm*(x*x + y*y)).sum()*om
    worst = 0
    for p in [np.array([7.027e6, 0, 0]), np.array([0, 9e6, 5e6]), np.array([3e6, -4e6, 1.1e7])]:
        d = np.sqrt((p[0] - x)**2 + (p[1] - y)**2 + (p[2] - z)**2)
        s = ((2 + 2)*G/c**2*(dm/d)*u).reshape(3, -1).sum(1)
        cf = 2*G*np.cross([0, 0, J], p)/(c**2*np.linalg.norm(p)**3)
        worst = max(worst, np.linalg.norm(s - cf)/np.linalg.norm(cf))
    return verdict(worst < 1e-3, f"largest relative difference at three outside points: {worst:.1e}")

@check("§11.8", "FORMULA", "Half the turning of the swirl equals the Lense-Thirring rate at every point",
       anchor=r"turns the rotor's axis at half the local turning")
def _():
    worst = 0
    for p in [np.array([7.027e6, 0, 0]), np.array([0, 0, 7.027e6]), np.array([4e6, 3e6, 5e6])]:
        n = p/np.linalg.norm(p); Jv = np.array([0, 0, J_earth])
        lt = G*(3*np.dot(Jv, n)*n - Jv)/(c**2*np.linalg.norm(p)**3)
        worst = max(worst, np.linalg.norm(0.5*curl(tilt_swirl, p) - lt)/np.linalg.norm(lt))
    return verdict(worst < 1e-5, f"largest relative difference: {worst:.1e}")

@check("§11.8 table", "SIMULATION", "Orbit-plane drift from Eq. (15): 30.6, 31.4, 118.1 mas/yr; Gravity Probe B 39.2 toward the guide star",
       anchor=r"$30.6$, $31.4$, $118.1$")
def _():
    GM = 3.986004418e14; mas = math.degrees(1)*3.6e6
    def node_rate(a, inc):
        n = math.sqrt(GM/a**3); hh = math.sqrt(GM*a); s = 0.0; N = 720
        for uu in np.linspace(0, 2*np.pi, N, endpoint=False):
            rv = a*np.array([np.cos(uu), np.sin(uu)*np.cos(inc), np.sin(uu)*np.sin(inc)])
            vel = a*n*np.array([-np.sin(uu), np.cos(uu)*np.cos(inc), np.cos(uu)*np.sin(inc)])
            W = np.cross(rv, vel); W /= np.linalg.norm(W)
            acc = -np.cross(vel - tilt_swirl(rv), curl(tilt_swirl, rv, hh=10.0))
            s += a*np.sin(uu)*np.dot(acc, W)/(hh*np.sin(inc))
        return s/N*yr*mas
    rates = [node_rate(12270e3, math.radians(109.84)), node_rate(12163e3, math.radians(52.64)), node_rate(7821e3, math.radians(69.5))]
    rg = 6.371e6 + 642e3; ths = np.linspace(0, 2*np.pi, 721)[:-1]
    avg = np.mean([0.5*curl(tilt_swirl, rg*np.array([np.cos(t), 0, np.sin(t)])) for t in ths], axis=0)
    gpb = np.linalg.norm(avg)*yr*mas*math.cos(math.radians(16.84))
    ok = all(close(r, t, 0.002) for r, t in zip(rates, [30.6, 31.4, 118.1])) and close(gpb, 39.2, 0.003)
    gr = [30.68, 31.50, 118.50]
    return verdict(ok, "drifts " + ", ".join(f"{r:.2f}" for r in rates) + f" mas/yr (GR as published: {gr}; ratio "
                   f"{rates[0]/gr[0]:.4f}); GP-B {gpb:.1f} mas/yr")

@check("§11.8", "SIMULATION", "Travel leaves no trace with both shares; ruler share missing leaves |V x grad u|; no tilt leaves (1+gamma)|V x grad u|",
       anchor=r"with both shares the travel leaves no turning")
def _(quick=False):
    import importlib.util as iu
    p = Path(__file__).with_name("fd_cancel.py")
    spec = iu.spec_from_file_location("fd_cancel", p); m = iu.module_from_spec(spec); spec.loader.exec_module(m)
    V = np.array([0.0, 0.01, 0.004]); x0 = np.array([1.0, 0.3, -0.2]); gradU = -m.M*x0/np.linalg.norm(x0)**3
    scale = np.linalg.norm(np.cross(V, gradU))
    res = {k: np.linalg.norm(m.run_back(V, k))/scale for k in [4.0, 2.0, 0.0]}
    ok = res[4.0] < 2e-3 and abs(res[2.0] - 1) < 2e-3 and abs(res[0.0] - 2) < 2e-3
    return verdict(ok, f"turning / |V x grad u|: both shares {res[4.0]:.4f}, clock share only {res[2.0]:.4f}, no tilt {res[0.0]:.4f} (gamma = 1)")

@check("§11.8", "SIMULATION", "A rotor whose parts obey Eq. (15) turns at half the local turning, whatever its spin (Larmor)",
       anchor=r"whatever the rotor's own spin")
def _():
    N = 32; ph = np.linspace(0, 2*np.pi, N, endpoint=False); body = np.c_[np.cos(ph), np.sin(ph), np.zeros(N)]
    Ib = np.diag([N/2, N/2, N]); Ibi = np.linalg.inv(Ib)
    sk = lambda w: np.array([[0, -w[2], w[1]], [w[2], 0, -w[0]], [-w[1], w[0], 0]])
    def deriv(R, L, B):
        om = R @ Ibi @ R.T @ L; r = body @ R.T; xd = np.cross(om, r); v = 0.5*np.cross(B, r)
        a = 0.5*np.cross(B, v) - np.cross(xd - v, B); return sk(om) @ R, np.cross(r, a).sum(0)
    rates = []
    for spin in [1.0, 4.0]:
        B = np.array([0, 0, 2e-3]); tl = math.radians(60)
        R = np.array([[1, 0, 0], [0, math.cos(tl), -math.sin(tl)], [0, math.sin(tl), math.cos(tl)]])
        L = R @ Ib @ np.array([0, 0, spin]); dt = 0.02; n = 10000; angs = []
        for i in range(n + 1):
            if i % 500 == 0: angs.append((i*dt, math.atan2(L[1], L[0])))
            k1 = deriv(R, L, B); k2 = deriv(R + dt/2*k1[0], L + dt/2*k1[1], B)
            k3 = deriv(R + dt/2*k2[0], L + dt/2*k2[1], B); k4 = deriv(R + dt*k3[0], L + dt*k3[1], B)
            R = R + dt/6*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0]); L = L + dt/6*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
            uu, _, vt = np.linalg.svd(R); R = uu @ vt
        t, a = np.array(angs).T; rates.append(np.polyfit(t, np.unwrap(a), 1)[0]/(B[2]/2))
    return verdict(all(abs(r - 1) < 1e-3 for r in rates), "rate / (B/2): " + ", ".join(f"{r:.5f}" for r in rates))

@check("§11.8", "SIMULATION", "Read point by point, quantized lines turn no pattern's travel in either sense",
       anchor=r"Read point by point, they do not turn a gyroscope")
def _():
    from scipy.integrate import solve_ivp
    a = 1.0; kap = 0.02; rc = 1e-3
    xs = np.arange(-6, 6.01, a); X, Y = np.meshgrid(xs, xs); P = np.c_[X.ravel() + 0.5*a, Y.ravel() + 0.37*a]
    def vl(p, s):
        d = p - P; r2 = (d**2).sum(1); f = np.where(r2 > rc**2, 1/r2, 1/rc**2)
        return s*kap/(2*np.pi)*np.c_[-d[:, 1]*f, d[:, 0]*f].sum(0)
    def cl(p, s): r2 = ((p - P)**2).sum(1); return s*np.sum(np.where(r2 < rc**2, kap/(np.pi*rc**2), 0.0))
    Om = kap/a**2
    def rhs(t, y, mode, s):
        p, u = y[:2], y[2:]
        vf = (lambda q: 0.5*Om*np.array([-q[1], q[0]])) if mode == "smooth" else (lambda q: vl(q, s))
        cc = Om if mode == "smooth" else cl(p, s); hh = 1e-5; v = vf(p)
        Jm = np.c_[(vf(p + [hh, 0]) - vf(p - [hh, 0]))/(2*hh), (vf(p + [0, hh]) - vf(p - [0, hh]))/(2*hh)]
        w = u - v; return np.r_[u, Jm @ v - np.array([-w[1]*cc, w[0]*cc])]
    y0 = [-5.5, 0.0, 1.0, 0.0]; T = 11.0; out = {}
    for mode, s in [("smooth", 1), ("lines", 1), ("lines", -1)]:
        out[(mode, s)] = solve_ivp(rhs, [0, T], y0, args=(mode, s), rtol=1e-9, atol=1e-12, max_step=0.01).y[3, -1]
    sense = abs(out[("lines", 1)] - out[("lines", -1)])/2
    ok = sense < 1e-6 and close(out[("smooth", 1)], -Om*T, 0.1)
    return verdict(ok, f"smooth {out[('smooth',1)]:+.3e}; lines {out[('lines',1)]:+.3e} and {out[('lines',-1)]:+.3e}; "
                       f"part reversing with the sense {sense:.1e}")

@check("§11.8", "NUMBER", "Travel's tilt near the Earth is several thousand times the spin's",
       anchor=r"several thousand")
def _():
    GM = 3.986004418e14; r = 6.371e6 + 642e3; Vt = 3.7e5
    shared = 4*GM/(c**2*r**2)*Vt                      # |curl(4 u V)| = 4 |grad u x V|, at most
    spin = np.linalg.norm(curl(tilt_swirl, np.array([r, 0, 0])))
    return verdict(1e3 < shared/spin < 1e4, f"ratio {shared/spin:.0f} at Gravity Probe B's height, travel 370 km/s")

@check("§11.8", "SIMULATION", "Lines read over one spacing turn a gyroscope at B/2 (Larmor), reverse with the lines, independent of spin; point by point: nothing (mixed senses: rotor_mixed.py)",
       anchor=r"they carry it exactly. Checked numerically, a gyroscope whose")
def _():
    import importlib.util as iu
    spec = iu.spec_from_file_location("rotor_lines", Path(__file__).with_name("rotor_lines.py"))
    m = iu.module_from_spec(spec); spec.loader.exec_module(m)
    one = m.run(radius=0.05, ell=1.0, T=200.0); rev = m.run(radius=0.05, ell=1.0, sense=-1.0, T=200.0)
    pt = m.run(radius=0.05, ell=0.02, T=200.0); fast = m.run(radius=0.05, ell=1.0, spin=3.0, T=200.0)
    ok = abs(one - 1) < 2e-3 and abs(rev + 1) < 2e-3 and abs(pt) < 0.02 and abs(fast - 1) < 2e-3
    return verdict(ok, f"turning/(B/2): one spacing {one:+.4f}; reversed {rev:+.4f}; spin x3 {fast:+.4f}; point by point {pt:+.4f}")

@check("§12.7", "NUMBER", "Share of capacity at the Earth's surface 1.4e-9 and at the Moon 2.3e-11; the Moon's turning (c^2/2) grad(share) = 2.70e-3 m/s^2",
       anchor=r"$(c_{0}^{2}/2)\nabla(\text{share})$ is $2.70 \times 10^{-3}\,\mathrm{m\,s^{-2}}$")
def _():
    GM = 3.986004418e14; R = 6.371e6; d = 3.844e8
    sh = lambda r: 2*GM/(r*c*c)
    turn = 0.5*c*c*2*GM/(d*d*c*c)
    return verdict(close(sh(R), 1.4e-9, 0.01) and close(sh(d), 2.3e-11, 0.01) and close(turn, 2.70e-3, 0.005),
                   f"share {sh(R):.3e} (surface), {sh(d):.3e} (Moon); turning {turn:.4e} m/s^2 = GM/d^2")

@check("§7.5, §7.7(5)", "NUMBER", "Dent (3.5 E_P) against the electron's 0.511 MeV, and the healing length against 386 fm: nearly 1e23",
       anchor=r"healing length, which lies nearly $10^{23}$ times below it")
def _():
    EP = math.sqrt(hbar*c**5/G)/eV; r = 3.54*EP/0.51099895e6
    return verdict(5e22 < r < 1.2e23, f"ratio {r:.2e}")

@check("§11.8", "FORMULA", "Phase around a spinning hole: theta = mu(t + F), Delta F' = 2 M r_+ solves the wave equation (Boyer-Lindquist) and is regular at r_+; no phi dependence, so zero circulation",
       anchor=r"$\theta = \mu_{\infty}[t + F(r)]$ with $\Delta F' = 2Mr_{+}$")
def _():
    M = 1.0; worst = 0; reg = []
    for a in [0.0, 0.5, 0.9, 0.998]:
        rp = M + math.sqrt(M*M - a*a)
        r = np.linspace(rp*1.05, 40, 20001); dr = r[1] - r[0]; D = r*r - 2*M*r + a*a
        box = np.gradient(D*(2*M*rp/D), dr)
        worst = max(worst, np.abs(box[5:-5]).max())
        x = rp*(1 + 1e-7); Dx = x*x - 2*M*x + a*a
        rm = M - math.sqrt(M*M - a*a); lim = -2*rp/(rp - rm)
        reg.append(abs((2*M*rp - (x*x + a*a))/Dx - lim)/abs(lim))
    return verdict(worst < 1e-9 and max(reg) < 1e-4, f"wave-equation residual {worst:.1e}; at r_+ F' - (r^2+a^2)/Delta tends to the finite -2r_+/(r_+ - r_-) (largest relative miss {max(reg):.1e})")

@check("§12.3", "NUMBER", "Clock at the Earth's surface: sqrt(1 - share) slows it by half the share, about 7e-10",
       anchor=r"half that, about $7 \times 10^{-10}$")
def _():
    sh = 2*3.986004418e14/(6.371e6*c*c); slow = 1 - math.sqrt(1 - sh)
    return verdict(close(slow, 7e-10, 0.01) and close(slow, sh/2, 1e-6), f"slowing {slow:.3e} = share/2")

@check("§12.7", "FORMULA", "Induced gravity count: carriers -8, 15 builds per family +15/2, conformal joining field 0: str[k1] = -1/2; cutoff 3.5 E_P; 16 per family gives 0",
       anchor=r"Twelve carriers give $-8$; three families of fifteen builds give $+\tfrac{15}{2}$")
def _():
    from fractions import Fraction as F
    k_vec, k_weyl, k_conf = F(-2, 3), F(-1, 6), F(0)
    s15 = 12*k_vec + 4*k_conf - 3*15*k_weyl; s16 = 12*k_vec + 4*k_conf - 3*16*k_weyl
    ratio = math.sqrt(2*math.pi/float(-s15)); EP = math.sqrt(hbar*c**5/G)/eV
    return verdict(s15 == F(-1, 2) and s16 == 0 and close(ratio, 3.5, 0.02) and 3.5e28 < ratio*EP < 4.8e28,
                   f"str = {s15} (15/family), {s16} (16/family); cutoff {ratio:.2f} E_P = {ratio*EP:.2e} eV")

@check("§12.7", "NUMBER", "Ocean's own sound speed with the dent at the Planck scale: a ~ 1e-120 for a flow rate below the expansion rate",
       anchor=r"$a \lesssim 10^{-120}$")
def _():
    EP = math.sqrt(hbar*c**5/G)/eV; mu = 1.43e-33   # expansion rate H0 ~ 1.4e-33 eV, an upper scale for today's rate
    a = 2*(mu/(3.5*EP))**2
    return verdict(1e-125 < a < 1e-118, f"a = {a:.1e} at a rate of order the expansion rate", note=False)

@check("§12.4", "NUMBER", "Baryon-to-photon ratio from the microwave background and from the light elements agree (Fields et al. 2020)",
       anchor=r"$(6.148 \pm 0.191) \times 10^{-10}$ from the light elements")
def _():
    z = abs(6.148 - 6.104)/math.hypot(0.058, 0.191)
    return verdict(z < 1, f"difference {z:.2f} standard deviations")

@check("§10.4(5)", "FORMULA", "mu is the cost of one more unit of Ocean charge for any law (de/dn = mu); opposite charges differ by 2 mu; antihydrogen 1S-2S (2e-12) bounds it below ~5e-7 eV",
       anchor=r"differ in rest energy by $2\mu$ per unit")
def _():
    worst = 0
    for P in [lambda m: m*m + m**4, lambda m: m*m + 0.3*m**6, lambda m: m*m/(1 + m*m)]:
        for mu in [0.05, 0.3, 0.8]:
            d = 1e-5; n = lambda m: (P(m + d) - P(m - d))/(2*d); e = lambda m: n(m)*m - P(m)
            worst = max(worst, abs((e(mu + 1e-3) - e(mu - 1e-3))/(n(mu + 1e-3) - n(mu - 1e-3)) - mu)/mu)
    bound = 2e-12*0.51099895e6/2
    return verdict(worst < 1e-4 and 4e-7 < bound < 6e-7, f"|de/dn - mu|/mu <= {worst:.1e} for three laws; bound mu < {bound:.1e} eV")

@check("§12.7", "SIMULATION", "In the minimal law a ripple in the amount at rest carries no Ocean charge; fast ripples (omega ~ k +/- mu) do",
       anchor=r"in the minimal law a ripple in the amount at rest carries no Ocean charge")
def _():
    lam = v = 1.0; mu = 0.3; rb = math.sqrt(v*v + 2*mu*mu/lam)
    def Lq(q):
        r, rt, rx, pt, px = q; rho = rb + r
        return (rt**2 - rx**2) + rho**2*((mu + pt)**2 - px**2) - lam/4*(rho**2 - v*v)**2
    H = np.zeros((5, 5)); dd = 1e-4
    for i in range(5):
        for j in range(5):
            e1 = np.eye(5)[i]*dd; e2 = np.eye(5)[j]*dd
            H[i, j] = (Lq(e1+e2) - Lq(e1-e2) - Lq(-e1+e2) + Lq(-e1-e2))/(4*dd*dd)
    def ripple(w, k):
        A = np.array([[1, -1j*w, 1j*k, 0, 0], [0, 0, 0, -1j*w, 1j*k]]).T
        _, _, vh = np.linalg.svd(A.conj().T @ H @ A); r, ph = vh.conj()[-1]
        dn = 4*rb*mu*r + 2*rb*rb*(-1j*w)*ph
        return abs(dn)/math.sqrt(abs(r)**2*w*w + abs(ph)**2*rb*rb*w*w)
    out = []
    for k in [1e-4, 30.0]:
        M2 = lam*rb*rb; b = 2*k*k + M2 + 4*mu*mu; cc = k*k*(k*k + M2); disc = math.sqrt(b*b - 4*cc)
        out.append(ripple(math.sqrt((b + disc)/2), k))
    return verdict(out[0] < 1e-6 and out[1] > 0.5, f"charge ripple / amplitude: amount ripple at rest {out[0]:.1e}; fast ripple {out[1]:.2f}")

# ================================================================ CONSISTENCY
@check("whole paper", "CONSISTENCY", "Every \\eqref and \\ref has a \\label; every \\cite has a \\bibitem")
def _():
    body = PAPER.body
    labels = set(re.findall(r"\\label\{([^}]+)\}", body))
    refs = set(re.findall(r"\\(?:eq)?ref\*?\{([^}]+)\}", body)) - {"LastPage"}
    cites = set(k.strip() for grp in re.findall(r"\\cite\{([^}]+)\}", body) for k in grp.split(","))
    items = set(re.findall(r"\\bibitem\{([^}]+)\}", body))
    missing_l = sorted(refs - labels); missing_b = sorted(cites - items); unused = sorted(items - cites)
    ok = not missing_l and not missing_b
    return verdict(ok, f"missing labels {missing_l}; missing bibitems {missing_b}; never cited {unused}")

@check("bibliography", "CONSISTENCY", "Bibliography is in first-citation order (as 3.10 states)")
def _():
    body = PAPER.body
    order = []
    for grp in re.findall(r"\\cite\{([^}]+)\}", body[:body.index(r"\begin{thebibliography}")]):
        for k in grp.split(","):
            k = k.strip()
            if k not in order: order.append(k)
    items = re.findall(r"\\bibitem\{([^}]+)\}", body)
    bad = [(i, a, b) for i, (a, b) in enumerate(zip(order, items)) if a != b]
    return verdict(not bad, "in order" if not bad else f"first mismatch at position {bad[0][0]+1}: cited {bad[0][1]}, listed {bad[0][2]}")

@check("whole paper", "CONSISTENCY", "Healing length stated consistently as 386 femtometers")
def _():
    vals = re.findall(r"(\d{3})(?:~|\\ |\s)(?:\\text\{)?femtometers", PAPER.body)
    return verdict(set(vals) == {"386"}, f"values found: {sorted(set(vals))} ({len(vals)} occurrences)")

@check("§11.6, §11.7, §11.8", "CONSISTENCY", "Symbol U is the rate of clocks only; the slowing is u (§11.6, Eq. 36); bold u is not reused for travel")
def _():
    clash = PAPER.has(r"U = \frac{G m}{c_{0}^{2}\, d}") or PAPER.has(r"U\, \mathbf{u}") or PAPER.has(r"\mathbf{V} \times \nabla U")
    return ("FAIL", "U or bold u reused in §11.8") if clash else ("PASS", "U is the clock rate (§11.6-11.7); u the slowing; bold V the travel")

@check("§2.2, §11.8 table", "CONSISTENCY", "Symbol mu is the Ocean's phase rate only (not reused in the §11.8 table)")
def _():
    clash = PAPER.has(r"$\mu = 0.991 \pm 0.02$") or PAPER.has(r"$\mu$ is the measured turning")
    return ("FAIL", "mu reused for the measured frame-dragging ratio") if clash else ("PASS", "mu is the phase rate throughout")

@check("whole paper", "CONSISTENCY", "Symbol w: travel relative to the Ocean (bold, Eq. 15) and equation of state w = -1; the clock deficit is u (§11.6)")
def _():
    clash = PAPER.has(r"Clocks slow by $w$") or PAPER.has(r"$1 - w$")
    return ("FAIL", "clock deficit still written w") if clash else ("NOTE", "bold w for travel and plain w = -1 for the equation of state remain, distinguished by typeface")

@check("§2.2, §2.5, §11.9", "CONSISTENCY", "Symbol n: density rho^2 (§2.2), refractive index n(r) (Eq. 10), exponent n (§11.9)")
def _():
    a = PAPER.has(r"n \equiv \rho^{2}"); b = PAPER.has(r"n(r) \;\simeq\;"); cc = PAPER.has(r"with $n = 1$ if")
    return ("NOTE", "three meanings of n, inherited from 3.10") if a and b and cc else ("PASS", "no clash")

@check("§11.4, §11.7, §11.9", "CONSISTENCY", "Symbol M is a mass only (Eq. 32 uses omega_rho for the heavy branch)")
def _():
    clash = PAPER.has(r"M^{2} = \lambda\bar{\rho}^{2}")
    return ("FAIL", "M^2 = lambda rho_bar^2 in Eq. (32) while M is a mass elsewhere") if clash else ("PASS", "M is a mass throughout")

@check("§3", "FORMULA", "The single-field equation omits the phase term -rho mu^2, which moves the settled amount by the fraction a/2",
       anchor=r"which moves the settled amount from $v$ by the fraction $a/2$")
def _():
    lam, v = 1.0, 1.0; out = []
    for a in (1e-3, 1e-6):
        mu2 = a*lam*v*v/2
        rho = math.sqrt(v*v + 2*mu2/lam)                    # settled amount of Eq. (14): lam rho (rho^2 - v^2)/2 = rho mu^2
        resid = 0.5*lam*rho*(rho*rho - v*v) - rho*mu2
        out.append((a, rho/v - 1, resid))
    ok = all(abs(sh/(a/2) - 1) < 1e-3 and abs(r) < 1e-12 for a, sh, r in out)
    return verdict(ok, "; ".join(f"a={a:g}: shift {sh:.3e} (a/2 = {a/2:.1e})" for a, sh, _ in out))

@check("§7.2, Eq. (18)", "FORMULA", "Two coupled fields: the quadratic action is the minimal law's expansion; branches c_s^2 = (1+a)/(1+3a), gap^2 = lambda v^2 + 6 mu^2, k^4 term 4a^2",
       anchor=r"+ 4\bar{\rho}\,\mu\,\delta\rho\, u^{\mu}\partial_{\mu}\delta\theta \Big].")
def _():
    lam, v, mu = 1.0, 1.0, 0.07; rb = math.sqrt(v*v + 2*mu*mu/lam); a = 2*mu*mu/(lam*v*v)
    # minimal law in the rest frame, unit carrying speed: L = rho_t^2 - rho_x^2 + rho^2 (theta_t^2 - theta_x^2) - lam/4 (rho^2 - v^2)^2
    def L(x):  # x = (r, r_t, r_x, th_t, th_x): perturbations about rho = rb, theta_t = mu
        r, rt, rx, tt, tx = x; rho = rb + r
        return rt*rt - rx*rx + rho*rho*((mu + tt)**2 - tx*tx) - lam/4*(rho*rho - v*v)**2
    h = 1e-4; H = np.zeros((5, 5)); e = np.eye(5)*h
    for i in range(5):
        for j in range(5):
            H[i, j] = (L(e[i]+e[j]) - L(e[i]-e[j]) - L(-e[i]+e[j]) + L(-e[i]-e[j]))/(4*h*h)
    want = np.zeros((5, 5)); want[0, 0] = -2*lam*rb*rb; want[1, 1] = 2; want[2, 2] = -2; want[3, 3] = 2*rb*rb; want[4, 4] = -2*rb*rb
    want[0, 3] = want[3, 0] = 4*rb*mu          # 2 x (quadratic-form coefficients of Eq. S2complex)
    ok1 = np.allclose(H, want, atol=1e-5)
    # branches of (w^2 - k^2)(w^2 - k^2 - lam rb^2) = 4 mu^2 w^2
    def w2(k):
        A = lam*rb*rb + 4*mu*mu; return [(2*k*k + A - s*math.sqrt(A*A + 16*mu*mu*k*k))/2 for s in (1, -1)]
    gap2 = w2(0.0)[1]; k = 1e-3; cs2 = w2(k)[0]/k**2
    kk = 1e-2; quart = (w2(kk)[0] - cs2*kk**2)/kk**4*(lam*v*v)
    ok = ok1 and close(gap2, lam*v*v + 6*mu*mu, 1e-9) and close(cs2, (1 + a)/(1 + 3*a), 1e-5) and close(quart, 4*a*a/(1 + 3*a)**3, 0.01)
    return verdict(ok, f"action from the minimal law: {'matches' if ok1 else 'MISMATCH'}; gap^2 {gap2:.6f} vs {lam*v*v+6*mu*mu:.6f}; c_s^2 {cs2:.6f} vs {(1+a)/(1+3*a):.6f}; k^4 term {quart:.2e} = 4a^2/(1+3a)^3 {4*a*a/(1+3*a)**3:.2e}, 4a^2 to leading order")

# ================================================================ run
def main():
    global PAPER
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", default=str(Path(__file__).resolve().parent.parent / "build_ocean_formalism.py"))
    ap.add_argument("--report", default=None)
    args = ap.parse_args()
    PAPER = Paper(args.build)
    rows = []
    for chk in RESULTS:
        if chk["anchor"] and not PAPER.has(chk["anchor"]):
            status, detail = "FAIL", "anchor not found in the paper: the wording or number has changed"
        else:
            try: status, detail = chk["fn"]()
            except Exception as ex: status, detail = "FAIL", f"error: {ex!r}"
        rows.append((chk["where"], chk["kind"], chk["what"], status, detail))
        print(f"[{status}] {chk['where']:22s} {chk['kind']:11s} {chk['what']}\n        {detail}")
    counts = {s: sum(r[3] == s for r in rows) for s in ("PASS", "NOTE", "FAIL")}
    print(f"\nVersion {PAPER.version}: {len(rows)} checks: {counts['PASS']} pass, {counts['NOTE']} note, {counts['FAIL']} fail")
    if args.report:
        with open(args.report, "w") as f:
            f.write(f"# Math check, version {PAPER.version}\n\n{len(rows)} checks: {counts['PASS']} pass, {counts['NOTE']} note, {counts['FAIL']} fail.\n\n")
            f.write("| Status | Where | Kind | Check | Result |\n|---|---|---|---|---|\n")
            for w, k, what, s, d in rows:
                f.write(f"| {s} | {w} | {k} | {what.replace('|','/')} | {d.replace('|','/')} |\n")
    return 1 if counts["FAIL"] else 0

if __name__ == "__main__":
    sys.exit(main())
