# Ocean

**Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium — A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology**

A theoretical proposal built on one premise: there is no empty space. The vacuum is a single continuous medium, called here the Ocean, with no edges and no outside. What we call matter is the Ocean's own energy gathered and circulating in place; light is a ripple in the same medium; and gravity is proposed to be the medium's response to concentrated energy. The Ocean has one speed, at which every disturbance travels. It rebuilds every pattern continuously, and gravity is the uneven making of time by that rebuild, slower where there is more to rebuild. No speed is fixed: the measured speed of light is that local speed as read by rulers and clocks made of the same Ocean. Einstein's equations are kept as the correct description of that response, with the Ocean offered as the reason they hold.

From that premise the paper asks whether dark matter and dark energy are two substances or two behaviors of one medium. Standard cosmology accounts for roughly ninety-five percent of the contents of the observable universe with two quantities that fit the data without being derived from anything. This document asks whether both might have a common origin in the dynamics of the Ocean.

**This is a proposal, not an established theory.** The paper states its own falsification conditions explicitly and carries an itemized research program, several items of which could terminate the framework outright.

---

## Contents

| File | Description |
|---|---|
| `Ocean_Scalar_Tensor_Hydrodynamics_v3_16.pdf` | The paper. 90 pages, including a non-technical preface, a glossary, Appendices A, B and C and a bibliography. Document digest `8563-1f7b-50ca`. |
| `Ocean_Appendix_A_Spinning_Black_Hole_v3_16.pdf` | Appendix A on its own: the rebuild of a spinning black hole (Sagittarius A*), 5 pages. Built from the same text as the paper's Appendix A, and carrying that part's token, `3cc643`. |
| `Ocean_Scalar_Tensor_Hydrodynamics_v3_16.manifest.txt` | The reading manifest, written by the build: every part of the paper with its checksum token and the document digest. |
| `build_ocean_formalism.py` | Generates the LaTeX source of the paper and of the standalone Appendix A, and compiles both. The source of truth. |
| `.zenodo.json` | Deposit metadata consumed by the Zenodo–GitHub integration. |
| `CITATION.cff` | Citation metadata for GitHub's *Cite this repository* widget. |
| `checks/` | `check_ocean_math.py`, a consistency and accuracy check of the paper's mathematics, with three helper modules it imports (run it from inside `checks/`), and `report.md`, its report on this release. |
| `sparc/` | The eddy fitted to 153 real galaxies one by one (SPARC), with the data tables, the fits, the results the paper and the checks read, and the scripts that draw Figures 1 and 2. See `sparc/README.md`. |
| `milky-way/` | The eddy fitted to the real Milky Way's stars and gas, rotation curve and vertical motions, on the same footing as cold dark matter and a contribution parallel to the baryons' own turning; draws Figure 3. See `milky-way/README.md`. |
| `expansion/` | The settled Ocean's slow thinning fitted to DESI's second-release distances and three supernova samples. The supernova data are fetched with git, as its README says. See `expansion/README.md`. |
| `validation-3.16.md` | The independent reading of 3.16 before release (Fable 5.1): every number recomputed from the PDF alone, and how each finding was handled. |
| `references/` | Verification notes, one per paper read: what each cited source supports, and where the paper's wording was corrected against it. Full texts are not stored. |

The `.tex` files are **generated**, not stored. They are produced by the build script and excluded by `.gitignore` to keep diffs meaningful. If you would rather ship the LaTeX source in the archive, remove the first non-comment line of `.gitignore` and commit it.

## Building

Requires Python 3.8+ and `pdflatex` on `PATH` (TeX Live or MiKTeX), with the `pgf` package (TikZ) for Figure 4. Figures 1 to 3 are read from `sparc/figures/` and `milky-way/figures/`, so build from the repository's root folder.

```bash
python3 build_ocean_formalism.py                 # writes the paper and the standalone Appendix A (.tex and .pdf)
python3 build_ocean_formalism.py --outdir build  # write elsewhere
python3 build_ocean_formalism.py --no-pdf        # emit the paper's .tex only
python3 build_ocean_formalism.py --keep-aux      # retain .aux/.log for debugging
```

