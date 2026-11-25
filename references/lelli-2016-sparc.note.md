# Lelli, McGaugh & Schombert 2016 — SPARC

AJ 152, 157 (2016); arXiv:1606.09251. Data tables (Keith supplied, 21 Nov 2026): SPARC_Lelli2016c.mrt (galaxy table) and MassModels_Lelli2016c.mrt (mass models), from the SPARC site (astroweb.case.edu/SPARC).

## Contents
- 175 disk galaxies, S0 to Irr, Spitzer 3.6 μm photometry and HI/Hα rotation curves; 3391 rotation-curve points.
- Galaxy table: Hubble type, distance and error, distance method (1 Hubble flow, 2 TRGB, 3 Cepheids, 4 Ursa Major, 5 supernovae), inclination and error, L[3.6] (10⁹ L☉), effective radius and surface brightness, disk scale length and central surface brightness, M_HI (10⁹ M☉), HI radius, V_flat, quality flag Q (1 high, 2 medium, 3 low), references.
- Mass models: per radius, V_obs and its error (random only; no inclination error), V_gas (includes ×1.33 for helium), V_disk and V_bul at M/L = 1, disk and bulge surface brightness.
- Note: the galaxy table's rows are one byte off its own byte-by-byte description; read by splitting on whitespace.

## Used for
Item 3 (the scale gap), v3.16: claude/sparc/.
