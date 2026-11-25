"""SPARC (Lelli, McGaugh & Schombert 2016): galaxy table and mass models.

Reads the two machine-readable tables in data/ and returns one record per galaxy.
Velocities in km/s, radii in kpc, masses in solar masses.
"""
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
G = 4.30091e-6                       # kpc (km/s)^2 / Msun
GDAG_UNIT = 1e-10 / 3.24078e-14      # 1e-10 m/s^2 in (km/s)^2/kpc


def _f(s):
    s = s.strip()
    return float(s) if s else np.nan


def read_galaxies(path=os.path.join(HERE, "data", "SPARC_Lelli2016c.mrt")):
    out = {}
    with open(path) as fh:
        lines = fh.readlines()
    # data lines start after the last dashed rule following the notes
    start = max(i for i, l in enumerate(lines) if l.startswith("-----")) + 1
    for l in lines[start:]:
        if len(l.strip()) == 0:
            continue
        # the file's rows are one byte off its own byte table, so split on spaces:
        # name, 17 numbers, references
        f = l.split()
        name, v = f[0], [float(x) for x in f[1:18]]
        out[name] = dict(
            name=name, T=int(v[0]), D=v[1], e_D=v[2], f_D=int(v[3]), inc=v[4], e_inc=v[5],
            L=v[6] * 1e9, e_L=v[7] * 1e9, Reff=v[8], Rdisk=v[10], MHI=v[12] * 1e9, RHI=v[13],
            Vflat=v[14], e_Vflat=v[15], Q=int(v[16]))
    return out


def read_models(path=os.path.join(HERE, "data", "MassModels_Lelli2016c.mrt")):
    rows = {}
    with open(path) as fh:
        lines = fh.readlines()
    start = max(i for i, l in enumerate(lines) if l.startswith("-----")) + 1
    for l in lines[start:]:
        if len(l.strip()) == 0:
            continue
        f = l.split()   # ID D R Vobs e_Vobs Vgas Vdisk Vbul SBdisk SBbul
        rows.setdefault(f[0], []).append([float(x) for x in f[1:10]])
    return {k: np.array(v) for k, v in rows.items()}


def disk_enclosed(R, SB):
    """Disk light inside radius R (Lsun, thin disk, so the sphere and the cylinder agree), from the
    face-on surface brightness (Lsun/pc^2). Inside the first point the profile is carried in on the
    exponential slope of the first two points."""
    Rpc = R * 1e3
    SB = np.maximum(SB, 0)
    s0, s1 = max(SB[0], 1e-6), max(SB[1], 1e-6) if len(SB) > 1 else max(SB[0], 1e-6)
    h = (Rpc[1] - Rpc[0]) / np.log(s0 / s1) if len(SB) > 1 and s0 > s1 else np.inf
    # inner part: integral of 2 pi r s0 exp(-(r - R0)/h) from 0 to R0
    R0 = Rpc[0]
    if np.isfinite(h) and h > 0:
        inner = 2 * np.pi * s0 * np.exp(R0 / h) * h * h * (1 - np.exp(-R0 / h) * (1 + R0 / h))
    else:
        inner = np.pi * R0 ** 2 * s0
    ring = 2 * np.pi * Rpc * SB
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (ring[1:] + ring[:-1]) * np.diff(Rpc))])
    return inner + cum


def sph_enclosed(R, V):
    """Mass inside radius R read as a sphere, R V|V|/G, never negative and never falling outward.
    Exact for a round component (the bulge); for a disk it is the usual round stand-in."""
    M = np.maximum(R * V * np.abs(V) / G, 0.0)
    return np.maximum.accumulate(M)


def load():
    gal = read_galaxies()
    mod = read_models()
    out = []
    for name, g in gal.items():
        a = mod[name]
        R, Vobs, eV, Vgas, Vdisk, Vbul = a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5], a[:, 6]
        has_bul = bool(np.any(Vbul > 0))
        # bulge light: mass inside the last point at M/L = 1, the bulge being nearly all inside it
        Lbul = Vbul[-1] ** 2 * R[-1] / G if has_bul else 0.0
        Ldisk = max(g["L"] - Lbul, 0.0)
        SBdisk = a[:, 7]
        out.append(dict(g, R=R, Vobs=Vobs, eV=eV, Vgas=Vgas, Vdisk=Vdisk, Vbul=Vbul,
                        has_bul=has_bul, Lbul=Lbul, Ldisk=Ldisk, Mgas=1.33 * g["MHI"],
                        Menc_disk=disk_enclosed(R, SBdisk), Menc_bul=sph_enclosed(R, Vbul),
                        # gas: SPARC gives no gas surface density, so the round stand-in, never more than
                        # the whole gas (1.33 M_HI); in a few galaxies V_gas implies far more gas than M_HI
                        Menc_gas=np.minimum(sph_enclosed(R, Vgas), 1.33 * g["MHI"]),
                        Menc_gas_v=sph_enclosed(R, Vgas), Menc_disk_v=sph_enclosed(R, Vdisk)))
    return out


if __name__ == "__main__":
    gs = load()
    n = sum(len(g["R"]) for g in gs)
    print(len(gs), "galaxies,", n, "points;", sum(g["has_bul"] for g in gs), "with bulges")
    sel = [g for g in gs if g["Q"] < 3 and g["inc"] >= 30]
    print(len(sel), "after Q<3 and i>=30")
