"""Published Milky Way data used for the vertical test (item 2 of the 3.16 list).

Rotation curve: Eilers, Hogg, Rix & Ness 2019 (arXiv:1810.09466), Table 1, the 26 points
5 <= R <= 18 kpc that Lisanti et al. 2023 (arXiv:1911.12365) use, statistical errors symmetrized.

Vertical force: Bovy & Rix 2013 (arXiv:1309.0809), Table 3: K_z at |z| = 1.1 kpc from 43
mono-abundance populations of SEGUE G dwarfs, in units of 2 pi G Msun/pc^2, at R0 - R given
in the table ("to be held constant when using our measurements with a different value of R0").

Baryon constraints, as Lisanti et al. 2023 use them: stellar disk scale length 2.6 +/- 0.5 kpc
and scale height 310 +/- 50 pc; midplane gas density at the Sun 0.041 +/- 0.004 Msun/pc^3;
stellar and gas surface densities within 1.1 kpc 31.2 +/- 1.6 and 12.6 +/- 1.6 Msun/pc^2
(McKee, Parravano & Hollenbach 2015).
"""
import numpy as np

R0 = 8.122  # kpc, GRAVITY 2018, as Eilers et al. and Lisanti et al.

# Eilers et al. 2019, Table 1: R, v_c, sigma-, sigma+  (5.27 ... 17.75 kpc: 26 points)
_eilers = """5.27 226.83 1.91 1.90
5.74 230.80 1.43 1.35
6.23 231.20 1.70 1.10
6.73 229.88 1.44 1.32
7.22 229.61 1.37 1.11
7.82 229.91 0.92 0.88
8.19 228.86 0.80 0.67
8.78 226.50 1.07 0.95
9.27 226.20 0.72 0.62
9.76 225.94 0.42 0.52
10.26 225.68 0.44 0.40
10.75 224.73 0.38 0.41
11.25 224.02 0.33 0.54
11.75 223.86 0.40 0.39
12.25 222.23 0.51 0.37
12.74 220.77 0.54 0.46
13.23 220.92 0.57 0.40
13.74 217.47 0.64 0.51
14.24 217.31 0.77 0.66
14.74 217.60 0.65 0.68
15.22 217.07 1.06 0.80
15.74 217.38 0.84 1.07
16.24 216.14 1.20 1.48
16.74 212.52 1.39 1.43
17.25 216.41 1.44 1.85
17.75 213.70 2.22 1.65"""
_e = np.array([[float(x) for x in l.split()] for l in _eilers.splitlines()])
RC_R, RC_V, RC_ERR = _e[:, 0], _e[:, 1], 0.5*(_e[:, 2] + _e[:, 3])

# Bovy & Rix 2013, Table 3: R0 - R (kpc), K_z,1.1 / 2 pi G (Msun/pc^2), uncertainty
_br = """3.37 217.6 41.5
3.32 230.6 36.8
1.29 84.2 18.5
3.23 209.0 33.2
3.41 194.7 38.6
2.96 180.5 29.2
2.78 179.0 25.6
3.32 211.4 33.7
0.62 62.2 11.2
1.47 97.5 18.0
1.38 109.8 12.9
1.34 119.0 12.9
2.92 176.8 30.1
0.58 61.7 11.0
1.47 115.9 14.8
0.89 92.0 7.5
1.29 121.9 10.9
1.47 96.1 18.0
0.80 77.3 11.8
0.80 95.2 9.3
1.66 146.3 11.5
1.21 101.2 13.4
0.71 84.9 9.1
0.71 88.5 7.4
0.98 98.7 8.2
1.43 100.8 17.1
0.44 74.5 8.1
1.25 114.3 11.7
1.16 108.4 9.4
2.46 168.6 20.9
0.71 87.2 9.6
1.43 140.1 12.4
2.33 170.6 19.5
0.30 72.8 8.0
0.12 62.4 8.2
0.30 73.9 7.8
1.92 147.4 17.7
1.43 113.2 14.9
0.08 69.2 6.8
-0.55 53.4 4.7
0.80 101.3 9.4
1.97 132.4 18.8
3.18 206.2 35.7"""
_b = np.array([[float(x) for x in l.split()] for l in _br.splitlines()])
KZ_R, KZ, KZ_ERR = R0 - _b[:, 0], _b[:, 1], _b[:, 2]
KZ_Z = 1.1  # kpc

# Baryon constraints (value, error)
HSTAR_R = (2.6, 0.5)      # kpc
HSTAR_Z = (0.31, 0.05)    # kpc
RHO_GAS0 = (0.041, 0.004) # Msun/pc^3 at (R0, 0)
SIG_STAR = (31.2, 1.6)    # Msun/pc^2 within 1.1 kpc
SIG_GAS = (12.6, 1.6)
GDAG = (1.20, 0.24)       # 1e-10 m/s^2, the radial acceleration relation (McGaugh, Lelli & Schombert 2016)

assert len(RC_R) == 26 and len(KZ) == 43