The script runs `pdflatex` three times so that cross-references and page breaks settle. It then writes the standalone Appendix A from the same text as the paper's appendix, filling in its section and equation numbers from the compiled paper, and compiles it.

### Font dependency

The preamble uses `mathptmx` (Times) rather than `lmodern`, because `lmodern` is absent from some minimal TeX Live installations and its absence triggers a Type 3 bitmap fallback. A consequence is that `mathptmx` leaves `\hbar` undefined, so the preamble restores it explicitly:

```latex
\DeclareRobustCommand{\hbar}{{\mathchar'26\mkern-9mu h}}
```

On a full TeX Live installation you can substitute `newtxtext`/`newtxmath` and remove that line.

## Reading completeness

Every part of the paper carries a checksum token: the first six hex digits of the SHA-256 of its LaTeX source. Each page footer gives the page, the page count and the part with its token; each part ends with a line giving its token; and the last page is a reading manifest listing every part, its first page and its token, followed by a document digest and the words "End of document". The standalone Appendix A carries the token of the paper's Appendix A part in its footers, title block and closing line, since it is built from the same text. A reader, human or automated, has read the whole paper when it reaches that line, and a summary or review that cannot give the digest was made from an incomplete reading. The digest for 3.16 is `8563-1f7b-50ca`. It is also written to the PDF's subject metadata and to the `.manifest.txt` file.

## Checking the mathematics

```bash
cd checks
python3 check_ocean_math.py --build ../build_ocean_formalism.py --report report.md
```

Requires `numpy` and `scipy`. The script re-derives the paper's equations numerically (equations of motion from the action, the disturbance equation from the expanded Lagrangian, the strong-field geometry), recomputes its numerical statements from CODATA 2018 constants, re-runs the frame-dragging simulations, reads the results of the three analyses (`sparc/results/`, `milky-way/best_fits.json`, `expansion/results.json`) and checks the paper's numbers against them, and checks references, citations and symbols for consistency. Each check is tied to a phrase of the paper's own LaTeX, so a change of wording or number that the check no longer matches makes it fail rather than pass silently. Outcomes are PASS, NOTE (agrees with a caveat, or cannot be decided from the text) and FAIL; the script exits with status 1 on any failure. For 3.16: 109 checks, 108 pass, 1 note, 0 fail.

## Running the analyses

Each folder has a README with its data, its method and its results, and each runs from inside its own folder. The commands below are one per line, so they work in PowerShell, the Windows command prompt and a Unix shell; on Windows, `python` or `py` may stand in for `python3`. They need `numpy`, `scipy` and, for the figures, `matplotlib`; fetching the data needs `git`.

### 1. Download the supernova data first

The SPARC tables (`sparc/data/`) and the Milky Way data (`milky-way/`) are in the repository. The three supernova samples the expansion fit uses are not: download them before running it, by following the steps in [`expansion/README.md`](expansion/README.md) (section "Data"). They go into `expansion/data/`, which git ignores, about 90 MB in all. Without them `expansion/fit.py` fits DESI's distances alone and writes `results_partial.json`, leaving `results.json` (the published results, which the math check reads) as it is.

### 2. Run them

From the repository's root folder:

```bash
cd sparc
python3 sparc_fit.py          # a few minutes; uses every processor core; rewrites results/profiles.npz
python3 sparc_report.py
python3 sparc_pushback.py
cd ..

cd milky-way
python3 mw_report.py          # reads the saved fits in seconds; refitting takes longer (see its README)
cd ..

cd expansion
python3 fit.py                # after step 1
cd ..
```

Then rerun the math check (above) to confirm the paper's numbers against your results.

## Structure of the paper

