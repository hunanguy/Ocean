#!/usr/bin/env python3
"""
build_ocean_formalism.py
------------------------
Generates the LaTeX source for "Scalar-Tensor Hydrodynamics: A Modified Gravity
Framework for Vacuum Viscosity and Cyclic Cosmology" and compiles it to
PDF with pdflatex.

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

DOCNAME = "Ocean_Scalar_Tensor_Hydrodynamics_v3_3"

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
  pdftitle={Scalar-Tensor Hydrodynamics: A Modified Gravity Framework for Vacuum Viscosity and Cyclic Cosmology},
  pdfauthor={Keith Hays},
  pdfsubject={Theoretical proposal, revised formalism},
  pdfkeywords={scalar-tensor, vacuum viscosity, modified gravity, superfluid vacuum, cyclic cosmology}
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
\normalsize A Modified Gravity Framework for Vacuum Viscosity\\
and Cyclic Vacuum Cosmology}
\date{Revised Formalism --- Version 3.3}
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
the transition between particulate matter and vacuum-field excitations can arise
from one underlying medium.

\medskip
\noindent
This document is a theoretical proposal, not an established physical theory. The
equations below define a research program whose consistency, stability,
conservation laws, and observational predictions must be demonstrated.
\end{abstract}

% =========================================================================
\section*{Preface: What This Paper Is For}
\addcontentsline{toc}{section}{Preface}

\subsection*{The problem}

Two of the largest numbers in cosmology are placeholders. Roughly a quarter of
the universe's contents is labelled \emph{dark matter}: a substance inferred
entirely from its gravitational pull on things we can see, and never once
detected directly. Most of the remainder is labelled \emph{dark energy}, which
is less a substance than a name for an observation --- that cosmic expansion is
speeding up when everything we understand says it should be slowing down.
Together these two labels cover something like ninety-five per cent of what the
universe is made of. Neither has an agreed physical identity.

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
for no reason beyond his conviction that the universe ought to be static, and
the inconvenient fact that his equations refused to make it so. No observation
supported the term. It was a number chosen to produce an anticipated result.
When Hubble demonstrated a little over a decade later that the universe is
expanding after all, Einstein abandoned it.

It is worth being precise about what happened next, because the common retelling
is wrong in a way that matters. $\Lambda$ returned in 1998, but not as Einstein's
unmeasured assumption quietly surviving. It returned because observations of
distant supernovae showed cosmic expansion to be accelerating, and $\Lambda$ was
the simplest term capable of describing that. The acceleration is real and
measured. What $\Lambda$ does not do is explain it: no theory predicts the
constant's value, and the various attempts to calculate it from first principles
fail by a margin discussed below. The term records what the universe does and is
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
them: they stop being two unknown constituents of the universe and become two
behaviours of one medium. The measurements survive intact. Only their cause is
reassigned.

\subsection*{Where our two best theories disagree}

General Relativity and quantum field theory are the most thoroughly confirmed
descriptions of nature ever constructed, and they are known to be mutually
incompatible. In ordinary practice this causes little trouble, because the two
rarely describe the same situation: one governs the very large, the other the
very small, and the regimes where both matter at once --- the first instants of
the universe, the interior of a black hole --- are exactly the regimes we cannot
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

\subsection*{The idea}

General Relativity treats spacetime as a stage. It can be curved and stretched
by what sits on it, but it has no substance of its own: no density, no pressure,
no internal motion. The vacuum, in that picture, is the absence of things.

This framework treats the vacuum as a \emph{medium} instead. Not empty, but
full: a continuous field, here called the Ocean, with its own energy, its own
pressure, its own internal flow, and its own resistance to being stirred. Matter
and light are not objects placed in a void; they are disturbances in something
that was already there.

The appeal of this move is that media do things stages cannot. They flow. They
drag. They carry waves. They can be stirred, and they push back when you stir
them. Each of those behaviours is a candidate for a phenomenon currently
attributed to something unknown:

\begin{itemize}
\item A galaxy rotating inside a medium that swirls along with it experiences
stress from that swirl. Stress gravitates. The extra pull currently assigned to
a halo of undetected particles might instead be the vacuum's own response to
being rotated.
\item A medium with internal pressure that can change character over time can
drive expansion without a constant pasted into the equations by hand. What is
now called dark energy would be the Ocean in a particular state rather than a
number in a table.
\item And --- this is the part developed furthest here --- a medium has a
smallest meaningful size. Below some scale, it cannot be disturbed in a
localized way at all. That gives a principled distinction between what counts as
a particle and what counts as a ripple.
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

Three revisions have followed, and they share a shape.

\textbf{The first} corrected a structural error. In the original formulation the
vacuum's viscous response \emph{replaced} the Einstein tensor --- the geometric
heart of General Relativity. This cannot work: a mathematical identity
guarantees that the Einstein tensor is conserved, and substituting something
else for it breaks the conservation of energy and momentum. The fix was to keep
the geometry intact and add the vacuum's stress alongside it rather than in its
place.

\textbf{The second} removed a number. The original drew the line between matter
and vacuum at $0.511\,\mathrm{MeV}$ --- the rest energy of the electron. Above
the line, particles; below it, vacuum. This was an acknowledged placeholder, and
it had three problems: the value was imported rather than derived, it was
observer-dependent (two observers moving relative to one another would disagree
about which side of the line a given thing fell), and it was an abrupt cutoff
where physics prefers continuity.

The replacement drops the number entirely and asks instead how small a
disturbance the medium can hold. Every medium has such a scale --- in a
laboratory superfluid it is called the healing length, the shortest distance
over which the medium can bend without tearing. Disturbances larger than it
spread out and remain part of the medium. Disturbances smaller than it stay put,
as lumps. The matter/vacuum distinction becomes a property of the Ocean rather
than a line drawn across it.

The result worth noting is what happened next. Calibrating that scale to present
conditions puts it at roughly $386\,\mathrm{fm}$, which is exactly the size an
electron occupies by the relevant measure. The electron, on this account, is
simply the lightest thing small enough to be a lump in the Ocean --- and
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

\medskip
\noindent
Each revision has the same form: something chosen by hand is removed, and
something forced by the structure takes its place. A substituted tensor, then an
imported number, then an unexamined assumption. That a framework can absorb that
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
another, and is still waiting on human confirmation.

\subsection*{What would kill it}

Three things, named here so that a reader does not have to hunt for them.

\textbf{The scale gap.} For the Ocean to explain galactic rotation it must be
able to act across thousands of light years. For it to place the matter boundary
at the electron it must have structure at the scale of a hundredth of an atom.
These two requirements differ by about thirty-two orders of magnitude. They are
set by different parts of the mathematics, so this is not an outright
contradiction --- but a framework that merely tolerates such a gap has not
explained anything, and this is the most serious unresolved problem in the
document.

\textbf{The sign.} As above: if the Ocean's self-interaction has the wrong sign,
nothing arrests collapse and the framework is not viable in its present form.
This is a single calculation away from being settled either way.

\textbf{The preferred frame.} Describing the vacuum as a medium gives it a state
of rest, and a state of rest is something Einstein spent a career removing from
physics. Real superfluids do exactly this, so it is not absurd --- but the
experimental limits on any such effect are extraordinarily tight, and the
framework must show it stays inside them.

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
assumed to behave as additional particulate mass.

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
speed, and possible cyclic behavior.

% =========================================================================
\section{The Ocean Interpretation}

The framework interprets the observable universe as a dynamical region of a
deeper vacuum medium. The Ocean is not required to begin at the Big Bang.
Instead, the Big Bang can be interpreted as a state transition, a phase
transition, or a rapidly expanding solution of the underlying field equations.

The observable universe is therefore not treated as the ontological boundary of
reality. It is the portion of the deeper continuous vacuum field accessible to
observation. This distinction is a conceptual premise of the framework and must
ultimately be connected to a mathematically well-defined global solution.

% =========================================================================
\section{Cosmological Heartbeat}

The proposed \emph{Heartbeat} cosmology associates
cosmic expansion and contraction with the evolution of $\phi$. A schematic cycle
is
\[
\phi\text{-state transition} \;\rightarrow\; \text{pressure reversal} \;\rightarrow\;
\text{expansion} \;\rightarrow\; \text{field evolution} \;\rightarrow\;
\text{contraction} \;\rightarrow\; \text{new phase}.
\]
The model does not require that each cycle create the underlying vacuum field.
Instead, each cosmological epoch may be a dynamical state of the same deeper
medium. Whether such a cycle can avoid singularities, entropy accumulation, and
instabilities is an open mathematical question.

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

% =========================================================================
\section{The Localization Threshold}
\label{sec:threshold}

\subsection{Why a fixed threshold fails}

The earlier formulation partitioned energy between sectors by a declared
inequality:
\[
E > 0.511\,\mathrm{MeV} \;\Rightarrow\; \text{particulate matter sector},
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
gradient term dominating. It is the Ocean's grain size.

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
&&\text{particle branch; localized; contributes to } \Tmat .
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
consequence rather than a coincidence. A particle of mass $m$ has Compton
wavelength $\bar{\lambda}_{C} = \hbar / mc$; it can localize within the medium
only if $\bar{\lambda}_{C} \lesssim \xi_{0}$, which requires
\begin{equation}
m \;\gtrsim\; \frac{\hbar}{c\, \xi_{0}} \;=\; m_{e} .
\end{equation}

The electron is therefore the lightest excitation the present vacuum can hold as
a localized object. Anything lighter has a Compton wavelength longer than the
Ocean's grain and cannot be a lump in it --- it is necessarily a coherent field
excitation. This is offered as the framework's explanation for why photons and
neutrinos behave as field phenomena while the electron is the floor of the
particulate sector. The value $0.511\,\mathrm{MeV}$ is demoted from axiom to
measurement: it is the readout of $\xi(\phi_{0})$, not an input.

\subsection{Consequences}

\textbf{The threshold is local and dynamical.} $E_{c} = E_{c}(\phi(x))$, so
regions in different vacuum states have different matter thresholds. This
connects the present section to the Heartbeat cosmology: a phase transition of
$\phi$ is also a transition in what the vacuum is \emph{able to hold} as matter.
Where $\xi$ grows, the localization floor rises and previously particulate
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
energies.
\item \textbf{Varying-$m_{e}$ bounds.} Quasar absorption spectra constrain drift
in $m_{p}/m_{e}$ at roughly the $10^{-5}$--$10^{-6}$ level over cosmological
time; the Oklo natural reactor constrains it locally. Any Heartbeat evolution of
$\xi$ must be negligibly slow in the present epoch and confined to transition
epochs.
\item \textbf{The scale hierarchy.} Galactic-scale effects require the scalar's
Compton range to be of order a kiloparsec, implying
$\Ogap \sim 10^{-26}\,\mathrm{eV}$. But $\xi_{0} \approx 386\,\mathrm{fm}$
implies a stiffness scale near $0.5\,\mathrm{MeV}$. These differ by roughly
thirty-two orders of magnitude. They are set by different operators ---
$\Veff''$ versus $\Gg$ --- so this is not immediately inconsistent, but a
credible model must \emph{explain} the separation rather than merely tolerate
it. This is the most serious open problem in the revised section.
\item \textbf{Relation to the Standard Model.} The Higgs mechanism already
accounts for $m_{e}$ via a Yukawa coupling. The framework must state whether
$\xi_{0}$ and the electron Yukawa are independent quantities that happen to
agree, or whether one is meant to determine the other.
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
Explain rotation curves without particulate dark matter \\
Cosmological &
$P(\phi)$ and $\Tphi$ contribute on large scales &
Generate expansion history and effective dark-energy behavior \\
Transition / Heartbeat &
$\phi$ evolves between dynamically distinct states; $\xi(\phi)$ shifts &
Provide a mechanism for expansion/contraction cycles and for changes in the
localization floor \\
High-energy &
Mode occupation crosses $\Qq \sim 1$ &
Test the derived localization threshold of
Section~\ref{sec:threshold} \\
\bottomrule
\end{tabularx}
\end{center}

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

A separate requirement, implicit in the previous version and made explicit here,
is that the medium remain smooth for all time. The framework cannot appeal to
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
standing as $L_{,X} > 0$ and $\Kk > 0$, not a modelling preference.

A successful formulation should explicitly establish:
\begin{enumerate}[label=(\arabic*)]
\item covariance;
\item total energy-momentum conservation;
\item a well-posed scalar-field equation;
\item absence of pathological ghosts or gradient instabilities;
\item a stable low-density / weak-field limit;
\item compatibility with precision tests of gravity and light propagation;
\item a defocusing self-interaction, $\lambda > 0$, so that the healing-length
cutoff of Section~\ref{sec:threshold} arrests rather than accelerates
concentration.
\end{enumerate}

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
$\xi_{0} \approx 386\,\mathrm{fm}$.
\item \textbf{Determine the sign of $\lambda$} from the chosen $L(\phi, X)$ and
verify the defocusing condition of Section~\ref{sec:defocusing}. A framework
whose potential turns out to be focusing has no mechanism arresting
concentration and is not viable as written.
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
\end{itemize}

% =========================================================================
\section{Summary of the Revised Formalism}

The revised Ocean framework is centered on a single idea: the vacuum is a
physical, dynamical medium whose state can influence geometry, pressure,
gravitational coupling, and hydrodynamic stress. The mathematical formulation
keeps the Einstein tensor as the geometric backbone while adding a scalar-field
stress sector, a viscous constitutive sector, a variable pressure contribution,
and a field-dependent effective coupling.

The framework extends that idea to the matter sector itself. If the vacuum is a
medium, it has a characteristic length over which it can heal; excitations
shorter than that length are localized objects, and excitations longer than it
are motions of the medium. The distinction between matter and vacuum then
becomes a statement about the medium's own excitation spectrum rather than an
imposed energy cut.

The central hypothesis is that phenomena conventionally divided into dark energy,
dark matter, and particulate matter may have a common origin in different
dynamical regimes of one vacuum field. Establishing that claim requires deriving
the relevant limits and demonstrating quantitative agreement with observations.

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
