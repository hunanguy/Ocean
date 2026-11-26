"""The Milky Way eddy's edge from the local escape speed, compared like for like: Deason et al. 2019
define the escape speed as the speed to reach 2 r200 (their outer boundary, about 380-450 kpc,
chosen from standard-account simulations - a borrowed step), not infinity. Uses mw_edge.py's real
Milky Way fits. Sun at r0 = 8.3 kpc as in Deason."""
import runpy, numpy as np, io, contextlib
with contextlib.redirect_stdout(io.StringIO()): m = runpy.run_path("mw_edge.py")
g_total, enclosed = m["g_total"], m["enclosed"]
def vesc_to(R0, Re, rout, p, gd):
    top = min(Re, rout); r = np.geomspace(R0, top, 4000)
    phi = np.trapezoid(g_total(r, p, gd), r)
    if Re < rout:
        gRe = g_total(np.array([Re]), p, gd)[0]; phi += gRe * Re**2 * (1/Re - 1/rout)
    return np.sqrt(2*phi)
for name, th in m["fits"].items():
    p = dict(zip(['rs','hR','hz','rg','hgz','Mb'], th[:6])); gd = th[6]
    print(name)
    for rout in (380, 410, 450):
        Re_grid = np.geomspace(20, 5000, 300); ve = np.array([vesc_to(8.3, Re, rout, p, gd) for Re in Re_grid])
        res = []
        for t in (503, 528, 552):
            i = np.searchsorted(ve, t); res.append(np.interp(t, ve, Re_grid) if 0 < i < len(ve) else (np.inf if t < ve[0] else -1) )
        print(f"  boundary {rout} kpc: speed with no edge {vesc_to(8.3, 1e9, rout, p, gd):.0f} km/s; edge for 503/528/552: " + ", ".join("none needed" if (np.isinf(x) or x<0 and ve[-1]<t) else f"{x:.0f}" for x,t in zip(res,(503,528,552))))
    print(f"  (old way, to infinity, edge 100 kpc: {m['vesc'](8.3, 100, p, gd):.0f} km/s)")
