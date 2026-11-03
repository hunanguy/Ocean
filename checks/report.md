# Math check, version 3.13.1

83 checks: 82 pass, 1 note, 0 fail.

| Status | Where | Kind | Check | Result |
|---|---|---|---|---|
| PASS | §3, Eq. (13) | FORMULA | Amount and phase equations follow from the minimal law, Eq. (28), by varying the action | largest relative mismatch between varied action and Eq. (13): 1.0e-06 |
| PASS | §3, Eq. (12) | FORMULA | Canonical case: L = X - V gives box(phi) = dV/dphi | largest relative mismatch: 1.2e-08 |
| PASS | §3 and §11.4 | CONSISTENCY | Uniform steady amount from Eq. (13) equals the value stated in §11.4 | root 0.9570174256 vs sqrt(v^2+2mu^2/lam) 0.9570174256 |
| PASS | §11.4 | FORMULA | Integrating out the amount gives P(mu^2) = v^2 mu^2 + mu^4/lambda and P' = rho_bar^2 | largest difference 8.8e-12 |
| PASS | §11.4, Eq. (31) | FORMULA | The disturbance equation (31) follows from the minimal law expanded numerically | largest relative difference in omega^2: 4.7e-09 |
| PASS | §11.4, Eq. (29) | CONSISTENCY | Sound speed three ways: from P, from the small-k slope of Eq. (31), and the stated (1+a)/(1+3a) | largest relative difference: 8.2e-11 |
| PASS | §11.4, Eq. (30) | FORMULA | gamma = -(2+3a)/(3a) from /g00/ = P' c_s and g_ij = P'/c_s; below -1 for all a; -> -1 at large a | largest relative difference 2.0e-05; always below -1: True; a=1e6 gives -1.0000007 |
| PASS | §11.4 | NUMBER | Gapped rest rhythm omega_0^2 = lambda v^2 + 6 mu^2 from Eq. (31) at k = 0 | 1.597000000000 vs 1.597000000000 |
| PASS | §11.4 | NUMBER | At high k both branches approach omega = k +/- mu | omega - k = -0.29983, +0.30017 (mu = 0.3) |
| PASS | §11.4 | NUMBER | 1 - c_s ~ a for small a | 1 - c_s = 9.997501e-05 vs a = 1.0e-04 |
| PASS | §13.2(3), §11.1 | FORMULA | Gapless branch of Eq. (31): omega^2 = c_s^2 k^2 + B k^4 with B about 4a^2 (in units of 1/M^2) | a=0.3: numerical/series 1.00000, B M^2 / 4a^2 = 0.190; a=0.05: numerical/series 1.00000, B M^2 / 4a^2 = 0.690; positive, and -> 4a^2 as a -> 0 |
| PASS | §13.2(3) | NUMBER | k^4 coefficient 4a^2 with a ~ 1e-23 | 4a^2 = 4e-46 for a = 1e-23 |
| PASS | §9.1, Eq. (26) | FORMULA | V'' = lambda(3 phi^2 - v^2), negative for /phi/ < v/sqrt(3) | largest difference 4.1e-08; sign changes at v/sqrt(3): True |
| PASS | §11.7, Eq. (34) | FORMULA | psi and U satisfy rule (a) div(psi^2 grad U) = 0 and rule (b) lap psi = 0 | max /rule (a)/ = 5.2e-07, max /rule (b)/ = 8.8e-07 |
| PASS | §11.7 | NUMBER | Point of no return at isotropic radius GM/2c^2, areal radius 2GM/c^2 | U = 0 at r = 0.500000 M, areal 2.000000 M |
| PASS | §11.7 | NUMBER | Light orbits at areal 3GM/c^2; shadow radius 3 sqrt(3) GM/c^2 | areal 3.000000 M, shadow 5.196152 M vs 5.196152 |
| PASS | §11.7 | FORMULA | U agrees with exp(-u) to second order, so beta = 1 | difference scales as u^3.00 (third order) |
| PASS | §11.6(v) | NUMBER | U = 1 - u gives beta = 1/2 and perihelion factor 7/6; U = exp(-u) gives beta = 1 | beta(1-u) = 0.500000, beta(exp) = 0.9993, factor = 1.166667 |
| PASS | §11.6(vi) | NUMBER | Exponential metric: no point of no return; shadow 4.6 percent larger than GR | shadow ratio 1.04627 (4.63 percent); clock rate exp(-M/r) > 0 everywhere |
| PASS | §11.6(v) | FORMULA | 'Rulers set by the amount looks fixed from afar would give gamma = -1/3' (and fail light bending) | amount fixed to first order only for gamma = -0.33333; light then bends 0.333 of the observed amount (the paper: 'a third as much'); amount = time part of the current of Eq. (13) |
| PASS | §11.9, Eq. (37) | FORMULA | theta = mu(t + f) solves the wave equation; only 4M^2 keeps it finite for a falling traveler; far away f' -> 4M^2/r^2 | wave equation residual 2.6e-14; at the edge f' - dr*/dr -> -2.0000 with 4M^2, -2.5e+06 with 3M^2; far-field ratio 1.000002 |
| PASS | §11.9, Eq. (37) with Eq. (6) | CONSISTENCY | With u = -grad(theta)/mu, the phase of Eq. (37) gives a flow forward in time and inward at every radius | future-directed inflow at r = 10M, 3M, 2.2M, 2.01M |
| PASS | §2.5, Eq. (10) | FORMULA | n = 1 + 2GM/(rc^2) bends light by 4GM/(bc^2), twice the slowing-only value | deflection 4.000000 GM/(b c^2) |
| PASS | §7.5, Eq. (24) | NUMBER | hbar c / 0.511 MeV = 386 femtometers | 386.16 fm |
| PASS | §13.2(5), Eq. (40) | NUMBER | alpha_G = G m_e^2/(hbar c) = (l_P/xi_0)^2 ~ 1.75e-45 | 1.7518e-45; (l_P/xi_0)^2 = 1.7518e-45 |
| PASS | §13.2(5) | NUMBER | Planck length ~1.6e-35 m, about 1e22 below the electron's localization length xi_e | l_P = 1.616e-35 m; xi_0/l_P = 2.39e+22 |
| PASS | Preface | NUMBER | Electric force between two electrons ~4e42 times their gravity | 4.166e+42 |
| PASS | Preface | NUMBER | Hurricane ~1e14 times the spacing of air molecules | 'hundreds of miles' (100-500 miles) / 3.34 nm = 4.8e+13 to 2.4e+14 |
| PASS | Preface, §13.2(5) | NUMBER | A kiloparsec is about 1e55 times the dent's width (Planck length / 3.5): more than fifty orders | kpc / dent width = 6.8e+54 |
| PASS | §13.2(7) | NUMBER | Electron size limit 1e-18 m is several hundred thousand times below xi_0 | 3.86e+05 |
| PASS | §11.8 | FORMULA | Circulation per line from the paper's flow u = -grad(theta)/mu: one turn of the phase gives 2 pi/mu (hc^2/mu in SI) | loop of mu u = -6.283185 (exactly -2 pi); loop of u -> -2.094398 (-2 pi/mu = -2.094395) |
| PASS | §7.6 | NUMBER | G-dot/G = (-5.0 +/- 9.6)e-15 per year: G changed by less than four parts in 1e4 over 13.8 Gyr | two-standard-deviation bound 3.34e-04 against the stated 4e-04 (strict: no margin) |
| PASS | §10.3, Eq. (27) | NUMBER | Lambda = G^2 m_e^6/(alpha^6 hbar^4) ~ 1.36e-52 m^-2 | 1.3629e-52 m^-2 |
| PASS | §14 | NUMBER | G = alpha^3 hbar^2 sqrt(Lambda)/m_e^3 within ~10 percent with measured Lambda, a few percent with local H0 | Planck 2018 Lambda: G ratio 0.894; H0 = 73 km/s/Mpc: 0.969 (inputs: Planck 2018 H0 and Omega_Lambda) |
| PASS | §8.1 | NUMBER | Hawking temperature of a solar-mass black hole ~60 nK; mass loss ~1e-45 kg/s | T = 61.7 nK; photon-only mass loss 1.0e-45 kg/s |
| PASS | §8.1, §8.2 | NUMBER | Evaporation: about 1e67 years for a solar mass (Page 2e66 with massless neutrinos); about 1e87 years for Sgr A* | photon-only estimate 2.1e+67 years for a solar mass; 1e67 x (4.3e6)^3 = 8.0e+86 years |
| PASS | §8.1 | NUMBER | Accretion efficiency about 6% (non-rotating), up to about 40% (rapidly rotating); fusion 0.7% | 5.72%, 42.3% (extreme spin), fusion 0.71% |
| PASS | §8.2 | NUMBER | 10 solar masses: tidal difference ~10 g at 3800 km; horizon ~30 km | 9.9 g over 2 m; horizon 29.5 km |
| PASS | §8.2 | NUMBER | Sagittarius A*: horizon radius ~12.7 million km; tidal difference at the horizon ~1e-4 g; lethal ~280 000 km | horizon 12.70 million km; 1.1e-04 g at the horizon; 10.6 g at 280 000 km (same 10 g criterion as above) |
| PASS | §8.2 | NUMBER | Longest time horizon to center pi GM/c^3: ~66 s Sgr A*, ~28 h M87* | 66.5 s; 27.9 h |
| PASS | §11.9 | NUMBER | Crossing to turnaround (falling from rest far away): ~1e-4 s (10 Msun), 28 s (Sgr A*), 12 h (M87*) | 6.6e-05 s; 28.2 s; 11.9 h (turnaround density far above the horizon density) |
| PASS | §11.9 | NUMBER | rho_c >~ 2.4e23 kg/m^3 (J0337) with rho_c c^2 ~ hbar c/l^4 gives l <~ 0.035 fm, ~1e4 below the electron's 386 fm | l = 0.0348 fm; xi_e/l = 11098 |
| PASS | §11.9 | NUMBER | q = 1 return: five solar masses merging after ten billion years needs l <~ 6e-19 m; Sgr A* return ~1e22 years | l < 5.8e-19 m; Sgr A* 7.1e+21 years |
| PASS | §11.9 | CONSISTENCY | Turnaround half a minute after crossing for Sgr A* (§8.2) matches 28 s (§11.9) | 28 s is about half a minute |
| PASS | §6, Eq. (16) | FORMULA | (s.grad)s - w x curl s = grad(s^2/2) - xdot x curl s, w = xdot - s (random fields) | largest relative difference 4.6e-16 |
| PASS | §6, Eq. (16) | FORMULA | Eq. (16) is the slow-motion limit of travel in ds^2 = -(1+2Phi)dt^2 + (dx - s dt)^2 (difference falls with the field strength) | largest relative difference 6.4e-03 (fields 3e-2), 2.2e-04 (3e-3) |
| PASS | §6 | FORMULA | Counting the self-held swirl as load and as tilt turns a co-moving star by 2V^2/r | load 1.0 + tilt 1.0 = 2.0 V^2/r |
| PASS | §6, Eq. (15) | NUMBER | Matching rule: V = sqrt(GM/R_t) at R_t = sqrt(GM/g) gives V^4 = G M g; Milky Way model 176 km/s, R_t 8.3 kpc | V^4/(GMg) = 1; Milky Way model V = 175.8 km/s, R_t = 8.35 kpc |
| PASS | §6 | SIMULATION | Model galaxies 10^7.5-10^11.5 Msun, compact/typical/diffuse: rms 0.046-0.057 dex from the RAR, no trend with compactness | rms 0.046, 0.051, 0.057; largest mean offset by compactness 0.040 dex |
| PASS | §6 | SIMULATION | Model Milky Way with the eddy: 159 -> 201 km/s at 8.1 kpc (RAR 205); radial x1.59; vertical +9.8% at 0.5 kpc, +16.8% at 1 kpc | 159 -> 201 km/s (RAR 205); radial x1.59; vertical +9.8%, +16.8% |
| PASS | §6 | SIMULATION | Eddy core load per area, Burkert-equivalent: 264 Msun/pc^2 (cored), 460-530 (spiked), mass-independent; measured 140 | cored: 264 (1e7) / 264 (1e11); x/(1+x): 459 (1e7) / 459 (1e11); 1-exp(-x): 526 (1e7) / 526 (1e11) |
| PASS | §6 | NUMBER | c H0/2pi = 1.04-1.13e-10 (H0 67.4, 73); late-time c H0 sqrt(OmL)/2pi = 0.86-0.93e-10; H(2.3)/H0 = 3.4 | 1.042e-10, 1.129e-10; late-time 8.626e-11, 9.342e-11; H(2.3)/H0 = 3.39 |
| PASS | §6 | SIMULATION | Genzel et al. 2017 six disks: fixed limit fits 5-6 of 6 dark-matter shares; limit following H(z) fails all three beyond z = 2 (0.09-0.36 predicted); bound 1.0-2.7x at z 2.2-2.4 | fixed limit inside range: [6, 5, 5] of 6; H(z) fails every z > 2 case: True; H(z) predictions 0.09-0.36; bound 1.02-2.70x |
| PASS | §6 | NUMBER | In-plane turning at most 15-19 km/s at the Sun: pressure-supported systems on the RAR within 0.10-0.13 dex | 15.3 and 19.3 km/s |
| PASS | §6 | SIMULATION | Escape speed 528 km/s at the Sun places the eddy's edge at about 150-350 kpc in the model | escape speed 528 km/s (edge 150 kpc) to 576 km/s (350 kpc), against 528 +24/-25 |
| PASS | Appendix B | NUMBER | The Sun's share at the Earth's distance about 2e-8; the eddy supplies about 37% of the turning at the Sun | share 1.97e-08; eddy fraction 0.371 |
| PASS | §11.8 | SIMULATION | Phase slices of a spinning hole spacelike down to r_-; Cotton-York of the rulers zero without spin and growing as spin squared | /C/ M^3: 2.1e-10 (no spin), 1.73e-04 (0.1), 4.31e-03 (0.5), ratio 24.885 (spin squared: 25); slices spacelike r_- to 40M: max -1.05 |
| PASS | §11.8, Eq. (35) | FORMULA | A boost of the resting mass's geometry gives the sideways tilt (2 + 2 gamma) u V | gamma=1.0: tilt coefficient 4.000004 (rule 4.0); gamma=0.5: tilt coefficient 3.000003 (rule 3.0) |
| PASS | §11.8, Eq. (36) | SIMULATION | Summed tilts of a spinning two-layer Earth equal 2G (J x r)/(c^2 r^3) | largest relative difference at three outside points: 8.8e-05 |
| PASS | §11.8 | FORMULA | Half the turning of the swirl equals the Lense-Thirring rate at every point | largest relative difference: 3.9e-10 |
| PASS | §11.8 table | SIMULATION | Orbit-plane drift from Eq. (16): 30.6, 31.4, 118.1 mas/yr; Gravity Probe B 39.2 toward the guide star | drifts 30.59, 31.41, 118.13 mas/yr (GR as published: [30.68, 31.5, 118.5]; ratio 0.9972); GP-B 39.2 mas/yr |
| PASS | §11.8 | SIMULATION | Travel leaves no trace with both shares; ruler share missing leaves /V x grad u/; no tilt leaves (1+gamma)/V x grad u/ | turning / /V x grad u/: both shares 0.0002, clock share only 1.0000, no tilt 2.0002 (gamma = 1) |
| PASS | §11.8 | SIMULATION | A rotor whose parts obey Eq. (16) turns at half the local turning, whatever its spin (Larmor) | rate / (B/2): 1.00000, 1.00000 |
| PASS | §11.8 | SIMULATION | Read point by point, quantized lines turn no pattern's travel in either sense | smooth -2.176e-01; lines +8.234e-04 and +8.234e-04; part reversing with the sense 0.0e+00 |
| PASS | §11.8 | NUMBER | Travel's tilt near the Earth is several thousand times the spin's | ratio 5302 at Gravity Probe B's height, travel 370 km/s |
| PASS | §11.8 | SIMULATION | Lines read over one spacing turn a gyroscope at B/2 (Larmor), reverse with the lines, independent of spin; point by point: nothing (mixed senses: rotor_mixed.py) | turning/(B/2): one spacing +1.0000; reversed -1.0000; spin x3 +0.9998; point by point -0.0002 |
| PASS | §12.7 | NUMBER | Share of capacity at the Earth's surface 1.4e-9 and at the Moon 2.3e-11; the Moon's turning (c^2/2) grad(share) = 2.70e-3 m/s^2 | share 1.392e-09 (surface), 2.308e-11 (Moon); turning 2.6976e-03 m/s^2 = GM/d^2 |
| PASS | §7.5, §13.2(5) | NUMBER | Dent (3.5 E_P) against the electron's 0.511 MeV, and the healing length against 386 fm: nearly 1e23 | ratio 8.46e+22 |
| PASS | §11.8 | FORMULA | Phase around a spinning hole: theta = mu(t + F), Delta F' = 2 M r_+ solves the wave equation (Boyer-Lindquist) and is regular at r_+; no phi dependence, so zero circulation | wave-equation residual 2.3e-13; at r_+ F' - (r^2+a^2)/Delta tends to the finite -2r_+/(r_+ - r_-) (largest relative miss 7.9e-07) |
| PASS | §12.3 | NUMBER | Clock at the Earth's surface: sqrt(1 - share) slows it by half the share, about 7e-10 | slowing 6.961e-10 = share/2 |
| PASS | §12.7 | FORMULA | Induced gravity count: carriers -8, 15 builds per family +15/2, conformal joining field 0: str[k1] = -1/2; cutoff 3.5 E_P; 16 per family gives 0 | str = -1/2 (15/family), 0 (16/family); cutoff 3.54 E_P = 4.33e+28 eV |
| PASS | §12.4 | NUMBER | Baryon-to-photon ratio from the microwave background and from the light elements agree (Fields et al. 2020) | difference 0.22 standard deviations |
| PASS | §12.7 | SIMULATION | In the minimal law a ripple in the amount at rest carries no Ocean charge; fast ripples (omega ~ k +/- mu) do | charge ripple / amplitude: amount ripple at rest 2.1e-09; fast ripple 1.48 |
| PASS | whole paper | CONSISTENCY | Every \eqref and \ref has a \label; every \cite has a \bibitem | missing labels []; missing bibitems []; never cited [] |
| PASS | bibliography | CONSISTENCY | Bibliography is in first-citation order (as 3.10 states) | in order |
| PASS | whole paper | CONSISTENCY | Healing length stated consistently as 386 femtometers | values found: ['386'] (5 occurrences) |
| PASS | §11.6, §11.7, §11.8 | CONSISTENCY | Symbol U is the rate of clocks only; the slowing is u (§11.6, Eq. 36); bold u is not reused for travel | U is the clock rate (§11.6-11.7); u the slowing; bold V the travel |
| PASS | §2.2, §11.8 table | CONSISTENCY | Symbol mu is the Ocean's phase rate only (not reused in the §11.8 table) | mu is the phase rate throughout |
| NOTE | whole paper | CONSISTENCY | Symbol w: travel relative to the Ocean (bold, Eq. 16) and equation of state w = -1; the clock deficit is u (§11.6) | bold w for travel and plain w = -1 for the equation of state remain, distinguished by typeface |
| PASS | §2.2, §2.5, §11.9 | CONSISTENCY | Symbol n: density rho^2 (§2.2), refractive index n(r) (Eq. 10), exponent n (§11.9) | no clash |
| PASS | §11.4, §11.7, §11.9 | CONSISTENCY | Symbol M is a mass only (Eq. 31 uses omega_rho for the heavy branch) | M is a mass throughout |
| PASS | §3 | FORMULA | The single-field equation omits the phase term -rho mu^2, which moves the settled amount by the fraction a/2 | a=0.001: shift 4.999e-04 (a/2 = 5.0e-04); a=1e-06: shift 5.000e-07 (a/2 = 5.0e-07) |
| PASS | §7.2, Eq. (20) | FORMULA | Two coupled fields: the quadratic action is the minimal law's expansion; branches c_s^2 = (1+a)/(1+3a), gap^2 = lambda v^2 + 6 mu^2, k^4 term 4a^2 | action from the minimal law: matches; gap^2 1.029400 vs 1.029400; c_s^2 0.980960 vs 0.980960; k^4 term 3.49e-04 = 4a^2/(1+3a)^3 3.52e-04, 4a^2 to leading order |
