# v3.16 validation report

**Read by:** Fable 5.1, an independent reviewer that had not seen the work being produced, 25 November 2026. Fable reported only. The changes below were made afterward from its report, with the author's decisions on the points that were his to make. Its findings are summarized here, with quoted passages in its own words.

**Method.** A complete reading of the 90-page PDF (23 parts), checking every part's end line against the reading manifest, and an independent recomputation, in a Python script from CODATA and IAU constants and the paper's own stated inputs, of every number the paper gives. Fable had the PDF only. It did not have the build script, the check suite or the analyses' data, so it recomputed instead of running them.

**Digest read:** `441f-e1fe-6ae4` (90 pages, 23 parts, "End of document" on page 90). Fable saw all 23 part tokens, and each matches that build's manifest.

**Released digest:** `8563-1f7b-50ca`, after the fixes below. No result changed. The check suite on the released text gives 109 checks: 108 pass, 1 note, 0 fail.

## Verdict (Fable)

Of 108 quantities recomputed, 103 agree with the paper, two could not be confirmed because the conversion used is not given, and three disagree. Every number the thirteenth revision adds reproduces, among them the model Milky Way "to the decimal". The states of the Ocean, the microwave background and the eddy's new form are carried consistently through the paper, with one contradiction (finding B1). "Nothing found here ends the framework; the must-fix items are wording and one citation."

## Findings and how each was handled

Fable marked each finding must fix, should fix or note.

### Mathematics and numbers

| Finding | Where | What Fable found | Handled |
|---|---|---|---|
| A1 | §6, the eddy's edge | 100 to 230 kpc could not be reproduced from the stated inputs; the method is not given. | Confirmed: the method was not stated. Fable cut the eddy off at the edge with nothing beyond it, which gives 274 to 630 kpc. The paper counts the turning of the stars and gas and of the eddy out to the edge, with everything inside the edge acting as one mass beyond it; §6 now says so. The range is unchanged. |
| A2 | §12.7 | "A twenty-fifth of one dent's energy" contradicts Eq. (38)'s capacity of a dent-width region (a hundred-and-fifth). | Partly. There is no contradiction: Eq. (38)'s capacity over a sphere of radius ξ is exactly the twenty-fifth; Fable took a cube of side ξ. §12.7 now says "a region a dent's width in radius". |
| A3 | §6, Donato et al. | The error bar 140 (+80/−30) M☉ pc⁻² is misquoted; ±0.2 dex gives +83/−52. | Not changed. The paper quotes the source as the source gives it. |
| A4 | §6, §12.7 | The settled Ocean's share of the critical density, on which 5.8–6.2 × 10⁻¹⁰ m s⁻² and 6.0–6.9 × 10⁻¹⁰ J m⁻³ rest, is never stated. Back-solved, 0.727 to 0.764, and every number downstream agrees. | Confirmed. §5.1 now states it, 0.727 to 0.764 of the critical density, where the fit is reported; §12.7 points to §6 for the energy. |
| A5 | §12.9, preface | The joining field's size is 5.7 × 10⁻¹⁸ of the dent, not 5.8 (the dent had been rounded first). | Fixed: 5.7 × 10⁻¹⁸. |
| A6 | §7.2, §11.1 | "A k⁴ term of relative size 4a²" omits a factor k²/λv². | Fixed: the coefficient is about 4a² in units of 1/λv². |
| A7 | §6, Figure 2 | How 2678 degrees of freedom were counted is not said. | The count is right; §6 now gives it: 3168 measured speeds, less the stars' mass, distance and tilt of each galaxy and the bulge's mass of the 31 with one. |
| A8 | §14 | The dynamo's output over H₀ 70 to 73 is 4.1 to 4.9 × 10⁻²⁷ W m⁻³, not "about 4". | Fixed: 4 to 5 × 10⁻²⁷. |
| A9 | §6 | The conversion from the core's pushback to 130 and 230–300 M☉ pc⁻² is not given, and neither usual conversion gives both. | They are not a conversion: they are a separate fit of the eddy's core load with the cored profile Donato et al. use. §6 now says so. |
| A10 | §12.3, Appendix A | The Earth's binding energy is 4.6 × 10⁻¹⁰ of its rest energy, not "about four". | Fixed: about five parts in 10¹⁰. |
| A11, A12 | §8.1 | The Hawking wavelength's convention and Page's 10¹⁴ kg for pair emission. | Defensible as written; not changed. |

### Internal consistency

