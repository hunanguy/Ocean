#!/usr/bin/env python3
"""
build_ocean_formalism.py
------------------------
Generates the LaTeX source for "Scalar-Tensor Hydrodynamics: Gravity as the
Response of a Vacuum Medium. A Modified Gravity Framework for Vacuum Viscosity
and Cyclic Vacuum Cosmology" and compiles it to PDF with pdflatex.

Usage:
    python3 build_ocean_formalism.py [--outdir DIR] [--no-pdf]

Requires: pdflatex on PATH (TeX Live or MiKTeX).
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# Version history
#   3.0  Base revised formalism: Einstein tensor separated from vacuum viscous
#        stress; scalar-field sector; P(phi) in place of Lambda; kappa(phi).
#   3.1  Section 7 rewritten. The fixed 0.511 MeV matter threshold is replaced
#        by a localization criterion derived from the excitation spectrum of
#        phi. Sections 8 and 10 updated to match.
#   3.2  Section 9 gains a global-regularity requirement and the defocusing
#        condition lambda > 0. Section 10 gains the sign-determination task and
#        the question of whether matter coupling acts as a forcing term.
#   3.3  Lay preface added as front matter: the motivating problem, the core
#        idea, the revision history, and the three conditions that would
#        falsify the framework, plus two further sections: the provenance
#        of Lambda and dark matter, and the GR / quantum-field-theory
#        disagreement over the vacuum. No change to the technical content.
#   3.4  Related-work section and bibliography added. Positions the
#        framework against superfluid-vacuum and viscous-cosmology
#        literature, isolates the distinctive claim, and records two
#        deficiencies: first-order dissipative form and the status of
#        c(phi). Section 10 gains the corresponding items.
#   3.5  Lisanti et al. added to the bibliography. Sections 10 and 11 gain
#        the vertical-acceleration (Gaia) constraint, which the galactic
#        sector had not addressed. Bibliography upgraded to journal versions
#        of record for Huang et al. and Berezhiani & Khoury. Section 10.3
#        corrected: Chavanis gives Lambda in terms of the electron mass, not
#        a minimum-length replacement for the Planck scale. Section 10 now
#        concedes Huang's galactic vortex result as the nearest precedent for
#        Section 6, narrowing the distinctive claim to the partition alone.
#        Section 10.2 further corrected: superfluid vacuum theory is not a
#        two-species model, so the distinctive claim is the partition plus a
#        retained fundamental geometry, not single-substance ontology.
#        Sections 10.4 and 11 corrected against the Lisanti et al. paper:
#        the failure mode is a force parallel to the baryonic field, not a
#        disk-shaped source. Earlier Lisanti et al. (2019) added.
#   3.6  Candidate route for the scale hierarchy recorded, not a resolution.
#        The galactic scale is reassigned from the medium to the individual
#        disturbance, so the gap needs only an upper bound; a U(1) shift
#        symmetry (phi as the phase of a complex field) is the proposed
#        protection. Section 2.2 states the condition and its cost, Section 6
#        adopts the single-structure reading of a galaxy, Section 7.7(5) and
#        the preface are updated, and the hierarchy item of the research
#        program is split into three tasks. The hierarchy remains listed as
#        the most serious open problem. The radial acceleration relation
#        (McGaugh, Lelli & Schombert 2016; Lelli et al. 2017) is cited as
#        the target for the no-per-galaxy-freedom prediction, with its
#        acceleration scale g_dagger recorded as a further obligation.
#   3.7  The medium is taken as primary. The preface opens with "The
#        premise": no empty space, an Ocean without edges or outside, no
#        particles as objects, and gravity as the medium's response to
#        concentrated energy. Einstein's equation is kept as the effective
#        description (Section 1); Section 2.5 gives the refractive account of
#        gravity and its three decisive tests; Sections 10-12 aligned, with the
#        distinctive claim restated. Subtitle extended to lead with the
#        gravity claim. Conventions and a glossary fix the terms: "particle"
#        and "cycle" only when reporting other work, "universe" never on its
#        own, beat / present beat / beat transition / epoch defined.
#        Section 5 split into "Within the present beat" (deceleration and
#        acceleration; evolving dark energy and the w = -1 caution) and
#        "Across beats" (counted, not timed; Steinhardt-Turok precedent;
#        primordial gravitational-wave test). Section 6 covers
#        pressure-supported galaxies and treats the vacuum contribution as a
#        flow with shear and wakes. Section 7 adds the vortex consistency
#        check, the g-dagger obligation, the size-and-spin item and a sharper
#        Lorentz-violation item. Section 8 gains a strong-field regime and a
#        black-hole subsection. Section 9.1 recast: regularity is a property
#        of the medium's state under a fixed Lagrangian. Section 10 gains the
#        observer argument and the measured-vacuum deficiency. Section 11
#        extended. Nine references added, each read before citing;
#        bibliography restored to first-citation order. Preface records the
#        fourth revision (the inherited stage removed) and corrects the
#        electron-size wording to match Section 7.7(7).

DOCNAME = "Ocean_Scalar_Tensor_Hydrodynamics_v3_7"

PREAMBLE = r"""
\documentclass[11pt,a4paper]{article}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
% Times-family text and math. Substitute lmodern or newtxtext/newtxmath if
% preferred; mathptmx is chosen here because it is present in minimal TeX Live
% installations and avoids Type 3 bitmap fallback.
\usepackage{mathptmx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{bm}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{enumitem}
\usepackage{microtype}
\usepackage[margin=1in]{geometry}
\usepackage[colorlinks=true,linkcolor=black,urlcolor=black,citecolor=black]{hyperref}

\hypersetup{
  pdftitle={Scalar-Tensor Hydrodynamics: Gravity as the Response of a Vacuum Medium. A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology},
  pdfauthor={Keith Hays},
  pdfsubject={Theoretical proposal, revised formalism},
  pdfkeywords={scalar-tensor, vacuum viscosity, modified gravity, emergent gravity, superfluid vacuum, cyclic cosmology}
}

% mathptmx leaves \hbar undefined; restore the standard glyph construction.
\DeclareRobustCommand{\hbar}{{\mathchar'26\mkern-9mu h}}

% --- notation shorthands -------------------------------------------------
\newcommand{\gmn}{g_{\mu\nu}}
\newcommand{\Gmn}{G_{\mu\nu}}
\newcommand{\Rmn}{R_{\mu\nu}}
\newcommand{\hmn}{h_{\mu\nu}}
\newcommand{\Pimn}{\Pi_{\mu\nu}}
\newcommand{\Tmat}{T^{\mathrm{matter}}_{\mu\nu}}
\newcommand{\Tphi}{T^{\phi}_{\mu\nu}}
\newcommand{\Veff}{V_{\mathrm{eff}}}
\newcommand{\Ogap}{\Omega_{\mathrm{gap}}}
\newcommand{\mstar}{m_{\star}}
\newcommand{\Kk}{\mathcal{K}}
\newcommand{\Gg}{\mathcal{G}}
\newcommand{\Qq}{\mathcal{Q}}

\setlist{itemsep=2pt,topsep=4pt}
\renewcommand{\arraystretch}{1.25}

\title{\Large Scalar--Tensor Hydrodynamics\\[4pt]
\normalsize Gravity as the Response of a Vacuum Medium:\\
A Modified Gravity Framework for Vacuum Viscosity and Cyclic Vacuum Cosmology}
\date{Revised Formalism --- Version 3.7}
\author{Keith Hays}
"""

BODY = r"""
\begin{document}
\maketitle

\begin{abstract}
\noindent
We propose a hydrodynamic extension of General Relativity in which the vacuum is
modeled as a dynamic, high-energy scalar medium described by a field $\phi$.
Rather than treating the vacuum as a fixed geometric background plus a constant
cosmological term, the framework assigns the vacuum its own stress-energy,
pressure, and dissipative response. The formulation separates the Einstein
geometric tensor from the vacuum viscous stress tensor, introduces a dynamical
scalar-field sector, replaces a fixed cosmological constant with a
field-dependent pressure contribution, and allows the effective gravitational
coupling to depend on the local vacuum state. The framework is intended to
investigate whether cosmological expansion, galactic dynamical anomalies, and
the transition between localized and delocalized excitations can arise from one
underlying medium. The medium is taken as primary. What are conventionally
called particles are treated as localized excitations of it, and spacetime
geometry, with Einstein's equation, as the effective description of how its
state is experienced. Gravity is proposed to be the medium's response to
concentrated energy.

\medskip
\noindent
This document is a theoretical proposal, not an established physical theory. The
equations below define a research program whose consistency, stability,
conservation laws, and observational predictions must be demonstrated.
\end{abstract}

% =========================================================================
\section*{Preface: What This Paper Is For}
\addcontentsline{toc}{section}{Preface}

\subsection*{The premise}

There is no empty space.

Everything this paper describes happens inside a single continuous medium,
called here the Ocean. The name is a metaphor, and one feature of real oceans
must be discarded at once: this Ocean has no edges. It has no shore and no
surface. There is no sky above it, no floor beneath it and no air over it. It is
not held in a basin, and it does not sit inside a space that could exist without
it. There is no outside. The edge of what we can see is a limit of seeing, not an
edge of the Ocean. Where things seem empty, the Ocean is there, quiet. Where
they seem full, the Ocean is there, gathered. Nothing in this framework
exists apart from it, beside it or beyond it.

What we call matter is the Ocean's own energy, gathered and circulating in
place. What physics calls a particle is not an object but a pattern the Ocean
keeps re-making. When a particle ``moves'', the place where the pattern is
re-made has shifted, the way a wave crosses a stadium while nobody leaves their
seat. Light is a ripple in the same medium. A galaxy is a vast region of
gathered energy and current. Every pattern exists against, alongside or within
others, adding to or taking from them, and every one is ultimately the Ocean's
response to what the rest of it has done. For that reason this document uses the
word ``particle'' only when reporting other authors' theories, and marks it as
theirs.

This work began with gravity. Einstein's theory describes what gravity does with
extraordinary precision: clocks run slow near a mass, space stretches, paths
curve. It does not say why concentrated energy should do this. The proposal here
is that gravity is the medium's response. Concentrated energy changes the state
of the Ocean around it, the Ocean runs slower there, and every pattern in it,
light included, leans toward where it runs slower. On this view Einstein's
equations remain the correct description, and the Ocean is offered as the reason
they are correct, as the gas laws stayed correct when atoms were found to
explain them. Whether the framework can carry that claim is the test it must
pass: every pattern must lean by exactly the same amount, and the stretching of
space must match the slowing of time exactly as Einstein requires.

\subsection*{The problem}

The same premise bears on the largest open problem in cosmology.

Two of the largest numbers in cosmology are placeholders. Roughly a quarter of
the contents of the observable universe is labelled \emph{dark matter}: a substance inferred
entirely from its gravitational pull on things we can see, and never once
detected directly. Most of the remainder is labelled \emph{dark energy}, which
is less a substance than a name for an observation --- that cosmic expansion is
speeding up when everything we understand says it should be slowing down.
Together these two labels cover something like ninety-five per cent of what the
observable universe contains. Neither has an agreed physical identity.

Standard cosmology handles this competently. It adds an invisible cold matter
component, and a constant term to Einstein's equations, and the resulting fit to
observation is superb --- good enough that the model deserves the confidence it
has. But a superb fit obtained by inserting two unexplained quantities is not
the same thing as an explanation. It is a description with two holes in it, and
the holes have names.

This paper asks whether both holes might have one filling.

\subsection*{A note on where these numbers came from}

There is a precedent in this subject for inserting a quantity because the answer
is expected rather than because anything has been measured. In 1917 Einstein
added a term to his field equations --- the cosmological constant, $\Lambda$ ---
for no reason beyond his conviction that the universe, as he conceived it, ought
to be static, and
the inconvenient fact that his equations refused to make it so. No observation
supported the term. It was a number chosen to produce an anticipated result.
When Hubble demonstrated a little over a decade later that the observable
universe is expanding after all, Einstein abandoned it.

It is worth being precise about what happened next, because the common retelling
is wrong in a way that matters. $\Lambda$ returned in 1998, but not as Einstein's
unmeasured assumption quietly surviving. It returned because observations of
distant supernovae showed cosmic expansion to be accelerating, and $\Lambda$ was
the simplest term capable of describing that. The acceleration is real and
measured. What $\Lambda$ does not do is explain it: no theory predicts the
constant's value, and the various attempts to calculate it from first principles
fail by a margin discussed below. The term records what the expansion does and is
silent on why.

Dark matter has an entirely separate and considerably stronger pedigree. Fritz
Zwicky noticed in 1933 that galaxies in the Coma cluster move too fast for the
visible mass to hold them together. Vera Rubin's rotation-curve measurements in
the 1970s found the same discrepancy inside individual galaxies. Gravitational
lensing, the structure of the cosmic microwave background, and the separation of
mass from gas in colliding clusters have since confirmed it from independent
directions. The evidence is not thin, and this document does not dispute any of
it.

The objection is therefore not that these quantities were invented. It is that
in both cases a measured discrepancy was given a name, and the name was then
promoted to a substance. $\Lambda$ is a parameter fitted to the expansion history
rather than derived from anything. Dark matter is a material known solely by its
gravity, which forty years of increasingly sensitive detectors have failed to
find by any other means. Each is a placeholder that has been in service long
enough to be mistaken for an answer.

If the framework set out here is even approximately correct, nothing
observational changes. The rotation curves remain exactly as measured. So do the
lensing maps, the microwave background, and the supernova data establishing
acceleration. What dissolves is the pair of substances invoked to account for
them: they stop being two unknown constituents of the observable universe and become
two behaviours of one medium. The measurements survive intact. Only their cause is
reassigned.

\subsection*{Where our two best theories disagree}

General Relativity and quantum field theory are the most thoroughly confirmed
descriptions of nature ever constructed, and they are known to be mutually
incompatible. In ordinary practice this causes little trouble, because the two
rarely describe the same situation: one governs the very large, the other the
very small, and the regimes where both matter at once --- the first instants
after the big bang, the interior of a black hole --- are exactly the regimes we cannot
observe.

There is one glaring exception, and it is directly relevant here. The two
theories overlap on the question of what the vacuum is, and there they do not
disagree by a little. General Relativity treats empty space as genuinely
empty: a smooth, featureless backdrop with no properties of its own. Quantum
field theory describes the same emptiness as the most active object in physics
--- fields in their lowest state, never still, producing effects that have been
measured in the laboratory for seventy years.

Ask both theories what that activity should weigh, and the answers differ by
something between sixty and a hundred and twenty orders of magnitude, depending
on where the calculation is cut off. This is not a discrepancy to be tidied away
with a correction factor. It is routinely described as the worst quantitative
prediction in the history of science, and it has stood unresolved for decades.

The observation that motivates this document is that the sharpest disagreement
between our two best theories is a disagreement about whether the vacuum is a
thing. One says no. The other says emphatically yes, and has the laboratory
results to support it. What follows takes the second answer seriously and asks a
further question that neither theory addresses: if the vacuum is a thing, does
it also have mechanical properties --- density, pressure, flow, resistance to
being stirred --- and if so, what would we expect to see?

\subsection*{What a medium can do}

General Relativity, read as it is usually taught, treats the vacuum as the
absence of things: a stage that can be curved by what sits on it but has no
density, pressure or motion of its own. A medium does things a stage cannot.
It flows. It drags. It carries waves. They can be stirred, and they push back when you stir
them. Each of those behaviours is a candidate for a phenomenon currently
attributed to something unknown:

\begin{itemize}
\item A galaxy rotating inside a medium that swirls along with it experiences
stress from that swirl. Stress gravitates. The extra pull that standard
cosmology assigns to a halo of undetected particles, in its own terms, might
instead be the vacuum's own response to
being rotated.
\item A medium with internal pressure that can change character over time can
drive expansion without a constant pasted into the equations by hand. What is
now called dark energy would be the Ocean in a particular state rather than a
number in a table.
\item And --- this is the part developed furthest here --- a medium has a
smallest meaningful size. Below some scale, it cannot be disturbed in a
localized way at all. That gives a principled distinction between what counts as
a localized pattern and what counts as a ripple.
\end{itemize}

The ambition is that dark matter and dark energy stop being two mysteries and
become two behaviours of one thing.

\subsection*{What this document is not}

It is not a theory. It is a proposal with its homework listed.

The equations below are consistent in form, but consistency in form is cheap. A
physical theory has to survive conservation laws, stability analysis, the
recovery of tested results in the appropriate limits, and quantitative agreement
with observations that were not used to build it. None of that has been done
here. Section~\ref{sec:program} is an itemized list of the work required, and
several items on it could terminate the framework outright. They are stated
plainly rather than buried, because a proposal that cannot specify how it would
fail is not worth the paper it occupies.

\subsection*{How this document came to exist}

The framework began as private speculation, written to a standard that
required only that the pieces appear to fit. That is a much weaker standard
than the one it has since been held to, and the gap between the two turned out
to be where the interesting work was.

Four revisions have followed, and they share a shape.

\textbf{The first} corrected a structural error. In the original formulation the
vacuum's viscous response \emph{replaced} the Einstein tensor --- the geometric
heart of General Relativity. This cannot work: a mathematical identity
guarantees that the Einstein tensor is conserved, and substituting something
else for it breaks the conservation of energy and momentum. The fix was to keep
the geometry intact and add the vacuum's stress alongside it rather than in its
place.

\textbf{The second} removed a number. The original drew the line between matter
and vacuum at $0.511\,\mathrm{MeV}$ --- the rest energy of the electron. Above
the line, matter; below it, vacuum. This was an acknowledged placeholder, and
it had three problems: the value was imported rather than derived, it was
observer-dependent (two observers moving relative to one another would disagree
about which side of the line a given thing fell), and it was an abrupt cutoff
where physics prefers continuity.

The replacement drops the number entirely and asks instead how small a
disturbance the medium can hold. Every medium has such a scale --- in a
laboratory superfluid it is called the healing length, the shortest distance
over which the medium can bend without tearing. Disturbances larger than it
spread out and remain part of the medium. Disturbances smaller than it stay put,
as localized patterns. The matter/vacuum distinction becomes a property of the
Ocean rather than a line drawn across it.

The result worth noting is what happened next. Calibrating that scale to present
conditions puts it at roughly $386\,\mathrm{fm}$, which is exactly the
electron's own characteristic length, the scale below which it cannot be pinned
down. It is a threshold, not a radius: probed directly, the electron shows no
size at all down to a scale a hundred million times smaller. The electron, on
this account, is simply the lightest pattern the Ocean can hold in place --- and
everything lighter, photons and neutrinos included, is necessarily a ripple
instead. The number that had been an unexplained input came back out as a
consequence. That is the kind of exchange that makes a framework worth
continuing.

\textbf{The third} responded to news from outside. In September 2026 a proof was
announced that a fluid with internal friction can, under smooth external
stirring, tear itself into a singularity in finite time --- a result about
ordinary fluid dynamics with no connection to this framework whatsoever. It
remains unverified and does not transfer directly to a relativistic medium. But
it removed an assumption this framework had been resting on without noticing:
that viscosity is enough to keep a continuum well-behaved forever.

The repair was already present. The smallest-scale limit introduced in the
second revision is precisely what stops a disturbance concentrating without
bound --- but only if the medium resists compression rather than welcoming it.
That condition had never been written down. It is now a stated requirement, and
if the Ocean turns out to have the other sign, the framework fails as written.

\textbf{The fourth} is the one this version records, and it is a change of
mind. The first revision had kept Einstein's geometry intact and set the Ocean
beside it, and every version since had carried that arrangement forward: a
stage, and a medium placed upon it. The stage was never argued for. It was
inherited, from the habit of treating spacetime as the thing that exists and
fields as things that happen in it. Asked directly what the stage was made of,
the framework had no answer, and a medium that fills everything leaves no room
for a second structure to occupy.

So the stage is removed. There is only the Ocean. Einstein's equation stays,
because it describes what is measured with extraordinary precision, but its
standing changes: it is now the description of how the medium's state is
experienced by patterns made of that medium, not a separate structure the medium
sits in. Gravity, on this account, is the medium's response to concentrated
energy. That claim brings obligations the earlier arrangement did not carry,
and they are set out in the technical sections; the heaviest is to derive the
geometry rather than assume it.

\medskip
\noindent
Each revision has the same form: something chosen by hand is removed, and
something forced by the structure takes its place. A substituted tensor, then an
imported number, then an unexamined assumption, then an inherited stage. That a framework can absorb that
process repeatedly is not evidence that it is true. It is evidence that it is
the right kind of thing to keep testing --- which is a lower bar, and the only
one this document claims to clear.

\medskip
\noindent
A note on method, since it is unusual enough to be worth recording. The
revisions above were worked out in dialogue with a large language model, used as
an interlocutor rather than an author: a way of being argued with at the speed
of thinking. There is a small irony in the third revision, where the result that
forced the change was itself produced by a machine, formally verified by
another, and is still waiting on human confirmation. The fourth went the other
way: the position had been the author's from the start, and the dialogue's work
was to notice that the document had never actually said it.

\subsection*{What would kill it}

Four things, named here so that a reader does not have to hunt for them.

\textbf{The scale gap.} For the Ocean to explain galactic rotation it must be
able to act across thousands of light years. For it to place the matter boundary
at the electron it must have structure at the scale of a hundredth of an atom.
These two requirements differ by about thirty-two orders of magnitude. They are
set by different parts of the mathematics, so this is not an outright
contradiction --- but a framework that merely tolerates such a gap has not
explained anything, and this is the most serious unresolved problem in the
document.

A route out now exists, and it is recorded as a route rather than a result. A
hurricane is hundreds of miles across, but that size is not a property of air.
It belongs to the storm: to how much energy and spin were gathered in one place.
Air itself has only small-scale properties. If the same holds here, the galactic
scale is not built into the Ocean at all. A galaxy is not an object that stirs
the medium; it is a region of the medium carrying excess energy and excess
current, of which the visible stars are the dense middle and the wide slow flow
is the outskirts. The Ocean would then need only one built-in size, the small
one, together with the ability to carry very long, slow disturbances at almost
no cost. Laboratory superfluids have that ability for a known reason, a symmetry
of the underlying field. The price is that the field must be a richer object
than the one written down below, and that the calculation showing such a
disturbance reproduces observed galaxies has not been done. Until it is, the gap
stays on this list.

The route does not make the gap smaller. A galaxy really is about $10^{32}$ times
larger than the Ocean's smallest structure, just as a hurricane is about
$10^{14}$ times wider than the spacing of air molecules. What the route changes
is whether that ratio needs explaining. If the large scale belongs to the
disturbance and not to the medium, it is the size of a storm, not a second
setting of the air.

\textbf{The sign.} As above: if the Ocean's self-interaction has the wrong sign
in its present state, nothing arrests collapse and the framework is not viable
in its present form. This is a single calculation away from being settled
either way. Settling it for the Ocean's present state does not settle it for
every time and place. The medium resists compression only in some of its
possible states; in others it may not, and the earliest moments of the present
beat or distant regions could have been in such a state. The rules do not change from place to place, but where the
medium sits within them can.

\textbf{The preferred frame.} Describing the vacuum as a medium gives it a state
of rest, and a state of rest is something Einstein spent a career removing from
physics. Real superfluids do exactly this, so it is not absurd --- but the
experimental limits on any such effect are extraordinarily tight, and the
framework must show it stays inside them.

\textbf{The measured vacuum.} Empty space has already been measured doing
things. It screens electric charge, it scatters light off light, and in very
strong magnetic fields it splits light by polarisation, as a crystal does.
Standard physics predicts these effects by other means, in some cases to many
decimal places. If the Ocean is real, these are its properties, and it must
reproduce the same numbers. Agreement would be strong support. Any disagreement
would be fatal.

To which should be added a possibility that no calculation will resolve: the
agreement between the Ocean's smallest scale and the size of the electron may
simply be a coincidence. The Standard Model already accounts for the electron's
mass by other means. Whether these are two descriptions of one fact or two
unrelated facts that happen to agree is, at present, unknown.

\medskip
\noindent
What follows is the technical statement of all of this. It is written for a
reader comfortable with tensor notation, but the argument it makes is the one
above: that the emptiness between things may not be empty, and that a great deal
of what we currently call unknown may be the behaviour of a single medium that
has been sitting in plain view the whole time.

\clearpage

% =========================================================================
\paragraph{Conventions.}
\label{sec:conventions}
No independent particulate entities are posited. An excitation of the medium
that is localized in the sense of Section~\ref{sec:threshold} is called a
\emph{localized excitation}; one that is not is a \emph{coherent excitation} or
a \emph{flow}. ``Matter'' and ``the matter sector'' denote the localized
population of the one medium, never a second substance. Particle-like behaviour
--- the exchange of energy, momentum and charge in whole units at a single point
--- is treated as a property of how excitations of a quantum field interact,
not as evidence of objects (Section~\ref{sec:threshold}). The word
``particle'' appears only when describing other work, and is marked as that
work's term. The framework is four-dimensional throughout: indices
$\mu,\nu$ run over one dimension of time and three of space, and the Ocean is a
medium in all four. Time is part of the medium's description, not a clock
standing outside it.

\paragraph{Glossary.}
\label{sec:glossary}
The following terms are used with fixed meanings throughout.
\begin{description}[leftmargin=1.5em,style=nextline,itemsep=1pt]
\item[The Ocean] The single continuous medium. It has no edges and no outside,
and it includes every beat. Nothing in the framework exists apart from it.
\item[Pattern] Any excitation of the Ocean, localized or not. Matter and light
are patterns; so is a galaxy.
\item[Localized excitation] A pattern localized in the sense of
Section~\ref{sec:threshold}; what other work calls a particle.
\item[Coherent excitation, flow] A pattern that is not localized.
\item[Matter, matter sector] The localized population of the Ocean, never a
second substance.
\item[The Heartbeat] The whole sequence of beats.
\item[A beat] One expansion and contraction of the Ocean, from one beat
transition to the next.
\item[The present beat] The beat we are in, and the only one any observation
can reach.
\item[Beat transition] The change of state between one beat and the next. Never
a phase change within a beat.
\item[The big bang] The most recent beat transition, as seen from within the
present beat. Not the beginning of the Ocean.
\item[Epoch] A phase within a beat, such as the radiation, matter or
dark-energy epoch. Never a beat.
\item[The observable universe] The part of the present beat that observation
can reach. Neither the whole present beat nor the Ocean.
\end{description}
\noindent ``Universe'' is not used on its own, since what it names is
redefined here; it appears only in ``the observable universe'' and in reporting
other work. ``Cycle'', like ``particle'', appears only when reporting other
work. ``Cyclic'' in the subtitle names the established category of cosmology to
which the Heartbeat belongs.

\section{The Field Equation}

The governing equation for the ``Ocean'' metric is formulated as Einstein
geometry coupled to a dynamic scalar vacuum medium. The central revision
relative to the original formulation is that the viscous response is treated as
a \emph{stress contribution} rather than as a replacement for the geometric
Einstein tensor:
\begin{equation}
\Gmn + P(\phi)\,\gmn \;=\; \kappa(\phi)\Big[\,\Tmat + \Tphi + \Pimn \,\Big],
\qquad
\kappa(\phi) = \frac{8\pi G(\phi)}{c(\phi)^{4}} .
\label{eq:field}
\end{equation}
Here $\Gmn = \Rmn - \tfrac{1}{2} R\, \gmn$ remains the geometric Einstein tensor;
$P(\phi)$ is the dynamic vacuum pressure; $\Tphi$ is the stress-energy of the
scalar field; and $\Pimn$ is its hydrodynamic dissipative stress.

\paragraph{Status of the equation.}
Equation~\eqref{eq:field} is retained as the working equation of the framework,
but its standing has changed. Earlier versions treated $\Gmn$ as a fundamental
structure with the medium added to it. Here the medium is primary: the geometry
on the left-hand side is the effective description of how the medium's state is
experienced by excitations of the medium, and the right-hand side records the
medium's own stresses. The equation is kept because Einstein's description is
correct to the precision it has been tested; the framework's claim is to
explain why it holds (Section~\ref{sec:refractive}), and deriving it from the
dynamics of the medium is the central task that claim creates
(Section~\ref{sec:program}).

% =========================================================================
\section{Tensor Definitions}

\subsection{Geometric Einstein tensor}

The geometric sector retains the standard covariant structure of General
Relativity:
\begin{equation}
\Gmn = \Rmn - \tfrac{1}{2} R\, \gmn .
\end{equation}
This separation is essential because the contracted Bianchi identity gives
$\nabla^{\mu} \Gmn = 0$. Any additional vacuum stresses must therefore satisfy
the corresponding total conservation requirement (Section~\ref{sec:conservation}).

\subsection{Scalar vacuum stress-energy $T^{\phi}_{\mu\nu}$}
\label{sec:Tphi}

The vacuum is represented by a dynamical scalar field rather than a purely
phenomenological density. Let
\begin{equation}
X \equiv -\tfrac{1}{2}\, \nabla_{\alpha}\phi\, \nabla^{\alpha}\phi ,
\end{equation}
and let $L(\phi, X)$ be the scalar-field Lagrangian. Its stress-energy tensor is
\begin{equation}
\Tphi \;=\; L_{,X}\, \nabla_{\mu}\phi\, \nabla_{\nu}\phi \;+\; L\, \gmn .
\end{equation}
This term gives the Ocean a genuine dynamical energy density and pressure. The
specific choice of $L$ determines whether the field behaves as a conventional
scalar, a $k$-essence-like medium, or a more specialized superfluid effective
theory. Section~\ref{sec:threshold} depends on this choice directly.

\paragraph{A candidate refinement.}
\label{sec:complex}
The candidate route for the scale hierarchy (Section~\ref{sec:sec7open},
item~(5)) requires more structure than a single real scalar. Take the medium to be
a complex field with a global $U(1)$ symmetry,
\begin{equation}
\Phi = \rho\, e^{i\theta},
\qquad
\theta \;\to\; \theta + \text{const},
\label{eq:complex}
\end{equation}
and identify the $\phi$ of the preceding expressions with the phase $\theta$.
The shift symmetry forbids a potential for $\theta$, so that
$L(\phi, X) \to L(X)$ and the long-wavelength excitation is a gapless Goldstone
phonon, as in a laboratory superfluid. The modulus $\rho$ is the natural home of
the self-interaction of Section~\ref{sec:defocusing}, and its excitation is
heavy.

This is a condition the route depends on, not an adopted change, and it has a
cost that propagates. An exact shift symmetry forbids any dependence on the
value of $\theta$ itself. The state-dependent quantities $P(\phi)$,
$\kappa(\phi)$, $\xi(\phi)$, $\eta(\phi)$ and $\zeta(\phi)$ would have to be
re-expressed as functions of the modulus $\rho$ or of $X$, and the beat
transitions of the Heartbeat would become transitions of $\rho$. The
same applies to the quartic potential of Section~\ref{sec:defocusing}, which
becomes a potential for $\rho$, and to the mass-gap entry of the table in
Section~\ref{sec:threshold}, which vanishes identically for $\theta$. The
route also brings the framework's field content closer to the complex-field
description of Huang and collaborators \cite{huang2013} and to the phonon
description of Berezhiani and Khoury \cite{berezhiani2015}; the distinctive
claim of Section~\ref{sec:related}, the partition with a retained fundamental
geometry, is unaffected.

\subsection{Vacuum viscosity tensor $\Pi_{\mu\nu}$}

The viscous response represents the dissipative stress response of the scalar
medium to local flow. For a relativistic effective fluid, a first-order
constitutive form is
\begin{equation}
\Pimn = -2\,\eta(\phi)\, \sigma_{\mu\nu} \;-\; \zeta(\phi)\, \theta\, \hmn ,
\end{equation}
where $\eta(\phi)$ is the shear viscosity, $\zeta(\phi)$ the bulk viscosity,
$\theta = \nabla_{\alpha} u^{\alpha}$ the expansion scalar,
$\hmn = \gmn + u_{\mu} u_{\nu}$ the spatial projector orthogonal to the medium
four-velocity $u^{\mu}$, and $\sigma_{\mu\nu}$ the shear tensor.

In regions with coherent vorticity or differential flow, $\Pimn$ can generate
additional gravitational stress. The model therefore investigates whether the
vacuum response can reproduce effects conventionally assigned to dark-matter
halos. The term \emph{rotational support} is used here as a hypothesis about the
gravitational effect of the vacuum stress response; viscosity itself is not
assumed to behave as additional localized mass.

\subsection{Scalar pressure $P(\phi)$}

$P(\phi)$ replaces a fixed cosmological constant as the phenomenological
vacuum-pressure contribution. It is a function of the state of the underlying
scalar field rather than a universal constant:
\begin{equation}
\Lambda\, \gmn \;\longrightarrow\; P(\phi)\, \gmn .
\end{equation}
The \emph{Heartbeat} hypothesis proposes that the scalar field can evolve through
alternating dynamical phases. An effective positive-pressure / negative-pressure
transition may then produce expansion (``diastole'') and contraction
(``systole'') phases. A complete model must derive this behavior from a field
potential or equation of state rather than prescribing an oscillating pressure
by hand.

\subsection{Effective coupling $\kappa(\phi)$}

The coupling between the vacuum state and ordinary stress-energy is allowed to
depend on the local scalar density:
\begin{equation}
\kappa(\phi) = \frac{8\pi G(\phi)}{c(\phi)^{4}} .
\end{equation}
$G(\phi)$ represents a field-dependent effective gravitational coupling. The
quantity $c(\phi)$ is treated initially as an effective propagation speed
associated with the vacuum medium. If it is interpreted as a genuine variable
causal speed, the theory must specify the resulting causal structure and recover
the observed local value $c_{0}$ in the appropriate limit.

\paragraph{The refractive reading.}
\label{sec:refractive}
The account of gravity adopted here is refractive. A wave in a
medium whose propagation speed varies curves toward the region where it travels
more slowly. If concentrated energy lowers the local propagation speed of the
Ocean, light curves inward, and so does every localized excitation, each of which is a
pattern the medium keeps re-making. Where the medium is slower on one side, the
re-making is uneven and the pattern is re-made slightly further toward the slow
side. Nothing pulls; trajectories are turned. This is consistent with the absence of any felt force in free fall. In
the weak field it reproduces the standard equivalence between gravitational
light bending and a refractive index
\begin{equation}
n(r) \;\simeq\; 1 + \frac{2GM}{rc^{2}} .
\end{equation}
Refraction alone does not reproduce the full weak-field and post-Newtonian
behaviour --- perihelion advance, frame dragging, gravitational radiation ---
and extending it to do so is the test this reading must pass
(Section~\ref{sec:program}). Three requirements are decisive. Every excitation
must respond to the medium's state in exactly the same proportion, since all
bodies and light are observed to fall alike to extraordinary precision; here
that equality must follow from everything being made of the same medium. The
response must slow time and stretch space in equal measure: the measured
deflection of starlight by the Sun is twice what slowing alone would give, and
the second half comes from the spatial part. And disturbances of the response
itself, gravitational waves, must travel at the speed of light, as observed when
a neutron-star merger's gravitational and light signals arrived together. The
alternative reading of $c(\phi)$, a genuine variable causal speed, is retained
as the fallback.

% =========================================================================
\section{Scalar-Field Dynamics}

The field $\phi$ must have an independent equation of motion. A generic covariant
form is
\begin{equation}
\Box \phi \;=\; \frac{\partial \Veff}{\partial \phi} \;+\; C\!\left(\phi,\, T,\, \nabla\phi,\, \ldots\right),
\label{eq:eom}
\end{equation}
where $\Veff(\phi)$ is an effective potential and $C$ represents permitted
couplings to matter, curvature, or hydrodynamic variables. The potential and
coupling structure determine the vacuum phases, stability, characteristic sound
speed, and possible Heartbeat behaviour.

% =========================================================================
\section{The Ocean Interpretation}

The framework interprets the observable universe as a dynamical region of a
deeper vacuum medium. The Ocean is not required to begin at the big bang.
Instead, the big bang is interpreted as a beat transition: a change of state of
the medium, a phase transition, or a rapidly expanding solution of the
underlying field equations.

The observable universe is therefore not treated as the ontological boundary of
reality. It is the portion of the deeper continuous vacuum field accessible to
observation. This distinction is a conceptual premise of the framework and must
ultimately be connected to a mathematically well-defined global solution.

% =========================================================================
\section{Cosmological Heartbeat}
\label{sec:heartbeat}

The proposed \emph{Heartbeat} cosmology associates
cosmic expansion and contraction with the evolution of $\phi$. A schematic beat
is
\[
\phi\text{-state transition} \;\rightarrow\; \text{pressure reversal} \;\rightarrow\;
\text{expansion} \;\rightarrow\; \text{field evolution} \;\rightarrow\;
\text{contraction} \;\rightarrow\; \text{new phase}.
\]
The model does not require that each beat create the underlying vacuum field.
Instead, each \emph{beat} (Section~\ref{sec:glossary}) may be a dynamical state
of the same deeper medium.

Two kinds of statement are kept apart in what follows. Section~\ref{sec:withinbeat}
concerns the present beat, which is the only one any observation can reach.
Section~\ref{sec:acrossbeats} concerns the sequence of beats and the transitions
between them, about which no observation made within a beat can speak directly.

\subsection{Within the present beat}
\label{sec:withinbeat}

Everything known about time is known from within the present beat. Every
observer and every instrument is a pattern of the Ocean in this
beat, and every observation is of this kind. Here time is the pace at which the
Ocean re-makes its patterns, measured by clocks that are themselves such
patterns. Durations are meaningful and measurable, but local: clocks run at
different rates in different places, as General Relativity describes and as the
account of Section~\ref{sec:refractive} requires.

The pace of the beat is not fixed. While matter dominated, its gravity slowed
the expansion; distant supernovae show that the expansion is now accelerating
\cite{riess1998, perlmutter1999}. There are further indications that the
acceleration is itself evolving: baryon acoustic oscillation measurements from
the DESI survey, combined with the microwave background and supernova samples,
prefer a dark-energy component that changes over time to a constant one, at
roughly $3$ to $4\sigma$ depending on the supernova sample, short of the level
conventionally required for discovery \cite{desi2025}. In this framework such
variation is the Ocean's state changing through $P(\phi)$, not a departure from
a constant. One caution follows from the same data. The preferred evolution
crosses the boundary $w = -1$, which a single scalar field with a standard
kinetic term cannot readily do; the survey's authors note that multiple fields,
additional internal degrees of freedom or a non-minimal coupling can evade the
difficulty \cite{desi2025}. If the evolution is confirmed, the Ocean's pressure
sector would need such structure, and the complex field of
Section~\ref{sec:complex} and the coupling $\kappa(\phi)$ are the candidates
already present.

\subsection{Across beats}
\label{sec:acrossbeats}

Nothing in this subsection is observable from within the present beat. It
states what the framework permits, not what has been found, and the two
subsections should not be read into one another.

No clock survives the transition between beats. The patterns that keep time
are diluted or remade, and the Ocean's state, including $\xi$, may differ from
one beat to the next. Durations therefore cannot be compared from beat to beat,
and ``faster'' or ``slower'' across beats can only mean that different beats
pass through different sequences of states. The framework requires no
repetition: each beat may differ in its expansion, its reset and its $\xi$.
Across beats the Heartbeat is counted, not timed.

Whether such a sequence can avoid singularities, entropy accumulation and
instabilities is an open mathematical question. Because the stiffness that
arrests collapse depends on the medium's state (Section~\ref{sec:defocusing}),
the answer may differ between phases of a beat: a contraction that drives the
medium out of its stiff state need not be arrested by the mechanism that
protects the present epoch.

The nearest established precedent is the cyclic model of Steinhardt and Turok
\cite{steinhardt2002}, in which a scalar field rolling in a potential drives an
endless sequence of expansions and contractions, each big bang being a
transition from a preceding contraction with finite temperature and density.
Two of its answers bear directly on the questions above. Entropy does not
accumulate from cycle to cycle because a long phase of accelerated expansion,
the present dark-energy epoch, dilutes the matter, radiation and black holes of
the previous cycle before contraction begins. And the nearly scale-invariant
density fluctuations are generated during the slow contraction rather than by
inflation, with the distinguishing prediction of no long-wavelength primordial
gravitational waves. Both are available to the Heartbeat in principle. The
difference lies at the bounce: in that model the transition is motivated by
colliding branes along an extra spatial dimension, with the four-dimensional
field theory carrying a matching rule supplied by hand. The premise of this
framework admits no space outside the Ocean, so the bounce must instead come
from the medium itself, through the healing-length floor and the state
dependence of its stiffness (Section~\ref{sec:defocusing}).

One consequence of this route can be tested from within the present beat. If
the Heartbeat seeds the density fluctuations of the present beat during the
preceding slow contraction, as in the Steinhardt--Turok model, rather than by
inflation, it predicts essentially no long-wavelength primordial gravitational
waves. The present upper limit on their amplitude relative to the density
fluctuations, from Planck combined with BICEP2/Keck Array data, is
$r < 0.056$ \cite{planck2018inflation}, and forthcoming microwave-background
experiments will test it much further. A detection of primordial gravitational
waves would count against a contraction-seeded Heartbeat; continued
non-detection would leave it viable. This route also avoids a difficulty noted
for inflation in this framework: the field values that inflation requires lie
far above the scale set by $\xi_{0}$.

% =========================================================================
\section{Galactic Dynamics}

In the galactic regime, the hypothesis is that spatial gradients, vorticity, and
coherent flow of the vacuum field generate an additional effective stress. The
observable circular velocity would then be determined by the combined baryonic
and vacuum-field gravitational response:
\begin{equation}
v_{c}^{2}(r) \;=\; v_{b}^{2}(r) \;+\; v_{\phi,\mathrm{eff}}^{2}(r).
\end{equation}
Here $v_{b}$ is the baryonic contribution and $v_{\phi,\mathrm{eff}}$ denotes the
effective contribution produced by the scalar field and its stress response. The
goal is not to insert an arbitrary halo profile, but to derive
$v_{\phi,\mathrm{eff}}(r)$ from $\phi$, $\Pimn$, and the field equations.

\paragraph{Rotation is a special case.}
The relation above applies to rotationally supported disks. Galaxies also carry
random motion, inflow and outflow, vertical oscillation, bars and spiral
patterns, and motion through their surroundings. Pressure-supported systems with
little net rotation --- elliptical galaxies and dwarf spheroidals --- follow the
same radial acceleration relation as disks \cite{lelli2017}. Whatever links the
vacuum contribution to the baryons therefore cannot depend on rotation, and the
framework must apply to pressure-supported galaxies as well.

\paragraph{One structure, not two.}
\label{sec:onestructure}
The decomposition above is bookkeeping and should not be read as a statement
that a galaxy acts on the medium from outside. In this framework a galaxy is a
region of the Ocean carrying excess localized energy and elevated current. Its
baryonic content is the $\Qq \gg 1$ population of that region and the extended
flow is the $\Qq \ll 1$ population, in the sense of
Section~\ref{sec:threshold}; the two are the dense interior and the diffuse
exterior of a single solution of the field equations. This differs from
treatments in which galaxies are external sources perturbing the superfluid
\cite{huang2013}.

Two consequences follow. First, the kiloparsec scale is a property of the
individual solution, fixed by the full state of the disturbance --- its energy,
its organised and random flow, and its exchange with the surrounding medium ---
and need not be a parameter of the medium; this is the basis of the
candidate route of Section~\ref{sec:sec7open}, item~(5). Second, if the solution
is fixed by its baryonic content --- the question posed by the Size task of
Section~\ref{sec:program} --- the baryonic distribution determines
$v_{\phi,\mathrm{eff}}(r)$ with no freedom adjusted galaxy by galaxy. The
observed radial acceleration relation has that form: across rotationally
supported galaxies the total acceleration is fixed by the baryonic acceleration
alone, with little or no intrinsic scatter and no sign of a second parameter
\cite{mcgaugh2016, lelli2017}. That is a target to be derived, not a result.

It also sharpens the exposure recorded in Section~\ref{sec:related}. A
contribution fixed by the baryons is precisely the kind that risks being
parallel to the baryonic gravitational field, and a parallel contribution is
excluded by Milky Way vertical kinematics \cite{lisanti2019, lisanti2023}. The
single-structure reading therefore needs a vacuum contribution whose magnitude
is set by the baryons while its direction is not slaved to theirs. Whether the
field equations permit that is not known.

\paragraph{The vacuum contribution is a flow.}
\label{sec:flowfield}
The decomposition $v_{c}^{2} = v_{b}^{2} + v_{\phi,\mathrm{eff}}^{2}$ reduces
the vacuum's response to a single radial quantity. In the framework it is a
flow in time and space together, not a single radial number. Momentum conservation means that any local acceleration
of the medium produces shear against neighbouring regions and, for a disturbance
moving through its surroundings, a wake; the shear term $\sigma_{\mu\nu}$ of
$\Pimn$ is where this enters. Such a flow is not constrained to lie parallel to
the baryonic gravitational field. A wake is aligned with the direction of
motion, not with the baryonic field. This is one way the vacuum contribution
could satisfy the parallelism criterion above, and it is untested. It also
implies an asymmetry: the vacuum contribution of a moving galaxy should be
offset or lopsided relative to its direction of motion. Colliding clusters, in
which the inferred extra mass follows the galaxies rather than the slowed gas,
are the hard case for any such picture.

% =========================================================================
\section{The Localization Threshold}
\label{sec:threshold}

\subsection{Why a fixed threshold fails}

The earlier formulation partitioned energy between sectors by a declared
inequality:
\[
E > 0.511\,\mathrm{MeV} \;\Rightarrow\; \text{localized matter sector},
\qquad
E \le 0.511\,\mathrm{MeV} \;\Rightarrow\; \text{scalar-fluid density } \phi .
\]
This has three defects, only the first of which is usually noticed.

\begin{enumerate}[label=(\arabic*)]
\item \textbf{It is an unexplained parameter.} The value is imported from the
electron rest mass, which the framework does not derive.
\item \textbf{It is not covariant.} $E$ is frame-dependent. A boost changes which
sector a given excitation belongs to, so the partition is observer-dependent ---
unacceptable in a theory built on the covariant field equation~\eqref{eq:field}.
\item \textbf{It is discontinuous.} A step function requires an exchange term
coupling $\Tmat$ and $\Tphi$. Combined with the variable coupling $\kappa(\phi)$,
this makes the conservation conditions of Section~\ref{sec:conservation}
essentially impossible to satisfy.
\end{enumerate}

The revision removes all three by replacing the declared threshold with a
property of the vacuum field's own excitation spectrum.

\subsection{The excitation spectrum of $\phi$}

Perturb the field about a background configuration,
\begin{equation}
\phi(x) = \bar{\phi}(x) + \delta\phi(x),
\end{equation}
and let $u^{\mu}$ be the four-velocity of the vacuum medium with spatial
projector $h^{\mu\nu} = g^{\mu\nu} + u^{\mu} u^{\nu}$. Expanding the Lagrangian
$L(\phi, X)$ of Section~\ref{sec:Tphi} to second order in $\delta\phi$ gives a
quadratic action of the form
\begin{equation}
S_{2} = \frac{1}{2}\int\! \sqrt{-g}\,\Big[
\Kk \big(u^{\mu}\partial_{\mu}\delta\phi\big)^{2}
- L_{,X}\, h^{\mu\nu} \partial_{\mu}\delta\phi\, \partial_{\nu}\delta\phi
- \Veff''\, \delta\phi^{2}
- \Gg \big(h^{\mu\nu}\partial_{\mu}\partial_{\nu}\delta\phi\big)^{2}
\Big],
\label{eq:S2}
\end{equation}
with $\Kk \equiv L_{,X} + 2X L_{,XX}$. The final term is a gradient-stiffness
(quantum-pressure) operator. In a superfluid effective theory it arises from the
same expansion; here it must be \emph{derived} from the chosen $L$ or from an
underlying superfluid EFT, not assumed (see Section~\ref{sec:sec7open}).

Varying~\eqref{eq:S2} and evaluating in the medium rest frame yields the
dispersion relation
\begin{equation}
\boxed{\;
\omega^{2}(k, \phi) \;=\; \Ogap^{2}(\phi) \;+\; c_{s}^{2}(\phi)\, k^{2}
\;+\; \frac{\hbar^{2}}{4 \mstar^{2}(\phi)}\, k^{4} \; }
\label{eq:dispersion}
\end{equation}

\subsection{The three characteristic scales}

Every coefficient in~\eqref{eq:dispersion} is fixed by the Lagrangian rather
than chosen:

\begin{center}
\begin{tabularx}{\textwidth}{@{}l l X@{}}
\toprule
\textbf{Quantity} & \textbf{Definition} & \textbf{Physical meaning} \\
\midrule
Sound speed & $c_{s}^{2} = L_{,X} / \Kk$ &
Propagation speed of coherent Ocean disturbances \\
Mass gap & $\Ogap^{2} = \Veff''(\bar{\phi}) / \Kk$ &
Curvature of the effective potential at the local vacuum state \\
Effective inertia & $\mstar = \mstar(\Gg, \Kk)$ &
Stiffness of the field against short-wavelength bending \\
\bottomrule
\end{tabularx}
\end{center}

From these follows the single scale that carries the whole section --- the
\emph{healing length}:
\begin{equation}
\xi(\phi) \;=\; \frac{\hbar}{\mstar(\phi)\, c_{s}(\phi)} .
\label{eq:healing}
\end{equation}
$\xi$ is the shortest distance over which the vacuum field can vary without the
gradient term dominating. It is the Ocean's localization scale: a threshold, not
a granularity (Section~\ref{sec:sec7open}, item~(7)).

\subsection{The localization criterion}

Define the dimensionless quantity
\begin{equation}
\Qq(\phi, k) \;\equiv\; \xi^{2}(\phi)\; h^{\mu\nu} k_{\mu} k_{\nu} .
\label{eq:criterion}
\end{equation}
Because $h^{\mu\nu}$ projects onto the rest frame of the medium, $\Qq$ is
constructed covariantly from the excitation's four-momentum and the medium's own
state. It replaces the frame-dependent $E$ of the old formulation.
\begin{align}
\Qq \ll 1 &\;\Longrightarrow\; \omega \approx c_{s} k
&&\text{phononic branch; delocalized; contributes to } \Tphi , \\
\Qq \gg 1 &\;\Longrightarrow\; \omega \approx \hbar k^{2} / 2\mstar
&&\text{localized branch; contributes to } \Tmat .
\end{align}

The crossover sits at $k_{c} = 1/\xi(\phi)$, and the corresponding energy is
\begin{equation}
E_{c}(\phi) = \hbar\, \omega(k_{c}) \;\approx\; \alpha\, \mstar(\phi)\, c_{s}^{2}(\phi),
\qquad \alpha = \mathcal{O}(1).
\label{eq:Ec}
\end{equation}

\paragraph{The partition is smooth, not switched.}
Define a monotonic weighting $f(\Qq)$ with $f(0) = 0$ and $f(\infty) = 1$ ---
for example $f = \Qq / (1 + \Qq)$ --- and split the mode integral:
\begin{equation}
\Tmat = \int\! d^{3}k \; f(\Qq)\, t_{\mu\nu}(k),
\qquad
\Tphi = \int\! d^{3}k \; \big[1 - f(\Qq)\big]\, t_{\mu\nu}(k).
\end{equation}
Since both sectors are populations of the \emph{same} field, their sum is
conserved identically. No exchange term is required, and the consistency
conditions of Section~\ref{sec:conservation} are no longer obstructed by the
threshold.

\subsection{Recovering $0.511$~MeV as a calibration}

Requiring $E_{c}(\phi_{0}) \approx 0.511\,\mathrm{MeV}$ in the present vacuum
state fixes
\begin{equation}
\xi(\phi_{0}) = \frac{\hbar c}{E_{c}} \approx 386\,\mathrm{fm},
\end{equation}
which is the reduced Compton wavelength of the electron. This is a derived
consequence rather than a coincidence. A localized excitation of rest energy
$mc^{2}$ has Compton wavelength $\bar{\lambda}_{C} = \hbar / mc$; it can localize within the medium
only if $\bar{\lambda}_{C} \lesssim \xi_{0}$, which requires
\begin{equation}
m \;\gtrsim\; \frac{\hbar}{c\, \xi_{0}} \;=\; m_{e} .
\end{equation}

The electron is therefore the lightest excitation the present vacuum can hold as
a localized pattern. Anything lighter has a Compton wavelength longer than the
Ocean's localization scale and cannot be localized in it --- it is necessarily a coherent field
excitation. This is offered as the framework's explanation for why photons and
neutrinos behave as field phenomena while the electron is the floor of the
localized sector. The value $0.511\,\mathrm{MeV}$ is demoted from axiom to
measurement: it is the readout of $\xi(\phi_{0})$, not an input.

\subsection{Consequences}

\textbf{The threshold is local and dynamical.} $E_{c} = E_{c}(\phi(x))$, so
regions in different vacuum states have different matter thresholds. This
connects the present section to the Heartbeat cosmology: a phase transition of
$\phi$ is also a transition in what the vacuum is \emph{able to hold} as matter.
Where $\xi$ grows, the localization floor rises and previously localized
states are no longer supported.

\smallskip
\noindent
\textbf{It predicts a varying electron mass.} If $\xi$ evolves, so does the
effective $m_{e}$. This is a genuine observational handle --- and a genuine
constraint.

\smallskip
\noindent
\textbf{It introduces a preferred frame.} The dispersion
relation~\eqref{eq:dispersion} is stated in the rest frame of $u^{\mu}$. This is
honest --- real superfluids do exactly this --- but it is a departure from exact
local Lorentz invariance and must be reconciled with precision tests.

\smallskip
\noindent
\textbf{Particle-like behaviour does not require smallness.} An excitation
appears particle-like because it exchanges energy, momentum and charge in whole
units and at a single point. Both properties follow from the medium being a
quantum field with local couplings, independently of the localization scale.
The healing length is a threshold for localization, not a radius, and above it
the term used here is \emph{excitation} or \emph{coherent structure}, whose
size is set by circumstance.

\subsection{Open items specific to this section}
\label{sec:sec7open}

\begin{enumerate}[label=(\arabic*)]
\item \textbf{Derive the gradient-stiffness term $\Gg$} from a covariant action
rather than importing it from the non-relativistic Bogoliubov form. Without
this, $\mstar$ and hence $\xi$ are not defined by the theory.
\item \textbf{Stability.} Require $L_{,X} > 0$ and $\Kk = L_{,X} + 2X L_{,XX} > 0$;
otherwise $c_{s}^{2} < 0$ (gradient instability) or the kinetic term flips sign
(ghost).
\item \textbf{Lorentz-violation bounds.} Show $c_{s} \to c_{0}$ in the local limit
to the precision demanded by clock-comparison and photon/neutrino time-of-flight
tests, and demonstrate that the $k^{4}$ term is suppressed at accessible
energies. The $k^{4}$ term becomes significant for wavelengths near $\xi_{0}$,
that is at energies near $0.5\,\mathrm{MeV}$. Photons from distant gamma-ray
bursts show no energy-dependent arrival times at energies far above this, so the
$k^{4}$ term cannot act on the electromagnetic sector, nor on electrons, at the
scale $\xi_{0}$. Either it is confined to excitations of $\phi$, with a stated
reason, or the framework is excluded. Relatedly, a gamma-ray photon has a
wavelength far below $\xi_{0}$, so the criterion~\eqref{eq:criterion} must be
stated as applying to excitations of $\phi$ only, or it would classify such
photons as localized.
\item \textbf{Varying-$m_{e}$ bounds.} Quasar absorption spectra constrain drift
in $m_{p}/m_{e}$ at roughly the $10^{-5}$--$10^{-6}$ level over cosmological
time; the Oklo natural reactor constrains it locally. Any Heartbeat evolution of
$\xi$ must be negligibly slow over the epochs these measurements probe, and
largely confined to beat transitions.
\item \textbf{The scale hierarchy.} Galactic-scale effects require the scalar's
Compton range to be of order a kiloparsec, implying
$\Ogap \sim 10^{-26}\,\mathrm{eV}$. But $\xi_{0} \approx 386\,\mathrm{fm}$
implies a stiffness scale near $0.5\,\mathrm{MeV}$. These differ by roughly
thirty-two orders of magnitude. They are set by different operators ---
$\Veff''$ versus $\Gg$ --- so this is not immediately inconsistent, but a
credible model must \emph{explain} the separation rather than merely tolerate
it. This is the most serious open problem in the revised section.

\emph{Candidate route.} The estimate $\Ogap \sim 10^{-26}\,\mathrm{eV}$ assumes
that the kiloparsec scale is intrinsic to the medium. On the single-structure
reading of Section~\ref{sec:onestructure} it is instead a property of the
individual galactic solution. The requirement on the medium then weakens from a
tuned value to an upper bound,
\begin{equation}
\Ogap \;\lesssim\; 10^{-26}\,\mathrm{eV},
\end{equation}
which $\Ogap = 0$ satisfies. A vanishing gap is protected, rather than tuned,
if $\phi$ is the phase of a complex field with a $U(1)$ shift
symmetry~\eqref{eq:complex}; a small nonzero gap from soft breaking of that
symmetry would be technically natural. The medium would then carry one intrinsic
length scale, $\xi_{0}$, and the hierarchy would be a ratio between a parameter of the
medium and the size of a particular solution, which is not a naturalness
problem. In the same construction the heavy modulus is the expected origin of
the $k^{4}$ term in~\eqref{eq:dispersion}, which would bear on item~(1).

None of this is established. The route trades the hierarchy for three
obligations: to show that the symmetry survives the couplings of
equation~\eqref{eq:field}; to say what fixes the size of a galactic solution;
and to pass the vertical-acceleration test in the form stated in
Section~\ref{sec:onestructure}. It also carries the cost recorded in
Section~\ref{sec:complex}. Until those are met the hierarchy stands as an open
problem.

The route does not remove the ratio between $\xi_{0}$ and galactic scales; it
changes it from a separation between two parameters of the medium into the size
of a solution relative to the medium's one intrinsic length. A consistency check
follows from the circulation quantum. A superfluid carries rotation in quantized
vortices whose areal density is fixed by the local rotation rate and the mass of
the condensate quanta (Feynman's rule). For quanta at the mass implied by
$\xi_{0}$, and the rotation of the solar neighbourhood
($220\,\mathrm{km\,s^{-1}}$ at $8\,\mathrm{kpc}$), the vortex spacing is of
order $600\,\mathrm{km}$, so the medium is smooth on galactic scales and the
route is not contradicted by granularity. The estimate assumes $c_{s} \approx c$
and local rigid rotation. Because the medium then carries a length and no
intrinsic acceleration, the acceleration scale $g_{\dagger}$ of the radial
acceleration relation \cite{mcgaugh2016} must arise elsewhere, most plausibly
from the cosmological background state.
\item \textbf{Relation to the Standard Model.} The Higgs mechanism already
accounts for $m_{e}$ via a Yukawa coupling. The framework must state whether
$\xi_{0}$ and the electron Yukawa are independent quantities that happen to
agree, or whether one is meant to determine the other.
\item \textbf{Size and spin of the localized excitation.} $\xi_{0}$ is the scale
below which an excitation localizes, not its radius. Quantum electrodynamics has
the same separation: the electron's reduced Compton wavelength limits how far it
can be localized without pair creation, while scattering and its magnetic moment
show no internal structure down to about $10^{-18}\,\mathrm{m}$. The framework
must show that its localized excitation responds as a point to probes at that
resolution. A second route exists: $\xi(\phi)$ is field-dependent, so the local
healing length inside a concentrated excitation may be far smaller than
$\xi_{0}$. That route is constrained from the other side, since the healing
length must not shrink without bound in states where the medium is stiff, or the
floor that arrests collapse in
Section~\ref{sec:defocusing} disappears.

Separately, the electron has spin $\tfrac{1}{2}$. Excitations of a scalar
field, real or complex, carry integer spin. The localized sector therefore
requires structure that the present scalar formulation does not contain, and
this applies to every fermion, including the neutrinos described above as field
phenomena.
\end{enumerate}

% =========================================================================
\section{Limiting Regimes}
\label{sec:regimes}

\begin{center}
\begin{tabularx}{\textwidth}{@{}l X X@{}}
\toprule
\textbf{Regime} & \textbf{Required behavior} & \textbf{Physical objective} \\
\midrule
GR / Solar System &
$\phi \to \phi_{0}$; $G(\phi) \to G_{0}$; $c(\phi) \to c_{0}$; vacuum stresses
negligible &
Recover tested General Relativity \\
Galactic &
$\Pimn$ and scalar gradients become significant &
Explain rotation curves without dark matter in the particle form its
proponents posit \\
Cosmological &
$P(\phi)$ and $\Tphi$ contribute on large scales &
Generate expansion history and effective dark-energy behavior \\
Beat transition / Heartbeat &
$\phi$ evolves between dynamically distinct states; $\xi(\phi)$ shifts &
Provide a mechanism for the expansion and contraction of beats and for changes
in the localization floor \\
High-energy &
Mode occupation crosses $\Qq \sim 1$ &
Test the derived localization threshold of
Section~\ref{sec:threshold} \\
Strong field / black hole &
Outward waves turned back at a horizon; collapse arrested near the healing
length if $\lambda > 0$ &
Match horizon-scale imaging and merger ringdowns; determine whether a
singularity forms \\
\bottomrule
\end{tabularx}
\end{center}

\subsection{Black holes}
\label{sec:blackholes}

In the refractive reading of Section~\ref{sec:refractive}, a black hole is a
region where waves are slowed enough that an outward-directed wave is turned
back. Laboratory analogues make this concrete. A fluid flowing faster than its
own sound speed forms a horizon that sound cannot cross, and such a horizon has
been made in an atomic Bose--Einstein condensate, where the spontaneous
analogue of Hawking radiation was observed together with the entanglement of its
pairs \cite{steinhauer2016}. In that system the shortest length scale is the
healing length $\xi = \hbar/mc_{s}$, the same construction as
Section~\ref{sec:threshold}. General Relativity itself admits an exact
description of a stationary black hole as space flowing inward through a flat
background, reaching the speed of light at the horizon \cite{hamilton2008}. For
a rotating black hole that description has the river twist rather than swirl. A
draining vortex in water is nonetheless an analogue of a rotating black hole,
and rotational superradiance --- waves extracting energy from the rotation --- has
been observed in one \cite{torres2017}.

Three questions follow.

\textbf{The core.} With $\lambda > 0$ the healing length resists compression,
so collapse may terminate in a core of finite density rather than a singularity.
That holds only while the compressed medium stays in a stiff state; if collapse
drives it out of that state, the arrest is not guaranteed
(Section~\ref{sec:defocusing}).
This is the question Section~5 asks of a contraction phase, posed for a single
object.

\textbf{Two horizons.} The authors of the river model stress that its flat
background has no observable meaning \cite{hamilton2008}. This framework
retains $\Gmn$ as fundamental and adds a physical medium, so a geometric
horizon (where escape requires $c$) and a horizon of the medium (where escape
requires $c_{s}$) need not coincide. If they differ, the shell between them
requires account. If they always coincide, that suggests the geometry is the
medium's own flow, which bears directly on the structural question of
Section~\ref{sec:related}. A medium that literally flowed inward would also have
to accumulate somewhere; the refractive reading avoids this, since the medium's
state changes near the mass without net inflow.

\textbf{Observation.} Horizon-scale imaging and gravitational-wave ringdowns
agree with General Relativity, so any departure must lie inside the horizon or
below current sensitivity.

% =========================================================================
\section{Conservation and Consistency Conditions}
\label{sec:conservation}

Because $\nabla^{\mu} \Gmn = 0$, the complete right-hand side of~\eqref{eq:field}
together with the pressure sector must satisfy a compatible conservation law.
With variable $\kappa(\phi)$, the simple condition $\nabla^{\mu} T_{\mu\nu} = 0$
is generally not sufficient by itself. The scalar equation~\eqref{eq:eom} and the
matter coupling must be chosen so that the full theory is
diffeomorphism-consistent.

The revised Section~\ref{sec:threshold} assists here rather than obstructing:
because $\Tmat$ and $\Tphi$ are now weighted populations of a single field rather
than two sectors joined by a step function, no discontinuous exchange term is
introduced at the threshold.

\subsection{Global regularity and the defocusing condition}
\label{sec:defocusing}

A separate question, treated in earlier versions as a requirement that the medium
remain smooth for all time, is whether it does. The framework cannot appeal to
dissipation alone to secure this. Viscosity is conventionally expected to drain
an energy cascade before it concentrates without bound, but that expectation is
not a theorem: finite-time blowup constructions for the forced three-dimensional
Navier--Stokes equations were announced in September 2026 and, while they remain
subject to independent verification and do not transfer directly to a
relativistic scalar medium, they remove the intuition that a viscous continuum is
automatically globally regular. The shear and bulk viscosities $\eta(\phi)$ and
$\zeta(\phi)$ of Section~2.3 therefore cannot be assumed to guarantee what they
were implicitly relied upon to guarantee.

The mechanism available to this framework is not dissipation but the ultraviolet
cutoff supplied by Section~\ref{sec:threshold}. The gradient-stiffness term in
the dispersion relation~\eqref{eq:dispersion} grows as $k^{4}$ and therefore
dominates the cascade at $k \sim 1/\xi(\phi)$, arresting concentration at the
healing length. This is the mechanism by which a laboratory superfluid remains
regular where the corresponding classical fluid description does not.

That arrest is conditional on the sign of the self-interaction. Writing the
relevant quartic term of the effective potential as
\begin{equation}
\Veff(\phi) \supset \frac{\lambda}{4}\left(\phi^{2} - v^{2}\right)^{2},
\end{equation}
the medium must be \emph{defocusing}, $\lambda > 0$: compression must raise the
energy and be resisted. The defocusing case is energy-coercive and the cutoff at
$\xi$ holds. In the focusing case $\lambda < 0$ the self-interaction rewards
further compression, the cutoff does not arrest the cascade, and concentration
accelerates instead. The sign is therefore a stability requirement of the same
standing as $L_{,X} > 0$ and $\Kk > 0$, not a modelling preference. On the
candidate route of Section~\ref{sec:complex} the potential belongs to the
modulus $\rho$ rather than to $\phi$, and the argument carries over unchanged.

\paragraph{Regularity is a property of the state, not a guarantee.}
The sign of $\lambda$ does not settle the matter for all times and places,
because the stiffness that resists compression is the response of the medium
\emph{around the state it occupies}. With the Lagrangian held fixed, that
response differs between states. Even the quartic form above, with
$\lambda > 0$, has curvature
\begin{equation}
\Veff''(\phi) = \lambda\left(3\phi^{2} - v^{2}\right),
\end{equation}
which is positive about the present vacuum $\phi = v$ and negative for
$|\phi| < v/\sqrt{3}$. A medium driven into that region --- by a beat
transition, a contraction, or the core of a collapsing object --- is no longer
protected by the mechanism above. For this form the instability drives the
medium back toward the stable state rather than into collapse; whether the full
potential admits genuinely focusing states is open. The law is fixed; what
varies is where the medium sits within it. No free function is added.

Four constraints follow. (i) Regions in different states are separated by
boundaries that carry energy; walls of this kind within the observable universe
are tightly excluded, so differing regions must lie beyond the horizon, in the
past, or be separated without such walls. (ii) The microwave background is
uniform to about one part in $10^{5}$, which bounds how far the state could
have varied across the observable universe at that epoch. (iii) A region that
loses its stiffness collapses quickly and leaves relics, compact objects or
primordial black holes, whose abundance is bounded. (iv) Where smoothness
fails, the framework must state what follows --- a bounce, a phase transition,
or a genuine singularity at which it ceases to predict --- and must tie each
failure to a specified state of the medium, so that the possibility cannot be
invoked case by case.

This section's argument rests on the framework's own structure. It does not
depend on the blowup constructions cited above, which await independent
verification.

A successful formulation should explicitly establish:
\begin{enumerate}[label=(\arabic*)]
\item covariance;
\item total energy-momentum conservation;
\item a well-posed scalar-field equation;
\item absence of pathological ghosts or gradient instabilities;
\item a stable low-density / weak-field limit;
\item compatibility with precision tests of gravity and light propagation;
\item a defocusing self-interaction about the present vacuum state, so that
the healing-length cutoff of Section~\ref{sec:threshold} arrests rather than
accelerates concentration there, together with an account of the states in
which it does not (Section~\ref{sec:defocusing}).
\end{enumerate}


% =========================================================================
\section{Relation to Existing Work}
\label{sec:related}

The proposal that the vacuum is a superfluid, and that dark matter and dark
energy are two behaviours of it rather than two substances, is not new. This
section states what is already established, so that the framework's actual
claim can be isolated from the parts of it that are inherited.

\subsection{Two families of superfluid-vacuum programme}

Existing work divides on whether spacetime geometry is fundamental.

\paragraph{Emergent gravity.} Volovik's programme \cite{volovik2003} treats the
quantum liquid as prior to spacetime: the metric, Lorentz invariance and gauge
structure appear as low-energy collective behaviour of the condensate.
Zloshchastiev's logarithmic superfluid vacuum theory \cite{zloshchastiev2020}
derives an induced gravitational potential from the vacuum wavefunction and
concludes that dark matter and dark energy are manifestations of the same
object and therefore cannot be independent. That conclusion is the one reached
here. The mechanism is not: Zloshchastiev distinguishes his approach explicitly
from models that work by modifying the stress-energy tensor of the Einstein
equations.

Volovik's programme also supplies an argument this framework can use.
Inhabitants of a superfluid, built from its own low-energy excitations, would
perceive an effectively relativistic world and could not detect the underlying
medium directly \cite{volovik2003}. The same argument would account for the
precision of Lorentz invariance at accessible energies here. It explains what
cannot be observed; it does not exempt the framework from effects that are
observed (Section~\ref{sec:related}, deficiency~(4)).

\paragraph{Modified source.} Huang and collaborators \cite{huang2013} treat a
complex vacuum scalar field as a cosmic superfluid within standard General
Relativity, identifying its energy density with dark energy and departures from
vacuum density with dark matter. That work also treats galaxies as external
sources perturbing the superfluid, and obtains the galactic halo together with
the creation of vortices by galactic rotation --- the closest existing
precedent for the galactic sector of Section~6. Berezhiani and Khoury \cite{berezhiani2015}
construct an effective field theory in which dark matter is a superfluid with a
galaxy-scale coherence length, described by phonons rather than, in the standard model's terms, collisionless
particles, recovering MOND phenomenology on galactic scales. That model has
since been disfavoured by Milky Way data \cite{lisanti2023}: it over-predicts
vertical accelerations of disk stars even while reproducing the rotation curve. Viscous cosmology
\cite{dou2011} models the dark sector as a single fluid whose bulk viscosity
produces a negative effective pressure and thereby mimics dark energy. The
logotropic models of Chavanis \cite{chavanis2026} belong to the same family,
yielding a density profile that falls as $r^{-1}$ and offering an alternative to
MOND that accounts for the Tully--Fisher relation.

On the cosmological side, the closest structural precedent is the cyclic model
of Steinhardt and Turok \cite{steinhardt2002} (Section~5). It, too, is a
four-dimensional scalar field theory in which one field accounts for dark
energy, the reversal from expansion to contraction, and the transition between
cycles, and it couples that field to matter through a field-dependent factor.
Its authors note that this coupling is a modification of General Relativity
and produces a fifth force violating the equivalence principle unless the
coupling's variation is very small at the present field value. The same
constraint applies to $\kappa(\phi)$ here, and it is the first of the
requirements of Section~\ref{sec:refractive}: every excitation must respond
to the medium in exactly the same proportion.

Earlier versions placed this framework in the second family. With the position
adopted in this version (the preface and Section~1), its account of what is
fundamental moves to the first: the medium is primary and geometry is its
effective description. Its working equation remains that of the second family,
Equation~\eqref{eq:field}, with the medium's stresses on the right-hand side.

\subsection{What is inherited and what is not}

Inherited: the identification of the vacuum as a scalar condensate; the
proposal that the dark sector is one medium rather than two substances; the
use of bulk and shear viscosity to generate an effective pressure; the
appearance of a coherence length in the galactic regime.

Inherited also, and more directly than the preceding list suggests: the
generation of galactic structure by vorticity in a vacuum superfluid. Huang and
collaborators \cite{huang2013} obtain vortices from galactic rotation within a
nonlinear Klein--Gordon description in which galaxies act as external sources.
Section~6 reaches for the same phenomenon through different machinery --- a
dissipative stress tensor $\Pimn$ entering the field equation~\eqref{eq:field}
rather than a source term in a wave equation. Whether these are distinct
physical mechanisms or one mechanism in two formalisms is not settled here, and
a credible version of this framework must say which.

The premise that ordinary matter is itself an excitation of the vacuum medium
is also not new, and it is worth being precise about who holds it. Huang
\cite{huang2013} and Berezhiani and Khoury \cite{berezhiani2015} are
two-species: the condensate constitutes the dark sector while baryonic matter
is a separate species coupled to it. Superfluid vacuum theory is not. Its
stated paradigm is a background quantum liquid of which ``elementary
particles'', in its own terms, are excitations --- one substance, as here.

What remains distinctive is narrower than earlier versions claimed. Superfluid
vacuum theory obtains a single substance by making geometry emergent from the
condensate, and this framework now takes the same position on what is
fundamental, so that is no longer a point of difference. Two elements remain.
The first is the route by which geometry is recovered: rather than deriving an
acoustic metric from the condensate and then seeking Einstein's equations, the
framework keeps Einstein's equation as the effective description and proposes a
refractive account of why it holds (Section~\ref{sec:refractive}), whose
decisive test is that the medium's response slows time and stretches space in
equal measure for every excitation. Whether that route is genuinely different
from the emergent programme's, or the same one approached from the other end,
must be settled. The second is the mechanism of the partition, the covariant
criterion of Section~\ref{sec:threshold}: the dimensionless quantity
$\Qq = \xi^{2} h^{\mu\nu} k_{\mu} k_{\nu}$ of~\eqref{eq:criterion}, with a
smooth weighting $f(\Qq)$ splitting the mode integral between $\Tmat$ and
$\Tphi$. The consequence developed in Section~\ref{sec:conservation} --- that
no discontinuous exchange term between the two is required, because both are
populations of one field --- follows from that construction. It removes an
obstruction to the conservation conditions; it does not by itself establish
them, which remains outstanding.

\subsection{The electron-scale coincidence}

The numerical agreement of Section~\ref{sec:threshold} has been approached from
the opposite direction. Working from a logotropic equation of state, Chavanis
\cite{chavanis2026} recalls an expression for the cosmological constant in terms
of the electron mass and the fundamental constants,
\begin{equation}
\Lambda = \frac{G^{2} m_{e}^{6}}{\alpha^{6} \hbar^{4}}
\approx 1.36 \times 10^{-52}\,\mathrm{m}^{-2},
\end{equation}
a relation of Eddington type. There the electron mass fixes $\Lambda$; here the
electron mass is the readout of $\xi(\phi_0)$. Both routes tie the electron
scale to a vacuum-scale quantity, from opposite ends.

Two cautions attach to this. The relation is \emph{recalled} rather than derived
in that work, so the primary source lies earlier in the logotropic literature.
And independent arrival at a coincidence is weak evidence that it is not
accidental; it is not this framework's discovery, and the open question of
Section~\ref{sec:sec7open}, item~(6), remains untouched by it.

\subsection{Known deficiencies relative to current practice}

Points where this document is behind the literature it should be engaging,
or exposed to measurements it has not yet addressed.

\begin{enumerate}[label=(\arabic*)]
\item \textbf{First-order dissipative hydrodynamics.} The constitutive form of
Section~2.3 is of Eckart--Landau type, which is known to be acausal and
generically unstable in relativistic settings \cite{hiscock1985}. Current
viscous cosmology uses causal second-order formulations of Israel--Stewart type
\cite{israel1979}. A viable version of this framework must do the same.
\item \textbf{Silence on vertical dynamics.} Section~6 states only a radial
relation. Milky Way kinematics constrain the two components separately, and
they do not want the same thing: the baryonic distribution supplies too little
gravity to account for the rotation curve but enough to account for the
vertical velocity dispersions near the Sun, so substantial enhancement is
required radially and essentially none vertically
\cite{lisanti2019, lisanti2023}. Superfluid dark matter fails this test because
its phonon-mediated force is approximately parallel to the baryonic
gravitational field and therefore enhances both components by the same factor
\cite{lisanti2023}. Cold dark matter passes because its vertical acceleration
is dominated by baryons, with the halo subdominant. The resulting criterion
applies to any model: the enhancement of vertical acceleration must be
suppressed relative to the radial enhancement. Whether this framework is
exposed depends on whether $v_{\phi,\mathrm{eff}}$ tracks the baryonic
acceleration field --- in which case it inherits the parallelism problem ---
or constitutes an independent source. Section~6 does not say which.
\item \textbf{The status of $c(\phi)$.} A variable effective propagation speed
is natural in the emergent-gravity family, where the metric is acoustic. It sits
awkwardly alongside a fundamental $\Gmn$. The framework must either justify
$c(\phi)$ as a refractive effect within fixed geometry, or acknowledge that
taking it as a genuine causal speed moves the proposal toward the emergent
family and incurs that family's obligations. The refractive reading is now the
framework's account of gravity (Section~\ref{sec:refractive}), which places it
with the emergent family on what is fundamental and incurs that family's chief
obligation: to derive the effective geometry rather than assume it.
\item \textbf{The vacuum is already measured at the electron scale.} In quantum
electrodynamics, vacuum polarization screens every charge out to the electron's
reduced Compton wavelength --- the same $386\,\mathrm{fm}$ as $\xi_{0}$ --- and
contributes measurably to the Lamb shift and to the electron's anomalous
magnetic moment, in agreement with theory to many significant figures. The
vacuum also behaves as a nonlinear optical medium. Light-by-light scattering,
forbidden in classical electrodynamics, has been observed in ultra-peripheral
heavy-ion collisions \cite{atlas2017}, and the strong linear polarization of
optical light from the neutron star RX~J1856.5$-$3754 is evidence for vacuum
birefringence in a strong magnetic field \cite{mignani2017}. The Casimir effect
is measured. If $\xi_{0}$ is a property of the Ocean, these are the Ocean's
responses at and near its healing length, and the framework must reproduce them
quantitatively. Until it does, the electron-scale coincidence of
Section~\ref{sec:threshold} is matched by an obligation of the same order.
\end{enumerate}

\subsection{The structural question}

If the vacuum is a medium possessing density, pressure and a rest frame, it is
reasonable to ask why it requires a background spacetime to occupy. The
emergent-gravity family answers that it does not, and that geometry is the
medium's own collective behaviour. Earlier versions of this framework posited a
medium and a geometry as distinct structures coupled through $\kappa(\phi)$.
This version answers the question in favour of the medium. There is no
background spacetime for the Ocean to occupy; the geometry of
Equation~\eqref{eq:field} is how the medium's state is experienced by
excitations of the medium, and $\kappa(\phi)$ expresses how strongly that state
responds to concentrated energy. The position is now stated. It has not yet
been derived, and deriving the effective geometry from the dynamics of the
medium is the task it creates (Section~\ref{sec:program}).

% =========================================================================
\section{Research Program and Testable Predictions}
\label{sec:program}

\begin{itemize}
\item Derive the field equations from a covariant action rather than introducing
stress terms phenomenologically.
\item Derive the effective equation of state $P(\phi)$ and determine whether a
stable oscillatory cosmological solution exists.
\item Solve the weak-field, stationary, rotating-galaxy limit and compare
predicted rotation curves with baryonic distributions.
\item Determine whether the same parameter set fits multiple galaxies without an
independently chosen halo profile.
\item Calculate the weak-field and post-Newtonian limits to verify recovery of
Solar-System observations.
\item Determine the propagation speed of scalar, gravitational, and
electromagnetic perturbations, and identify whether $c(\phi)$ is a true causal
speed or an effective refractive velocity.
\item Test cosmological expansion, structure growth, gravitational lensing, and
background-radiation constraints.
\item \textbf{Derive the gradient-stiffness coefficient $\Gg$}, and with it the
healing length $\xi(\phi)$ of~\eqref{eq:healing}, from the scalar Lagrangian.
\item \textbf{Confront the predicted drift in $\xi$} --- and hence in the
effective electron mass --- with quasar absorption spectra and Oklo constraints.
\item \textbf{Resolve or explain the hierarchy} between the mass gap $\Ogap$
required by galactic dynamics and the stiffness scale implied by
$\xi_{0} \approx 386\,\mathrm{fm}$. The candidate route of
Section~\ref{sec:sec7open}, item~(5), divides this into three tasks.
\begin{itemize}
\item \emph{Protection.} Reformulate the scalar sector with $\phi$ as the phase
of a complex field~\eqref{eq:complex}, re-express $P$, $\kappa$, $\xi$, $\eta$,
$\zeta$ and the quartic potential of Section~\ref{sec:defocusing} in terms of
the modulus or of $X$, and determine whether the shift symmetry survives the
matter coupling and the dissipative sector. If it does
not, compute the gap that results.
\item \emph{Size.} Determine what fixes the extent of a galactic solution,
given that the medium supplies no kiloparsec scale of its own: which features of
the full state of the disturbance set it --- energy, organised and random flow,
exchange with the surrounding medium --- and where their values originate.
\item \emph{Rotation curves without per-galaxy freedom.} Derive
$v_{\phi,\mathrm{eff}}(r)$ from the baryonic distribution alone, with no
per-galaxy freedom, and compare with the observed radial acceleration relation
\cite{mcgaugh2016, lelli2017}, including its universal acceleration scale
$g_{\dagger} \approx 1.2 \times 10^{-10}\,\mathrm{m\,s^{-2}}$, which the
framework must then account for, and extend the derivation to
pressure-supported galaxies, which follow the same relation \cite{lelli2017}.
This must be done jointly with the vertical-acceleration item below, since a contribution fixed by the baryons is
the kind most exposed to it.
\end{itemize}
\item \textbf{Determine the sign of $\lambda$} from the chosen $L(\phi, X)$ and
verify the defocusing condition of Section~\ref{sec:defocusing}. A framework
whose potential turns out to be focusing about the present vacuum has no
mechanism arresting concentration and is not viable as written. Map the states
in which stiffness is lost, determine what the medium does there, and confront
the result with domain-wall, microwave-background and relic-abundance bounds.
\item \textbf{Distinguish the galactic mechanism from its precedent.}
Determine whether the rotational support of Section~6, generated by $\Pimn$,
is physically distinct from the vortex formation obtained by Huang and
collaborators \cite{huang2013} from a nonlinear Klein--Gordon equation with
galaxies as external sources, or whether the two are the same mechanism
expressed in different formalisms.
\item \textbf{Establish the direction of the vacuum contribution.} Determine
whether the acceleration produced by $\Pimn$ is parallel to the baryonic
gravitational field, as a scalar-mediated MOND-like force is, or whether its
anisotropic shear components yield a contribution with an independent
orientation. This is the question on which the galactic sector turns: a
parallel contribution enhances radial and vertical accelerations by a common
factor and is excluded by local Milky Way data \cite{lisanti2019, lisanti2023},
whereas an independent, quasi-spherical contribution is not. Then compute the
predicted vertical acceleration explicitly and confront it, together with the
rotation curve of Section~6, with stellar kinematics.
\item \textbf{Reformulate the dissipative sector causally.} Replace the
first-order constitutive relation of Section~2.3 with a second-order
Israel--Stewart or BDNK form, and verify that the resulting system is causal and
stable in the weak-field limit.
\item \textbf{Settle the status of $c(\phi)$} as either a refractive effect
within fixed geometry or a genuine causal speed, and state the consequences for
the framework's relation to emergent-gravity formulations
(Section~\ref{sec:related}).
\item \textbf{Establish whether matter coupling constitutes a forcing term.}
The known finite-time blowup constructions for viscous media require an external
force injecting momentum; the unforced problem remains open. In this framework
the candidate forcing is the matter sector acting on the vacuum through
$\kappa(\phi)\Tmat$ in~\eqref{eq:field}. Determine whether that coupling can
drive the medium to finite-time concentration, or whether the healing-length
cutoff bounds it for any physically admissible matter distribution. This is the
sharp form of the question raised in Section~5 as to whether a contraction phase
terminates in a singularity or is arrested, and the answer turns on
$\xi(\phi)$ and the sign of $\lambda$ rather than on the viscosity
coefficients.
\item \textbf{Derive the viscosities from vortex dynamics.} Determine whether
$\eta$ and $\zeta$ follow from the creation, motion and reconnection of
quantized vortices, as effective dissipation does in laboratory superfluids,
removing two free functions from the theory.
\item \textbf{Simulate a galactic disturbance.} Once the equation is fixed,
solve the condensate wave equation (Gross--Pitaevskii or nonlinear
Klein--Gordon type) for a galaxy-scale disturbance, including shear, wakes and
vortex structure.
\item \textbf{Reproduce the measured vacuum.} Compute the Ocean's contribution
to vacuum polarization, and hence to the Lamb shift and the anomalous magnetic
moment, together with light-by-light scattering, vacuum birefringence and the
Casimir force, and compare with quantum electrodynamics and with measurement
(deficiency~(4) of Section~\ref{sec:related}).
\item \textbf{Size and spin of the localized excitation.} Compute the probe
response of the localized excitation and show it is pointlike to about
$10^{-18}\,\mathrm{m}$; determine how $\xi(\phi)$ behaves at high
concentration consistently with the collapse floor; and identify the structure
that supplies spin~$\tfrac{1}{2}$.
\item \textbf{Motion through the surroundings.} Determine the flow regimes of a
disturbance moving relative to the medium, including the superfluid critical
speed. Test for vacuum contributions offset relative to the direction of
motion; for residuals of the radial acceleration relation that track speed
through the environment, a property not among those tested in
\cite{lelli2017}; and against colliding clusters.
\item \textbf{Derive gravity from the medium.} Derive the effective geometry of
Equation~\eqref{eq:field} from the dynamics of the medium, and show that the
refractive account of Section~\ref{sec:refractive} meets its three decisive
requirements: every excitation responds in exactly the same proportion; time is
slowed and space stretched in equal measure, giving the observed deflection of
starlight; and gravitational waves travel at the speed of light. Then extend it
to perihelion advance, frame dragging and gravitational radiation, or identify
where it fails.
\item \textbf{Black holes.} Determine whether collapse terminates near the
healing length, whether the geometric and medium horizons coincide, and what
horizon-scale imaging and ringdown measurements constrain
(Section~\ref{sec:blackholes}).
\item \textbf{Hearing the medium.} If the gapless phonon of the candidate route
couples to matter, it implies a weak long-range force or an energy-loss channel.
Compare with torsion-balance and atom-interferometer bounds.
\end{itemize}

% =========================================================================
\section{Summary of the Revised Formalism}

The revised Ocean framework rests on a single premise: there is no empty space.
The Ocean is one continuous medium without edges or outside, and everything
in it, matter and light included, is a pattern of that medium. Gravity is
proposed to be the medium's response to concentrated energy. The mathematical
formulation keeps Einstein's equation as the effective description of that
response, with a scalar-field stress sector, a viscous constitutive sector, a
variable pressure contribution and a field-dependent effective coupling as the
medium's contributions to it.

The framework extends that idea to the matter sector itself. If the vacuum is a
medium, it has a characteristic length over which it can heal; excitations
shorter than that length are localized patterns, and excitations longer than it
are motions of the medium. The distinction between matter and vacuum then
becomes a statement about the medium's own excitation spectrum rather than an
imposed energy cut.

The central hypothesis is that phenomena conventionally divided into dark energy,
dark matter, and localized matter may have a common origin in different
dynamical regimes of one vacuum field. Establishing that claim requires deriving
the relevant limits and demonstrating quantitative agreement with observations.


% =========================================================================
\begin{thebibliography}{99}
\footnotesize

\bibitem{huang2013}
K.~Huang, C.~Xiong and X.~Zhao, \emph{Scalar-field theory of dark matter},
Int. J. Mod. Phys. A \textbf{29}, 1450074 (2014);
doi:10.1142/S0217751X14500742; arXiv:1304.1595.

\bibitem{berezhiani2015}
L.~Berezhiani and J.~Khoury, \emph{Theory of dark matter superfluidity},
Phys. Rev. D \textbf{92}, 103510 (2015); arXiv:1507.01019.

\bibitem{riess1998}
A.~G. Riess \emph{et al.}, \emph{Observational evidence from supernovae for an
accelerating universe and a cosmological constant}, Astron. J. \textbf{116},
1009 (1998); arXiv:astro-ph/9805201.

\bibitem{perlmutter1999}
S.~Perlmutter \emph{et al.}, \emph{Measurements of $\Omega$ and $\Lambda$ from
42 high-redshift supernovae}, Astrophys. J. \textbf{517}, 565 (1999);
arXiv:astro-ph/9812133.

\bibitem{desi2025}
DESI Collaboration, \emph{DESI DR2 results II: Measurements of baryon acoustic
oscillations and cosmological constraints}, arXiv:2503.14738 (2025).

\bibitem{steinhardt2002}
P.~J. Steinhardt and N.~Turok, \emph{A cyclic model of the universe}, Science
\textbf{296}, 1436 (2002); doi:10.1126/science.1070462; arXiv:hep-th/0111030.

\bibitem{planck2018inflation}
Planck Collaboration, \emph{Planck 2018 results. X. Constraints on inflation},
Astron. Astrophys. \textbf{641}, A10 (2020); doi:10.1051/0004-6361/201833887;
arXiv:1807.06211.

\bibitem{lelli2017}
F.~Lelli, S.~S. McGaugh, J.~M. Schombert and M.~S. Pawlowski, \emph{One law to
rule them all: The radial acceleration relation of galaxies}, Astrophys. J.
\textbf{836}, 152 (2017); doi:10.3847/1538-4357/836/2/152; arXiv:1610.08981.

\bibitem{mcgaugh2016}
S.~S. McGaugh, F.~Lelli and J.~M. Schombert, \emph{Radial acceleration relation
in rotationally supported galaxies}, Phys. Rev. Lett. \textbf{117}, 201101
(2016); arXiv:1609.05917.

\bibitem{lisanti2019}
M.~Lisanti, M.~Moschella, N.~J. Outmezguine and O.~Slone, \emph{Testing dark
matter and modifications to gravity using local Milky Way observables},
Phys. Rev. D \textbf{100}, 083009 (2019); arXiv:1812.08169.

\bibitem{lisanti2023}
M.~Lisanti, M.~Moschella, N.~J. Outmezguine and O.~Slone, \emph{A preference for
cold dark matter over superfluid dark matter in local Milky Way data},
arXiv:1911.12365v2 (2023).

\bibitem{steinhauer2016}
J.~Steinhauer, \emph{Observation of quantum Hawking radiation and its
entanglement in an analogue black hole}, Nature Phys. \textbf{12}, 959 (2016);
arXiv:1510.00621.

\bibitem{hamilton2008}
A.~J.~S. Hamilton and J.~P. Lisle, \emph{The river model of black holes},
Am. J. Phys. \textbf{76}, 519 (2008); doi:10.1119/1.2830526; arXiv:gr-qc/0411060.

\bibitem{torres2017}
T.~Torres, S.~Patrick, A.~Coutant, M.~Richartz, E.~W. Tedford and
S.~Weinfurtner, \emph{Rotational superradiant scattering in a vortex flow},
Nature Phys. \textbf{13}, 833 (2017); doi:10.1038/nphys4151; arXiv:1612.06180.

\bibitem{volovik2003}
G.~E. Volovik, \emph{The Universe in a Helium Droplet}, International Series of
Monographs on Physics \textbf{117}, Clarendon Press / Oxford University Press
(2003).

\bibitem{zloshchastiev2020}
K.~G. Zloshchastiev, \emph{An alternative to dark matter and dark energy:
Scale-dependent gravity in superfluid vacuum theory}, Universe \textbf{6}, 180
(2020); doi:10.3390/universe6100180; arXiv:2011.12565.

\bibitem{dou2011}
X.~Dou and X.-H. Meng, \emph{Bulk viscous cosmology: unified dark matter},
Advances in Astronomy \textbf{2011}, 829340 (2011); arXiv:1012.3045.

\bibitem{chavanis2026}
P.-H. Chavanis, \emph{Polytropes, logotropes, the universal value of the surface
density of dark matter halos, and the value of the cosmological constant},
arXiv:2603.21302.

\bibitem{hiscock1985}
W.~A. Hiscock and L.~Lindblom, \emph{Generic instabilities in first-order
dissipative relativistic fluid theories}, Phys. Rev. D \textbf{31}, 725 (1985).

\bibitem{israel1979}
W.~Israel and J.~M. Stewart, \emph{Transient relativistic thermodynamics and
kinetic theory}, Annals of Physics \textbf{118}, 341 (1979).

\bibitem{atlas2017}
ATLAS Collaboration, \emph{Evidence for light-by-light scattering in heavy-ion
collisions with the ATLAS detector at the LHC}, Nature Phys. \textbf{13}, 852
(2017); doi:10.1038/nphys4208; arXiv:1702.01625.

\bibitem{mignani2017}
R.~P. Mignani, V.~Testa, D.~Gonz\'alez Caniulef, R.~Taverna, R.~Turolla,
S.~Zane and K.~Wu, \emph{Evidence for vacuum birefringence from the first
optical-polarimetry measurement of the isolated neutron star
RX~J1856.5$-$3754}, Mon. Not. R. Astron. Soc. \textbf{465}, 492 (2017);
arXiv:1610.08323.

\end{thebibliography}

\vfill
\noindent\rule{\textwidth}{0.4pt}

\noindent
\footnotesize
\textbf{Reference basis.} Revised from an earlier formalism supplied by the
author. That document defines the Ocean metric, the
vacuum viscosity tensor, the scalar pressure term, the effective coupling
$\kappa(\phi)$, the VSL interpretation, and the proposed $0.511\,\mathrm{MeV}$
matter threshold. The matter-threshold section of that document is superseded
by Section~\ref{sec:threshold} below.

\end{document}
"""


def write_tex(outdir: Path) -> Path:
    """Emit the LaTeX source file and return its path."""
    outdir.mkdir(parents=True, exist_ok=True)
    tex_path = outdir / f"{DOCNAME}.tex"
    tex_path.write_text(PREAMBLE.lstrip() + BODY, encoding="utf-8")
    return tex_path


def compile_pdf(tex_path: Path, passes: int = 2) -> Path:
    """Run pdflatex in the source directory. Two passes resolve \\ref cross-links."""
    if shutil.which("pdflatex") is None:
        raise RuntimeError("pdflatex not found on PATH")

    workdir = tex_path.parent
    for i in range(passes):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             tex_path.name],
            cwd=workdir, capture_output=True, text=True,
        )
        if result.returncode != 0:
            tail = "\n".join(result.stdout.splitlines()[-40:])
            raise RuntimeError(f"pdflatex failed on pass {i + 1}:\n{tail}")

    pdf_path = tex_path.with_suffix(".pdf")
    if not pdf_path.exists():
        raise RuntimeError("pdflatex reported success but produced no PDF")
    return pdf_path


def clean_aux(outdir: Path) -> None:
    for ext in (".aux", ".log", ".out", ".toc"):
        for f in outdir.glob(f"*{ext}"):
            f.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", default=".", help="output directory")
    parser.add_argument("--no-pdf", action="store_true",
                        help="emit .tex only, skip compilation")
    parser.add_argument("--keep-aux", action="store_true",
                        help="retain .aux/.log files")
    args = parser.parse_args()

    outdir = Path(args.outdir).resolve()
    tex_path = write_tex(outdir)
    print(f"wrote {tex_path}")

    if args.no_pdf:
        return 0

    pdf_path = compile_pdf(tex_path)
    if not args.keep_aux:
        clean_aux(outdir)
    print(f"wrote {pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