1. **Preface** — non-technical, after a reader's note on how to confirm a complete reading. The premise (no empty space; an Ocean without edges or outside; one speed for every disturbance, and no fixed speed; gravity as the medium's response), the motivating problem, where the standard account's numbers come from, the General Relativity / quantum field theory disagreement over the vacuum, what a medium can do, black holes, the revisions the framework has undergone, and what would end the framework as written.
2. **Conventions and glossary** — fixed meanings for the Ocean, its amount and phase, the settled Ocean, flow, travel, the carrying speed, light, the gas of light and the normal fluid, matter, energy, the rebuild with building and reclaiming, the books, the joining field, the plexus, the dynamo, the Ocean's capacity and grip, the flow's energy, gravity, the load, the Ocean's rivers, the eddy and the pushback; then the Heartbeat, a beat and the observable universe. A key gives the status tags used in the body.
3. **§1–§4** — the field equation and its status as the effective description of the medium; tensor definitions, including the complex field Φ = ρe^{iθ} with the re-made state, the viscous stress (kept, but carrying nothing in the settled Ocean) and the refractive account of gravity; the equations of motion; the Ocean interpretation.
4. **§5** — the Heartbeat cosmology. Within the present beat: expansion as divergence rather than transport; the settled Ocean holding the expansion steady while what is gathered drives its flow, and thinning once that drive falls short, fitted directly to the measured distances (DESI's second release with Pantheon+, DES-SN5YR and DES-Dovekie) and about as good as DESI's own two-number formula with one number fewer and no crossing of w = −1; the microwave background as the light of the first builds' pairs, set free once the expansion had cooled it to about 3000 K. Across beats: at a beat's end the reclaiming carries the Ocean; between beats it is first a gas of light and then a normal fluid, the same everywhere; the build makes the Ocean out of the normal fluid nearly all at once.
5. **§6** — galactic dynamics. A galaxy and its eddy are one region of the Ocean; the eddy acts through the load the build carries in it. At each distance the eddy answers to the galaxy's own turning there and is built only from the Ocean the galaxy's own loans leave free, with one limit for every galaxy (Eq. 15). Fitted to 153 SPARC galaxies one by one, it does nearly as well as the measured radial acceleration relation (Figures 1 and 2). Fitted to the real Milky Way's stars and gas, rotation curve and vertical motions, on the same data and in the same way as the test that ruled out superfluid dark matter, it does as well as the standard dark-matter account (Figure 3). The limit belongs to the loans and does not follow the expansion; the eddy's beginning (one of the Ocean's rivers), its edge and its center. The Hubble constant here comes only from its direct measurements.
6. **§7** — matter and its threshold. The partition is by kind of wave: a kind with a lowest energy can be held in place as matter, a kind without one cannot. The electron's 0.511 MeV is the lowest energy of its own kind of wave, set by the field the dynamo sustains.
7. **§8–§9** — limiting regimes; black holes (no accumulation, stripping as the no-hair theorem, Hawking radiation, recycling rather than draining) and a traveler falling in, also in the rebuild's terms; conservation conditions, nothing is destroyed, and where a wave's energy goes.
8. **§10** — relation to existing work: what is inherited and what is not, and the known deficiencies against current practice and measurement.
9. **§11** — one speed and the split, with Figure 4, how a pattern's one speed is shared between its travel and its own rhythm; the first-order law, which one speed and preservation fix uniquely; the current through time; the strong field and the point of no return; frame dragging; beyond first order, rulers that stretch by direction, so a spinning hole's outside is General Relativity's; travel below the one speed leaves no wake; the edge, the inside and the core, where the Ocean's grip stops a collapse and turns it.
10. **§12** — the rebuild and the law: building and reclaiming, time made in the build, the rebuild of the Earth, antimatter as the reclaiming, the beat's turn, what a build knows, the law and its rules, the phase in the build's terms, the strength of gravity from a count of the kinds of wave, the family the rebuild allows, and the plexus law with its seven tests.
11. **§13–§16** — §13, everything open in one list: what would kill it first (§13.1), then everything else (§13.2); §14, the research program; §15, the predictions, each with its test, what settles it and what would show it wrong; §16, a summary.
12. **Appendix A** — the rebuild of a spinning black hole: Sagittarius A* taken through the same steps as the Earth's rebuild, a table comparing the two regimes, and what the account settles and leaves open. Also issued as a standalone PDF.
13. **Appendix B** — the rebuild of the Milky Way's eddy, which carries the Earth and holds the black hole at its center, with a table comparing the Earth, Sagittarius A* and the eddy.
14. **Appendix C** — the rebuild across a change of beat: the end of a beat, the bottom, the turn and the beginning of the next, step by step, with what it settles and what it leaves open.

## Known open problems

Stated in the paper (§13), repeated here so that they are visible before reading.

**What would kill it** (§13.1), in the order they are being worked, the likeliest to end the framework first:

- **Galaxy clusters.** Whether the Ocean gives clusters the turning their hot gas and their bending of light show, colliding clusters included. Whether a cluster has an eddy per galaxy, one of its own, or both is not worked out, and decides the outcome.
- **The acoustic peaks.** How much the departures from the settled Ocean carry. The peaks come out as in the standard account if they carry what its cold dark matter carries, about 5.4 times the energy of ordinary matter; that must be derived from the first builds, and the spectrum and the sound horizon computed with the Ocean's own content.
- **The scale gap.** How much Ocean can be lent at a place, set by the flow's energy through the plexus, which sets the limit g† ≈ 1.2 × 10⁻¹⁰ m s⁻²; how the Ocean's law makes and holds an eddy, and what sets its size.
- **The strength of gravity.** The count's order-one factors; whether the field that gives mass responds to the rulers' overall scale (if it does, gravity repels); whether further kinds of wave exist. The exact count must give the measured G.
- **The plexus's own waves.** Their spectrum: each wave's energy must be in proportion to its frequency, and the waves must give the frame law. If not, travel below light's speed would leave a wake, and gravity's law would have no source in the medium.
- **The measured vacuum.** The plexus's share in vacuum polarization (the Lamb shift, the electron's magnetic moment), light-by-light scattering, vacuum birefringence and the Casimir force; this needs the strength of the field the dynamo sustains.
- **The settled Ocean's pressure.** The settled Ocean holds w = −1 and can only rise above it as the supply runs down. A confirmed crossing of w = −1 ends it; later DESI releases, with the microwave background and supernovae, settle it.

**What else is open** (§13.2): which waves the dynamo makes; the size of the matter that remained at the start of the beat; why the flow's energy has the size it has, and how the drive from what is gathered falls short and deepens into a beat's end; the eddy's limit (how the tie-up compounds inward, how a round eddy answers to the sphere's average, the core's load per area, the eddy's shape far out, the black-hole threshold); the eddy's beginning (what a river carries, how far bound matter bends it, where the swirl hands back); what the eddy has not been tested on (ellipticals and dwarf spheroidals, the early disks galaxy by galaxy, the growth of the large-scale web); the plexus law's open items, among them the scale the neutrinos' masses need and the joining field's size far below the dent; the phase's departures and what holds an eddy up in the law; energy's books across expansion; inside a spinning hole; the couplings in C; and the turn (whether it is free of instabilities, how the gas of light loosens, at what temperature it becomes the normal fluid, how evenly that forms). Under matter and its threshold: each kind's lowest energy; the scale hierarchy and its twin; the relation to the Standard Model; the size and spin of the localized excitation; the conserved sense shared across kinds.

