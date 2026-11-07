# v3.14 validation report

**Read by:** Claude (Fable 5.1), 7 November 2026, from Keith's validation prompt (`claude/argon-validation-prompt-3.14.md`). **Disclosure:** this is the session that produced the draft, so it is not an unseen reader. To compensate, every number below was recomputed in a fresh script written without reading the check suite (`recompute.py`, 35 items), the generated text was read in full from the PDF, and the comparison with 3.13.1 was made by diffing the two scripts rather than from the change record.

**Method.** Rebuilt from the project copy of `claude/build_ocean_formalism_3.14-draft.py` (identical to the working copy): **document digest 3d68-158b-66e3, 74 pages, 21 parts**, as expected. Every part token seen in the end lines: Abstract d098a6, Preface 430476, Glossary 0a791a, §1 c6c077, §2 2bd699, §3 c5371c, §4 bf999b, §5 88ec54, §6 68bb8a, §7 f72705, §8 accc26, §9 f0a01d, §10 743e35, §11 5acec0, §12 c46dba, §13 495c6f, §14 d09a31, §15 ef5186, Appendix A 95a73b, Appendix B 30ed33, References 64e11e; reading manifest on page 74. Check suite reproduced: **86 checks, 85 pass, 1 note, 0 fail** (the note is the bold-w/plain-w typeface note). LaTeX log: no overfull lines, no unresolved reference or citation. Equations and inline math diffed against 3.13.1 (digest ab74-7444-62ce): 774 items before, 824 after.

**Verdict.** No mathematical error. Every new number is reproduced independently (table in §4). The corrections that claim to be words only are words only: the diff shows exactly three real changes of mathematics, all presented as such (Eq. 37's free-fall form in place of r²(1 − 2M/r)f′ = 4M²; the Kerr slicing √(2Mr(r² + a²)) in place of 2Mr₊; Eq. 38 added), plus the removal of the 3.13.1 intake rate ∝ μ∞²M² and of the c₀H₀/2π figures, both consequences of those three. The eleven decisions are carried through the paper with the exceptions in B below. Two are substantive enough to fix before release: §6's open list still asks what 3.14 answered (B8), and §12.3 says the Ocean's own build is supplied through the dynamo, which §12.7 now contradicts and cross-references (B6). The rest are single words.

---

## A. Mathematical errors

None found.

## B. Contradictions with a 3.14 decision

**B6. §12.3, p. 50, and §12.5, p. 52: the Ocean's own build and the dynamo.** §12.3: "A pattern's build is supplied from the Ocean around it, while the Ocean's own build is supplied by its flow, through the dynamo; that is why the drive running out ends a beat (Section 12.5)." §12.5, item 1: "the flow no longer drives the dynamo, and builds are no longer supplied." §12.7 (new in 3.14) says: "The settled Ocean falls freely because it borrows nothing: its build needs no more than it carries (Section 12.3)", and cross-references the §12.3 sentence that says the opposite source. Decision 6 keeps the flow's work powering the plexus apart from the supply of builds. *This one needs Keith's ruling, not a wording fix:* either the Ocean's own build is supplied by the Ocean's energy at each place (then §12.3 and §12.5 should say the beat ends when the flow no longer powers the dynamo and the plexus is no longer kept running, and §12.5's "builds are no longer supplied" should say what is no longer supplied), or the dynamo does supply the settled Ocean's build, and §12.7's sentence should say so. Raised on 7 Nov 09:28; not yet answered.

**B8. §6 "What is open", p. 24.** "The limit's value and the factor 2π; how much each build borrows at a place, and what sets the most one place can have on loan; … an eddy set by mass alone". The same section's limit paragraph (A1, applied) states what sets it (the settled Ocean's own energy per volume) and replaces the 2π with the factor 0.2, not derived; §13.1 was updated to match ("the factor in its closeness"). Fix: "The limit's value and the share of the settled Ocean's energy per volume it takes; how much each build borrows at a place; … an eddy whose strength follows the mass at its middle alone".

**B3 (minor). §7.2, p. 28.** "there are two branches … One has no gap: the sound of the phase, with c_s² = (1 + a)/(1 + 3a)". The paragraph opens "Perturbing the minimal law, Equation (28)", so it is labeled, but a reader does not learn here that in the build's terms the phase's branch is absent. Fix: add "; in the build's terms the phase carries no wave of its own (Section 12.7)".

**B4/B6 (wording). §5.1, p. 17.** "Near a black hole the settled Ocean does flow inward, falling freely as every pattern does". §11.9, p. 44: "the Ocean's own phase flows inward with the traveler". Decision 6 names this motion the fall, to keep it apart from the flow's work. Fix: "the settled Ocean falls inward, freely, as every pattern does"; "the Ocean's own phase falls inward with the traveler".

## C. Borrowed reasoning

