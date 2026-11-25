# The settled Ocean's shortfall against the measured expansion

The analysis behind Section 5.1's paragraph "The shape, against the measured distances". It fits the candidate of Section 5.1 directly to measured distances. The settled Ocean holds w = −1 while what is gathered drives enough. Once the drive per volume falls short, it thins. The fit is compared with w = −1 held fixed and with the two-number form w = w0 + wa(1 − a) that DESI uses.

## Model (`model.py`)

- **Holding.** The settled Ocean holds its default energy per volume while the drive meets the need.
- **Drive.** The drive per volume is K times the energy per volume of what is gathered.
- **Need.** Holding the default takes 3(1 + w_u) H ε.
- **After the onset.** dε/d ln a = −3(1 + w_u) ε + K ρ_m/H, never above the default.
- **How it thins.** How the settled Ocean thins where it is not made up is not yet in the law, so two readings are run:
  - w_u = 0: its energy only spreads over the growing volume.
  - w_u = 1: its current thins.
- **The one free number.** K, traded for the redshift at which the shortfall begins.
- **Simplifications.** The Ocean is flat, and radiation is neglected (under 0.1% at z ≤ 2.33).

## Data

**BAO distances.** DESI DR2, Table IV of arXiv:2503.14738, are written into `model.py`. The BGS point is D_V/r_d; the other six tracers give D_M/r_d and D_H/r_d with their correlation. h r_d is left free, so no early-universe input enters.

**Supernovae.** These are not copied here; fetch them with git and run each sample as its own release's likelihood does. Every command below starts in this `expansion` folder, not the repository's root (from the root, `cd expansion` first), and each sample ends with `cd ../..`, which brings you back to it. Type them one per line; they work in PowerShell and a Unix shell alike. The samples land in `expansion/data/`, where `fit.py` looks for them. In every case the absolute brightness is left free and removed analytically.

- **Pantheon+** (Scolnic et al. 2022; Brout et al. 2022):

  ```
  git clone --filter=blob:none --no-checkout --depth 1 https://github.com/PantheonPlusSH0ES/DataRelease data/pantheon
  cd data/pantheon
  git sparse-checkout set --no-cone "Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat" "Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES_STAT+SYS.cov"
  git checkout main
  cd ../..
  ```

  The fit uses m_b_corr with STAT+SYS and zHD > 0.01, which leaves 1,590 supernovae.

- **DES-SN5YR, 2024** (DES Collaboration 2024), tag 1.3:

  ```
  git clone --filter=blob:none --no-checkout --depth 1 --branch 1.3 https://github.com/des-science/DES-SN5YR data/des2024
  cd data/des2024
  git sparse-checkout set --no-cone "4_DISTANCES_COVMAT/DES-SN5YR_HD.csv" "4_DISTANCES_COVMAT/STAT+SYS.txt.gz"
  git checkout 1.3
  cd ../..
  ```

  The fit uses all 1,829 supernovae, with STAT+SYS plus MUERR_FINAL² on the diagonal.

- **DES-Dovekie, 2026** (Popovic et al. 2026), the main branch:

  ```
  git clone --filter=blob:none --no-checkout --depth 1 https://github.com/des-science/DES-SN5YR data/dovekie
  cd data/dovekie
  git sparse-checkout set --no-cone "4_DISTANCES_COVMAT/DES-Dovekie_HD.csv" "4_DISTANCES_COVMAT/STAT+SYS.npz"
  git checkout main
  cd ../..
  ```

  The fit uses all 1,820 supernovae. STAT+SYS.npz holds the inverse covariance, stored as its upper triangle.

Pantheon+ and DES share low-redshift supernovae, so each sample is fitted with DESI separately, never together.

## Running

From inside this `expansion` folder, `python3 fit.py` writes `results.json`; the paper's check reads that file. If any supernova sample has not been fetched, it fits what it has (DESI's distances are built in) and writes `results_partial.json` instead, leaving `results.json` as it was. `python3 figures.py` draws the figures. The data folders can also be set with the environment variables `PANTHEON_DIR`, `DES2024_DIR` and `DOVEKIE_DIR`.

## Result

The shortfall uses one number; the two-number form uses two. Δχ² is measured against w = −1 held fixed. Each range covers the two thinning readings.

| DESI DR2 + | Shortfall Δχ² | Two-number form Δχ² | Onset z | Settled Ocean today |
|---|---|---|---|---|
| Pantheon+ | −3.4 | −4.9 | 0.10–0.14 | 95% of default |
| DES-SN5YR 2024 | −14.0 | −13.7 | 0.16–0.23 | 90% |
| DES-Dovekie 2026 | −7.8 | −7.2 | 0.14–0.19 | 92% |

Fitted to the same data, the two-number form dips to w ≈ −1.02 to −1.22 at z = 1.5. The shortfall never goes below −1.
