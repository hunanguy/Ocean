"""The Milky Way eddy's edge from the measured local escape speed, with the real Milky Way's
fitted stars and gas (Section 6: Lisanti et al.'s data, eddy of Eq. (15); best fit
'lisanti_eddy' of milky-way/best_fits.json: stars and gas 6.7e10, bulge 1.3e10, g† 1.22).
Method as Section 6: the turning of the stars and gas and of the eddy counted out to the
edge, and beyond it everything inside the edge acting as one mass; the escape speed at the
Sun is sqrt(2 x potential). Measured: 528 +24/-25 km/s (Deason et al. 2019).
Units kpc, km/s, Msun.
"""
import numpy as np
G = 4.30091e-6; ACC = 3.2408e-14; GD_UNIT = 1e-10 / ACC
_X, _W = np.polynomial.legendre.leggauss(64)

def disk_sph_mass(r, rho0, hR, hz):
    r = np.asarray(r, float)[:, None]; zt = np.minimum(r, 40 * hz)
    z = 0.5 * zt * (_X + 1); w = 0.5 * zt * _W
    a = np.sqrt(np.maximum(r * r - z * z, 0))
    ring = 2 * np.pi * hR**2 * (1 - np.exp(-a / hR) * (1 + a / hR))
    return 2 * rho0 * np.sum(w * np.exp(-z / hz) * ring, axis=1)

def enclosed(r, p):
    return (disk_sph_mass(r, p['rs'] * 1e9, p['hR'], p['hz']) + disk_sph_mass(r, p['rg'] * 1e9, 2 * p['hR'], p['hgz'])
            + p['Mb'] * 1e10 * r**2 / (r + 0.6)**2)

def g_total(r, p, gdag):
    gd = gdag * GD_UNIT
    gN = G * enclosed(r, p) / r**2
    c = (gN / gd) / np.sqrt(3); B = c * c + c * np.sqrt(c * c + 1)
    return gN + np.sqrt(gN * gd) / (1 + B)

def vesc(R0, Re, p, gdag):
    r = np.geomspace(R0, Re, 4000); g = g_total(r, p, gdag)
    phi = np.trapezoid(g, r) + g_total(np.array([Re]), p, gdag)[0] * Re   # beyond: everything inside as one mass
    return np.sqrt(2 * phi)

fits = {
 "real Milky Way, Lisanti et al.'s data": [2.9336598242119534, 2.015838871018057, 0.302304244492705, 0.30803234283197617, 0.14407209309040997, 1.303483696973275, 1.2193064567494736],
 "real Milky Way, Bovy & Rix data":       [3.048602326776905, 2.007738797056165, 0.3113311903330136, 0.3094226230861268, 0.16683879944828003, 0.9474106686910173, 1.1865702071798654],
}
for name, th in fits.items():
    p = dict(zip(['rs', 'hR', 'hz', 'rg', 'hgz', 'Mb'], th[:6])); gdag = th[6]
    Mtot = enclosed(np.array([1e4]), p)[0]
    print(f"{name}: stars and gas {Mtot:.2e}, g† {gdag:.2f}")
    for R0 in (8.1, 8.2):
        Re_grid = np.geomspace(30, 2000, 400)
        ve = np.array([vesc(R0, Re, p, gdag) for Re in Re_grid])
        for target in (503, 528, 552):
            i = np.searchsorted(ve, target)
            Re = np.interp(target, ve, Re_grid) if 0 < i < len(ve) else np.nan
            print(f"   Sun at {R0} kpc, escape speed {target} km/s -> edge {Re:6.0f} kpc")
    print("   (escape speed with edge 100, 150, 230 kpc at 8.1 kpc: " +
          ", ".join(f"{vesc(8.1, x, p, gdag):.0f}" for x in (100, 150, 230)) + " km/s)")
