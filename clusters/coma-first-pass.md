# Galaxy clusters, first pass: Coma (25 Nov 2026)

Kill item 1 of 3.17. Script: `claude/clusters/coma.py` (run `python3 coma.py <2MRS asu.tsv> run`; the 2MRS table is VizieR J/ApJS/199/26 table3, downloaded by Keith, not in the project). Not in the paper.

## Measured side
Hot gas, isothermal beta model, h = 0.7: T = 8.21 keV, beta = 0.705, rc = 275 kpc, n_e0 = 3.64e-3 cm^-3 (Sanders 2003 Table 1, from Reiprich 2001); cross-check Reiprich & Bohringer 2002 Table 4 (T 8.38, beta 0.654, rc 246 kpc): within 5%. Read as hydrostatic balance only (no cosmological model): the turning that holds the gas, g = 3 beta kT r / (mu m_p (r^2 + rc^2)). At 1.45 Mpc it corresponds to 8.9e14 suns, as RB02's M500 (8.6e14). Assumes the gas settled and isothermal; RB02 note isothermal masses may run ~20% high where the temperature falls outward. Lensing not yet used.

Measured turning: 1.33, 1.13, 0.68, 0.49, 0.36 g† at 0.25, 0.5, 1, 1.45, 2 Mpc. Hot gas inside 1 Mpc 5.8e13 suns, 2 Mpc 1.4e14.

## Galaxies
2MRS: 117 galaxies within 3 Mpc (projected, D = 100 Mpc) and 3,000 km/s of Coma's redshift; complete only to M_K = -23.25. K light 1.4e13 Lsun. Stars with M/L_K 0.6-1.0. Galaxies below the limit added with a Schechter K-band function (M* = -24.2, faint slope -1.0 or -1.3); that extrapolation carries 48-86% of the summed eddies, so it is the weakest step. 79% by number and 83% by light are ellipticals and S0s (95% by light inside 0.5 Mpc).

## Results (load inside cylinders, against what the gas balance needs; sphere cut at 3 Mpc)
- Stars and gas alone: about 0.1 of the measured turning.
- One eddy for the whole cluster from its stars and gas (Eq. 15): 0.34-0.71 of the measured turning (0.25 to 2 Mpc), short most in the core: the modified-dynamics shortfall, reproduced.
- One eddy from the stars only (gas begins none): 0.20-0.34.
- Each galaxy's own settled eddy (Eq. 15, stars as a point, edge 100 or 230 kpc, fixed or scaled with the eddy's speed as the Milky Way's), loads summed with gas and stars: 0.20 to 1.0 of what the gas balance needs, depending on the edge, M/L and the faint slope; the ratio is nearly flat from 0.5 to 2 Mpc in every case, so the summed eddies follow the measured profile in shape. Only the largest edges with many faint galaxies reach the full amount.

