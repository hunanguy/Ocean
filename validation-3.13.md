# v3.13 validation and consistency report

**Read by:** Claude (Fable 5.1), 3 November 2026. Full reading of the published v3.13: 71 pages, 20 parts, every part token seen in the footers and end lines (fec17c, 893104, c6c077, 60b342, 265287, bf999b, 104ec2, 138edb, f72705, d07fc2, 434ca9, 2ec111, 64d8f8, a2f3b7, e4b52c, 44a7b2, ef5186, 45c30c, ebf97f, 6aa4a5), ending at the reading manifest. **Document digest 5c47-4c91-967c.** The local build from the published `build_ocean_formalism.py` reproduces that digest exactly.

**Checks.** `checks/check_ocean_math.py` on the published source: 83 checks, 82 pass, 1 note (the bold-w/plain-w typeface note), 0 fail. A dozen numbers recomputed independently of the suite (below) all agree.

**Verdict.** No mathematical error found. No broken cross-reference or citation. The 3.13 decisions (flow versus build, no drag, the build supplying the current, the eddy acting through its load, rulers by direction, the plexus law) are carried consistently through the paper with **one exception** (A1) and a handful of passages that still speak in the earlier voice or understate what 3.13 settled (B). Nothing below changes a result; all of it is wording.

---

## A. Contradiction with a 3.13 decision (fix in 3.13.1 or 3.14)

**A1. §2.3, p. 13.** "Whether the vacuum's response can reproduce effects conventionally assigned to dark-matter halos does not rest on Πμν: in a galaxy that response is **the tilt of the eddy** in which the galaxy sits (Section 6)." Section 6 now says the eddy acts through its energy (the load) and that a tilt alone cannot do it; the in-plane tilt is at most 15–19 km/s. Replace "the tilt of the eddy" with "the energy of the eddy, which adds to the load". This is the only sentence in the paper that still states the superseded mechanism as the mechanism.

## B. Stale or imprecise passages (no result changes)

**B1. §14, group 2, "Derive gravity from the medium (decisive)", p. 55.** Ends "extend the account to perihelion advance, frame dragging and gravitational radiation, or identify where it fails." All three are now obtained to the order stated: β = 1 (§11.7), frame dragging to first order and Kerr outside beyond it (§11.8), the binary-pulsar decay at 0.9983 (§12.7). The item should say so and keep only what remains: Eq. (1) in general, from the medium.

**B2. §14, group 2, "Antimatter and circulation sense", p. 57.** "Derive from the rebuild that partners have identical mass and magnetic moment" — §10.4(5) now says this follows exactly because the partner is the same wave run backward (§12.9 test 5). Keep "opposite electric charge" and the CPT/Lorentz confrontation; drop or reword the mass/moment part.

**B3. §14, group 1, "The waves the dynamo makes", p. 55.** "This is where the three parts of the strong force's mixing and the three families must come from." §12.8, §12.9 and §13.1 now say the plexus law fixes three complex directions and exactly three families; what remains is that the dynamo makes exactly these. Align the wording with §13.1.

**B4. §13.2(3), p. 53.** "the cosmic-ray bounds place any such effect beyond the Planck scale" sits beside §12.9 test 7, where a quadratic grain at the dent (3.5 E_P) passes Auger by only a factor 1.35. "Beyond" should read "at or above about the Planck scale, and a quadratic grain at the dent passes the cosmic-ray bound by only about 1.35 (§12.9)."

**B5. §5.1 "One root, two effects", p. 16.** Two accounts of the fixed energy density stand side by side: "the uniform change is supplied by the build: each place keeps its amount ρ at v and its turning, so the Ocean, flowing apart, keeps its energy per volume" and, two sentences later, the 3.11 wording "a medium with negative pressure does work on itself as it flows apart, adding energy at the rate that keeps its energy density fixed." They are the same fact in the Ocean's words and in the standard words; say so in one clause ("which is how the standard description states the same thing"), or drop the second.

**B6. §8.2, pp. 27–28.** "the traveler crosses intact, carried by a swift current that is barely felt" and "the Ocean's own phase flows inward with the traveler" are the flow picture the 1 Nov sorting kept for black holes ("both"). They stand 20 pages from §12.1's "a star is not carried by a current: it is rebuilt at every moment" and Appendix B step 5's "It is not carried by a current". One sentence in §8.2 reconciling them (the gentle inflow of §11.9 is the Ocean keeping in step; the traveler is rebuilt within it) would spare a careful reader the apparent conflict.

