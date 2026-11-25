"""Supernova distance samples, each used as its own release's likelihood uses it.

The releases are not copied here; fetch them with git (see README.md) and point
the environment variables at their distance folders, or keep the default
layout under ./data:
  PANTHEON_DIR  Pantheon+_Data/4_DISTANCES_AND_COVAR   (PantheonPlusSH0ES/DataRelease)
  DES2024_DIR   4_DISTANCES_COVMAT at tag 1.3          (des-science/DES-SN5YR)
  DOVEKIE_DIR   4_DISTANCES_COVMAT on main             (des-science/DES-SN5YR)
In every case the supernovae's absolute brightness (and with it H0) is left
free and removed analytically, so only the shape of the expansion is tested.
"""
import os, gzip, numpy as np
from pathlib import Path
from scipy.integrate import cumulative_trapezoid

HERE = Path(__file__).resolve().parent
DIRS = {
    'Pantheon+': os.environ.get('PANTHEON_DIR', str(HERE/'data/pantheon/Pantheon+_Data/4_DISTANCES_AND_COVAR')),
    'DES-SN5YR 2024': os.environ.get('DES2024_DIR', str(HERE/'data/des2024/4_DISTANCES_COVMAT')),
    'DES-Dovekie 2026': os.environ.get('DOVEKIE_DIR', str(HERE/'data/dovekie/4_DISTANCES_COVMAT')),
}

def load(name):
    D = DIRS[name]
    if name == 'Pantheon+':
        # Brout et al. 2022: m_b_corr with STAT+SYS, zHD > 0.01 (Cepheid hosts out)
        t = np.genfromtxt(f'{D}/Pantheon+SH0ES.dat', names=True, dtype=None, encoding=None)
        raw = np.loadtxt(f'{D}/Pantheon+SH0ES_STAT+SYS.cov'); n = int(raw[0])
        m = t['zHD'] > 0.01
        C = raw[1:].reshape(n, n)[np.ix_(m, m)]
        return t['zHD'][m], t['zHEL'][m], t['m_b_corr'][m], np.linalg.inv(C)
    if name == 'DES-SN5YR 2024':
        # tag 1.3 likelihood: STAT+SYS.txt.gz plus MUERR_FINAL^2 on the diagonal
        t = np.genfromtxt(f'{D}/DES-SN5YR_HD.csv', delimiter=',', names=True, dtype=float, usecols=(3, 4, 5, 6), encoding=None)
        with gzip.open(f'{D}/STAT+SYS.txt.gz', 'rt') as fh:
            raw = np.array(fh.read().split(), dtype=float)
        n = int(raw[0]); C = raw[1:].reshape(n, n)
        C[np.diag_indices(n)] += t['MUERR_FINAL']**2
        return t['zHD'], t['zHEL'], t['MU'], np.linalg.inv(C)
    # DES-Dovekie: STAT+SYS.npz holds the inverse covariance, upper triangle
    lines = open(f'{D}/DES-Dovekie_HD.csv').read().splitlines()
    hdr = [l.split() for l in lines if l.startswith('VARNAMES:')][0][1:]
    rows = [l.split() for l in lines if l.startswith('SN:')]
    col = {k: i for i, k in enumerate(hdr)}
    get = lambda k: np.array([float(r[1 + col[k]]) for r in rows])
    d = np.load(f'{D}/STAT+SYS.npz'); n = int(d[d.files[0]][0])
    IC = np.zeros((n, n)); IC[np.triu_indices(n)] = d[d.files[1]]
    il = np.tril_indices(n, -1); IC[il] = IC.T[il]
    return get('zHD'), get('zHEL'), get('MU'), IC

class Sample:
    def __init__(self, name):
        self.name = name
        self.zhd, self.zhel, self.mu, self.ic = load(name)
        self.one = np.ones_like(self.mu); self.a11 = self.one @ self.ic @ self.one
    def chi2(self, z, E):
        DM = np.concatenate([[0], cumulative_trapezoid(1/E, z)])
        r = self.mu - 5*np.log10((1 + self.zhel)*np.interp(self.zhd, z, DM))
        b = self.one @ self.ic @ r
        return float(r @ self.ic @ r - b*b/self.a11)
