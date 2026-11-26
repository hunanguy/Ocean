"""What Coma's hot gas needs, without the isothermal assumption: hydrostatic balance with the
measured electron pressure from Planck's SZ map (Planck Intermediate Results X, 2013, Model C:
P0 = 2.2e-2 keV cm^-3, c500 = 2.9, gamma ~ 0, alpha = 1.8, beta = 3.1, R500 = 1.31 Mpc, h = 0.7)
and the X-ray electron density (beta model, Sanders 2003 / Reiprich 2001, as coma.py).
g(r) = -(1/(mu m_p n_e)) dP_e/dr. Compared with the isothermal beta model used so far.
Borrowed: spherical symmetry (Coma is a merger; Planck finds 10-15% lower pressure than XMM and
sector differences up to 25-30%); Planck's R500 comes from an X-ray scaling relation, but here it
only sets the radius scale of the fitted shape.
"""
import importlib.util, numpy as np
spec = importlib.util.spec_from_file_location("coma", __file__.replace("coma_need_planck.py", "coma.py"))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
keV, kpc, Mpc = c.keV, c.kpc, c.Mpc
P0, c5, ga, al, be, R5 = 2.2e-2, 2.9, 0.0, 1.8, 3.1, 1.31 * Mpc
Pe = lambda r: P0 * keV * 1e6 / ((c5 * r / R5) ** ga * (1 + (c5 * r / R5) ** al) ** ((be - ga) / al))   # J/m^3
T, b, rcg, ne0 = c.GAS["Sanders 2003 / Reiprich 2001"]; rc = rcg * kpc
ne = lambda r: ne0 * 1e6 * (1 + (r / rc) ** 2) ** (-1.5 * b)
r = np.geomspace(5 * kpc, 3.2 * Mpc, 4000)
g_sz = -np.gradient(Pe(r), r) / (c.mu * c.mp * ne(r))
g_iso = c.g_obs(r, T, b, rcg)
for R in (0.25, 0.5, 1, 1.5, 2, 2.5):
    i = np.searchsorted(r, R * Mpc)
    print(f"r {R:4.2f} Mpc: T from P/n {Pe(r[i])/ne(r[i])/keV:4.1f} keV; needed turning SZ/isothermal = {g_sz[i]/g_iso[i]:.2f}")
Mr = g_sz * r**2 / c.G
dM = np.gradient(Mr, r); rho_sz = dM / (4 * np.pi * r**2)
rho_fn = lambda x: np.interp(x, r, rho_sz)
rt = 3 * Mpc
RR = np.array([0.5, 1.0, 1.5, 2.0]) * Mpc
A = 3 * b * T * keV / (c.mu * c.mp)
rho_iso = lambda x: A / (4 * np.pi * c.G) * (x**2 + 3 * rc**2) / (x**2 + rc**2) ** 2
need_sz = np.array([c.project_density(rho_fn, R, rt) for R in RR])
need_iso = np.array([c.project_density(rho_iso, R, rt) for R in RR])
print("needed in cylinders 0.5,1,1.5,2 Mpc (1e14 suns): isothermal", " ".join(f"{x/c.Msun/1e14:.2f}" for x in need_iso),
      "| SZ pressure", " ".join(f"{x/c.Msun/1e14:.2f}" for x in need_sz))
print("scale factor to apply to earlier shares (isothermal need / SZ need):", " ".join(f"{x:.2f}" for x in need_iso / need_sz))
np.save("/tmp/need_ratio.npy", need_iso / need_sz)
