# Ocean

**Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium — A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology**

A theoretical proposal built on one premise: there is no empty space. The vacuum is a single continuous medium, called here the Ocean, with no edges and no outside. What we call matter is the Ocean's own energy gathered and circulating in place; light is a ripple in the same medium; and gravity is proposed to be the medium's response to concentrated energy. The Ocean has one speed, at which every disturbance travels. It rebuilds every pattern continuously, and gravity is the uneven making of time by that rebuild, slower where there is more to rebuild. No speed is fixed: the measured speed of light is that local speed as read by rulers and clocks made of the same Ocean. Einstein's equations are kept as the correct description of that response, with the Ocean offered as the reason they hold.

From that premise the paper asks whether dark matter and dark energy are two substances or two behaviors of one medium. Standard cosmology accounts for roughly ninety-five percent of the contents of the observable universe with two quantities that fit the data without being derived from anything. This document asks whether both might have a common origin in the dynamics of the Ocean.

**This is a proposal, not an established theory.** The paper states its own falsification conditions explicitly and carries an itemized research program, several items of which could terminate the framework outright.

---

## Contents

| File | Description |
|---|---|
| `Ocean_Scalar_Tensor_Hydrodynamics_v3_13.pdf` | The paper. 71 pages, including a non-technical preface, a glossary, Appendices A and B and a bibliography. Document digest `5c47-4c91-967c`. |
| `Ocean_Appendix_A_Spinning_Black_Hole_v3_13.pdf` | Appendix A on its own: the rebuild of a spinning black hole (Sagittarius A*), 5 pages. Built from the same text as the paper's Appendix A, and carrying that part's token, `45c30c`. |
| `Ocean_Scalar_Tensor_Hydrodynamics_v3_13.manifest.txt` | The reading manifest, written by the build: every part of the paper with its checksum token and the document digest. |
| `build_ocean_formalism.py` | Generates the LaTeX source of the paper and of the standalone Appendix A, and compiles both. The source of truth. |
| `.zenodo.json` | Deposit metadata consumed by the Zenodo–GitHub integration. |
| `CITATION.cff` | Citation metadata for GitHub's *Cite this repository* widget. |
| `checks/` | `check_ocean_math.py`, a consistency and accuracy check of the paper's mathematics, with three helper modules. |
| `references/` | Verification notes, one per paper read: what each cited source supports, and where the paper's wording was corrected against it. Full texts are not stored. |

The `.tex` files are **generated**, not stored. It is produced by the build script and excluded by `.gitignore` to keep diffs meaningful. If you would rather ship the LaTeX source in the archive, remove the first non-comment line of `.gitignore` and commit it.

## Building

Requires Python 3.8+ and `pdflatex` on `PATH` (TeX Live or MiKTeX).

```bash
python3 build_ocean_formalism.py                 # writes the paper and the standalone Appendix A (.tex and .pdf)
python3 build_ocean_formalism.py --outdir build  # write elsewhere
python3 build_ocean_formalism.py --no-pdf        # emit the paper's .tex only
python3 build_ocean_formalism.py --keep-aux      # retain .aux/.log for debugging
```

The script runs `pdflatex` three times so that cross-references and page breaks settle. It then writes the standalone Appendix A from the same text as the paper's appendix, filling in its section and equation numbers from the compiled paper, and compiles it.

## Reading completeness

Every part of the paper carries a checksum token: the first six hex digits of the SHA-256 of its LaTeX source. Each page footer gives the page, the page count and the part with its token; each part ends with a line giving its token; and the last page is a reading manifest listing every part, its first page and its token, followed by a document digest and the words "End of document". The standalone Appendix A carries the token of the paper's Appendix A part in its footers, title block and closing line, since it is built from the same text. A reader, human or automated, has read the whole paper when it reaches that line, and a summary or review that cannot give the digest was made from an incomplete reading. The digest for 3.13 is `5c47-4c91-967c`. It is also written to the PDF's subject metadata and to the `.manifest.txt` file.

## Checking the mathematics

```bash
cd checks
python3 check_ocean_math.py --build ../build_ocean_formalism.py --report report.md
```

Requires `numpy` and `scipy`. The script re-derives the paper's equations numerically (equations of motion from the action, the disturbance equation from the expanded Lagrangian, the strong-field geometry), recomputes its numerical statements from CODATA 2018 constants, re-runs the frame-dragging simulations, and checks references, citations and symbols for consistency. Each check is tied to a phrase of the paper's own LaTeX, so a change of wording or number that the check no longer matches makes it fail rather than pass silently. Outcomes are PASS, NOTE (agrees with a caveat, or cannot be decided from the text) and FAIL; the script exits with status 1 on any failure. For 3.12.1: 79 checks, 78 pass, 1 note, 0 fail.

### Font dependency

