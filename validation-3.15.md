# v3.15 validation report

**Read by:** Argon, an independent reviewer that had not seen the work being produced, 12 November 2026, from the validation prompt for 3.15. Argon reported only; the changes below were made afterward from its report. Its full report is reproduced here in summary; quoted findings are in its words.

**Method.** A complete reading of the 81-page PDF (22 parts) and an independent recomputation, from CODATA constants and the primary literature, of every equation, number and cited observational value new or changed in 3.15. Argon had the PDF only, not the build script or the check suite, so it did not run the checks; it recomputed instead.

**Digest read:** `365e-0a05-aa10` (81 pages, 22 parts, "End of document" on page 81). Part tokens seen, all 22, matching that build's manifest: Abstract e7b767, Preface 1cab55, Glossary d44418, §1 c6c077, §2 ad88f1, §3 c5371c, §4 bf999b, §5 36797d, §6 fbb7fe, §7 6eb475, §8 0ab2c2, §9 6f7f5f, §10 18c371, §11 919470, §12 fb6473, §13 3719ff, §14 f47b66, §15 0953d9, Appendix A cc6fd7, Appendix B 72cba1, Appendix C 114815, References 107198.

**Released digest:** `a3b9-ab23-4d9c`, after the fixes below (wording only; no equation or number changed). Check suite on the released text: 93 checks, 92 pass, 1 note, 0 fail.

## Verdict (Argon)

"Version 3.15 is mathematically sound, internally consistent, and nearly ready for release. Every equation and numerical result introduced or updated in 3.15 … checks out upon independent recomputation. The nine locked decisions of 3.15 are carried faithfully across the Preface, Glossary, body sections, and Appendices A–C." It found seven wording or rule problems and one comparison to make explicit, and no unattributed borrowed reasoning.

## Findings and how each was handled

| Finding | Where | What Argon found | Handled |
|---|---|---|---|
| A.1 | §6 | "some 10²¹ times as much" beside §12.7's "some 10²⁰ times the energy of the flow": both right (one against an eddy's central loan, one against the flow's energy), but the referent unclear | §6: "some 10²¹ times that amount, and some 10²⁰ times the flow's energy per volume (Sections 12.3 and 12.7)" |
| B.1 | Appendix A, step 6 and table | "the rotational loan", "spin loan" detach the loan from the builds | "what the hole's builds hold on loan for its spin"; "Total rest energy held on loan by the builds inside the horizon; the part held for its spin extractable in the ergosphere" |
| D.1 | Preface, twelfth revision | "no extra pull" in the paper's own voice | "no extra turning" |
| D.2 | §14, "Galaxies with no eddy" | "pull" twice | "extra turning" twice |
| D.3a | Preface; §11.9 | "What is now called dark energy"; "With r now the areal radius" | "What other work calls dark energy"; "With r here the areal radius" |
| D.4 | Appendix A | unspaced dashes where the rest of the paper spaces them | spaced to match |
| F (note) | Preface epigraph | "universe" outside "the observable universe" in a general epigraph | kept by the author; the epigraph reads "exquisite in detail" |

Argon's other checks passed: the abstract under arXiv's 1,920 characters; the reader's note on page 1 and the preface from page 2; no stranded heading or lone end line; every equation reference (1)–(42), section and appendix reference resolving; all 90 references in order of first citation. Borrowed material is attributed where it appears: loop quantum cosmology as reaching the same expansion equation for its own reasons [80, 81]; Hawking, Jacobson, Unruh, Brout et al. and Barbado, Barceló & Garay for the radiation; the laboratory superfluid marked as an illustration; the river model of black holes kept apart from the Ocean's rivers; the collision account of NGC 1052-DF2 and DF4 marked as its discoverers' reading.

## Numbers recomputed by Argon

