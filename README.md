# Ocean

**Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium — A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology**

A theoretical proposal built on one premise: there is no empty space. The vacuum is a single continuous medium, called here the Ocean, with no edges and no outside. What we call matter is the Ocean's own energy gathered and circulating in place; light is a ripple in the same medium; and gravity is proposed to be the medium's response to concentrated energy. Einstein's equations are kept as the correct description of that response, with the Ocean offered as the reason they hold.

From that premise the paper asks whether dark matter and dark energy are two substances or two behaviours of one medium. Standard cosmology accounts for roughly ninety-five per cent of the contents of the observable universe with two quantities that fit the data without being derived from anything. This document asks whether both might have a common origin in the dynamics of the Ocean.

**This is a proposal, not an established theory.** The paper states its own falsification conditions explicitly and carries an itemized research program, several items of which could terminate the framework outright.

---

## Contents

| File | Description |
|---|---|
| `Ocean_Scalar_Tensor_Hydrodynamics_v3_7.pdf` | The paper. 25 pages, including a non-technical preface, a glossary and a bibliography. |
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

1. **Preface** — non-technical. The premise (no empty space; an Ocean without edges or outside; no particles as objects; gravity as the medium's response), the motivating problem, the provenance of Λ and of dark matter, the General Relativity / quantum field theory disagreement over the vacuum, what a medium can do, and the four conditions that would falsify the framework.
2. **Conventions and glossary** — fixed meanings for the Ocean, pattern, localized excitation, the Heartbeat, a beat, the present beat, beat transition, the big bang and epoch. "Particle" and "cycle" appear only when reporting other work, and "universe" is not used on its own.
3. **§1–§4** — the field equation and its status as the effective description of the medium; tensor definitions, including the refractive account of gravity (§2.5) and the complex-field condition the scale-hierarchy route depends on (§2.2); scalar-field dynamics; the Ocean interpretation.
4. **§5** — the Heartbeat cosmology, in two fenced parts: what can be said within the present beat (deceleration, acceleration and the evidence for evolving dark energy), and what the framework permits across beats (counted, not timed; the nearest precedent; the primordial gravitational-wave test).
5. **§6** — galactic dynamics, including pressure-supported galaxies and the vacuum contribution as a flow with shear and wakes.
6. **§7** — the localization threshold. The matter/vacuum partition is derived from the excitation spectrum of the medium rather than declared at a fixed energy, and the healing length recovers the electron rest energy as a calibration. §7.7 records the open items, including the candidate route for the scale hierarchy and the size and spin of the localized excitation.
7. **§8–§9** — limiting regimes, a strong-field regime and black holes, conservation conditions, and regularity as a property of the medium's state.
8. **§10** — relation to existing work: the superfluid-vacuum, viscous-cosmology and cyclic-cosmology literature, what is inherited, what remains distinctive, and four known deficiencies, including the vacuum effects already measured at the electron scale.
9. **§11–§12** — the research program and a summary.

## Known open problems

Stated in the paper, repeated here so that they are visible before reading:

- **Deriving gravity from the medium.** The paper proposes that gravity is the Ocean's response to concentrated energy. To hold, every pattern must respond in exactly the same proportion (everything falls alike), time must slow and space stretch in equal measure (the observed bending of starlight), and gravitational waves must travel at the speed of light. None of this has yet been derived.
- **The scale hierarchy.** Galactic-scale effects and the matter-localization scale are separated by roughly thirty-two orders of magnitude. A candidate route treats the galactic scale as a property of the individual disturbance rather than of the medium; the ratio remains, and the route's tasks are not done. This remains the most serious unresolved problem in the document.
- **The measured vacuum.** Empty space has been measured screening charge, scattering light off light and splitting light by polarization in strong fields. If the Ocean is real, these are its properties, and it must reproduce them quantitatively.
- **The sign of the self-interaction.** If the medium is focusing rather than defocusing in its present state, nothing arrests concentration and the framework is not viable as written.
- **The preferred frame.** Treating the vacuum as a medium gives it a rest frame. Experimental limits on Lorentz violation are extremely tight and compatibility has not been demonstrated.
- **Vertical galactic dynamics.** Local Milky Way data require a large enhancement of radial acceleration and essentially none vertically. Models whose extra force is parallel to the baryonic gravitational field fail this test.
- **Size and spin.** The localized excitation must appear pointlike to probes at about 10⁻¹⁸ m, and spin ½ requires structure the scalar formulation does not yet contain.
- **First-order dissipative hydrodynamics.** The viscous sector is of Eckart–Landau type, which is known to be acausal and generically unstable in relativistic settings. A causal second-order or BDNK reformulation is required.

## Citing

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23142440.svg)](https://doi.org/10.5281/zenodo.23142440)

Please cite the archived release rather than the repository.

- **All versions** — `10.5281/zenodo.23142440`. Resolves to the latest release. Use this when citing the work as an evolving artifact.
- **Version 3.7** — `10.5281/zenodo.XXXXXXXX`. Pinned to this release and its exact files; filled in once the release is archived.
- **Version 3.6** — `10.5281/zenodo.23324587`. Earlier version DOIs are listed on the Zenodo record.

> Hays, K. (2026). *Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium. A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology* (Version 3.7) [Preprint]. Zenodo. <https://doi.org/10.5281/zenodo.23142440>

## License

Dual-licensed, because the repository holds both a document and a program.

- **The written work** — the paper, its generated LaTeX source, and the prose embedded in the build script — is licensed **CC BY 4.0**. See [`LICENSE`](LICENSE).
- **The build tooling** — `build_ocean_formalism.py` as a program — is licensed **MIT**. See [`LICENSE-CODE`](LICENSE-CODE).

© 2026 Keith Hays
