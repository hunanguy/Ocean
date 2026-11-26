# Six clusters run forward (25 Nov 2026, 20:29)

**Script:** `claude/clusters/cluster_budget.py`.
**Members:** SDSS spectroscopic galaxies, downloaded by Keith: Keith's five SDSS CSVs (not stored in the project, which is at its size limit; rerun the single-cluster queries to get them); Coma from `coma_sdss.csv`.
**Gas:** `references/cluster-gas-parameters.note.md`.
**Outputs:** `five.out`, `five_a2147cut.out`.

**Method.** The same as Coma's sixth pass, with nothing set from any cluster:
- Each member galaxy's eddy carries the load an isolated galaxy with the same stars carries (from stacked lensing).
- In the cluster, the eddy holds its own region and takes in the hot gas there until its load reaches that amount.
- The result is the share of the turning the hot gas needs (isothermal β model) inside cylinders of 0.5, 1, 1.5 and 2 Mpc.

**Central case:** stars Taylor ×1.4, f 1.5, R_iso 700 kpc.

| Cluster | T (keV) | Members (faintest M_r) | Central case | Full range of cases | Median reach |
|---|---|---|---|---|---|
| Coma | 8.2 | 808 (−17.1) | 0.81–0.95 | 0.78–1.28 | 186 kpc |
| A1367 | 3.6 | 359 (−16.9) | 1.03–1.13 | 0.85–1.51 | 211 kpc |
| A2199 | 4.1 | 459 (−17.7) | 0.82–1.25 | 0.76–1.74 | 245 kpc |
| A1795 | 6.0 | 155 (−18.8) | 0.53–0.76 | 0.46–1.15 | 294 kpc |
| A2029 | 8.7 | 216 (−19.5) | 0.57–0.82 | 0.50–1.19 | 296 kpc |
| A2147 | 4.9 | 578 (−17.8) | 1.20–2.09 | 1.07–2.94 | 226 kpc |
| A2147, background group removed | | 406 | 1.10–1.85 | 0.88–2.63 | 231 kpc |

**Reading.**
- **Coma, A1367 and A2199:** near the measured amount (0.8–1.25 in the central case). The measured amount is inside each one's range.
- **A1795 and A2029** come out low: 0.53–0.82 in the central case. They reach 1 only for isolated reaches of 1 Mpc. Both are distant, so their member lists stop at M_r about −18.8 and −19.5. Cutting Coma the same way lowered it by about 5–12%, so allowing for that they would be about 0.6–0.9. Both are cool-core clusters fitted by single β models with small cores, and both are among the hottest of the six. Whether the eddies fall short in the most massive clusters, or the fits and member depth cause it, is open.
- **A2147** overshoots, rising outward to about 2. Two causes, both on the measured side:
  - A background group (the A2152 region of the Hercules supercluster, median z 0.043) lies inside the circle. Removing galaxies above z 0.0395 lowers the result only modestly.
  - Its gas fit (β 0.444) extrapolated to 3 Mpc gives 2.5 × 10¹⁴ suns of gas against a need of 5.8 × 10¹⁴ inside 2 Mpc: a gas share of about 0.43. The others run about 0.14–0.28. So the shallow single-β fit far outside where ROSAT measured is the likely cause.
  - A2147 is not a fair test as fitted.
- **Shape:** flat with radius in Coma and A1367. Rising outward in A2199, A1795 and A2029 (central cases rise by about 0.25–0.45 from 0.5 to 2 Mpc). Single-β cool-core fits with small cores make the needed turning fall off fast outside the core. Measured temperature profiles would test this.

**Borrowed steps:**
- isothermal single-β gas fits (cool cores fit better with double-β models);
- stars' mass from population models;
- distances cz/H0 with H0 = 70, and no k-corrections;
- galaxies' depths placed as the gas;
- the SDSS spectroscopic limit;
- the isolated load from stacked lensing.
