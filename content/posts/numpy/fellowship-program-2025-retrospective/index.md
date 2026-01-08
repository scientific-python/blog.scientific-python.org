---
title: "A Year of Typing: My NumPy Fellowship Retrospective"
date: 2026-01-08
draft: false
description: |
  A Year of Typing: My NumPy Fellowship Retrospective
tags: ["numpy", "developer-in-residence"]
displayInList: true
author: ["Joren Hammudoglu"]
---

It’s been exactly one year since I started my journey as a NumPy Fellow, and looking back, it has honestly been the best job I've ever had. My main goal for 2025 was to push the boundaries of static typing within the Scientific Python ecosystem. I'm happy to report that we didn't just push the boundaries; we reshaped them.

Here is a high-level look at what we achieved, from making `numpy` fully type-checked to bridging the gap between scientific computing and the wider Python typing community.

## NumPy is Now Fully Type-Checked

One of the biggest wins this year is that NumPy is now fully type-checked. When I started, there were significant gaps between the runtime behavior and the typing stubs.

For example, I spent a lot of time integrating `stubtest` — a [mypy](https://github.com/python/mypy) tool that checks if stubs match the runtime — into the CI pipeline. For this I had to fix thousands (yes, thousands) of errors in the stubs. Now typing correctness is enforced by running `stubtest` and `mypy` on the stubs in CI, ensuring that technical debt doesn't creep back in.

Crucially, NumPy is now largely compatible with the official [Python typing specification](https://typing.python.org/en/latest/). I helped drop support for Python 3.11 to update our stubs to use the modern PEP 695 syntax, making the codebase cleaner and more future-proof.

Besides static typing, since NumPy 2.4.0, all function- and class-signatures can now also be inspected at runtime using `inspect.signature`. This is a game-changer for runtime type-checkers like [beartype](https://github.com/beartype/beartype) and [typeguard](https://github.com/agronholm/typeguard).

Over the past year I've made [hundreds of contributions](https://github.com/numpy/numpy/pulls?q=is%3Apr+author%3Ajorenham+created%3A2025-01-01..2025-12-31+is%3Amerged) to NumPy, so there's a good chance I'm forgetting some important achievements.

## The Shape-Typing Frontier: NumType

A massive part of my fellowship was dedicated to the "holy grail" of array typing: shape-typing. For this I had to rely on type-checker behavior that isn't well-specified, and therefore subject to change. Using these typing acrobatics in NumPy would be too risky, so we decided to create a new project for this, called [NumType](https://github.com/numpy/numtype).

When NumType is installed, your static type-checker will use its `.pyi` stubs instead of those bundled with NumPy. There are three main advantages to this:

1. Improved ufunc annotations.
2. Full support of the [NEP 50](https://numpy.org/neps/nep-0050-scalar-promotion.html) promotion rules for all scalars, exhaustively verified to be 100% accurate.
3. Experimental shape-typing with automatic static broadcasting types.

The "magic" types that enable the dtype promotion and shape-type broadcasting are currently only accessible from the private type-check-only `_numtype` API. But the plan is to eventually make these part of the public `numtype` API.

But before you drop everything to install NumType, note that it's currently in alpha, so there's no backwards-compatibility guarantee. However, if you _do_ decide to use it and encounter an issue, be sure to complain about it in high definition at https://github.com/numpy/numtype/issues :)

## Strengthening the Ecosystem: `scipy-stubs` and Beyond

Typing NumPy is useless if the libraries built _on top_ of it aren't typed. A significant portion of my time went into `scipy-stubs`.

- We transferred ownership of [`scipy-stubs`](https://github.com/scipy/scipy-stubs/) — which started as `jorenham/scipy-stubs` — to the official SciPy organization.
- `scipy-stubs` now covers the full SciPy API, and only uses `Any` when absolutely necessary.
- It has grown massively — it now contains over 72,000 lines of code (according to [`scc`](https://github.com/boyter/scc)), making it the largest hand-written stubs-only Python package; even if you include `typeshed`'s standard library stubs (which currently counts 69,439 lines of code).
- We added runtime support for the generic types, including the sparse arrays, probability distributions, and interpolation classes.
- I helped large libraries such as [`pandas`](https://github.com/pandas-dev/pandas), [`jax`](https://github.com/jax-ml/jax), [`colour`](https://github.com/colour-science/colour), and [`pyspark`](https://github.com/apache/spark) adopt `scipy-stubs`.

I also made sure to spread the love to other corners of the ecosystem by adding typing support to [`numpy-financial`](https://github.com/numpy/numpy-financial), [`numpy-stl`](https://github.com/wolph/numpy-stl), [`numpy-quaddtype`](https://pypi.org/project/numpy-quaddtype/), [`numexpr`](https://github.com/pydata/numexpr), and [`threadpoolctl`](https://github.com/joblib/threadpoolctl).

## Bridging Communities

Perhaps the achievement I'm most proud of is the collaboration with the type-checker maintainers. Scientific Python has complex needs that often stretch the limits of Python's type system.

Throughout the year, I discovered and investigated bugs in all five major type-checkers: [`mypy`](https://github.com/python/mypy), [`pyright`](https://github.com/microsoft/pyright), [`basedpyright`](https://github.com/DetachHead/basedpyright), [`pyrefly`](https://github.com/facebook/pyrefly), and [`ty`](https://github.com/astral-sh/ty). [Some](https://github.com/python/mypy/pulls?q=is%3Apr+author%3Ajorenham+created%3A2025-01-01..2025-12-31) of the `mypy` bugs I even managed to fix myself. We fixed critical bugs affecting NumPy users and improved analysis times.

I feel that this work has brought the Scientific Python community much closer to the Python Typing community. I'm incredibly grateful to the maintainers of these tools for their responsiveness and willingness to collaborate.

## Wrapping Up

This fellowship has been an absolute privilege, and I feel like I've made the most out of it. If you want to dive into the nitty-gritty details, you can find all of my activity on my GitHub profile ([`@jorenham`](https://github.com/jorenham)), but for now, I'm just happy to have made those squiggly lines a bit more meaningful.

Thanks to everyone who made this possible, and type safe!
