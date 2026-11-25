# DESI DR2 BAO (Abdul-Karim et al. 2025, DESI Collaboration)

**Citation.** DESI Collaboration, M. Abdul-Karim et al., "DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints", arXiv:2503.14738 (v3). Read 22 Nov 2026 (PDF, via fetch) for the dynamo-output work (`claude/dynamo-output.md`). Cited in the 3.16 paper as desi2025 (Sections 5.1 and 13.1).

**Used: Table IV, the BAO distances** (r_d the sound horizon at the drag epoch):

| Tracer | z_eff | D_V/r_d | D_M/r_d | D_H/r_d | r_M,H |
|---|---|---|---|---|---|
| BGS | 0.295 | 7.942 ± 0.075 | — | — | — |
| LRG1 | 0.510 | 12.720 ± 0.099 | 13.588 ± 0.167 | 21.863 ± 0.425 | −0.459 |
| LRG2 | 0.706 | 16.050 ± 0.110 | 17.351 ± 0.177 | 19.455 ± 0.330 | −0.404 |
| LRG3+ELG1 | 0.934 | 19.721 ± 0.091 | 21.576 ± 0.152 | 17.641 ± 0.193 | −0.416 |
| ELG2 | 1.321 | 24.252 ± 0.174 | 27.601 ± 0.318 | 14.176 ± 0.221 | −0.434 |
| QSO | 1.484 | 26.055 ± 0.398 | 30.512 ± 0.760 | 12.817 ± 0.516 | −0.500 |
| Lyα | 2.330 | 31.267 ± 0.256 | 38.988 ± 0.531 | 8.632 ± 0.101 | −0.431 |

Thirteen numbers used: BGS's D_V, and D_M, D_H with their correlation for the other six.

**Quoted results used as checks.** BAO alone, flat ΛCDM: Ω_m = 0.2975 ± 0.0086, h r_d = 101.54 ± 0.73 Mpc. BAO alone, w0waCDM: w0 = −0.48 (+0.35/−0.17), wa < −1.34, Δχ² = −4.7 against ΛCDM (1.7σ; Table VI). DESI+CMB+DESY5, w0waCDM (Table V): w0 = −0.752 ± 0.057, wa = −0.86 (+0.23/−0.20). Preference for dynamical dark energy: 3.1σ for DESI BAO + CMB, 2.8–4.2σ with supernovae depending on the sample.

**What the work takes from it.** Only the distances, with h r_d left free, so no early-universe input enters. The pipeline reproduces DESI's own BAO-alone numbers (Ω_m 0.2973, h r_d 101.55 Mpc, w0–wa Δχ² −4.73).
