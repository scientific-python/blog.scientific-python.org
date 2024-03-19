---
title: "The Scientific Python Development Guide"
date: 2023-08-26T12:00:00-05:00
draft: false
description: >
  Introducing the Scientific Python Development Guide!
tags: ["tutorials", "cookie", "scientific-python", "summit"]
displayInList: true
author: ["Henry Schreiner"]

resources:
  - name: featuredImage
    src: "henriii.png"
    params:
      description: |
        Henry Schreiner presenting the Development Guide and cookie project
        template at the first Scientific Python Developer Summit.
      showOnTop: true
---

One outcome of the
[2023 Scientific Python Developer Summit](https://scientific-python.org/summits/developer/2023/)
was the [Scientific Python Development Guide][], a comprehensive guide to modern
Python package development, complete with a [new project template][cookie]
supporting 10+ build backends and a [WebAssembly-powered checker][sp-repo-review]
with checks linked to the guide. The guide covers topics like [modern][],
[compiled][], and [classic][] packaging, [style][] checks, [type
checking][mypy], [docs][], [task runners][], [CI][gha_basic], [tests][pytest],
and much more! There also are sections of [tutorials][], [principles][], and
some common [patterns][].

<!--more-->

This guide (along with cookie & repo-review) started in [Scikit-HEP][] in 2020.
During the summit, it was merged with the [NSLS-II][] guidelines, which provided
the basis for the [principles][] section. I'd like to thank and acknowledge Dan
Allan and Gregory Lee for working tirelessly during the summit to rework,
rewrite, merge, and fix the guide, including writing most of the [tutorials][]
pages and first [patterns][] page, and rewriting the [environment][] page as a
tutorial.

## The guide

The core of the project is the guide, which is comprised of four sections:

- [Tutorials][]: How to go from "research" code to a basic package, for
  beginning readers.
- [Topical guides][topics]: The core of the guide, for intermediate to advanced
  readers.
- [Principles][]: Some general principles from the [NSLS-II][] guide.
- [Patterns][]: Recipes for common situations. Three pages are there now;
  [including data][], [backports][], and [exports][].

From the original [Scikit-HEP dev pages][], a lot was added:

- Brand new guide page on documentation, along with new [sp-repo-review][] checks to
  help with readthedocs.
- A compiled projects page! Finally! With [scikit-build-core][],
  [meson-python][], and [maturin][]. The page shows real outputs from the
  [cookiecutter][], kept in sync with [cog][] (a huge benefit of using a single
  repo for all three components!)
- Big update to [GHA CI page][gha_basic] including a section on Composite
  Actions given at the Dev summit.
- CLI entry points are now included.
- Python 3.12 support added, Python 3.7 dropped.
- New [sp-repo-review][] badges throughout (more on that later!)
- Updates for [Ruff][]'s move and support for requires-python.
- Lots of additions for GitHub Actions.

The infrastructure was updated too:

- Using latest Jekyll (version 4) and latest Just the Docs theme. More colorful
  callout boxes. Plugins are used now.
- Live PR preview (provided by probably the world’s first readthedocs Jekyll
  build!). Developed with the Zarr developers during the summit.
- Better advertising for [cookie][] and [sp-repo-review][] on the index page(s).
- Auto bump and auto-sync CI jobs.

## Cookie

We also did something I've wanted to do for a long time: the guide, the
cookiecutter template, and the checks are all in a single repo! The repo is
[scientific-python/cookie][cookie], which is the moved `scikit-hep/cookie` (the
old URL for cookiecutter still works!).

Cookie is a new project template supporting multiple backends (including
compiled ones), kept in sync with the dev guide. We recommend starting with
the dev guide and setting up your first package by hand, so that you understand
what each part is for, but once you've done that, [cookie][] allows you to get
started on a new project in seconds.

A lot of work went into [cookie][], too!

- Generalized defaults. We still have special integration if someone sets the
  org to `scikit-hep`; the same integration can be offered to other orgs.
- All custom hooks removed; standard jinja now used throughout templates. Using
  cookiecutter computed variables idiom too. Windows still fully supported and
  tested. Adding new choices is much easier now.
- Added cruft (a cookiecutter updater) testing.
- Dual-supporting [copier][] now too, a [cookiecutter][] replacement with a huge
  CLI improvement (and also supports updating). Might be the first project to
  support both at the same time. CI (or [nox][] locally) checks to ensure
  generation is identical. Much better interface with copier, including
  validation, descriptive text, arrow selection, etc.
- Improved CLI experience even if using cookiecutter (like no longer requesting
  current year).
- Reworked docs template.
- Support for cookiecutter 2.2 pretty descriptions (added about four hours after
  cookiecutter 2.2.0 was released) and cookiecutter 2.2.3 choice descriptions.
- GitLab CI support when not targeting github.com URLs (added by Giordon Stark).
- Support for selecting VCS or classic versioning.

## Repo-review

See the [introduction to repo-review](https://iscinumpy.dev/post/repo-review/)
for information about this one!

Along with this was probably the biggest change, one requested by several people
at the summit: [scientific-python/repo-review][repo-review] (was
`scikit-hep/repo-review`) is now a completely general framework for implementing
checks in Python 3.10+. The checks have been moved to `sp-repo-review`, which is
now part of scientific-python/cookie. There are too many changes to list here,
so just the key ones in 0.6, 0.7, 0.8, 0.9, and 0.10:

- Extensive, beautiful [documentation](https://repo-review.readthedocs.io) for
  check authors at (used to help guide the new docs guide page & template
  update!)
- Support for four output formats, [rich][] (improved), svg, json (new), html
  (new).
- Support for listing all checks.
- GitHub Actions support with HTML step summary, [pre-commit][] support.
- Generalized topological sorting to fixtures, dynamic fixtures.
- Dynamic check selection (via fixtures! Basically everything is powered by
  fixtures now.)
- URL support in all output formats (including the terminal and WebApp!)
- Support for package not at root of repo.
- Support for running on a remote repo from the command line.
- Support for select/ignore config in `pyproject.toml` or command line.
- Pretty printed and controllable sorting for families.
- Supports running from Python, including inside a readme with something like
  cog.
- Support for dynamic family descriptions (such as to output build system and
  licence used).
- Support for limiting the output to just errors or errors and skips.
- Support for running on multiple repos at once, with output tailored to
  multiple repos. Also supports passing `pyproject.toml` path instead to make
  running on mixed repos easier.
- Support for linting `[tool.repo-review]` with [validate-pyproject][].

The
[full changelog](https://repo-review.readthedocs.io/en/latest/changelog.html)
has more - you can even see the 10 beta releases in-between 0.6.x and 0.7.0
where a lot of this refactoring work was happening. If you have configuration
you’d like to write check for, feel free to write a plugin!

[validate-pyproject][] 0.14 has added support for being used as a repo-review
plugin, so you can validate `pyproject.toml` files with repo-review! This lints
`[project]` and `[build-system]` tables, `[tool.setuptools]`, and other tools
via plugins. [Scikit-build-core][] 0.5 can be used as a validate-project plugin
to lint `[tool.scikit-build]`. Repo-review has a plugin for
`[tool.repo-review]`.

## sp-repo-review

Finally, [sp-repo-review][] contains the previous repo-review plugins with checks:

- Fully cross-linked with the development guide. Every check has a URL that
  points to a matching badge inside the development guide where the thing the
  check is looking for is being discussed!
- Full list of checks (including URLs), produced by cog, in
  [readme](https://pypi.org/p/sp-repo-review).
- Also ships with GitHub Action and [pre-commit][] checks
- Released (in sync with cookie & guide, as they are in the same repo) as
  CalVer,
  [with release notes](https://github.com/scientific-python/cookie/releases).
- Split CI that selects just want to run based on changed files, with green
  checkmark that respects skips (based on the excellent contrition to
  pypa/build).

<!-- prettier-ignore-start -->
{{< figure >}}
src = 'cibw_example.png'
caption = 'Running sp-repo-review on cibuildwheel'
alt = 'Image of sp-repo-review showing checks'
width = '60%'
{{< /figure >}}
<!-- prettier-ignore-end -->

## Using the guide

If you have a guide, we'd like for you to compare it with the Scientific Python
Development Guide, and see if we are missing anything - bring it to our
attention, and maybe we can add it. And then you can link to the centrally
maintained guide instead of manually maintaining a complete custom guide. See
[scikit-hep/developer][] for an example; many pages now point at this guide.
We can also provide org integrations for [cookie][], providing some
customizations when a user targets your org (targeting `scikit-hep` will add a
badge).

[style]: https://learn.scientific-python.org/development/guides/style/
[mypy]: https://learn.scientific-python.org/development/guides/mypy/
[modern]: https://learn.scientific-python.org/development/guides/packaging-simple/
[compiled]: https://learn.scientific-python.org/development/guides/packaging-compiled/
[classic]: https://learn.scientific-python.org/development/guides/packaging-classic/
[gha_basic]: https://learn.scientific-python.org/development/guides/gha-basic/
[pytest]: https://learn.scientific-python.org/development/guides/pytest/
[docs]: https://learn.scientific-python.org/development/guides/docs/
[topics]: https://learn.scientific-python.org/development/guides/
[task runners]: https://learn.scientific-python.org/development/guides/tasks/
[tutorials]: https://learn.scientific-python.org/development/tutorials/
[principles]: https://learn.scientific-python.org/development/principles/
[patterns]: https://learn.scientific-python.org/development/patterns/
[nsls-ii]: https://nsls-ii.github.io/
[environment]: https://learn.scientific-python.org/development/tutorials/dev-environment/
[including data]: https://learn.scientific-python.org/development/patterns/data-files/
[backports]: https://learn.scientific-python.org/development/patterns/backports/
[exports]: https://learn.scientific-python.org/development/patterns/exports/
[scikit-hep]: https://scikit-hep.org
[scikit-hep/developer]: https://scikit-hep.org/developer
[2023 scientific python developer summit]: https://scientific-python.org/summits/developer/2023
[scientific python development guide]: https://learn.scientific-python.org/development
[cookie]: https://github.com/scientific-python/cookie
[repo-review]: https://github.com/scientific-python/repo-review
[sp-repo-review]: https://learn.scientific-python.org/development/guides/repo-review
[scikit-hep dev pages]: https://scikit-hep.org/developer
[scikit-build-core]: https://scikit-build-core.readthedocs.io
[meson-python]: https://meson-python.readthedocs.io
[maturin]: https://www.maturin.rs
[cookiecutter]: https://www.cookiecutter.io
[copier]: https://copier.readthedocs.io
[ruff]: https://beta.ruff.rs
[cog]: https://nedbatchelder.com/code/cog
[nox]: https://nox.thea.codes
[pre-commit]: https://pre-commit.com
[rich]: https://rich.readthedocs.io
[validate-pyproject]: https://validate-pyproject.readthedocs.io
[scikit-build-core]: https://scikit-build-core.readthedocs.io
