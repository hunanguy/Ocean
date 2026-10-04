# Ocean

**Scalar–Tensor Hydrodynamics: A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology**

A theoretical proposal that treats the vacuum not as a geometric background but as a dynamic scalar medium with its own stress-energy, pressure, internal flow and dissipative response.

The question it asks is whether dark matter and dark energy are two substances or two behaviours of one medium. Standard cosmology accounts for roughly ninety-five per cent of the universe's contents with two quantities that fit the data without being derived from anything. This document asks whether both might have a common origin in the dynamics of a single vacuum field.

**This is a proposal, not an established theory.** The paper states its own falsification conditions explicitly and carries an itemized research program, several items of which could terminate the framework outright.

---

## Contents

| File | Description |
|---|---|
| `Ocean_Scalar_Tensor_Hydrodynamics_v3_3.pdf` | The paper. 12 pages, including a non-technical preface. |
| `build_ocean_formalism.py` | Generates the LaTeX source and compiles it. The source of truth. |
| `.zenodo.json` | Deposit metadata consumed by the Zenodo–GitHub integration. |
| `CITATION.cff` | Citation metadata for GitHub's *Cite this repository* widget. |

The `.tex` file is **generated**, not stored. It is produced by the build script and excluded by `.gitignore` to keep diffs meaningful. If you would rather ship the LaTeX source in the archive, remove the first non-comment line of `.gitignore` and commit it.

## Building

Requires Python 3.8+ and `pdflatex` on `PATH` (TeX Live or MiKTeX).

```bash
python3 build_ocean_formalism.py                 # writes .tex and .pdf to the current directory
python3 build_ocean_formalism.py --outdir build  # write elsewhere
python3 build_ocean_formalism.py --no-pdf        # emit the .tex only
python3 build_ocean_formalism.py --keep-aux      # retain .aux/.log for debugging
```

The script runs `pdflatex` twice so that cross-references resolve.

### Font dependency

The preamble uses `mathptmx` (Times) rather than `lmodern`, because `lmodern` is absent from some minimal TeX Live installations and its absence triggers a Type 3 bitmap fallback. A consequence is that `mathptmx` leaves `\hbar` undefined, so the preamble restores it explicitly:

```latex
\DeclareRobustCommand{\hbar}{{\mathchar'26\mkern-9mu h}}
```

On a full TeX Live installation you can substitute `newtxtext`/`newtxmath` and remove that line.

## Structure of the paper

1. **Preface** — non-technical. The motivating problem, the provenance of Λ and of dark matter, the General Relativity / quantum field theory disagreement over the vacuum, the core idea, and the three conditions that would falsify the framework.
2. **§1–§6** — the field equation, tensor definitions, scalar-field dynamics, and the cosmological and galactic regimes.
3. **§7** — the localization threshold. The matter/vacuum partition is derived from the excitation spectrum of the scalar field rather than declared at a fixed energy. The crossover is set by the medium's healing length, which recovers the electron rest energy as a calibration of that length rather than as an input.
4. **§8–§9** — limiting regimes, conservation conditions, global regularity, and the defocusing requirement.
5. **§10–§11** — the research program and a summary.

## Known open problems

Stated in the paper, repeated here so that they are visible before reading:

- **The scale hierarchy.** Galactic-scale effects and the matter-localization scale are separated by roughly thirty-two orders of magnitude. They are set by different operators, so this is not an outright contradiction, but the separation is not yet explained. This is the most serious unresolved problem in the document.
- **The sign of the self-interaction.** If the medium's self-interaction is focusing rather than defocusing, nothing arrests concentration and the framework is not viable as written.
- **The preferred frame.** Treating the vacuum as a medium gives it a rest frame. Experimental limits on Lorentz violation are extremely tight and compatibility has not been demonstrated.

## Citing

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23142440.svg)](https://doi.org/10.5281/zenodo.23142440)

Please cite the archived release rather than the repository.

- **All versions** — `10.5281/zenodo.23142440`. Resolves to the latest release. Use this when citing the work as an evolving artifact.
- **Version 3.3** — `10.5281/zenodo.23142441`. Pinned to this release and its exact files. Use this when the specific version matters.

> Hays, K. (2026). *Scalar–Tensor Hydrodynamics: A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology* (Version 3.3) [Preprint]. Zenodo. <https://doi.org/10.5281/zenodo.23142441>

## License

Dual-licensed, because the repository holds both a document and a program.

- **The written work** — the paper, its generated LaTeX source, and the prose embedded in the build script — is licensed **CC BY 4.0**. See [`LICENSE`](LICENSE).
- **The build tooling** — `build_ocean_formalism.py` as a program — is licensed **MIT**. See [`LICENSE-CODE`](LICENSE-CODE).

© 2026 Keith Hays
