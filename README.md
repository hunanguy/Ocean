# Ocean

**Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium — A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology**

A theoretical proposal built on one premise: there is no empty space. The vacuum is a single continuous medium, called here the Ocean, with no edges and no outside. What we call matter is the Ocean's own energy gathered and circulating in place; light is a ripple in the same medium; and gravity is proposed to be the medium's response to concentrated energy. The Ocean has one speed, at which every disturbance travels, and gravity is where that speed varies from place to place. Einstein's equations are kept as the correct description of that response, with the Ocean offered as the reason they hold.

From that premise the paper asks whether dark matter and dark energy are two substances or two behaviors of one medium. Standard cosmology accounts for roughly ninety-five percent of the contents of the observable universe with two quantities that fit the data without being derived from anything. This document asks whether both might have a common origin in the dynamics of the Ocean.

**This is a proposal, not an established theory.** The paper states its own falsification conditions explicitly and carries an itemized research program, several items of which could terminate the framework outright.

---

## Contents

| File | Description |
|---|---|
| `Ocean_Scalar_Tensor_Hydrodynamics_v3_9.pdf` | The paper. 40 pages, including a non-technical preface, a glossary and a bibliography. |
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

The script runs `pdflatex` three times so that cross-references and page breaks settle.

### Font dependency

The preamble uses `mathptmx` (Times) rather than `lmodern`, because `lmodern` is absent from some minimal TeX Live installations and its absence triggers a Type 3 bitmap fallback. A consequence is that `mathptmx` leaves `\hbar` undefined, so the preamble restores it explicitly:

```latex
\DeclareRobustCommand{\hbar}{{\mathchar'26\mkern-9mu h}}
```

On a full TeX Live installation you can substitute `newtxtext`/`newtxmath` and remove that line.

## Structure of the paper