**The predictions** (§15): no long-wavelength primordial gravitational waves; neutrinoless double-beta decay must occur (if the neutrino masses are shown to be in the inverted ordering and the next generation of searches does not see it, the framework fails with the account of the families); no sterile neutrino.

## Citing

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23142440-blue)](https://doi.org/10.5281/zenodo.23142440)

Please cite the archived release rather than the repository.

- **All versions** — `10.5281/zenodo.23142440`. Resolves to the latest release. Use this when citing the work as an evolving artifact. Each version's own DOI is listed on the Zenodo record.

> Hays, K. (2026). *Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium. A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology* (Version 3.16) [Preprint]. Zenodo. <https://doi.org/10.5281/zenodo.23142440>

## License

Dual-licensed, because the repository holds both a document and a program.

- **The written work** — the paper, its generated LaTeX source, and the prose embedded in the build script — is licensed **CC BY 4.0**. See [`LICENSE`](LICENSE).
- **The code** — `build_ocean_formalism.py` as a program, and the scripts in `checks/`, `sparc/`, `milky-way/` and `expansion/` — is licensed **MIT**. See [`LICENSE-CODE`](LICENSE-CODE).
- **Published data** included for the analyses remain their authors': the SPARC tables in `sparc/data/` (Lelli, McGaugh & Schombert 2016), the DESI DR2 distances in `expansion/model.py`, and the Milky Way measurements in `milky-way/` (Eilers et al. 2019; Bovy & Rix 2013; Lisanti et al. 2023, Fig. A1). Cite the sources if you use them.

© 2026 Keith Hays
