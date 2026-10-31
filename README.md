# Ocean

**Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium — A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology**

A theoretical proposal built on one premise: there is no empty space. The vacuum is a single continuous medium, called here the Ocean, with no edges and no outside. What we call matter is the Ocean's own energy gathered and circulating in place; light is a ripple in the same medium; and gravity is proposed to be the medium's response to concentrated energy. The Ocean has one speed, at which every disturbance travels, and gravity is where that speed varies from place to place. No speed is fixed: the measured speed of light is that local speed as read by rulers and clocks made of the same Ocean. Einstein's equations are kept as the correct description of that response, with the Ocean offered as the reason they hold.

From that premise the paper asks whether dark matter and dark energy are two substances or two behaviors of one medium. Standard cosmology accounts for roughly ninety-five percent of the contents of the observable universe with two quantities that fit the data without being derived from anything. This document asks whether both might have a common origin in the dynamics of the Ocean.

**This is a proposal, not an established theory.** The paper states its own falsification conditions explicitly and carries an itemized research program, several items of which could terminate the framework outright.

---

## Contents

| File | Description |
|---|---|
| `Ocean_Scalar_Tensor_Hydrodynamics_v3_12_1.pdf` | The paper. 64 pages, including a non-technical preface, a glossary, Appendix A and a bibliography. Document digest `a764-2c56-a31a`. |
| `Ocean_Appendix_A_Spinning_Black_Hole_v3_12_1.pdf` | Appendix A on its own: the rebuild of a spinning black hole (Sagittarius A*), 5 pages. Built from the same text as the paper's Appendix A, and carrying that part's token, `132e4c`. |
| `Ocean_Scalar_Tensor_Hydrodynamics_v3_12_1.manifest.txt` | The reading manifest, written by the build: every part of the paper with its checksum token and the document digest. |
| `build_ocean_formalism.py` | Generates the LaTeX source of the paper and of the standalone Appendix A, and compiles both. The source of truth. |
| `.zenodo.json` | Deposit metadata consumed by the Zenodo–GitHub integration. |
| `CITATION.cff` | Citation metadata for GitHub's *Cite this repository* widget. |
| `checks/` | `check_ocean_math.py`, a consistency and accuracy check of the paper's mathematics, with two helper modules. |
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

Every part of the paper carries a checksum token: the first six hex digits of the SHA-256 of its LaTeX source. Each page footer gives the page, the page count and the part with its token; each part ends with a line giving its token; and the last page is a reading manifest listing every part, its first page and its token, followed by a document digest and the words "End of document". The standalone Appendix A carries the token of the paper's Appendix A part in its footers, title block and closing line, since it is built from the same text. A reader, human or automated, has read the whole paper when it reaches that line, and a summary or review that cannot give the digest was made from an incomplete reading. The digest for 3.12.1 is `a764-2c56-a31a`. It is also written to the PDF's subject metadata and to the `.manifest.txt` file.

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
2. **Conventions and glossary** — fixed meanings for the Ocean, flow, circulation, travel, the carrying speed, the speed of light, light, state, pattern, carried quantities, excitation, the healing length, circulation sense, horizon, matter, and, new in 3.12, the rebuild, building, reclaiming, the plexus, the re-made state and the dynamo; then the Heartbeat, a beat, the present beat, beat transition, the big bang, epoch and the present expansion epoch.
3. **§1–§4** — the field equation and its status as the effective description of the medium; tensor definitions, including the complex field Φ = ρe^{iθ} with the re-made state, the viscous stress (kept, but carrying nothing in the settled Ocean), and the refractive account of gravity; the equations of motion, with the single real field standing for the Ocean's amount; the Ocean interpretation.
4. **§5** — the Heartbeat cosmology, within the present beat and across beats. In 3.12 the contraction is the reclaiming carrying the Ocean once the drive runs out: nothing new forms, time and disorder are reclaimed, and the energy returns compressed, so disorder does not accumulate from beat to beat. The turn into the next beat is open.
5. **§6** — galactic dynamics. A galaxy sits in an eddy of the Ocean's current and cannot make its own. The swirl that turns its stars' travel inward is the tilt of the re-made state, not a flow of the phase. With no source in the galaxy the swirl grows slightly with height, adding about 9 to 15 per cent to the vertical pull within a kiloparsec of the disk against a radial enhancement of more than a factor of two: a prediction for the Milky Way data.
6. **§7** — matter and its threshold. The partition is by kind of wave: a kind with a lowest energy can be held in place as matter, a kind without one cannot. The Ocean's own amount and phase are written out as two coupled fields. The electron's 0.511 MeV is the lowest energy of its own kind of wave, set by the field the dynamo sustains; 386 fm is the electron's own localization length, and the Ocean's healing length lies near the Planck length.
7. **§8–§9** — limiting regimes; black holes (no accumulation, stripping as the no-hair theorem, Hawking radiation, recycling rather than draining) and the traveler falling in, now also in the rebuild's terms; conservation conditions, nothing is destroyed, and where a wave's energy goes.
8. **§10** — relation to existing work: what is inherited and what is not, set out as labeled lists, and the known deficiencies against current practice and measurement.
9. **§11** — one speed and the split; the candidate current through time; the strong field and the point of no return; frame dragging, carried by the re-made tilt rather than quantized lines, with the phase needing no whirl even at a spinning black hole; the edge and the core, with the turnaround density bounded by the triple pulsar PSR J0337+1715; what the Ocean must be made of.
10. **§12** — new in 3.12, the rebuild and the law. Building, with three arrows and a left twist, makes matter and time; reclaiming, with a right twist, unmakes them and is antimatter. Time is made in the build, each place making its own, and gravity is the uneven making of time. The Ocean itself is rebuilt the same way. The Earth's rebuild is worked through step by step; antimatter stays hidden because it runs into a past that was never a present; the collapse ends a beat. The law states what a build carries and the rules for each quantity, the Ocean's own waves, and the strength of gravity from a count of the kinds of wave the plexus carries: with fifteen builds per family gravity attracts and the medium's smallest scale lies near the Planck length. It commits to one prediction, neutrinoless double-beta decay.
11. **§13–§15** — new in 3.12, all open items gathered in one section; the research program in dependency order; a summary.
12. **Appendix A** — new in 3.12.1, the rebuild of a spinning black hole: Sagittarius A* taken through the same steps as the Earth's rebuild of §12.3, a table comparing the two regimes, and what the account settles and leaves open. Also issued as a standalone PDF.