## What decides it
1. Whether ellipticals and S0s, which barely rotate, have eddies (Keith's "rotating bound matter"). If only ordered rotation begins eddies, Coma, 80%+ early types, has almost none, and the item fails here.
2. The edge of an eddy in a cluster, where neighbors sit inside each other's edges.
3. Galaxies fainter than 2MRS: a deeper member catalog (SDSS spectroscopy reaches several magnitudes fainter) replaces the extrapolation.
4. Lensing (Coma weak lensing) as the independent measure, with distances from the paper's own expansion fit.

## Second pass (25 Nov, 18:23, Keith: "it has to be everything together ... you have not counted the gas surrounding an eddy as part of its pattern?")
Each galaxy's eddy now answers to everything inside it: its stars and the hot gas around it (Eq. 15 with M(<r) stars plus gas). Scripts `claude/clusters/coma_gas.py` and `coma_gas2.py`. Gas counted two ways: shared out (each parcel to the nearest galaxy whose edge reaches it) and counted by every eddy it lies in (an upper bound); the two differ little for the 117 visible galaxies. Galaxies placed in depth as the gas is (only their projected positions are measured). Share of the turning the gas balance needs, at 0.5, 1, 1.5, 2 Mpc (M/L 0.8):

| edge | 117 visible, stars only | 117 visible, with gas | + fainter galaxies to M_K -19, slope -1.0 (about 700) | slope -1.3 (about 1,600) |
|---|---|---|---|---|
| 100 kpc | 0.16-0.17 | 0.18-0.19 | 0.34-0.39 | 0.54-0.64 |
| 150 kpc | 0.19 | 0.23-0.28 | 0.60-0.76 | 0.97-1.10 |
| 230 kpc | 0.23-0.24 | 0.36-0.48 | 1.13-1.29 | 1.89-1.94 |

Reading: the gas around the eddies counts only once many eddies share it. An eddy's turning grows as the square root of what it holds, so the same gas shared among more eddies gives more in total; one eddy holding all of it is the modified-dynamics case (0.34-0.71). With Coma's whole population each holding its share, the measured amount is reached for edges of about 150 to 230 kpc. The shape stays right (the ratio nearly flat with radius). Not settled: the total keeps growing as fainter galaxies are added unless smaller galaxies have smaller edges, so the edge rule (the edge of an eddy whose holdings are mostly the cluster's gas, among neighbors) decides the amount; and a measured member list fainter than 2MRS should replace the drawn galaxies.

## Correction and third pass (25 Nov, 18:25–18:27)
Correction (18:25, Keith: "I just want to be sure you are calculting alll of this based on the Ocean's builds and not some other system?"): the second pass added eddies' loads where eddies overlap, which is how masses combine in Newton's and Einstein's gravity, not a rule of the builds; its "share the gas among many eddies" gain came from that overlap. The one-eddy result and the shape did not depend on it.

Keith, 18:27: "The eddy, aside from anything else, is a spinning pattern being rebuilt." Read as: each eddy is its own pattern, rebuilt with its own energy at its own places, so no place carries two eddies; distinct patterns' loads count each once, as stars' do. Third pass (`claude/clusters/coma_cells.py`): each galaxy's eddy fills the region nearer to it than to any other galaxy (its cell), out to at most the isolated edge; it holds the stars and gas in its cell; its load is Eq. (15) at the cell's size. Eddy sizes inside 1 Mpc come out 110 to 220 kpc (median). Share of the turning the gas needs, at 0.5, 1, 1.5, 2 Mpc (M/L 0.8):

| isolated edge | 117 visible | + faint to M_K -19 (slope -1.0 / -1.3) | + faint to M_K -17 (slope -1.0 / -1.3) |
|---|---|---|---|
| 150 kpc | 0.22-0.27 | 0.55-0.63 / 0.84-0.91 | 0.67-0.73 / 1.03-1.29 |
| 230 kpc | 0.34-0.45 | 0.83-0.96 / 1.02-1.41 | 0.92-1.16 / 1.18-1.92 |

With eddies as separate patterns, Coma's full population reaches about 0.6 to 1.9 of the measured turning, most cases near one; the visible 117 alone give a quarter to a half. Remaining non-Ocean inputs: stars' mass for their light (stellar population models), the faint galaxies drawn from the luminosity function (to be replaced by measured members), galaxy depths placed as the gas, the isothermal gas fit. Ocean question still open: whether eddies as patterns can overlap at all, and what an eddy's edge is among neighbors (here: its cell).

## Fourth pass: Coma's measured members (25 Nov, 18:45)
Keith downloaded the SDSS spectroscopic galaxies within 105 arcmin of Coma's center with 0.013 < z < 0.033 (SkyServer SpecPhoto: ra, dec, z, modelMag g r i, petroMag r; 812 rows, three with broken photometry dropped, 808 used; complete to about r 17.8, M_r about -17.2), plus the 7 2MRS members with no SDSS match. Script `claude/clusters/coma_sdss.py` (the CSV is not in the project; rerun the query to get it). These replace the drawn galaxies. Stars' mass from g-i colour and i light by two standard rules (Bell et al. 2003; Taylor et al. 2011), written from recollection, not yet read; both give 4.6 to 9 x 10^12 suns of stars inside 1 Mpc. Each eddy its own pattern, filling the region nearer its galaxy than any other, capped at the isolated edge, holding the stars and gas there.

Share of the turning the hot gas needs, at 0.5, 1, 1.5, 2 Mpc:
- cap 150 kpc: 0.54-0.70 (core eddies about 135 kpc)
- cap 230 kpc: 0.88-0.97 (core eddies about 172 kpc)
The rule for the stars' mass barely matters: the eddies' holdings are mostly the hot gas. Still missing: galaxies fainter than SDSS's spectroscopic limit (a small addition, since the total grows slowly with more, smaller cells); the isothermal gas fit may overstate what is needed by up to about 20% where the gas cools outward (Reiprich & Bohringer 2002); lensing not yet used.

## Fifth pass (25 Nov, 18:56 onward): the Bullet Cluster, the Milky Way's edge, and the edge in Coma
**Bullet Cluster** (Clowe et al. 2006 Table 2, read 25 Nov; 100 kpc apertures; their plasma and stellar masses; kappa converted with their distances, sources at z 0.8 to 1.3): lensing at the main cluster's BCG 29-36 x 10^12 suns against 6.0 of plasma and stars (5 to 6 times); at the subcluster's BCG 16-20 against 3.3 (5 to 6 times); at the plasma peaks the residual is 0.3-0.7 of the plasma alone (residuals after subtracting the BCG-centred profiles), so nothing beyond the gas there. Clowe et al. also report that the peaks' absolute levels match clusters of the same temperature whose gas and galaxies coincide. In the paper's terms (eddies keep themselves going once set, energy handed forward, eddies go on with their bound matter, §6 and §12.1): eddies set before the collision went on with the galaxies and kept their strength, so the lensing at the galaxies stays at the level of an undisturbed cluster. That is the measurement. The amount is then the same question as Coma's: whether a cluster's eddies give an undisturbed cluster's turning.

**The Milky Way's edge with the real Milky Way** (`claude/clusters/mw_edge.py`): §6's method (turning of stars, gas and eddy out to the edge; beyond it everything inside as one mass; escape speed 528 +24/-25 km/s at the Sun, Deason et al. 2019) with the real Milky Way's fitted stars and gas (6.7-6.8 x 10^10 suns, g† 1.19-1.22) puts the edge at 100 kpc (70 to 150 within the measurement), not the 100 to 230 kpc the model Milky Way gives (§6 and Appendix B state it for the model, so they are not wrong as written; the real Milky Way's value is the better one to carry).

**Coma with that edge** (measured members, eddies as separate patterns, each capped at the isolated edge): cap 70 kpc 0.22-0.29; 100 kpc 0.33-0.44; 150 kpc 0.54-0.70. With no cap, each eddy filling the whole region out to its neighbours (core eddies about 185 kpc): 1.15-1.83, rising outward. So the result turns on what bounds an eddy inside a cluster: its isolated edge, where it meets settled Ocean (then Coma is short by about 2.5 times, as the modified-dynamics case), or its neighbours, with no settled Ocean between eddies (then enough, or more in the outskirts).

**Correction to the fifth pass (25 Nov, 19:35–19:52).** The Milky Way's "100 kpc edge" compared Deason's escape speed with escape to infinity. Deason define it as the speed to reach 2 r200, about 380–450 kpc, a boundary chosen from standard-account simulations. Compared like for like (`claude/clusters/mw_edge_2r200.py`), the edge is at least about 90 kpc and the escape speed sets no upper bound. Stacked lensing of isolated galaxies (`claude/lensing/edge-fit-results.md`) needs no edge out to 1 Mpc; the 95% lower limits are about 0.2–0.8 Mpc. The "short by 2.5 times" reading above is withdrawn.

## Sixth pass (25 Nov, 19:59–20:02): Coma run forward, nothing set from Coma
Keith, 19:59: "Why is probably the build. Just building because you can doesn't make any sense." An eddy does not spread into room because the room is there. It carries what it was given at its setting, plus what rivers and collisions delivered, and its reach follows: R ≈ G·(load)/V². Script: `claude/clusters/coma_budget.py`; output `coma_budget.out`.

**Method.**
- Each Coma galaxy's eddy carries the load an isolated galaxy with the same stars carries, read from stacked lensing: Eq. (15) out to the isolated reach R_iso, which lensing puts at 0.5–1 Mpc or more.
- A mass factor f covers the isolated galaxy's own gas and the lensing excess. Lensing needs f = 1.0 for spirals and 1.3–1.8 for ellipticals.
- In Coma the eddy holds only its own region and takes in the hot gas there. Its reach is where its load reaches that amount. If its region cannot hold the amount, it fills the region.
- Nothing is set from Coma.

**Share of the turning the hot gas needs** (cylinders 0.5, 1, 1.5, 2 Mpc):

| Stars' mass | f | R_iso 500 kpc | 700 kpc | 1000 kpc |
|---|---|---|---|---|
| Bell | 1.0 | 0.73–0.78 | 0.83–0.95 | 0.95–1.14 |
| Bell | 1.5 | 0.80–0.89 | 0.90–1.05 | 1.01–1.27 |
| Taylor | 1.0 | 0.58–0.60 | 0.69–0.75 | 0.80–0.92 |
| Taylor | 1.5 | 0.65–0.69 | 0.78–0.85 | 0.85–1.03 |

**Reach in Coma.** Median 117–172 kpc inside 1 Mpc and 170–260 kpc outside. Between 10% and 46% of eddies fill their whole region before carrying the full amount.

**Reading.**
- With the eddy's load carried over from measured isolated galaxies, Coma comes out at 0.6–1.3 of the turning its hot gas needs. The measured amount lies inside the range the inputs allow.
- The shape is nearly flat from 0.5 to 2 Mpc.
- The central case: Bell masses, which sit nearest the lensing paper's mass scale for ellipticals (their ETG masses are Brouwer's ×1.4); f = 1.5; R_iso = 700 kpc. It gives 0.90–1.05.
- The spread comes from the inputs: the stars' mass rule (about a factor of two), the isolated reach (lensing gives only a lower bound), and f.

