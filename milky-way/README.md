# milky-way/: the vertical test on the real Milky Way

The analysis behind Section 6's statement that, fitted to the Milky Way's measured stars and gas, rotation curve and vertical motions, the eddy does about as well as a halo of cold dark matter (and better on Bovy & Rix's vertical force), while a contribution parallel to the baryons' own turning does not. It repeats the fit of Lisanti et al. 2023 (arXiv:1911.12365) for three accounts on the same footing.

| File | Contents |
|---|---|
| `mw_data.py` | The published data, with sources: the rotation curve (Eilers et al. 2019, Table 1, 26 points 5–18 kpc), the vertical force at 1.1 kpc from 43 star populations (Bovy & Rix 2013, Table 3), and the stars-and-gas constraints Lisanti et al. use. |
| `fig_a1.json` | The 53 vertical data points of Lisanti et al. 2023, Fig. A1 (Zhang et al. 2013's three K-dwarf populations: ln n and σ_z at 0.35–1.15 kpc), read from the PDF's vector drawing. |
| `fig_a1_extract.py` | The script that read them: `python3 fig_a1_extract.py 1911.12365v2.pdf > fig_a1.json` (the PDF from arXiv; needs `pdfplumber`). |
| `mw_fit.py` | Stars and gas as Lisanti et al. (Hernquist bulge, double-exponential stellar and gas disks, exact disk forces), the three accounts (cold dark matter, the parallel contribution, the eddy of Eq. 15), and the fit with Bovy & Rix's vertical data. |
| `mw_fit_zhang.py` | The same fit with Lisanti et al.'s own vertical data, through their Eq. (11). |
| `best_fits.json` | The best-fit parameters of both fits, written by the two scripts above. |
| `mw_report.py` | χ² and the turning at the Sun for the saved fits (seconds). |
| `mw_figure.py` | The paper's figure, `figures/fig_milky_way.pdf` (needs `matplotlib`). |
| `mw_plot.py`, `mw_plot_zhang.py` | Working figures (need `matplotlib`). |

Run from inside this folder. `python3 mw_report.py` reads the saved fits. To refit (numpy and scipy; about 10 minutes for `mw_fit.py`, 30–40 for `mw_fit_zhang.py` per account): `python3 mw_fit.py cdm parallel eddy eddy_fixed`, then `python3 mw_fit_zhang.py cdm parallel eddy eddy_fixed`.

Results (χ², with free parameters), with the eddy of Section 6 (Equation 15: at each radius it answers to the galaxy's own turning averaged over the sphere, and is built from the Ocean the galaxy's own loans leave free; `DEFAULT_FORM = "loans"` in `mw_fit.py`): on Lisanti et al.'s data, cold dark matter 83.0 (15), the parallel contribution 124.5 (13), the eddy 85.1 (13; g† 1.22, bulge 1.3 × 10¹⁰ M☉), the eddy with g† held at 1.20, 85.2 (12); Lisanti et al. found 77 for cold dark matter and 144 for superfluid dark matter. On Bovy & Rix's vertical force: 85.9 (9), 145.4 (7), 77.8 (7), 77.9 (6). The check suite (`checks/check_ocean_math.py`) recomputes these from `best_fits.json`. The form of versions 3.13–3.15, set by the total mass alone, runs with `EDDY_FORM=cored` (Lisanti et al.'s data 87.9, Bovy & Rix 85.3); other forms are comparisons.