| Finding | Where | What Fable found | Handled |
|---|---|---|---|
| B1 | §13.1, §14 | Both say part of the flow's energy "can be lent", against §12.7 and the glossary (a loan draws on the Ocean at the dent's scale; only the plexus draws on the flow's energy). | Confirmed. Both now read: how much Ocean can be lent at a place, set by the flow's energy through the plexus, about one part in fifty of that energy. "The rest being what the patterns there need" removed. |
| B2 | Glossary, §5.2, Appendix C | The gas of light "expands and cools" between beats, where by the paper's own account no time is made and there is no flow. | Confirmed. It now loosens, which is not flow, and cools as it loosens; how it loosens is listed as open (§13.2, Appendix C), the candidate being that, with nothing built, nothing holds it in. |
| B3 | §9.1 | Argues against a reliance on viscosity the paper no longer has. | Rewritten: the settled Ocean dissipates nothing, so regularity cannot rest on its viscosities. |
| B4 | §4 | Offers alternatives for the big bang that the body no longer entertains. | §4 now gives the body's account and points to §5.2 and Appendix C. |
| B5 | §15 | Neutrinoless double-beta decay: §15 said its failure would end the account of the families, "not the framework", and did not say which mass ordering makes the test decisive. | Confirmed, and the error was the paper's: §15's own reason (a partner built in every family brings gravity's count to zero) means the framework fails with that account. §15 now says so, and names the inverted ordering as the decisive case. |
| B6 | §6 | "Where the galaxy is thin" is undefined. | Fixed: where the galaxy's own turning is far below the limit. |
| B7 | §12.7 | Cites §5.1 for the flow's energy, which is worked out in §6. | Fixed: Sections 5.1 and 6. |
| B8 | §6 | "The eddy is round, so … it answers" while §13.2 lists how it comes to as open. | Fixed: "is taken to answer". |
| B9 | §13 | The joining field's size appears four times. | One entry, in the plexus law's open items; the others point to it. |
| B10 | §6 | The limit's 1.12 (SPARC's own), 1.22 (the Milky Way) and the 1.20 carried. | Not changed: 1.20 is the measured value, used throughout; the fits' own values are reported as theirs. |
| B11 | Preface | The Hubble constant is §6's, not §5.1's. | Fixed. |
| B12 | Preface | Points to §14 for what could end the framework, not §13.1. | Fixed. |

### Borrowed reasoning and borrowed numbers

| Finding | Where | What Fable found | Handled |
|---|---|---|---|
| C1 | §6 | The eddy's far-out form, √(g_N g†) and V⁴ = G M g†, is modified dynamics', unattributed. | Fixed: credited to modified dynamics (Famaey & McGaugh 2012); the eddy departs from it through its second relation. Reference read and added. |
| C2, C3 | §12.8, §12.9, §13.2 | Standard-model results used as the framework's reasoning without citation: the balance conditions, the running of the three strengths, the argument for the joining field's shape, the seesaw scale and the strengths' near-meeting. | Fixed: each marked as the standard model's and cited (Particle Data Group 2024). Reference read and added. |
| C4 | §5.1 | The damping of the smallest spots is Silk damping, unnamed; "about 380 000 years" is the standard account's conversion. | Fixed: named and cited (Hu & Dodelson 2002); the light is set free once the expansion has cooled it to about 3000 K, a 1100-fold stretch, the measured fact, in §5.1 and Appendix C. |
| C5 | §12.4 | The baryon-to-photon ratio from the microwave background is the standard account's fit. | Fixed: said so. |
| C6 | §14 | "The measured Λ" is the standard account's fit. | Fixed: Λ as the standard account fits it. |
| C7 | §6 | The Milky Way's stars and gas "at their measured values" are fitted. | Fixed: within their measured ranges. |

### The paper's own rules

| Finding | Where | What Fable found | Handled |
|---|---|---|---|
| D1 | Figure 2, preface | "pull" in the paper's own voice. | Fixed: the axis now reads "galaxy's own turning over the limit"; the preface says "gravitational effect". §2.5's "Nothing pulls" is a denial and stays. |
| D2 | Preface | "universe" on its own. | Fixed in the thirteenth revision: "the observable universe". The epigraph is the author's and stays. |
| D3 | Glossary, Reclaiming | "particles" in the glossary's own voice. | Fixed: antimatter is other work's term for what is seen, and the rebuild works several levels below what is seen. |
| D4 | §13.2, §14 | "neighbours". | Fixed: neighbors. |
| D5 | Throughout | [Candidate], "the books" and "the joining field" used without definition. | Fixed: a key for the status tags in the Conventions; glossary entries for the books and the joining field. |
| D6, D8 | §6; §1–§4, §9 | A reference to the form the framework used before; the older formal register of the early sections. | Not changed: the first is the author's; the second is a larger rewrite, not for this release. |

