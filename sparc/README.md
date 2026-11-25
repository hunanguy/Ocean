# SPARC: the eddy galaxy by galaxy

The analysis behind Section 6's statement that the eddy of Equation 15, with one limit for every
galaxy, fits the rotation curves of the SPARC galaxies (Lelli, McGaugh & Schombert 2016; 175 disk
galaxies) nearly as well as the measured radial acceleration relation, galaxy by galaxy, as Li,
Lelli, McGaugh & Schombert 2018 (A&A 615, A3; arXiv:1803.00022) fit the relation.

Each galaxy gets its own disk and bulge mass-to-light ratios, distance and inclination, held near
their measured values by the same priors Li et al. use. Each galaxy's fit is profiled over the limit
g_dagger, so one run gives both the fit with one limit shared by all galaxies and the fit with the
limit free in each.

The eddy (`DEFAULT_FORM = "loans"` in `sparc_fit.py`): at each radius it answers to the galaxy's own
turning averaged over the sphere there, g_N = G M(<r)/r², and is built only from the Ocean the
galaxy's own loans leave free, g_e = √(g_N g†)/(1 + B) with B/√(1 + 2B) = (g_N/g†)/√3 (B, the tie-up; the paper keeps ρ for the Ocean's amount). The mass
inside r comes from the stellar disk's surface brightness, the bulge as a round body, and the gas as
its round stand-in R V_gas²/G (never above 1.33 M_HI). The form of versions 3.13–3.15, set by the
total mass alone, is `cored`; other forms are comparisons (see `sparc_fit.py`).

## Files

| File | What it does |
|---|---|
| `data/SPARC_Lelli2016c.mrt` | galaxy table: distance, inclination, luminosity, HI mass, quality |
| `data/MassModels_Lelli2016c.mrt` | rotation curves and the baryons' contributions |
| `sparc_data.py` | reads both tables; the mass inside each radius |
| `sparc_fit.py` | fits all galaxies over a grid of the limit; writes `results/profiles.npz` |
| `sparc_report.py` | the summary: shared limit, free limit, residual scatter, trends; writes `results/summary.json` |
| `sparc_pushback.py` | each galaxy's central pushback and core load per area; writes `results/pushback.json` |
| `sparc_figures.py` | the paper's figures, `figures/fig_sparc.pdf` and `figures/fig_free_share.pdf` |
| `sparc_plot.py` | a working figure, `results/sparc_test.png` |

## Run

    python3 sparc_fit.py                # the RAR and the eddy; about 5 minutes on 2 cores
    python3 sparc_report.py
    python3 sparc_pushback.py
    python3 sparc_fit.py cored          # the 3.13-3.15 eddy, for comparison (eddy only)
    python3 sparc_report.py cored
    python3 sparc_figures.py

Needs numpy, scipy, matplotlib. Li et al. sample with emcee and report the maximum of the
posterior; these scripts find that maximum directly.

## Results (153 galaxies: quality 1-2, inclination at least 30 degrees; 3168 points)

| | χ² at the shared limit (2678 dof) | shared limit | χ² gain, each galaxy's own limit | own limit against mass (Spearman) | residual rms |
|---|---|---|---|---|---|
| radial acceleration relation | 13 729 | 1.12 | 11% | +0.04 (p 0.6) | 0.057 dex |
| eddy (Section 6) | 14 358 | 1.12 | 16% | +0.08 (p 0.3) | 0.061 dex |
| eddy set by the total mass (3.13-3.15) | 17 041 | 0.50 | 42% | +0.42 (p 1e-7) | 0.065 dex |

## Check against Li et al. 2018

The control reproduces their fits: NGC 2841 gives disk and bulge ratios 0.81 and 0.93,
distance 15.6 Mpc, inclination 81.9 degrees and reduced chi-squared 1.52 (theirs: 0.81,
0.93, 15.5, 81.9, 1.515); IC 2574 gives 1.44 (theirs 1.44); DDO 154 gives 3.47 (theirs
3.48). The residual scatter on their selection (153 galaxies, points with velocity
errors under 10%) is 0.057 dex, theirs 0.057.