The preamble uses `mathptmx` (Times) rather than `lmodern`, because `lmodern` is absent from some minimal TeX Live installations and its absence triggers a Type 3 bitmap fallback. A consequence is that `mathptmx` leaves `\hbar` undefined, so the preamble restores it explicitly:

```latex
\DeclareRobustCommand{\hbar}{{\mathchar'26\mkern-9mu h}}
```

On a full TeX Live installation you can substitute `newtxtext`/`newtxmath` and remove that line.

## Structure of the paper

1. **Preface** — non-technical, after a reader's note on how to confirm a complete reading. The premise (no empty space; an Ocean without edges or outside; no particles as objects; one speed for every disturbance, and no fixed speed; gravity as the medium's response), the motivating problem, the provenance of Λ and of dark matter, the General Relativity / quantum field theory disagreement over the vacuum, what a medium can do, black holes, the nine revisions the framework has undergone (the ninth: the rebuild and the law), and the five conditions that would falsify the framework.
2. **Conventions and glossary** — fixed meanings for the Ocean, flow, circulation, travel, the carrying speed, the speed of light, light, state, pattern, carried quantities, excitation, the healing length, circulation sense, horizon, matter, and, new in 3.12, the rebuild, building, reclaiming, the plexus, the re-made state and the dynamo, and, new in 3.13, the load, the eddy and the swirl in time; then the Heartbeat, a beat, the present beat, beat transition, the big bang, epoch and the present expansion epoch.
3. **§1–§4** — the field equation and its status as the effective description of the medium; tensor definitions, including the complex field Φ = ρe^{iθ} with the re-made state, the viscous stress (kept, but carrying nothing in the settled Ocean), and the refractive account of gravity; the equations of motion, with the single real field standing for the Ocean's amount; the Ocean interpretation.
4. **§5** — the Heartbeat cosmology, within the present beat and across beats. In 3.12 the contraction is the reclaiming carrying the Ocean once the drive runs out: nothing new forms, time and disorder are reclaimed, and the energy returns compressed, so disorder does not accumulate from beat to beat. The turn into the next beat is open.
5. **§6** — galactic dynamics, rewritten in 3.13. A galaxy sits in an eddy of the Ocean's current far bigger than itself, set going by a larger current and then holding itself as a swirl in time. The eddy acts through its own energy, which adds to the load every star reads, not through a swirl in the disk's plane (which leaves stars at rest, pressure-supported galaxies and stacked lensing untouched). Its strength is set by the galaxy's baryonic mass and one limit: V⁴ = G M g†, the baryonic Tully–Fisher relation, with model galaxies on the radial acceleration relation to 0.05 dex. The limit is held at the eddy's center (every eddy's core holds the same load per area, as halo surface densities show) and has not followed the expansion over eleven billion years (Genzel et al. 2017; RC100). The reading rule, Eq. 16, now follows from the frame law; the eddy's energy is counted once. In the model Milky Way the eddy raises the radial turning by 1.59 and the vertical by 10–17 percent within a kiloparsec, passing the Gaia criterion. The edge, the center and black holes, and what is open.
6. **§7** — matter and its threshold. The partition is by kind of wave: a kind with a lowest energy can be held in place as matter, a kind without one cannot. The Ocean's own amount and phase are written out as two coupled fields. The electron's 0.511 MeV is the lowest energy of its own kind of wave, set by the field the dynamo sustains; 386 fm is the electron's own localization length, and the Ocean's healing length lies near the Planck length.
7. **§8–§9** — limiting regimes; black holes (no accumulation, stripping as the no-hair theorem, Hawking radiation, recycling rather than draining) and the traveler falling in, now also in the rebuild's terms; conservation conditions, nothing is destroyed, and where a wave's energy goes.
8. **§10** — relation to existing work: what is inherited and what is not, set out as labeled lists, and the known deficiencies against current practice and measurement.
9. **§11** — one speed and the split; the current through time, now the uneven making of time with no drag; the strong field and the point of no return; frame dragging, carried by the re-made tilt rather than quantized lines; new in 3.13, beyond first order, the Ocean's rulers stretch by direction, set by the plexus's frame law, so a spinning hole's outside is General Relativity's (checked in the Ocean's own slicing by the phase); the edge and the core.
10. **§12** — the rebuild and the law (3.12), with, new in 3.13, §12.9 the plexus law: seven computed tests. Its frame law is the teleparallel equivalent of General Relativity; light and the eleven other carriers are twist-only laws (LEP's color factors pick three complex directions); the joining field's shape is forced by the measured W/Z ratio; matter is half-angle waves on the frame, the reclaiming its backward solution; exactly three families; a half-angle from whole units; and a sea of plexus waves that lets nothing feel drag. The build supplies the Ocean's current as it expands: there is no separate phase rate to set.
11. **§13–§15** — all open items gathered in one section, brought up to date for 3.13; the research program in dependency order; a summary.
12. **Appendix A** — the rebuild of a spinning black hole: Sagittarius A* taken through the same steps as the Earth's rebuild of §12.3, a table comparing the two regimes, and what the account settles and leaves open. Also issued as a standalone PDF.
13. **Appendix B** — new in 3.13, the rebuild of the Milky Way's eddy, which carries the Earth and holds the black hole at its center: the three stories as one, with a table comparing the Earth, Sagittarius A* and the eddy.

## Known open problems

Stated in the paper (§13), repeated here so that they are visible before reading:

- **The eddy's limit.** Why every eddy's core stops at the same load per area, and so the value of g† ≈ 1.2 × 10⁻¹⁰ m s⁻² and its closeness to c₀H₀/2π; the smoothing inside the meeting radius; the eddy's shape far from the disk; the early/late-type lensing difference; the black-hole threshold in the swirl's speed in time.
- **The plexus law's open items.** The strong force's hand term; the scale the neutrinos' masses need; the reading strengths; the joining field's size far below the dent; the odd hand count for patterns with no strong books; two weak directions; the grain's strength (Auger passes it by only about 1.35).
- **The phase in the build's terms.** Its equation with no outside time, and that the supplied current leaves it gapless; and energy's books across expansion.
- **Which waves the dynamo makes.** The plexus law narrows the strong force's mixing to three complex directions and the families to exactly three; that the dynamo makes exactly these is not derived.
- **The leftover.** The rebuild must give the matter remaining at the start of the beat, a baryon-to-photon ratio of about 6.1 × 10⁻¹⁰.
- **The plexus's own waves.** That they carry energy in proportion to frequency, as nothing feeling drag requires, is not derived; their health beyond that is not checked.
- **Deriving the frame law.** The frame law gives Einstein's form in full and a spinning hole's outside; deriving it from the plexus's own waves, and the region inside a spinning hole's inner edge, remain.
- **The Milky Way test.** The eddy's vertical prediction must be confronted with the full Milky Way analysis, and prograde and retrograde halo stars should differ in their turning by up to 2vV_s/r.
- **The scale hierarchy and its twin.** Galactic effects act across kiloparsecs while the medium's own scale lies near the Planck length; and the electron's lowest energy lies nearly 10²³ below that scale, which the field the dynamo sustains must explain.
- **The measured vacuum.** The plexus law gives light and the electron the form of the laws quantum electrodynamics quantizes, so vacuum polarization, light-by-light scattering and birefringence follow in form; the numbers need the strength of charge, not derived.
- **The sign of the self-interaction.** If the medium is focusing in its present state, nothing arrests concentration and the framework is not viable as written.
- **The preferred frame.** Treating the vacuum as a medium gives it a rest frame; compatibility with the tight limits on Lorentz violation has not been demonstrated.
- **Black-hole cores and the turn.** The turnaround of collapse rests on one candidate mechanism, a loosening of the Ocean's grip at extreme density; what turns a beat's collapse into the next beat is open.
- **Size and spin.** The localized excitation must appear pointlike to probes at about 10⁻¹⁸ m, and spin ½ must come from the order the dynamo makes.
- **The couplings in C.** How the Ocean's amount and phase couple to the re-made state, to the viscous stress (whether Π_μν has any role; if it does, its first-order form must be replaced by a causal one) and to the plexus.
- **The committed prediction.** Neutrinoless double-beta decay must occur. If the neutrino masses are shown to be ordered so that its rate cannot be small, and the next generation of searches does not see it, the account of the family fails.

## Citing

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23142440-blue)](https://doi.org/10.5281/zenodo.23142440)

Please cite the archived release rather than the repository.

- **All versions** — `10.5281/zenodo.23142440`. Resolves to the latest release. Use this when citing the work as an evolving artifact.
- **Version 3.13** — `10.5281/zenodo.23884689`.
- **Version 3.12.1** — `10.5281/zenodo.23827267`.
- **Version 3.12** — `10.5281/zenodo.23812291`.
- **Version 3.11** — `10.5281/zenodo.23718695`.
- **Version 3.10** — `10.5281/zenodo.23586999`.
- **Version 3.9** — `10.5281/zenodo.23549277`.
- **Version 3.8** — `10.5281/zenodo.23488580`.
- **Version 3.7** — `10.5281/zenodo.23368921`.
- **Version 3.6** — `10.5281/zenodo.23324587`. Earlier version DOIs are listed on the Zenodo record.

> Hays, K. (2026). *Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium. A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology* (Version 3.13) [Preprint]. Zenodo. <https://doi.org/10.5281/zenodo.23142440>

## License

Dual-licensed, because the repository holds both a document and a program.

- **The written work** — the paper, its generated LaTeX source, and the prose embedded in the build script — is licensed **CC BY 4.0**. See [`LICENSE`](LICENSE).
- **The build tooling** — `build_ocean_formalism.py` as a program — is licensed **MIT**. See [`LICENSE-CODE`](LICENSE-CODE).

© 2026 Keith Hays