**Assumptions and borrowed steps.**
- Coma's galaxies carry what isolated galaxies of the same stars carry. In Keith's picture, history could raise or lower that.
- Stars' mass rules from population models (Bell, Taylor), written from recollection and not yet read.
- The isothermal gas fit may overstate what is needed by up to about 20%.
- Galaxy depths are placed as the gas is.
- Lensing distances and masses (see the note).

## Seventh pass (25 Nov, 20:09 onward, Keith: "Let's make it so"): the checks
**1. Stars' mass rules read** (`references/stellar-mass-colour-rules.note.md`).
- Both coefficients were right. One fix: Bell's solar i magnitude is 4.56, not 4.53 (0.012 dex).
- Bell (diet Salpeter) sits about 0.31 dex above Taylor (Chabrier) at g − i = 1.2.
- The lensing paper's mass scale for ellipticals is close to Taylor ×1.4. That is the consistent choice for clusters.
- Rerun with Taylor ×1.4, f 1.5, R_iso 700 kpc, SDSS members only (`cluster_budget.py`): 0.81–0.95. Bell gives 0.92–1.09. R_iso 1000 kpc gives 0.94–1.14 (Taylor ×1.4) and 1.01–1.28 (Bell).

**2. Coma without the isothermal assumption** (`coma_need_planck.py`; `references/coma-mass-measurements.note.md`).
- Method: hydrostatic balance with Planck's measured SZ pressure (Model C) and the X-ray density.
- The needed turning comes out at 0.69–0.92 of the isothermal value inside 1 Mpc, 0.75 at 1.5 Mpc and 0.62 at 2 Mpc. In cylinders, isothermal needs divided by SZ needs are 1.17, 1.35, 1.63 and 1.91 at 0.5, 1, 1.5 and 2 Mpc.
- Hydrostatic masses in merging outskirts are themselves doubtful (Planck shocks; Okabe 2014 finds hydrostatic/lensing about 0.4 at the virial radius). So a third measure decides the outskirts: the galaxies' motions.

