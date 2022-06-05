---
title: "SciPy Internship: 2021-2022"
date: 2022-06-04
draft: false
description: "Internship Experience"
tags: ["SciPy", "internship", "meson-build", "uarray"]
displayInList: true
author: ["Smit Lunagariya"]
---

I was [selected as an intern](https://mail.python.org/archives/list/scipy-dev@python.org/message/4S43BYHDQIPQENNJ6EMQY5QZDZK3ZT5I/) to work on SciPy build system. In this blog post, I will be describing my journey of this 10-months long internship at SciPy. I worked on a variety of topics starting from migrating the SciPy build system to [Meson](https://mesonbuild.com/index.html), cleaning up the public API namespaces and adding [Uarray](https://uarray.org/en/latest/) support to SciPy submodules.

# Experience

## Meson Build System

The main reasons for switching to Meson include (in addition to `distutils` being deprecated):

1. _Much faster builds_
2. _Reliability_
3. _Support for cross-compiling_
4. _Better build logs_
5. _Easier to debug build issues_

_For more details on the initial proposal to switch to Meson, see [scipy-13615](https://github.com/scipy/scipy/issues/13615)_

I was initially selected to work on the migrating the SciPy build system to [meson](https://mesonbuild.com/index.html). I started by adding Meson build support
for [scipy.misc](https://github.com/rgommers/scipy/pull/35) and [scipy.signal](https://github.com/rgommers/scipy/pull/37). While working on this, we came across many [build warnings](https://github.com/rgommers/scipy/issues/42) which we wanted to fix, since they unnecessarily increased the build log and might point to some hidden bugs. I fixed these warnings, the majority of which came from [deprecated NumPy C API calls](https://github.com/rgommers/scipy/issues/30).

- I also started [benchmarking](https://github.com/rgommers/scipy/issues/58) the Meson build with various optimization levels, during which I ended up finding some [failing benchmark tests](https://github.com/scipy/scipy/issues/14667) and tried to fix them.
- I implemented the [dev.py](https://github.com/rgommers/scipy/pull/94) interface that works in a similar way to `runtests.py`, but using Meson for building SciPy.
- I extended my work on the Meson build by writing Python scripts for checking the installation of all [test files](https://github.com/rgommers/scipy/issues/69) and [.pyi files](https://github.com/scipy/scipy/pull/16010).
- I documented how to use [dev.py](https://github.com/rgommers/scipy/pull/96), and use [parallel builds and optimization levels](https://github.com/scipy/scipy/pull/15953) with Meson.
- I added [meson option](https://github.com/rgommers/scipy/pull/130) to switch between BLAS/LAPACK libraries.

Meson build support including all the above work was merged into SciPy's `main` branch around Christmas 2021. Meson will now become the default build in the upcoming 1.9.0 release.

## Making cleaner public namespaces

#### What's the issue?

_"A basic API design principle is: a public object should only be available from one namespace. Having any function in two or more places is just extra technical debt, and with things like dispatching on an API or another library implementing a mirror API, the cost goes up."_

```py
>>> from scipy import ndimage
>>> ndimage.filters.gaussian_filter is ndimage.gaussian_filter  # :(
True
```

The [API reference docs](http://scipy.github.io/devdocs/reference/index.html#api-definition) of SciPy define the public API. However, SciPy still had some submodules that were _accidentally_ somewhat public by missing an underscore at the start of their name.
I worked on [cleaning the pubic namespaces](https://github.com/scipy/scipy/issues/14360) for about a couple of months by carefully adding underscores to the `.py` files that were not meant to be public and added depecrated warnings if anyone tries to access them.

#### The solution:

```py
>>> from scipy import ndimage
>>> ndimage.filters.gaussian_filter is ndimage.gaussian_filter
<stdin>:1: DeprecationWarning: Please use `gaussian_filter` from the `scipy.ndimage` namespace, the `scipy.ndimage.filters` namespace is deprecated.
True
```

## Adding Uarray support

_"SciPy adopted uarray to support a multi-dispatch mechanism with the goal being: allow writing backends for public APIs that execute in parallel, distributed or on GPU."_

For about the last four months, I worked on adding [Uarray support](https://github.com/scipy/scipy/issues/14353) to SciPy submobules. I do recommend reading [this blog post](https://labs.quansight.org/blog/2021/10/array-libraries-interoperability/) by Anirudh Dagar covering the motivation and actual usage of `uarray`. I picked up the following submodules for adding `uarray` compatibility:

- [signal](https://github.com/rgommers/scipy/pull/101)
- [linalg](https://github.com/scipy/scipy/pull/15610)
- [special](https://github.com/scipy/scipy/pull/15665)

At the same time, in order to show a working prototype, I also added `uarray` backends in CuPy to the following submodules:

- `cupyx.scipy.ndimage` ([PR #6403](https://github.com/cupy/cupy/pull/6403))
- `cupyx.scipy.linalg` ([PR #6460](https://github.com/cupy/cupy/pull/6460))
- `cupyx.scipy.special` ([PR #6564](https://github.com/cupy/cupy/pull/6564))

The pull requests contain links to Colab notebooks which show these features in action.

#### What does usage of such a backend look like?

```py
import scipy
import cupy as cp
import numpy as np
from scipy.linalg import inv, set_backend
import cupyx.scipy.linalg as _cupy_backend

x_cu, x_nu = cp.array([[1., 2.], [3., 4.]]), np.array([[1., 2.], [3., 4.]])
y_scipy = inv(x_nu)

with set_backend(_cupy_backend):
    y_cupy = inv(x_cu)
```

## Miscelleanous Work

- [Fix path issues in runtests.py](https://github.com/scipy/scipy/pull/15440)
- [Array inputs for stats.kappa4](https://github.com/scipy/scipy/pull/15250)
- [Fixes mac CI conda env cache](https://github.com/rgommers/scipy/pull/115)

## Future Work

- The "switch to Meson" project is nearing its completion. One of the final issues was to allow [building wheels](https://github.com/scipy/scipy/pull/15476) with the `meson-python` backend.
- The PRs opened for adding `uarray` support are still under heavy discussion, and the main aim will be get them merged as soon as possible once we have reached a concrete decision.

## Things to remember

1. _Patience_: Setting up new project always takes some time. We might need to update/fix the system libraries and try to resolve the errors gradually.
2. _Learning_: Learning new things was one of the main key during the internship. I was completely new to build systems and GPU libraries.

## Thank You!!

I am very grateful to [Ralf Gommers](https://github.com/rgommers) for providing me with this opportunity and believing in me. His guidance, support and patience played a major role during the entire course of internship.
I am also thankful to whole SciPy community for helping me with the PR reviews and providing essential feedback. Also, huge thanks to [Gagandeep Singh](https://github.com/czgdp1807) for always being a part of this wonderful journey.

_In a nutshell, I will remember this experience as: [Ralf Gommers](https://github.com/rgommers) has boosted my career by millions!_