**C1. §5.2 "Where the heat comes from", p. 19 (marked [Candidate]).** "A laboratory superfluid has two parts, the superfluid itself and a normal fluid that is its heat, a gas of its own ripples, and above its lambda point it is all normal fluid. The compressed Ocean at the turn is all heat, above its lambda point." The lambda point is liquid helium's; nothing in the Ocean's law gives the compressed Ocean a transition of that kind, and the sentence states the Ocean's turn in helium's terms. It is attributed by the comparison and tagged [Candidate], and it sits in the open section's territory (the turn is for 3.15). Suggest: "The compressed Ocean at the turn is all heat, as a laboratory superfluid above its lambda point is all normal fluid; whether the Ocean has such a point is open (Section 13.1)."

**C2. "Normal component" (glossary; §2.3; §5.1; §12.5; §14).** A superfluid-physics term used in the paper's own voice for the Ocean's heat. It is introduced with the helium comparison in §5.1 and the glossary, so it is attributed as an illustration; §5.1's "an illustration of why the factor appears, not evidence for the reading" (new in 3.14) carries the right weight. No change required, noted because Keith asked for every borrowed term.

**C3. §11.9, p. 43: the loosening grip's form.** Labeled and cited as decided ("That is the bounce equation of loop quantum cosmology … the Ocean borrows the form, not the reason", refs [73], [74]); the times and the ρc bound are marked as the illustration's; §13.1, §14 and Appendix A say the Ocean's own form is not derived. Carried through.

Nothing else found: "river model" [hamilton2008], "healing length" (named as a laboratory term in the preface), "superfluid helium-3 A" [35], and the laboratory horizons [unruh1981, steinhauer2016] are attributed where they appear. "Virial", "isothermal", "MOND" and "Silk damping" do not appear in the paper's own voice.

## D. Rule and wording problems

**D1. §6, p. 23: "pull".** "a fixed limit gives the measured share of the pull at the half-light radius that the stars and gas do not supply" (new in 3.14). The paper's own voice does not use "pull". Fix: "the measured share of the turning at the half-light radius that the stars and gas do not supply".

**D2. §6, p. 23: "still".** "is therefore still taken from measurement." Prior-state word in the body. Fix: "is taken from measurement."

**D3. §6, p. 24: "now".** "the smoothing inside R_t, now favored but not derived". Fix: "favored but not derived".

**D4. §10.3, p. 37: "now".** "The plexus's frame law now gives the geometry's law, Einstein's form in full (Section 12.9)". Fix: "The plexus's frame law gives the geometry's law …".

**D5. §7.6, p. 30: "particle-like".** "Particle-like behavior does not require smallness. An excitation appears particle-like because it exchanges energy, momentum and charge in whole units and at a single point." The convention keeps "particle" to other work's terms. Fix: "Point-like behavior does not require smallness. An excitation appears point-like because …", or "in the standard model's terms, particle-like".

Checked and clean: American spelling throughout (no British forms found); "universe" only in "the observable universe" and in reference titles; "no longer" in the body only as physics ("no longer supplied", "can no longer form"), not as the paper's prior state; "particle" otherwise only in reporting other work or in reference titles.

## E. Layout

Clean. Abstract 1,859 characters without the disclaimer (limit 1,920); reader's note on page 1; the preface opens page 2 as its own part; no heading at the foot of a page, no part's end line alone, no gap over five lines except where a part opens a fresh page (end of abstract, preface, §15, Appendix A, the manifest); citations numbered in order of first citation, 1–83, bibliography in the same order; every cross-reference and citation resolves.

**E1 (packaging, not the paper).** `check_ocean_math.py` imports three sibling scripts (`rulers_direction.py`, `rotor_lines.py`, `fd_cancel.py`); run alone it reports 3 failures (FileNotFound). The validation prompt should say to copy the whole `claude/checks-3.14/` folder, or the suite should say so in its header.

## F. Notes needing no change