**3D enclosed load (10¹⁴ M☉)** (`coma_compare3d.py`):

| r (Mpc) | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 | 2.9 |
|---|---|---|---|---|---|---|
| hot gas, isothermal | 2.43 | 5.89 | 9.20 | 12.44 | 15.65 | 18.22 |
| hot gas, Planck SZ pressure | 2.25 | 5.38 | 6.91 | 7.68 | 8.11 | 8.34 |
| galaxy motions (Łokas & Mamon) | | | | | | 14.0 ± 4.2 |
| eddies, Taylor ×1.4, f 1.0, R_iso 700 | 1.40 | 4.23 | 7.33 | 10.22 | 13.12 | 15.93 |
| eddies, Taylor ×1.4, f 1.5, R_iso 700 | 1.48 | 4.29 | 7.39 | 11.14 | 14.66 | 17.70 |
| eddies, Taylor ×1.4, f 1.5, R_iso 1000 | 1.61 | 4.95 | 8.85 | 13.69 | 18.01 | 21.62 |
| eddies, Bell, f 1.0, R_iso 700 | 1.43 | 4.54 | 7.88 | 11.59 | 14.97 | 18.01 |
| eddies, Bell, f 1.5, R_iso 700 | 1.64 | 5.03 | 8.63 | 12.42 | 16.73 | 20.14 |
| eddies, Bell, f 1.5, R_iso 1000 | 1.69 | 5.55 | 9.64 | 14.43 | 19.53 | 23.95 |