1. **Preface** — non-technical. The premise (no empty space; an Ocean without edges or outside; no particles as objects; one speed for every disturbance; gravity as the medium's response), the six revisions the framework has undergone, the motivating problem, the provenance of Λ and of dark matter, the General Relativity / quantum field theory disagreement over the vacuum, what a medium can do, black holes, and the five conditions that would falsify the framework.
2. **Conventions and glossary** — fixed meanings for the Ocean, flow, circulation, travel, the carrying speed, light, state, pattern, carried quantities, excitation, the healing length, circulation sense, horizon, the Heartbeat, a beat, the present beat, beat transition, the big bang, epoch and the present expansion epoch. "Particle" and "cycle" appear only when reporting other work, "universe" is not used on its own, and "dark matter" and "dark energy" name only what other work calls them.
3. **§1–§4** — the field equation and its status as the effective description of the medium; tensor definitions, including the refractive account of gravity (§2.5) and the complex field Φ = ρe^{iθ} as the baseline representation, with the state split into the amount ρ and the phase rate μ (§2.2); scalar-field dynamics; the Ocean interpretation.
4. **§5** — the Heartbeat cosmology, in two fenced parts: what can be said within the present beat (expansion as divergence; one root, two effects: a gradient of state refracts, a uniform change of state flows; deceleration, acceleration and the hints of evolving dark energy), and what the framework permits across beats (counted, not timed; the nearest precedent; the primordial gravitational-wave test; the horizon problem and the age of the Ocean).
5. **§6** — galactic dynamics, including pressure-supported galaxies and the vacuum contribution as a flow, with shear bound to the galaxy as the proposed route past the vertical-acceleration constraint; whether it reaches the stars as the required radial-over-vertical enhancement is still to be calculated.
6. **§7** — the localization threshold. The matter/vacuum partition is derived from the excitation spectrum of the medium rather than declared at a fixed energy, and the healing length recovers the electron rest energy as a calibration. The electron's mass, and the strength of gravity with it, are constants of the beat. §7.7 records the open items, including the candidate route for the scale hierarchy, the strength of gravity as the measured ratio α_G, the size and spin of the localized excitation, and circulation sense.
7. **§8–§9** — limiting regimes; black holes rewritten around a refractive horizon (no accumulation, stripping as the no-hair theorem, Hawking radiation, recycling rather than draining), with a living worked case, "A traveler falls in" (§8.2); conservation conditions, regularity as a property of the medium's state, and two new sections: nothing is destroyed (§9.2) and where a wave's energy goes (§9.3).
8. **§10** — relation to existing work: the superfluid-vacuum, viscous-cosmology and cyclic-cosmology literature, the nearest precedents in the ether theories of Arminjon and Broekaert, what is inherited, what remains distinctive, and five known deficiencies, including the vacuum effects already measured at the electron scale and the matter–antimatter comparisons.
9. **§11** — one speed and the split, new in 3.9: why the Ocean has a single carrying speed; the rules are fixed and every pattern responds alike; what sits on each side of the field equation; why the minimal law cannot carry the split (it bends light the wrong way and gives light and matter different speed limits); the weak-field condition; a candidate mechanism, the Ocean's current through time slowed by drag, which reproduces General Relativity's γ = β = 1 from two stated inputs and departs from it in the strong field; and what the Ocean must be made of.
10. **§12–§13** — the research program and a summary.

## Known open problems

Stated in the paper, repeated here so that they are visible before reading:

- **Deriving gravity from the medium.** The paper proposes that gravity is the Ocean's response to concentrated energy. To hold, every pattern must respond in exactly the same proportion (everything falls alike), time must slow and space stretch in equal measure (the observed bending of starlight), and gravitational waves must travel at the speed of light. None of this has yet been derived. The minimal law fails it, and the one-speed law that must replace it is not yet written. The candidate mechanism matches General Relativity's weak-field tests only given two inputs it does not yet derive, and it predicts a horizon at a different radius, which black-hole imaging and merger ringdowns can test.
- **The scale hierarchy.** Galactic-scale effects and the matter-localization scale are separated by roughly thirty-two orders of magnitude. A candidate route treats the galactic scale as a property of the individual disturbance rather than of the medium; the ratio remains, and the route's tasks are not done. This remains the most serious unresolved problem in the document.
- **The measured vacuum.** Empty space has been measured screening charge, scattering light off light and splitting light by polarization in strong fields. If the Ocean is real, these are its properties, and it must reproduce them quantitatively.
- **The sign of the self-interaction.** If the medium is focusing rather than defocusing in its present state, nothing arrests concentration and the framework is not viable as written.
- **The preferred frame.** Treating the vacuum as a medium gives it a rest frame. Experimental limits on Lorentz violation are extremely tight and compatibility has not been demonstrated.
- **Vertical galactic dynamics.** Local Milky Way data require a large enhancement of radial acceleration and essentially none vertically. Models whose extra force is parallel to the baryonic gravitational field fail this test.
- **The strength of gravity.** The medium must produce the observed strength of gravity, the ratio α_G = Gm_e²/ħc ≈ 1.75 × 10⁻⁴⁵; the electric force between two electrons is about 4 × 10⁴² times their gravity. The Planck length is treated as a readout of the medium's state, not a fundamental length, and the medium must account for a gap of about 10²² below its own scale as well as 10³² above.
- **Size and spin.** The localized excitation must appear pointlike to probes at about 10⁻¹⁸ m, and spin ½ requires structure the scalar formulation does not yet contain.
- **First-order dissipative hydrodynamics.** The viscous sector is of Eckart–Landau type, which is known to be acausal and generically unstable in relativistic settings. A causal second-order or BDNK reformulation is required.

## Citing

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23142440-blue)](https://doi.org/10.5281/zenodo.23142440)

Please cite the archived release rather than the repository.

- **All versions** — `10.5281/zenodo.23142440`. Resolves to the latest release. Use this when citing the work as an evolving artifact.
- **Version 3.9** — `10.5281/zenodo.23549277`.
- **Version 3.8** — `10.5281/zenodo.23488580`.
- **Version 3.7** — `10.5281/zenodo.23368921`.
- **Version 3.6** — `10.5281/zenodo.23324587`. Earlier version DOIs are listed on the Zenodo record.

> Hays, K. (2026). *Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium. A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology* (Version 3.9) [Preprint]. Zenodo. <https://doi.org/10.5281/zenodo.23142440>

## License

Dual-licensed, because the repository holds both a document and a program.

- **The written work** — the paper, its generated LaTeX source, and the prose embedded in the build script — is licensed **CC BY 4.0**. See [`LICENSE`](LICENSE).
- **The build tooling** — `build_ocean_formalism.py` as a program — is licensed **MIT**. See [`LICENSE-CODE`](LICENSE-CODE).

© 2026 Keith Hays
