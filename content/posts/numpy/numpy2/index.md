---
title: "18 years in the Making: NumPy 2.0 Released"
date: 2024-06-16
draft: false
description: "
We announce the release of NumPy 2.0, which brings major improvements in
functionality and usability. Improvements to NumPy internals set the stage
for future development. We discuss the motivation behind breaking changes
and how those impact users, as well as some of the history of the 2.0
development process.
"
tags: ["News", "numpy"]
displayInList: true
author: ["NumPy Developers"]
---

Eighteen years since the release of NumPy 1.0, we are thrilled to announce the
launch of NumPy 2.0! This major release marks a significant milestone in the
evolution of NumPy, bringing a wealth of enhancements and improvements to users,
and setting the stage for future feature development.

NumPy has improved and evolved over the past 18 years, with many old releases bringing
significant performance, usability, and consistency improvements.
That said, our approach for a long time has been to make only incremental changes while
carefully managing backward compatibility. This approach minimizes user breakage,
but also limits the scope of improvements that can be made, both to the API and its underlying implementation.
Therefore, for this one-off major release, we are breaking backward compatibility to implement significant improvements in NumPy's type system. The type system is fundamental to NumPy, and major
behavioral changes could not be made incrementally without mixing two different
type systems, which would be a recipe for disaster.

The journey to an actual 2.0 release has been long, and it was difficult to
build the necessary momentum. In part, this may be because, for a time, the NumPy developers associated a NumPy 2.0 release with nothing less than a revolutionary 
rewrite of significant key pieces in the code base. Many of these rewrites and
changes happened over the years, but because of backward compatibility concerns
they remained largely invisible to the users. NumPy 2.0 is the
culmination of these improvements, allowing us to discard some legacy
ABI (Application Binary Interface) that prevented future improvements.

Some major changes to NumPy internals that were required for key features in
2.0 have been in the works since 2019 at least.
We started concrete plans for the 2.0 release itself more than a year ago, at a four hour
long [public planning meeting](https://github.com/numpy/archive/tree/main/2.0_developer_meeting)
in April 2023. Many of the key changes were proposed and discussed. The key goals
we decided on there were perhaps even larger and more ambitious in scope than
some of us expected. This also unlocked some extra energy - which has been great to see.
After the meeting and over the course of the last year, NumPy enhancement
proposals ([NEPs](https://numpy.org/neps/)) were written,
reviewed, and implemented for each major change.

Some key highlights are:

- Cleaned-up and streamlined Python API ([NEP 52](https://numpy.org/neps/nep-0052-python-api-cleanup.html)):
  The Python API has undergone a thorough cleanup, making it easier to learn
  and use NumPy. The main namespace has been reduced by approximately 10%, and
  the more niche `numpy.lib` namespace has been reduced by about 80%, providing
  a clearer distinction between public and private API elements.

- Improved scalar promotion rules: The scalar promotion rules have been
  updated, as proposed in [NEP 50](https://numpy.org/neps/nep-0050-scalar-promotion.html)
  addressing surprising behaviors in type promotion, e.g. with zero dimensional arrays.

- Powerful new DType API and a new string dtype: NumPy 2.0 introduces a new API
  for implementing user-defined custom data types as proposed by
  [NEP 41](https://numpy.org/neps/nep-0041-improved-dtype-support.html). We used
  this new API to implement `StringDType`, offering efficient and painless
  support for variable length strings which was proposed in
  [NEP 55](https://numpy.org/neps/nep-0055-string_dtype.html). And it is our hope
  that enable future new data types with interesting new capabilities in the
  PyData ecosystem and in NumPy itself.

- Windows compatibility enhancements: The default 32-bit integer representation
  on Windows has been updated to 64-bit on 64-bit architectures, addressing one
  of the most common problems with having NumPy work portably across operating
  systems.

- Support for the Python array API standard: This is the first release to
  include full support for the array API standard (v2022.12), made possible
  by the new promotion rules, APIs, and API cleanup mentioned above.
  We also aligned existing APIs and behavior with the standard,
  as proposed in [NEP 56](https://numpy.org/neps/nep-0056-array-api-main-namespace.html).

These are just some of the more impactful changes in behavior and usability. In addition,
NumPy 2.0 contains significant performance and documentation improvements,
and more much - for an extensive list of changes, see
the [NumPy 2 release notes](https://numpy.org/devdocs/release/2.0.0-notes.html).

To adopt this major release, users will likely need to adjust existing code, but we
worked hard to strike a balance between improvements and ensuring that the
transition to NumPy 2.0 is as seamless as possible. We wrote a comprehensive
[migration guide](https://numpy.org/devdocs/numpy_2_0_migration_guide.html),
and a [ruff plugin](https://numpy.org/devdocs/numpy_2_0_migration_guide.html#ruff-plugin)
that helps to update Python code so it will work with both NumPy 1.x and
NumPy 2.x.

While we do require C API users to recompile their projects to support
NumPy 2.0, we prepared for this in NumPy 1.25 already. The build process was
simplified so that you can now compile with the latest NumPy version,
and remain backward compatible.
This means that projects build with NumPy 2.x are "magically" compatible with
1.x. It also means that projects no longer need to build their binaries using
the oldest supported version of NumPy.

We knew throughout development that rolling out NumPy 2.0
would be (temporarily) disruptive, because of the backwards-incompatible API and
ABI changes. We spent an extraordinary amount of effort communicating these
changes, helping downstream projects adapt, tracking compatibility of popular
open source projects (see, e.g.,
[numpy#26191](https://github.com/numpy/numpy/issues/26191), and completing the
release process at limited pace to provide time for adoption. No
doubt, the next few weeks will bring to light some new challenges, however we fully expect these
to be manageable and well worth it in the long run.

The NumPy 2.0 release is the result of a collaborative, largely volunteer,
effort spanning many years and involving contributions from a diverse community
of developers. In addition, many of the changes above would not have been
possible without funders and institutional sponsors allowing several team members
to work on NumPy as part of their day jobs. We'd like to acknowledge in particular:
the Gordon and Betty Moore Foundation, the Alfred P. Sloan Foundation,
NASA, NVIDIA, Quansight Labs, the Chan Zuckerberg Initiative, and Tidelift.

We are excited about future improvements to NumPy, many of which will be
possible due to changes in NumPy 2.0. See [the NumPy roadmap](https://numpy.org/neps/roadmap.html)
for some features in the pipeline or on the wishlist. Let's
continue working together to improve NumPy and the scientific Python and PyData
ecosystem!
