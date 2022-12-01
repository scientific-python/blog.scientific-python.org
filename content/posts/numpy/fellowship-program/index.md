---
title: "NumPy's first Developer in Residence: Sayed Adel"
date: 2022-12-01
draft: false
description: |
  Introducing the NumPy Fellowship Program and our first
  Developer in Residence, Sayed Adel, who will be working on performance
  optimization.
tags: ["numpy", "developer-in-residence"]
displayInList: true
author: ["Ralf Gommers", "Inessa Pawson", "Stéfan van der Walt"]
---

The NumPy team is excited to announce the launch of the NumPy Fellowship
Program and the appointment of Sayed Adel
([@seiko2plus](https://github.com/seiko2plus)) as the first NumPy
Developer in Residence. This is a significant milestone in the history
of the project: for the first time, NumPy is in a position to use its
project funds to pay for a full year of maintainer time. We believe that
this will be an impactful program that will contribute to NumPy's
long-term sustainability as a community-driven open source project.

Sayed has been making major contributions to NumPy
since the start of 2020, in particular around computational performance.
He is the main author of the NumPy SIMD architecture ([_NEP
38_](https://numpy.org/neps/nep-0038-SIMD-optimizations.html),
[_docs_](https://numpy.org/devdocs/reference/simd/index.html)),
generously shared his knowledge of SIMD instructions with the core
developer team, and helped integrate the work of various volunteer and
industry contributors in this area. As a result, we've been able to
expand support to multiple CPU architectures, integrating contributions
from IBM, Intel, Apple, and others, none of which would have been
possible without Sayed. Furthermore, when NumPy tentatively started
using C++ in 2021, Sayed was one of the proponents of the move and
helped with its implementation.

The NumPy Steering Council sees Sayed's appointment to this role as both
recognition of his past outstanding contributions as well as an
opportunity to continue improving NumPy's computational performance. In
the next 12 months, we'd like to see Sayed focus on the following:

- SIMD code maintenance,
- code review of SIMD contributions from others,
- performance-related features,
- sharing SIMD and C++ expertise with the team and growing a NumPy
  sub-team around it,
- SIMD build system migration to Meson,
- and wherever else Sayed's interests take him.

> _"I'm both happy and nervous: this is a great opportunity, but also a
> great responsibility," said Sayed in response to his appointment._

The funds for the NumPy Fellowship Program come from a partnership with
Tidelift and from individual donations. We sincerely thank both
Tidelift and everyone who donated to the project---without you, this
program would not be possible! We also acknowledge the CPython
Developer-in-Residence and the Django Fellowship programs, which
served as inspiration for this program.

Sayed officially starts as the NumPy Developer in Residence today, 1
December 2022. Already, we are thinking about opportunities beyond
this first year: we imagine "in residence" roles that focus on
developing, improving, and maintaining other parts of the NumPy
project (e.g., documentation, website, translations, contributor
experience, etc.). We look forward to this exciting new chapter of the
NumPy contributor community and will keep you posted on our progress.