**B7. §6, "The limit does not follow the expansion", p. 20.** "The limit at redshift 2.2 to 2.4 was at most 1.0 to 2.7 times today's." That range is the bound from one galaxy (zC 400569) across the three smoothings. The tightest galaxy under the favored cored smoothing (zC 406690) gives at most 1.2 times today's; under the other two smoothings it bounds below 1.0, i.e. it wants less eddy than a fixed limit gives, which the working note records as a point against the model, not the bound. Say which galaxy sets the quoted bound, or quote the tightest (≤ 1.2) under the favored smoothing. The conclusion (H(z) needs 3.25–3.5) stands either way.

**B8. §6 and Appendix B.** The model Milky Way's eddy speed is V = 176 km/s (Appendix B step 2), so its rotation curve far out is flat at about 176 km/s, while the observed outer Milky Way runs at roughly 200–230 km/s. §6 half-says this ("the model's stars and gas are on the light side": 201 vs 229 at the Sun). It should say it plainly for the flat part too: V⁴ = G M_b g† puts the model Milky Way at 176 because M_b = 6 × 10¹⁰; the observed flat speed would need about 1.5 × 10¹¹ by the same relation, or the Milky Way sits off the baryonic Tully–Fisher relation. This is a known tension for the Milky Way in the RAR literature, not something 3.13 introduced; it just should not be left for a reader to discover.

**B9. §11.8, "The rule", p. 41.** "A pattern's disturbance includes the slowed Ocean around it (Section 6)." The pointer survives from when §6 carried that sentence; §6 "One structure, not two" now only says a galaxy and its eddy are one region. Point to §12.3 step 8 (the surroundings are rebuilt with everything the Earth carries) instead, or drop the pointer.

## C. Notes, no change needed

- **Glossary "Carrying speed" and "Speed of light", §2.5, §11.1, §15:** "seen from afar it varies, and that variation is gravity" is the sixth-revision wording; §12.2 says gravity is the uneven making of time. They are the same statement at two levels (slower clocks from afar = less time made), and §12.2 and the preface already connect them. Fine as is.
- **§8.1 and Appendix A step 4, "typical wavelength about eighty times the horizon radius":** this is Giddings's thermal wavelength λ_T = 2π/T = 8π²R ≈ 79R, as cited. A reader expecting the blackbody peak will get 16–28 R. The word "typical" with the citation is adequate.
- **Abstract, "the limit has not followed the slowing of the expansion over eleven billion years":** stated flatly in the abstract; §6 qualifies it ("strong in direction and loose in size"). Acceptable for an abstract, given B7 holds.
- **§12.9 test 4 "5.8 × 10⁻¹⁸ of the dent":** recomputed, 5.76 × 10⁻¹⁸ with the dent at 3.54 E_P.
- **The flow language retained in §5.1, §8.1, §8.2, §11.9, Appendix A** is as the 1 Nov sorting decided (expansion, being carried, black holes: both). Consistent with that decision.

## D. Numbers recomputed independently of the check suite (all agree)

| Claim | Paper | Recomputed |
|---|---|---|
| Electric/gravitational force ratio, two electrons | 4 × 10⁴² | 4.17 × 10⁴² |
| Galaxy's own tilt at the Sun, (2+2γ)u v_c | a few × 10⁻⁴ km/s | 3.2 × 10⁻⁴ km/s |
| Share of capacity near the Sun from v_esc = 528 km/s | a few millionths | 3.1 × 10⁻⁶ |
| Sun's share at the Earth's distance | ~2 × 10⁻⁸ | 1.97 × 10⁻⁸ |
| Earth's record reaches the Moon | 1.28 s | 1.282 s |
| Ġ/G bound over the expansion epoch (2σ) | < 4 × 10⁻⁴ | 3.3 × 10⁻⁴ |
| Sgr A* horizon radius | 12.7 × 10⁶ km | 12.70 × 10⁶ km |
| Sgr A* Hawking temperature | 1.4 × 10⁻¹⁴ K | 1.43 × 10⁻¹⁴ K |
| Head-to-foot tide at Sgr A*'s horizon | ~10⁻⁴ g | 1.1 × 10⁻⁴ g |
| Share at the photon orbit | two-thirds | 2/3 |
| Eddy fraction of turning at the Sun, 1 − 1/1.59 | 37 percent | 37.1 percent |
| V = (G M_b g†)^{1/4}, M_b = 6 × 10¹⁰ | 176 km/s | 175.8 km/s |
| Joining field / dent | 5.8 × 10⁻¹⁸ | 5.76 × 10⁻¹⁸ |

## E. Suggested handling

A1 and B1–B4 are one-line edits and could go out as 3.13.1 with the DOI chain intact, or be folded into 3.14. B5–B9 are two or three sentences each. None affects the check suite's anchors except A1 (no anchor on that sentence) and B7 (the "1.0 to 2.7" string is anchored in the Genzel check; change both together).
