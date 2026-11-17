# v3.15.1 validation report

**Read by:** Argon, an independent reviewer that had not seen the work being produced, 16 November 2026. Argon reported only. The changes below were made afterward from its report. Its findings are summarized here, with quoted passages in its own words.

**Method.** A complete reading of the 84-page PDF (23 parts), checking every page footer against the reading manifest, and an independent recomputation of the equations and numbers that are new or changed in 3.15.1 and those they rest on. Argon had the PDF only. It did not have the build script or the check suite, so it recomputed instead of running the checks.

**Digest read:** `65e0-4205-88e3` (84 pages, 23 parts, "End of document" on page 84). Argon saw all 23 part tokens, and each matches that build's manifest.

**Released digest:** `8b08-7b97-a49a`, after the fixes below and one approved pointer in §16. No result changed. The check suite on the released text gives 101 checks: 100 pass, 1 note, 0 fail.

## Verdict (Argon)

Each core calculation and structural update introduced or refined in this version "checks out algebraically and numerically". Argon found one structural point to state, two places where a reader could plug in the wrong quantity, and four minor items.

## Findings and how each was handled

| Finding | Where | What Argon found | Handled |
|---|---|---|---|
| 1 | §9 and §11.9 | The grip's two expansion equations assume that what is in a region is kept, ε̇ + 3H(ε + p) = 0. If κ_eff(ε) is inserted directly as a multiplicative prefactor in Eq. (1), "the contracted Bianchi identity ∇^μ G_μν = 0 requires ∇^μ[κ_eff(ϵ)T_μν] = 0, which modifies ϵ̇". | Confirmed. The paper's equations are right, but it did not say how the grip enters. A bare factor would give 1 − ε/ε_c in dH/dt instead of 1 − 2ε/ε_c. §11.9 now states that the grip enters as a correction to the stress: energy density ε(1 − ε/ε_c) and pressure p(1 − 2ε/ε_c) − ε²/ε_c, which are kept together. Argon's Δp = −ε²/ε_c is the case p = 0. §14's task asks for that correction to be derived. A check was added. |
| 2 | §12.7 rules table; Appendix A, step 7 | With r the isotropic radius, 1 − share = U² only when the distance in the share is the areal radius. | Both places now say the distance is the one read from the area of the sphere through the place. Appendix A gives share = 2GM/(rψ²c₀²). |
| 3 | §6; Appendix C | V²/(4πGr²) is the eddy's load density far out. With Eq. (15) it levels off at the center at 3V²/(4πG R_t²) = 3g†/(4πG R_t). | Both places now say so. |
| 4a | Page 1 | The token in the abstract's end line reads close to "21elc3" in the text layer. | No change. The PDF has 21e1c3. |
| 4b | Page 14 footer | The footer listed §1, which ended on page 13. | Fixed in the footer: a part is listed only on pages that hold some of it. Every page was checked. |
| 4c | Eqs. (18) and (20) | The action integrals omit d⁴x. | Added. |
| 4d | Page 60 | "ener energy" | Not in the source, and not in the PDF's text, which reads "brings that energy to bear there". No change. |

## Numbers recomputed by Argon

| Claim | Paper | Argon |
|---|---|---|
| The grip, Eq. (38) | κ_eff = κ(1 − ε/ε_c), ε_c = 3c₀⁴/(8πGξ²) | Follows from the share drawn by a region of width ξ: (8πG/3)εξ²/c₀⁴ |
| Dent from the count, Eq. (40) | about 3.5 E_P, about 4 × 10²⁸ eV | str[k₁] = −1/2 (12 carriers −8; 45 builds +15/2; joining field 0); √(4π) E_P ≈ 3.54 E_P ≈ 4.3 × 10²⁸ eV |
| ε_c | about 1.5 Planck energy densities, near 10⁹⁷ kg m⁻³ | 3/2 exactly at ξ = l_P/√(4π); 7.7 × 10⁹⁶ kg m⁻³ |
| Eq. (39) in the settled Ocean | energy per volume v²μ₀², w = −1 | Varying the supply fixes μ² = μ₀²; with s = −v² and V₀ = 2v²μ₀², T_μν = −v²μ₀² g_μν |
| The flow's energy per volume | 5–6 × 10⁻¹⁰ J m⁻³ | matches |
| The Earth's builds' loans per volume | about 2 × 10¹¹ J m⁻³ | 2.24 × 10³² J over 1.08 × 10²¹ m³: 2.07 × 10¹¹ J m⁻³ |
| Against the flow's energy; against an eddy's central pushback | 10²⁰; 10²¹ | matches; g†²/4πG ≈ 1.72 × 10⁻¹¹ Pa |
| c₀H∞ | 5.4–5.9 × 10⁻¹⁰ m s⁻² | 5.42–5.87 × 10⁻¹⁰ m s⁻²; g† is 0.20–0.22 of it |
| Hawking glow traced back to a dent's width | about 2 ms (1 M☉); about 2.5 h (Sgr A*) | 93 e-folds × 1.97 × 10⁻⁵ s ≈ 1.8 ms; 109 × 84.7 s ≈ 2.56 h |
| Strong field, §11.7 | ∇²ψ = 0, ∇·(ψ²∇U) = 0; γ = β = 1; edge at isotropic GM/2c₀², areal 2GM/c₀²; light orbit at areal 3GM/c₀²; shadow 3√3 GM/c₀² | identical |
| The phase around a spinning hole, §11.8 | θ = μ∞[t + F(r)], ΔF′ = √(2Mr(r² + a²)) | g^μν∂_μθ∂_νθ = −μ∞² identically, outside and across the edge; no circulation, with frame dragging carried entirely by the tilt (the shift vector s) |

## Changes after the reading that Argon did not see

The fixes above, and one pointer approved by the author on 17 November: §16 now names Section 13.3 for what would end the framework, next to Section 15 for the predictions. Both rebuilds kept the preface ending on page 8, and every footer was checked again.