### Citations and layout

| Finding | Where | What Fable found | Handled |
|---|---|---|---|
| E1 | §6 | As A3. | As A3. |
| E2 | Bibliography | All 110 citations resolve, in order of first citation; the spot-checked sources support what is cited. | Recorded. Three references added from the findings above (113 in all), each read, in order of first citation. |
| F1, F2 | Pages 59–61 | A floated table splits a sentence; Equation (40) and its "where" clause fall on facing pages. | Not changed: cosmetic, and the layout is legal. |

## Numbers recomputed by Fable

Fable recomputed 108 quantities. A selection, with those the thirteenth revision adds:

| Claim | Paper | Fable |
|---|---|---|
| Eq. (15), its three limits | B → y/√3, 2y²/3; half tied up at y = 1 | 0.577 = 1/√3; 0.667 = 2/3; B(1) = 1.000 |
| Model Milky Way at 8.1 kpc | 159 km/s from stars and gas; 203 with the eddy; ×1.62 | 159.3; 202.6; ×1.62 |
| Model Milky Way, vertical turning | +10.3 % at 0.5 kpc, +17.5 % at 1 kpc | +10.3 %, +17.5 % |
| Far-out speed, V⁴ = G M_b g† | 176 km/s (6 × 10¹⁰ M☉); about 180 (6.7 × 10¹⁰) | 175.8; 180.7 |
| c₀H₀/2π, H₀ = 70–73 | 1.08–1.13 × 10⁻¹⁰ m s⁻² | 1.082–1.129 × 10⁻¹⁰ |
| The one speed times the steady rate | 5.8–6.2 × 10⁻¹⁰ m s⁻² | 5.80–6.20 × 10⁻¹⁰ (with the share back-solved, A4) |
| The flow's energy | 6.0–6.9 × 10⁻¹⁰ J m⁻³ | 6.01–6.87 × 10⁻¹⁰ |
| The lendable Ocean against the flow's energy | one part in 47 to 53 | 46.7 to 53.4 |
| Onset of the shortfall | z 0.10–0.23, 1.3–2.7 Gyr ago; 1.8–3.7σ | 1.30–2.74 Gyr; 1.84–3.74σ |
| Dent, Eq. (40) | about 3.5 E_P, about 4 × 10²⁸ eV | 3.545 E_P = 4.33 × 10²⁸ eV |
| ε_c | about 1.5 Planck energy densities, near 10⁹⁷ kg m⁻³ | 1.50; 7.7 × 10⁹⁶ kg m⁻³ |
| Exponential-metric shadow against General Relativity | 4.6 % larger | 4.63 % |
| Hawking temperature, Sagittarius A*; the glow met at the crossing | 1.4 × 10⁻¹⁴ K; about 6 × 10⁻¹⁴ K | 1.43 × 10⁻¹⁴; 5.7 × 10⁻¹⁴ |
| Eq. (27), Λ = G²m_e⁶/(α⁶ħ⁴) | 1.36 × 10⁻⁵² m⁻² | 1.363 × 10⁻⁵² |
| The eddy's edge | 100 to 230 kpc | 274 to 630 kpc with the eddy cut off at the edge (A1) |
| Capacity of a dent-width region | a twenty-fifth of a dent | 1/25.1 by the load rule; 1/105 for a cube (A2) |
| Donato et al.'s surface density | 140 (+80/−30) | 141 (+83/−52) from ±0.2 dex (A3) |

What Fable could not check, and why: the expansion fits, the SPARC fits and the real Milky Way fit need the data and the code, which are now in the repository's `expansion/`, `sparc/` and `milky-way/` folders, and the check suite reads their results; the frame-dragging numbers from the paper's own rule need the two-layer Earth model the checks run; three citations could not be reached from its environment.

## Changes after the reading that Fable did not see

The fixes above, applied in one batch on 25 November; Figure 2 redrawn with its new axis label; and "(draft)" taken off the title page, which changes no part's token. The released PDF was checked again for a footer on every page and for the digest in its manifest, its metadata and the manifest file.