| Claim | Paper | Argon |
|---|---|---|
| Dent energy, ħc₀κ_cut | about 3.5 E_P | 3.545 E_P (κ_cut = √(4π)/l_P) |
| Critical energy density ε_c = 3c₀⁴/(8πGξ²) | about 1.5 Planck energy densities | 1.500 (dent √(4π) E_P); 1.462 (dent 3.5 E_P) |
| Critical mass density | near 10⁹⁷ kg m⁻³ | 7.73 × 10⁹⁶ kg m⁻³ |
| A dent-width region's contents, as a share of a dent | about 1/25 | 1/24.67 (1/24.5 at 3.5 E_P) |
| Expansion with the grip | H² = (8πG/3c₀²)ε(1 − ε/ε_c); dH/dt = −4πG(ε + p)(1 − 2ε/ε_c)/c₀² | exact; sign flips at ε_c/2 |
| Share in a neutron star's core | about 10⁻⁷⁹ | 1.3 × 10⁻⁷⁹ |
| Fall from rest far away to the center, (4/3)GM/c₀³ | 7 × 10⁻⁵ s (10 M☉); 28 s (Sgr A*); 12 h (M87*) | 6.57 × 10⁻⁵ s; 28.24 s; 11.86 h |
| Longest time inside, πGM/c₀³ | 66 s (Sgr A*); 28 h (M87*) | 66.54 s; 27.94 h |
| Step bound, 5 M☉ over 10¹⁰ yr | ≤ 6 × 10⁻¹⁹ m | 5.77 × 10⁻¹⁹ m |
| Return with dent-width steps | about 10²⁷ yr (5 M☉); 10³⁹ yr (Sgr A*) | 1.26 × 10²⁷ yr; 9.35 × 10³⁸ yr |
| Far time per e-fold of the clocks parting | 4GM/c₀³ | 4GM/c₀³ |
| Hawking temperature | about 60 nK (1 M☉); 1.4 × 10⁻¹⁴ K (Sgr A*) | 61.69 nK; 1.435 × 10⁻¹⁴ K |
| Glow traced back to a dent's scale | about 2 ms (1 M☉); 2.5 h (Sgr A*) | 1.75–1.81 ms; 2.47–2.54 h |
| Falling traveler at the crossing | about 4 T_H, 6 × 10⁻¹⁴ K (Sgr A*) | 5.74 × 10⁻¹⁴ K |
| Eq. 39 with V₀ = 2v²μ₀² | ε = v²μ₀² = −p | exact |
| Flow's energy per volume | 5–6 × 10⁻¹⁰ J m⁻³ | 5.2–6.2 × 10⁻¹⁰ J m⁻³ |
| The Earth's builds' loans per volume | about 2 × 10¹¹ J m⁻³ | 2.07–2.30 × 10¹¹ J m⁻³ |
| Against the flow's energy; against an eddy's central loan | 10²⁰; 10²¹ | 3.8 × 10²⁰; 3.8 × 10²¹ |
| c₀H∞ | 5.4–5.9 × 10⁻¹⁰ m s⁻² | 5.41–5.86 × 10⁻¹⁰ m s⁻² |
| g†/(c₀H∞) | about 0.2 (0.16–0.27) | 0.205–0.222 (0.160–0.270) |
| Central pushback g†²/4πG | about 1.7 × 10⁻¹¹ Pa | 1.717 × 10⁻¹¹ Pa |
| An eddy's central loan as a share of the flow's energy | about a tenth | 0.03–0.10; order a tenth confirmed |
| NGC 1052-DF4 (van Dokkum et al. 2019) | stars about 1.5 × 10⁸ M☉; clusters roughly 4 km s⁻¹; stars alone about 7 km s⁻¹; usual galaxy about 30 km s⁻¹ | (1.5 ± 0.4) × 10⁸ M☉; 4.2 (+4.4/−2.2) km s⁻¹; 7.0 km s⁻¹; about 30 km s⁻¹: match the source |

## Earlier readings of this version

Argon read an intermediate state on 11 November (digest `ca45-b3f4-0d59`) and found one leftover, in §14 ("the inward lean toward stopped time"), which was fixed. The drafting session also validated its own work; that reading was not independent, and several wording problems reached the author or Argon first. The final reading above is the independent one.
