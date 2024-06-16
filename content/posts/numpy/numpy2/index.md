---
title: "18 years in the Making: NumPy 2.0 Released"
date: 2024-06-16
draft: false
description: "
18 years in the Making: NumPy 2.0 Released
"
tags: ["News", "numpy"]
displayInList: true
author: ["NumPy Developers"]
---

After 18 years since the release of NumPy 1.0, the NumPy community is thrilled
to announce the launch of NumPy 2.0! This major release marks a significant
milestone in the evolution of the popular scientific computing library,
bringing a wealth of enhancements and improvements to users and unlocks future
developments.

NumPy has improved and evolved over the past 18 years and many old releases had
significant performance, understandability, and consistency improvements.
The journey to an actual 2.0 release has been long and it was difficult to
build the necessary momentum. In part this may be because for a time the idea
of a NumPy 2 among the NumPy developers required a revolutionary change with a
large code rewrite. Many of these rewrites and changes happened over the years,
but because of backward compatibility concerns they remained largely invisible
to the users and NumPy 2 is in part, just the culmination of these
improvements, allowing us to discard some of the legacy behaviors or details of
the ABI that prevent future improvements.

We started concrete plans for the 2.0 release more than a year ago at a
[public planning meeting](https://github.com/numpy/archive/tree/main/2.0_developer_meeting)
in April 2023 where many of the below changes were proposed and discussed.
After the meeting and over the course of the last year, NumPy enhancement
proposals ([NEPs](https://numpy.org/neps/)) written, reviewed, and implemented.

Some of the key highlights and major changes are:

- Cleaned-up and Streamlined API ([NEP 52](https://numpy.org/neps/nep-0052-python-api-cleanup.html)):
  The Python API has undergone a thorough cleanup, making it easier to learn
  and use NumPy. The main namespace has been reduced by approximately 10%, and
  the more niche `numpy.lib` namespace has been reduced by about 80%, providing
  a clearer distinction between public and private API elements.

- Improved Scalar Promotion Rules: The scalar promotion rules have been
  updated, as proposed in [NEP 50](https://numpy.org/neps/nep-0050-scalar-promotion.html)
  addressing surprising behaviors in type promotion e.g. with zero dimensional arrays.

- Powerful new DType API and a new string dtype: NumPy 2.0 introduces a new API
  for implementing user-defined custom data types as proposed by
  [NEP 41](https://numpy.org/neps/nep-0041-improved-dtype-support.html). We used
  this new API to implement `StringDType` offering efficient and painless
  support for variable length strings which was proposed in
  [NEP 55](https://numpy.org/neps/nep-0055-string_dtype.html). And it is our hope
  that enable future DTypes in PyData ecosystem and NumPy itself.

- Windows Compatibility Enhancements: The default 32-bit integer representation
  on Windows has been updated to 64-bit on 64 bit architectures, addressing one
  of the most common issues a developer runs into trying to get NumPy code to
  work portably on Windows and Unix-like operating systems.

These are just some of the more impactful changes and does not include
significant performance improvements. For a more extensive list of changes, see
also the [NumPy 2 release notes](https://numpy.org/devdocs/release/2.0.0-notes.html).

A major release comes with changes that users may have to adapt to, but we
worked hard to strike a balance between improvements and ensuring that the
transition to NumPy 2 is as seamless as possible. We wrote a comprehensive
[migration guide](https://numpy.org/devdocs/numpy_2_0_migration_guide.html),
and a [ruff plugin](https://numpy.org/devdocs/numpy_2_0_migration_guide.html#ruff-plugin)
helps to automatically update Python code so it will work with both NumPy 1 and
NumPy 2.

While we do require C API users to recompile their projects to support running
with NumPy 2, we prepared for this already in NumPy 1.25. The build process was
simplified so that you can now always compile with the latest NumPy version.
This means that projects build with NumPy 2 are "magically" compatible with
1.x. It also means that projects no longer need to build their binaries using
the oldest supported NumPy.

The release of NumPy 2.0 is the result of a collaborative and largely volunteer
effort spanning many years and involving contributions from a diverse community
of developers. Many of the changes above would not have been possible without
grants and institutional sponsors enabling many of us to work on NumPy. These
are the Gordon and Betty Moore Foundation, the Alfred P. Sloan Foundation,
NASA, NVIDIA, Quansight Labs, and the Chan Zuckerberg Initiative.

We are excited about future improvements to NumPy some of which will be
possible due to changes in NumPy 2. Let's continue to work together to improve
NumPy and our ecosystem.
