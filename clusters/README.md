# Galaxy clusters (v3.17 working files)

Kill item 1 of 3.17. Working notes: `coma-first-pass.md` (Coma, passes one to seven) and `six-clusters.md` (six clusters run forward).

- `members/`: SDSS SpecPhoto member lists (ra, dec, z, model g r i, Petrosian r). Coma within 105′; A1367, A2199, A2147, A1795, A2029 within about 3 Mpc of the Reiprich & Böhringer 2002 centers, ±3,000 km/s.
- `cluster_budget.py`: runs any cluster forward. `python3 cluster_budget.py <members csv with a cluster label in the first column> [cluster ...]`
- `coma_*.py`: the Coma passes. `coma_sdss.py` needs `members/COMA.csv` and the 2MRS table (VizieR J/ApJS/199/26 table3, not included).
- `mw_edge_2r200.py`: the Milky Way eddy's edge from the escape speed, compared like for like with Deason et al. 2019's 2 r200 boundary.

Reference notes for these are in the claude.ai project under `references/` (stellar-mass-colour-rules, coma-mass-measurements, cluster-gas-parameters, mistele-2024-flat-lensing, deason-2019).
