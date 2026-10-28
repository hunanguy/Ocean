# Ocean

**Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium — A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology**

A theoretical proposal built on one premise: there is no empty space. The vacuum is a single continuous medium, called here the Ocean, with no edges and no outside. What we call matter is the Ocean's own energy gathered and circulating in place; light is a ripple in the same medium; and gravity is proposed to be the medium's response to concentrated energy. The Ocean has one speed, at which every disturbance travels, and gravity is where that speed varies from place to place. No speed is fixed: the measured speed of light is that local speed as read by rulers and clocks made of the same Ocean. Einstein's equations are kept as the correct description of that response, with the Ocean offered as the reason they hold.

From that premise the paper asks whether dark matter and dark energy are two substances or two behaviors of one medium. Standard cosmology accounts for roughly ninety-five percent of the contents of the observable universe with two quantities that fit the data without being derived from anything. This document asks whether both might have a common origin in the dynamics of the Ocean.

**This is a proposal, not an established theory.** The paper states its own falsification conditions explicitly and carries an itemized research program, several items of which could terminate the framework outright.

---

## Contents

| File | Description |
|---|---|
| `Ocean_Scalar_Tensor_Hydrodynamics_v3_11.pdf` | The paper. 51 pages, including a non-technical preface, a glossary and a bibliography. Document digest `9031-3435-17da`. |
| `Ocean_Scalar_Tensor_Hydrodynamics_v3_11.manifest.txt` | The reading manifest, written by the build: every part of the paper with its checksum token and the document digest. |
| `build_ocean_formalism.py` | Generates the LaTeX source and compiles it. The source of truth. |
| `.zenodo.json` | Deposit metadata consumed by the Zenodo–GitHub integration. |
| `CITATION.cff` | Citation metadata for GitHub's *Cite this repository* widget. |
| `checks/` | `check_ocean_math.py`, a consistency and accuracy check of the paper's mathematics, with two helper modules. |
| `references/` | Verification notes, one per paper read: what each cited source supports, and where the paper's wording was corrected against it. Full texts are not stored. |

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

## Reading completeness

Every part of the paper carries a checksum token: the first six hex digits of the SHA-256 of its LaTeX source. Each page footer gives the page, the page count and the part with its token; each part ends with a line giving its token; and the last page is a reading manifest listing every part, its first page and its token, followed by a document digest and the words "End of document". A reader, human or automated, has read the whole paper when it reaches that line, and a summary or review that cannot give the digest was made from an incomplete reading. The digest for 3.11 is `9031-3435-17da`. It is also written to the PDF's subject metadata and to the `.manifest.txt` file.

## Checking the mathematics

```bash
cd checks
python3 check_ocean_math.py --build ../build_ocean_formalism.py --report report.md
```

Requires `numpy` and `scipy`. The script re-derives the paper's equations numerically (equations of motion from the action, the disturbance equation from the expanded Lagrangian, the strong-field geometry), recomputes its numerical statements from CODATA 2018 constants, re-runs the frame-dragging simulations, and checks references, citations and symbols for consistency. Each check is tied to a phrase of the paper's own LaTeX, so a change of wording or number that the check no longer matches makes it fail rather than pass silently. Outcomes are PASS, NOTE (agrees with a caveat, or cannot be decided from the text) and FAIL; the script exits with status 1 on any failure. For 3.11: 75 checks, 70 pass, 5 notes, 0 fail.

### Font dependency

The preamble uses `mathptmx` (Times) rather than `lmodern`, because `lmodern` is absent from some minimal TeX Live installations and its absence triggers a Type 3 bitmap fallback. A consequence is that `mathptmx` leaves `\hbar` undefined, so the preamble restores it explicitly:

```latex
\DeclareRobustCommand{\hbar}{{\mathchar'26\mkern-9mu h}}
```

On a full TeX Live installation you can substitute `newtxtext`/`newtxmath` and remove that line.

## Structure of the paper

