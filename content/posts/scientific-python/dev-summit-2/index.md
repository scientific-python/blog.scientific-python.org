---
title: "Developer Summit 2"
date: 2024-09-29
draft: false
description: "Summary of the 2024 Scientific Python Developer summit."
tags: ["Summit", "Scientific-Python"]
displayInList: true
author:
  [
    "Stéfan van der Walt",
    "Jarrod Millman",
    "Brigitta Sipőcz",
    "Pamphile Roy",
    "Matt Haberland",
    "Nabil Freij",
    "Elliott Sales de Andrade",
    "Matthew Feickert",
    "Dan Schult",
    "Ross Barnowsk",
    "Melissa Mendonça",
    "Dan McCloy",
    "Lars Grüter",
    "Sebastian Berg",
    "Mridul Seth",
    "Eric Larson",
    "Sanket Verma",
    "Inessa Pawson",
  ]

resources:
  - name: featuredImage
    src: "group.jpg"
    params:
      description: "Group picture of (most of the) summit attendees."
      showOnTop: true

summary: |
  The 2024 Scientific Python Developer summit was held 3–5 June in Seattle. Here's a summary of what we did.
---

This post is a while overdue, but it's been a busy summer for everyone!

In June, several of us got together for the "annual" (well, we've had it twice now) Scientific Python developer summit in Seattle.
Our friends at the eScience Institute were again kind enough to host us.
This time around, we made the event a bit shorter to avoid clashing with graduation.

As before, the Developer Summits are for members of the community to come together, in person, so they can work.
Of course, we work together already online, but the event allows us to focus our energies on cross-project concerns (that often fall by the wayside) with planning and intent.

This is why, before the summit, we have planning Zoom calls, where we identify topics of interest, which are turned into issues, which are then fleshed out and discussed prior to the event.
That way, we hoped to hit the ground running—as we did!

## Topics

You can get a rough idea of what we worked on by browsing the [planning issues](https://github.com/scientific-python/summit-2024/issues/) and the [summit worklog](https://hackmd.io/wsJVTMYdQGG_Zgz7rgxSzw).

Broad topics included [SPECs](https://scientific-python.org/specs/), documentation, tools & bots, [lectures](https://lectures.scientific-python.org/), `scipy.sparse`, telemetry, Array API, and type annotation.

### Documentation

Documentation was a much more popular topic than anticipated!

- The new [mystmd](https://mystmd.org/guide) tooling generated some excitement, and an [experimental port of the NumPy tutorials](https://github.com/numpy/numpy-tutorials/tree/mystjs) was made by Melissa and Ross.
- Recommendations on consistent use of [backticks](https://github.com/numpy/numpydoc/pull/525) and [monospaced font](https://github.com/pydata/pydata-sphinx-theme/issues/1852) were submitted to numpydoc and pydata-sphinx-theme, respectively.
- Madicken, Paul, and Dan worked together to [extend PyData Sphinx Theme's testing infrastructure](https://github.com/pydata/pydata-sphinx-theme/pull/1861), by combining Sphinx Build Factory (for generating small test sites) with Playwright (for browser automation).
- Eric and Elliott fixed an [intersphinx issue in sphinx-gallery](https://github.com/sphinx-gallery/sphinx-gallery/pull/1320).

### SPECs

The Scientific Python Ecosystem Coordination documents (SPECs) aim to improve coordination of technical development across the ecosystem.

Several new SPECs were started:

- [SPEC-?: Dispatching (`spatch`)](https://hackmd.io/yI1iAqekQIq0a4jLS9WPyw)
- [SPEC-8: Securing The Release Process](https://scientific-python.org/specs/spec-0008/)
- [SPEC-9: Governance](https://scientific-python.org/specs/spec-0009/)
- [SPEC-10: Changelog and release documentation](https://github.com/scientific-python/specs/pull/321)
- [SPEC-12: Formatting mathematical expressions](https://github.com/scientific-python/specs/pull/326)
- [SPEC-13: Naming conventions](https://github.com/scientific-python/specs/pull/324)

Some existing SPECs were discussed and improved:

- [SPEC-7: Seeding pseudo-random number generation (SPRaNG)](https://scientific-python.org/specs/spec-0007/)

Matplotlib [endorsed](https://scientific-python.org/specs/purpose-and-process/#decision-points) several SPECs.

### Tooling

- We created a new tools team to handle the ever-growing [list of tools we maintain](https://tools.scientific-python.org/).
- Eric added his [circleci-artifacts-redirector-action](https://github.com/scientific-python/circleci-artifacts-redirector-action) to the suite.
- Matthias brought over his [backport bot](https://github.com/scientific-python/MeeseeksDev) and set up a maintenance team.

### SciPy

Several of the SciPy developers were present, and we used the opportunity to celebrate Dan Schult joining as a core developer 🎉!
Matt and Pamphile did some work on the new distribution infrastructure, Dan worked on sparse (remotely with CJ), and a [PR adding newly-supported `const` statements to Cython code](https://github.com/scipy/scipy/pull/20891) got reviewed and merged.
Eric isolated [a non-deterministic bug in Sphinx](https://github.com/sphinx-doc/sphinx/issues/12409) that was impacting parallel builds of SciPy's documentation.
He found a work-around that had been eluding the team for months!

### Unplanned collaborations

As is the nature of these events, some collaborations arise spontaneously.
For example:

- Nick and Ariel explored using Awkward Array for neuro-tractography.
- Nick and Mridul explored using [scipp](https://scipp.github.io/index.html) for high-energy physics data.
- Guen worked on telemetry.
- Inessa and Sanket discussed best practices for community surveys and project governance.
- Sebastian and Thomas [discussed parallelization APIs](https://hackmd.io/84thx0ucQ2ab17ZYrBhWRw).
- Inessa, with input from Tim and Thomas, finalized the design of the 2024 scikit-learn user survey.
- Erik and Dan discussed index compression options for CSR-like nD sparse arrays.

### Conclusion

Numerous other PRs were made, of which a number were probably not even captured in the [worklog](https://hackmd.io/wsJVTMYdQGG_Zgz7rgxSzw).
But, besides the inherent satisfaction of working together with this great group, the best feature of the summit was that we were able to hang out, bonding over our communal joys and struggles—both technical and personal.

We are grateful to the ecosystem developers who gave up their time to attend the summit (many had to put in leave _just to do more work_!).
The summits are valuable, and translate to a lot of work getting done and decisions being made.
We hope that there will be more on the horizon!