## Known open problems

Stated in the paper (§13), repeated here so that they are visible before reading:

- **Flow versus build.** How the Ocean's behaviors divide between its flow and the rebuild, most likely a bit of both. Several sections use the flow picture (gravity as a current slowed by drag, expansion as divergent flow, black-hole inflow, the geometry built from the flow, the larger current that sets a galaxy's eddy); the law of §12 says nothing feels drag.
- **The phase rate today.** What sets it. The slow rate the paper uses is not derived; stiffness alone allows it up to about 10¹⁷ eV.
- **Which waves the dynamo makes.** The kind, version and extent of a pattern, and with them the threefold mixing of the strong force and the three families, are not yet derived.
- **The leftover.** The rebuild must give the matter remaining at the start of the beat, a baryon-to-photon ratio of about 6.1 × 10⁻¹⁰.
- **The plexus's own waves.** Their spectrum and health are not yet checked.
- **Deriving gravity from the medium.** General Relativity's geometry outside a non-spinning mass and frame dragging to first order are obtained; the full law, spinning black holes beyond first order and merger ringdowns are not yet covered.
- **The galactic swirl.** How the larger current puts the eddy's tilt in place, how patterns read it, and what sets its strength from a galaxy's baryons are open; the vertical prediction must be confronted with the full Milky Way analysis.
- **The scale hierarchy and its twin.** Galactic effects act across kiloparsecs while the medium's own scale lies near the Planck length; and the electron's lowest energy lies nearly 10²³ below that scale, which the field the dynamo sustains must explain.
- **The measured vacuum.** Vacuum polarization, light-by-light scattering and vacuum birefringence must be reproduced quantitatively from the plexus.
- **The sign of the self-interaction.** If the medium is focusing in its present state, nothing arrests concentration and the framework is not viable as written.
- **The preferred frame.** Treating the vacuum as a medium gives it a rest frame; compatibility with the tight limits on Lorentz violation has not been demonstrated.
- **Black-hole cores and the turn.** The turnaround of collapse rests on one candidate mechanism, a loosening of the Ocean's grip at extreme density; what turns a beat's collapse into the next beat is open.
- **Size and spin.** The localized excitation must appear pointlike to probes at about 10⁻¹⁸ m, and spin ½ must come from the order the dynamo makes.
- **The viscous stress.** Whether Π_μν has any role; if it does, its first-order form must be replaced by a causal one.
- **The committed prediction.** Neutrinoless double-beta decay must occur. If the neutrino masses are shown to be ordered so that its rate cannot be small, and the next generation of searches does not see it, the account of the family fails.

## Citing

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23142440-blue)](https://doi.org/10.5281/zenodo.23142440)

Please cite the archived release rather than the repository.

- **All versions** — `10.5281/zenodo.23142440`. Resolves to the latest release. Use this when citing the work as an evolving artifact.
- **Version 3.12.1** — assigned on release.
- **Version 3.12** — `10.5281/zenodo.23812291`.
- **Version 3.11** — `10.5281/zenodo.23718695`.
- **Version 3.10** — `10.5281/zenodo.23586999`.
- **Version 3.9** — `10.5281/zenodo.23549277`.
- **Version 3.8** — `10.5281/zenodo.23488580`.
- **Version 3.7** — `10.5281/zenodo.23368921`.
- **Version 3.6** — `10.5281/zenodo.23324587`. Earlier version DOIs are listed on the Zenodo record.

> Hays, K. (2026). *Scalar–Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium. A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology* (Version 3.12.1) [Preprint]. Zenodo. <https://doi.org/10.5281/zenodo.23142440>

## License

Dual-licensed, because the repository holds both a document and a program.

- **The written work** — the paper, its generated LaTeX source, and the prose embedded in the build script — is licensed **CC BY 4.0**. See [`LICENSE`](LICENSE).
- **The build tooling** — `build_ocean_formalism.py` as a program — is licensed **MIT**. See [`LICENSE-CODE`](LICENSE-CODE).

© 2026 Keith Hays
