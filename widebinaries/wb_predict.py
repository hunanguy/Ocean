"""What each reading gives a wide binary, as the boost g/g_N of the pair's turning on each other (g_N = G M / r^2).
(A) no eddy of its own (Keith: one galaxy, one eddy; no eddy inside an eddy): g = g_N, boost 1.
(B) its own eddy, Eq. (15) with the tie-up from the pair's own turning only: g = g_N + sqrt(g_N g+)/(1+B(y)), y = g_N/g+.
(C) its own eddy, the tie-up read from all the turning at its place (the pair's plus the Milky Way's own, about 0.8 g+ at the Sun
    for the model Milky Way of App. B, whose own turning falls to the limit at 6.3 kpc): B from y_tot = sqrt(g_N^2 + g_MW^2)/g+.
Not modelled: how a pair's eddy would sit inside the Milky Way's (no rule for it in the paper)."""
import numpy as np
from scipy.optimize import brentq
gd = 1.2e-10
def B(y): return brentq(lambda b: b/np.sqrt(1 + 2*b) - y/np.sqrt(3), 0, 1e12)
gMW = 0.8*gd
print("  g_N (m/s^2)   (A)    (B)    (C)      [Chae et al. report about 1.4-1.5 below 1e-10; Banik et al. report 1 (Newtonian)]")
for gN in (1e-8, 1e-9, 3e-10, 1e-10, 3e-11, 1e-11):
    b = 1 + np.sqrt(gN*gd)/(1 + B(gN/gd))/gN
    c = 1 + np.sqrt(gN*gd)/(1 + B(np.hypot(gN, gMW)/gd))/gN
    print(f"  {gN:9.0e}     1.00   {b:5.2f}  {c:5.2f}")