1. **Preface** — non-technical, after a reader's note on how to confirm a complete reading. The premise (no empty space; an Ocean without edges or outside; no particles as objects; one speed for every disturbance, and no fixed speed; gravity as the medium's response), the eight revisions the framework has undergone (the eighth: spin and frame dragging), the motivating problem, the provenance of Λ and of dark matter, the General Relativity / quantum field theory disagreement over the vacuum, what a medium can do, black holes (a point of no return, not a surface), and the five conditions that would falsify the framework.
2. **Conventions and glossary** — fixed meanings for the Ocean, flow, circulation, travel, the carrying speed (its two readings, on the spot and from afar), the speed of light, light, state, pattern, carried quantities, excitation, the healing length, circulation sense, horizon, the Heartbeat, a beat, the present beat, beat transition, the big bang, epoch and the present expansion epoch. "Particle" and "cycle" appear only when reporting other work, "universe" is not used on its own, and "dark matter" and "dark energy" name only what other work calls them.
3. **§1–§4** — the field equation and its status as the effective description of the medium; tensor definitions, including the refractive account of gravity (§2.5) and the complex field Φ = ρe^{iθ} as the baseline representation, with the state split into the amount ρ and the phase rate μ (§2.2; in 3.11 two requirements select it, while antimatter partners and circulation sense are assigned to a second internal phase); the equations of motion for the general law and for the complex field (§3, rewritten in 3.11); scalar-field dynamics; the Ocean interpretation.
4. **§5** — the Heartbeat cosmology, in two fenced parts: what can be said within the present beat (expansion as divergence; one root, two effects: a gradient of state refracts, a uniform change of state flows; deceleration, acceleration and the hints of evolving dark energy), and what the framework permits across beats (counted, not timed, and driven by events rather than a preset clock; the nearest precedent; the primordial gravitational-wave test; the horizon problem and the age of the Ocean).
5. **§6** — galactic dynamics, including pressure-supported galaxies and the vacuum contribution as a flow, with shear bound to the galaxy as the proposed route past the vertical-acceleration constraint. A column-like swirl turns a star's travel only inward, not vertically, the property the local Milky Way data require; in 3.11 the swirl is carried by quantized lines that stars read as smooth, about 1200 km apart if the phase rate equals the electron's rest energy. Its strength from a galaxy's baryons, and the confrontation with Gaia data, are still to be done.
6. **§7** — the localization threshold. The matter/vacuum partition is derived from the excitation spectrum of the medium rather than declared at a fixed energy. Restated in 3.10 on two branches of one field: the gapped amount mode, whose quanta are localized (matter), and the gapless phase ripple, which is coherent. The healing length is the inverse cost of a dent in the Ocean and recovers the electron rest energy as a calibration. The electron's mass, and the strength of gravity with it, are constants of the beat. §7.7 records the open items, including the candidate route for the scale hierarchy (in 3.11 with the circulation per quantized line set by the phase rate, hc₀²/μ), the strength of gravity as the measured ratio α_G, the size and spin of the localized excitation, and circulation sense.
7. **§8–§9** — limiting regimes; black holes (no accumulation, stripping as the no-hair theorem, Hawking radiation, recycling rather than draining), with the horizon a point of no return where the geometric and medium horizons coincide, and the worked case "A traveler falls in" (§8.2), rewritten for 3.10; conservation conditions, regularity as a property of the medium's state, and two new sections: nothing is destroyed (§9.2) and where a wave's energy goes (§9.3).
8. **§10** — relation to existing work: the superfluid-vacuum, viscous-cosmology and cyclic-cosmology literature, the nearest precedents in the ether theories of Arminjon and Broekaert, what is inherited, what remains distinctive, and five known deficiencies, including the vacuum effects already measured at the electron scale and the matter–antimatter comparisons (in 3.11: patterns of opposite charge under the Ocean's U(1) would differ by 2μ, so matter and antimatter must carry the same Ocean charge).
9. **§11** — one speed and the split: why the Ocean has a single carrying speed, and (new in 3.10) why no speed is fixed, the law being written on the Ocean's own rulers and clocks; the rules are fixed and every pattern responds alike; what sits on each side of the field equation; why the minimal law cannot carry the split, and how a stiff Ocean removes the light–matter mismatch; the weak-field condition; the current through time, rebuilt in 3.10 (the Ocean stays in step, its amount stays fixed, drag composes in layers), reproducing General Relativity's γ = β = 1; new §11.7, the strong field: two principles (staying in step; nothing counted twice) give General Relativity's geometry outside a non-spinning mass, with the point of no return at 2GM/c₀² and the observed shadow of Sagittarius A*; new in 3.11, §11.8, frame dragging: a pattern's slowed surroundings are re-made as it travels and tilted by its travel; summed over the Earth's spinning parts they give the turning measured by Gravity Probe B, LAGEOS, LARES and LARES-2, and travel through the Ocean itself leaves no trace; the turning is carried by quantized lines, which a gyroscope reads as smooth over at least one line spacing; §11.9, at the edge and inside (§11.8 in 3.10): nothing happens at the edge, what falls in flows through, and a loosening coupling turns collapse around, with bounds and a return time set by the substrate scale; and what the Ocean must be made of (§11.10).
10. **§12–§13** — the research program and a summary. New in 3.11: the program is set out in dependency order, in six groups (what the Ocean is made of; the law; what the law gives; the dissipative sector; black holes, galaxies and the largest flows; cosmology and the beats), with the items that could end the framework marked decisive and duplicates merged; it adds "The required law", a law in which the phase rate today is large enough for frame dragging while the Ocean stays stiff, and states the heartbeat mechanism in the Ocean's own terms.

## Known open problems

Stated in the paper, repeated here so that they are visible before reading:

- **Deriving gravity from the medium.** The paper proposes that gravity is the Ocean's response to concentrated energy. To hold, every pattern must respond in exactly the same proportion (everything falls alike), time must slow and space stretch in equal measure (the observed bending of starlight), and gravitational waves must travel at the speed of light. Version 3.10 obtains General Relativity's geometry outside a non-spinning mass from two principles of the framework, and passes the Sagittarius A* shadow test; version 3.11 adds frame dragging to first order in spin. The full one-speed law is not yet written. Spinning black holes beyond first order and merger ringdowns are not yet covered.
- **The required law.** Frame dragging carried by quantized lines needs the Ocean's phase rate today to be of order 10 keV or more; the minimal law the paper writes down allows at most about 10⁻⁶ eV. A law in which the phase rate is that large while the Ocean stays stiff, and the energy its turning carries stays small, is required and not yet found.
- **The scale hierarchy.** Galactic-scale effects and the matter-localization scale are separated by roughly thirty-two orders of magnitude. A candidate route treats the galactic scale as a property of the individual disturbance rather than of the medium; the ratio remains, and the route's tasks are not done. This remains the most serious unresolved problem in the document.
- **The measured vacuum.** Empty space has been measured screening charge, scattering light off light and splitting light by polarization in strong fields. If the Ocean is real, these are its properties, and it must reproduce them quantitatively.
- **The sign of the self-interaction.** If the medium is focusing rather than defocusing in its present state, nothing arrests concentration and the framework is not viable as written.
- **The preferred frame.** Treating the vacuum as a medium gives it a rest frame. Experimental limits on Lorentz violation are extremely tight and compatibility has not been demonstrated.
- **Vertical galactic dynamics.** Local Milky Way data require a large enhancement of radial acceleration and essentially none vertically. Models whose extra force is parallel to the baryonic gravitational field fail this test.
- **Black-hole cores.** The turnaround of collapse inside a point of no return rests on one candidate mechanism, a loosening of the Ocean's grip at extreme density. The return time depends on the scale of what the Ocean is made of, which is not yet known.
- **The strength of gravity.** The medium must produce the observed strength of gravity, the ratio α_G = Gm_e²/ħc₀ ≈ 1.75 × 10⁻⁴⁵; the electric force between two electrons is about 4 × 10⁴² times their gravity. The Planck length is treated as a readout of the medium's state, not a fundamental length, and the medium must account for a gap of about 10²² below its own scale as well as 10³² above.
- **Size and spin.** The localized excitation must appear pointlike to probes at about 10⁻¹⁸ m, and spin ½ requires structure the scalar formulation does not yet contain.
- **First-order dissipative hydrodynamics.** The viscous sector is of Eckart–Landau type, which is known to be acausal and generically unstable in relativistic settings. A causal second-order or BDNK reformulation is required.

## Citing

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23142440-blue)](https://doi.org/10.5281/zenodo.23142440)

Please cite the archived release rather than the repository.

- **All versions** — `10.5281/zenodo.23142440`. Resolves to the latest release. Use this when citing the work as an evolving artifact.
- **Version 3.11** — DOI to be added once Zenodo issues it.
- **Version 3.10** — `10.5281/zenodo.23586999`.
- **Version 3.9** — `10.5281/zenodo.23549277`.
- **Version 3.8** — `10.5281/zenodo.23488580`.
- **Version 3.7** — `10.5281/zenodo.23368921`.
- **Version 3.6** — `10.5281/zenodo.23324587`. Earlier version DOIs are listed on the Zenodo record.

> Hays, K. (2026). *Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium. A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology* (Version 3.11) [Preprint]. Zenodo. <https://doi.org/10.5281/zenodo.23142440>

## License

Dual-licensed, because the repository holds both a document and a program.

- **The written work** — the paper, its generated LaTeX source, and the prose embedded in the build script — is licensed **CC BY 4.0**. See [`LICENSE`](LICENSE).
- **The build tooling** — `build_ocean_formalism.py` as a program — is licensed **MIT**. See [`LICENSE-CODE`](LICENSE-CODE).

© 2026 Keith Hays
