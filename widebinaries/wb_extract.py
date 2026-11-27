"""Run on your own computer (needs: pip install astropy numpy).
Reads El-Badry, Rix & Heintz 2021's Gaia eDR3 binary catalogue (zenodo.org/records/4435257, all_columns_catalog.fits.gz,
1.4 GB; you do not need the _shift file) and writes a small CSV of the pairs the wide-binary test needs:
  - both stars within 250 pc (parallax > 4 mas) and parallax measured to better than 1 part in 20 (10 for the pair mean);
  - chance-alignment probability R_chance_align < 0.01;
  - projected separation 200 au to 50,000 au;
  - main-sequence pairs (binary_type 'MSMS') where the column exists.
Usage:  python wb_extract.py all_columns_catalog.fits.gz wb_250pc.csv
Commit the CSV (expected a few tens of MB) to the repository as flows/../widebinaries/wb_250pc.csv (any folder you like)."""
import sys, numpy as np
from astropy.table import Table
src, out = sys.argv[1], sys.argv[2]
t = Table.read(src)
cols = t.colnames
print(len(t), "rows,", len(cols), "columns")
want = []
for base in ("source_id", "ra", "dec", "parallax", "parallax_error", "pmra", "pmra_error", "pmdec", "pmdec_error",
             "pmra_pmdec_corr", "phot_g_mean_mag", "phot_bp_mean_mag", "phot_rp_mean_mag", "bp_rp", "ruwe",
             "radial_velocity", "radial_velocity_error", "l", "b"):
    for s in ("1", "2"):
        if base + s in cols: want.append(base + s)
for c in ("sep", "sep_AU", "R_chance_align", "binary_type", "pairdistance"):
    if c in cols: want.append(c)
missing = [c for c in ("parallax1", "parallax2", "pmra1", "pmra2", "pmdec1", "pmdec2", "phot_g_mean_mag1", "sep_AU", "R_chance_align") if c not in cols]
if missing:
    print("columns not found:", missing); print("available:", cols); sys.exit(1)
k = (t["parallax1"] > 4) & (t["parallax2"] > 4) & (t["R_chance_align"] < 0.01) & (t["sep_AU"] > 200) & (t["sep_AU"] < 50000)
k &= (t["parallax1"] / t["parallax_error1"] > 20) & (t["parallax2"] / t["parallax_error2"] > 10)
if "binary_type" in cols:
    k &= np.array([str(x).strip() == "MSMS" for x in t["binary_type"]])
s = t[k][want]
print(k.sum(), "pairs kept; columns:", want)
s.write(out, format="csv", overwrite=True)
print("written", out)