- **F1.** §6 "a galaxy seen at redshift 2.3 would have a limit 3.4 times today's": 3.39 with Ω_m = 0.30, 3.46 with Planck's 0.315. Consistent with the "3.32 at 2.2" elsewhere only if Ω_m ≈ 0.30 is used in one place and 0.315 in the other; both round to the text. Worth one parameter throughout at some point.
- **F2.** The second revision now ends "(The ninth revision reads this match differently.)" and the ninth gives the reading; the account is consistent and in time order.
- **F3.** The eddy enters the account in the ninth ("placed galaxies in eddies"); the tenth says how it acts; the eleventh what holds it. The preface's opening list ("What it might explain") uses "the energy rebuilt in the eddy" and so does the abstract; no "its own energy" remains anywhere.
- **F4.** §12.7's Eq. 38 paragraph states the zero net current outright (validation C1 settled). §2.2's "the build supplies that charge" stands and is the same fact counted the other way.
- **F5.** Event-horizon and particle-horizon ratios (1.5, 5) are the physical (not comoving) horizon distances; my first comoving attempt gave 1.63 and 0.48 before I used the right quantity. The text says "the horizon of the moment", which is the physical one; fine.
- **F6.** Out-of-scope items are presented as open everywhere they appear (the grip's form in §11.9, §13.1, §14, Appendix A; the turn in §13.1; Appendix B says it uses the model Milky Way).

---

## 4. Numbers recomputed (all agree)

| Claim (new or changed in 3.14) | Paper | Recomputed |
|---|---|---|
| Eq. 37, (∇θ)²/μ² with (1 − 2M/r)f′ = √(2M/r) | −1 exactly | −1 to 4 × 10⁻¹² over r = 2.0001M … 200M |
| Fall speed √(2GM/r): 1 AU; Earth's surface | 42; 11.2 km/s | 42.1; 11.19 |
| Kerr slicing ΔF′ = √(2Mr(r² + a²)), (∇θ)²/μ², a = 0 … 0.999, inside both horizons | −1, regular | max deviation 3 × 10⁻¹¹ at 4000 random points per spin; exact by hand (numerator −ΔΣ) |
| Eq. 38 settled state s = −v²: w; energy; net current 2(v² + s)μ | −1; V₀ − v²μ₀²; 0 | −1.000000000000; equal; 0 |
| Eq. 38 departure, μ held: extra pressure / extra energy | 0 (dust) | 0 |
| Central pushback g†²/4πG | 1.7 × 10⁻¹¹ Pa | 1.72 × 10⁻¹¹ |
| cH∞ (H₀ = 67.4, 73; Ω_Λ = 0.685, 0.69) | 5.4–5.9 × 10⁻¹⁰ m s⁻² | 5.42, 5.89 × 10⁻¹⁰ |
| g†/(cH∞) | 0.20–0.22 | 0.221, 0.204 |
| … with g† ± 0.26 × 10⁻¹⁰ (sys) | 0.16–0.27 | 0.16–0.27 |
| Loan cap ÷ settled energy per volume | about a tenth | 0.098 (67.4), 0.083 (73) |
| Virial identity, whole loan ÷ whole pushback, hydrostatic V²/4πGr² sphere | 3 | 3.0000 |
| Horizon-of-the-moment limits at z = 2.2 (Ω_m 0.315): Hubble; event (physical); particle (physical) | 1.5 to 5 (3.32, 1.53, 5.29 in the record) | 3.32; 1.53; 5.23 |
| Share 2GM/(c²r) at the horizon; fall speed ÷ c√share | 1; 1 | 1.000000000000; 1 − 3 × 10⁻¹⁶ |
| Sound speed of a gas of waves at one speed | c/√3 | ⟨cos²⟩ = ⅓ |
| Light set free (Planck 2018 parameters, z* = 1090) | about 380 000 yr | 371 000 yr |
| Turnaround (illustrative form, ρc = 2.4 × 10²³): 10 M☉; Sgr A*; M87* | 10⁻⁴ s; 28 s; 12 h | 6.6 × 10⁻⁵ s; 28.2 s; 11.9 h |
| ρc from PSR J0337+1715, \|Δ\| < 2.6 × 10⁻⁶, ⟨ρ⟩ ≈ 6 × 10¹⁷ | ≳ 2.4 × 10²³ kg m⁻³ | 2.3 × 10²³ |
| ℓ = (ħ/ρc c)^{1/4} | ≲ 0.035 fm | 0.035 fm |
| Model Milky Way: V from V⁴ = GMg†, M = 6 × 10¹⁰ M☉ | 176 km/s | 176 |
| M for V = 200, 230 km/s | 1.0–1.8 × 10¹¹ M☉ | 1.00, 1.76 |
| MicroBooNE 2025: excludes a single light sterile neutrino as the LSND/MiniBooNE explanation at 95% CL; three kinds fit, p = 0.96 | as stated | matches `references/microboone-2025-two-beam.note.md` |
| Abstract length | < 1,920 characters | 1,859 |

## 5. Suggested handling

**Before release:** B8 (one sentence in §6's open list), D1–D4 (single words), B3 and B4 (a clause each). All are words; none touches an equation.

**Needs Keith's decision before release:** B6, because §12.7 now cross-references §12.3 for a claim §12.3 does not make. The paper should say one thing about what supplies the settled Ocean's build.

**Can wait:** C1 (the lambda-point sentence is tagged [Candidate] and belongs with the 3.15 turn work), D5, F1, E1.

---

## 6. Resolution (7 Nov 21:18, Keith: "fix everything because we are getting ready to publish")

Keith settled B6: "The oceans flow runs the dynamo full with a left twist. The dynamo provides the power to the plexus which supplies the energy to the build." Consistent with the equations (Eq. 38's supply term is the plexus's feed, its coupling not yet written; the closed loop is the settled state's w = −1). Applied: B6 (§12.3, §12.5, §12.7), B8, B3, B4, D1–D5. Left as noted: C1, F1, E1. Keith added (21:20) that the plexus supplies the build by recycling, the energy of the built plexus being reclaimed to do it; §12.3, §12.5 and §12.7 say so. Rebuilt: and (21:22) that a pattern's build always needs more than the pattern carries and borrows the rest, only the settled Ocean's not. Keith then (21:25) withdrew "always": a pattern that borrowed nothing is not precluded but would have to be made of settled Ocean, and none is known. Rebuilt: digest **ef19-c44f-56b7**, 75 pages (§15 opens a fresh page again); checks 86: 85 pass, 1 note, 0 fail; the only change to the math is the removal of the `2π` symbol from §6's open list.