Reading:
- **At 2.9 Mpc** the eddies give 16–24 against galaxy motions' 14 ± 4. The central cases (Taylor ×1.4, R_iso 700) give 16–18, within 1σ.
- **Within 1 Mpc** the eddies give 4.2–5.6 against the gas's 5.4–5.9.
- **Inside 0.5 Mpc** the eddies give 1.4–1.7 against 2.25–2.43. The core is short by about a third in 3D. The cylinders hid this, because they add in material from the outskirts.
- Possible causes of the core shortfall, not yet separated:
  - galaxies' depths placed as the gas, which spreads them more than the real core;
  - galaxies below SDSS's limit;
  - core eddies that fill their whole regions.
- **Faint-limit test** (Coma cut to brighter members): M_r < −19.1 lowers the cylinder shares by about 5%, −19.7 by about 12%, −20.3 by about 30%.

**3. Coma lensing** (Kubo 2007; Gavazzi 2009; note above). Both measurements are low signal-to-noise and NFW-fitted (a borrowed shape).
- Gavazzi: M200c = 5.1 (+4.3/−2.1) × 10¹⁴ inside 1.8 Mpc, or 9.7 (+6.1/−3.5) inside 2.2 Mpc with the prior.
- Kubo: 2.7 (+3.6/−1.9) × 10¹⁵ inside about 2.8 Mpc.
- The eddies give about 9–12 at 1.8 Mpc, 12–17 at 2.2 Mpc and 16–23 at 2.8 Mpc. Within 1σ of each, at Gavazzi's no-prior upper edge.
- Not a sharp test. A measured shear profile, not an NFW mass, would be the Ocean-proper comparison.

**4. Bullet Cluster, rough** (Clowe Table 2).
- Method: the aperture's own stars treated as one galaxy (this gives the smallest eddy load for the stars, since load grows as the square root of mass), carrying the isolated amount (f 1.5, R_iso 700) and reaching 150–250 kpc.
- Main BCG: 18–25 × 10¹² with plasma and stars, against lensing 29–36 (0.5–0.85). Sub BCG: 15–23 against 16–20.
- Not counted: other galaxies' eddies seen through the aperture, which would add.
- The stars' M/L_I uncertainty (0.5–3) moves the eddy part by about ×0.5 to ×1.2.
- A forward run needs a member catalog with photometry. The Bullet is not in SDSS.

**5. More clusters.** `cluster_budget.py` is ready, with gas from Chen et al. 2007 (`references/cluster-gas-parameters.note.md`). It waits for Keith's SDSS query for A1367, A2199, A2147, A1795 and A2029. A1795 and A2029 reach only M_r ≈ −19.1 and −19.7, so expect them about 5–12% low on that count alone.
