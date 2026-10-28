# Rotor in a field of quantized lines, each part read by Eq. (15):
#   a = (v.grad)v - (xdot - v) x (curl v)
# where v is the Ocean's flow READ over a scale ell (the pattern's disturbance): the line field smoothed with a
# Gaussian of width ell. A point line smoothed this way is a Lamb-Oseen line:
#   v_phi = k/(2 pi r) (1 - exp(-r^2 / 2 ell^2)),  curl = k/(2 pi ell^2) exp(-r^2 / 2 ell^2).
# ell -> 0 is pointwise reading. Lines along z on a square lattice (spacing a = 1) filling a disk; the smooth average
# is rigid turning with curl B = k/a^2. Smooth result (Larmor): the spin axis turns about z at B/2.
import numpy as np, sys, time
a = 1.0; B0 = 2e-3; k = B0*a*a; Rdisk = 14.0
g = np.arange(-Rdisk, Rdisk + 1e-9, a) + 0.31*a
X, Y = np.meshgrid(g, g + 0.17*a); X = X.ravel(); Y = Y.ravel(); keep = X**2 + Y**2 < Rdisk**2
LX, LY = X[keep], Y[keep]
def field(px, py, ell, sense):
    """v (2), Jacobian (2x2), curl at points px, py (arrays), summed over all lines."""
    dx = px[:, None] - LX[None, :]; dy = py[:, None] - LY[None, :]; r2 = dx*dx + dy*dy + 1e-30
    q = r2/(2*ell*ell); e = np.exp(-q); f = (1 - e)/r2
    fp = (e*r2/(2*ell*ell) - (1 - e))/(r2*r2)            # df/d(r^2)
    c = sense*k/(2*np.pi)
    vx = (c*(-dy*f)).sum(1); vy = (c*(dx*f)).sum(1)
    dvx_dx = (c*(-dy*fp*2*dx)).sum(1); dvx_dy = (c*(-f - dy*fp*2*dy)).sum(1)
    dvy_dx = (c*(f + dx*fp*2*dx)).sum(1); dvy_dy = (c*(dx*fp*2*dy)).sum(1)
    curl = dvy_dx - dvx_dy
    return vx, vy, dvx_dx, dvx_dy, dvy_dx, dvy_dy, curl
def run(radius, ell, sense=1.0, spin=1.0, T=600.0, dt=0.1, N=24):
    ph = np.linspace(0, 2*np.pi, N, endpoint=False); body = radius*np.c_[np.cos(ph), np.sin(ph), np.zeros(N)]
    Ib = np.diag([N/2, N/2, N])*radius**2; Ibi = np.linalg.inv(Ib)
    sk = lambda w: np.array([[0, -w[2], w[1]], [w[2], 0, -w[0]], [-w[1], w[0], 0]])
    def deriv(R, L):
        om = R @ Ibi @ R.T @ L; r = body @ R.T; xd = np.cross(om, r)
        vx, vy, a11, a12, a21, a22, cu = field(r[:, 0], r[:, 1], ell, sense)
        v = np.c_[vx, vy, 0*vx]
        conv = np.c_[vx*a11 + vy*a12, vx*a21 + vy*a22, 0*vx]          # (v.grad)v
        w = xd - v; Cz = np.c_[0*cu, 0*cu, cu]
        acc = conv - np.cross(w, Cz)
        return sk(om) @ R, np.cross(r, acc).sum(0)
    tl = np.radians(60); R = np.array([[1, 0, 0], [0, np.cos(tl), -np.sin(tl)], [0, np.sin(tl), np.cos(tl)]])
    L = R @ Ib @ np.array([0, 0, spin*1.0]); n = int(T/dt); angs = []
    for i in range(n + 1):
        if i % 50 == 0: angs.append((i*dt, np.arctan2(L[1], L[0])))
        k1 = deriv(R, L); k2 = deriv(R + dt/2*k1[0], L + dt/2*k1[1])
        k3 = deriv(R + dt/2*k2[0], L + dt/2*k2[1]); k4 = deriv(R + dt*k3[0], L + dt*k3[1])
        R = R + dt/6*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0]); L = L + dt/6*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
        u, _, vt = np.linalg.svd(R); R = u @ vt
    t, an = np.array(angs).T
    return np.polyfit(t, np.unwrap(an), 1)[0]/(B0/2)
if __name__ == "__main__":
    cases = [
        ("large rotor (3 spacings), pointwise reading",       dict(radius=3.0,  ell=0.02)),
        ("large rotor, reading over 0.25 spacing",            dict(radius=3.0,  ell=0.25)),
        ("large rotor, reading over 0.5 spacing",             dict(radius=3.0,  ell=0.5)),
        ("large rotor, reading over 1 spacing",               dict(radius=3.0,  ell=1.0)),
        ("large rotor, reading over 2 spacings",              dict(radius=3.0,  ell=2.0)),
        ("small rotor (0.05 spacing), pointwise reading",     dict(radius=0.05, ell=0.02)),
        ("small rotor, reading over 0.5 spacing",             dict(radius=0.05, ell=0.5)),
        ("small rotor, reading over 1 spacing",               dict(radius=0.05, ell=1.0)),
        ("small rotor, reading over 2 spacings",              dict(radius=0.05, ell=2.0)),
        ("small rotor, 2 spacings, lines reversed",           dict(radius=0.05, ell=2.0, sense=-1.0)),
        ("small rotor, 2 spacings, spin x3",                  dict(radius=0.05, ell=2.0, spin=3.0)),
    ]
    for label, kw in cases:
        t0 = time.time(); r = run(**kw)
        print(f"{label:48s} turning / (B/2) = {r:+.4f}   [{time.time()-t0:.0f}s]", flush=True)
