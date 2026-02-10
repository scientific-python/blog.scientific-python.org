---

title: "Developer Summit 1: Sparse Arrays"
date: 2023-07-09T10:07:40-04:00
draft: false
description: "
Sparse Arrays at the May Developer Summit in Seattle
"
tags: ["Summit", "Scientific-Python", "scipy.sparse", "Sparse"]
displayInList: true
authors: ["Dan Schult", "Stéfan van der Walt <stefanv>"]
summary: |
    The first [Scientific Python Developer Summit](https://blog.scientific-python.org/scientific-python/dev-summit-1/) provided an opportunity
    for core developers from the scientific Python ecosystem to come together to:

    1. improve joint infrastructure
    2. better coordinate core projects
    3. work on a shared strategic plan

    One of the focuses of the summit was Sparse Arrays, and specifically their implementation in SciPy.
    This post attempts to recap what happened with "sparse" at the summit
    and a glimpse of plans for our continuing work.
---

(May 22-26, 2023, Seattle WA) --
The first [Scientific Python Developer Summit](https://blog.scientific-python.org/scientific-python/dev-summit-1/) provided an opportunity
for core developers from the scientific Python ecosystem to come together to:

1. improve joint infrastructure
2. better coordinate core projects
3. work on a shared strategic plan

Related notes/sites:

- [Worklog](https://hackmd.io/iEtdfbxfSbGwOAJTXmqyIQ?view).
- [Planning Meeting Notes and Info](https://scientific-python.org/summits/developer/2023/).

One of the focuses of the summit was Sparse Arrays, and specifically their implementation in SciPy.
This post attempts to recap what happened with "sparse" at the summit
and a glimpse of plans for our continuing work. The Sparse Array working group
holds [open follow-up meetings](https://scientific-python.org/calendars), currently scheduled every two weeks,
to continue the momentum and move this project forward.

At the Summit, we focused on improving the newly added Sparse Array API
in SciPy, that lets users manipulate sparse data with NumPy
semantics (before, SciPy used NumPy's 2D-only Matrix API, but that is [slated for deprecation](https://stackoverflow.com/questions/53254738/deprecation-status-of-the-numpy-matrix-class)).
Our goal at the summit was to give focused energy to the effort,
bring new people on board, and connect downstream users with the development
effort. We also worked to create a working group for this project that would
last beyond the summit itself.

The specific PRs and Issues involved in `scipy.sparse` are detailed in the
[Summit 2023 scipy.sparse Report](https://hackmd.io/1Q2832LDR_2Uv_-cV-wnYg),
with more detailed description appearing in the
[Summit Worklog](https://hackmd.io/iEtdfbxfSbGwOAJTXmqyIQ?view).
Some big picture take-aways are:

- Reorganized how to check for matrix/array/format info. This involved
  adding a `format` attribute describing which format of sparse storage is used,
  changing functions `issparse`/`isspmatrix` as well as shifting
  the class hierarchy to allow easy `isinstance` checking.
  The interface going forward includes:
  - `issparse(A)`: True when a sparse array or matrix.
  - `isinstance(A, sparray)`: True when a sparse array.
  - `isspmatrix(A)`: True when a sparse matrix.
    To check the format of a sparse array or matrix use `A.format == "csr"` or similar.
- Made decisions about how to approach the "creation functions" for sparse arrays.
  The big-picture approach is to introduce new functions with an `_array` suffix which
  construct sparse arrays. The old names will continue to create sparse matrix until
  post-deprecation removal.
  Some specific changes made include:
  - Add the creation function `diags_array(A)` (and planned for `eye_array`, `random_array` and others).
  - Create a `sparse.linalg.matrix_power` function for positive integer matrix power of a sparse array
- Made progress toward 1D sparse arrays. The data structures for 1d may be quite different from 2d.
  A prototype `coo_array` allowed exploration of possible n-d arrays, though that is not a short-term goal.
- Explored feasibility and usefulness of defining `__array_ufunc__` and other `__array_*__` protocols for sparse arrays
- Made clearer distinction between private and public methods for sparse arrays
- Improved documentation for sparse arrays

Our goal is to have a working set of sparse array construction functions
and a 1d sparse array class (focusing on `coo_array` first) in plenty of
time for intensive testing before SciPy v1.12. This will then allow us to
focus on creating migration documents and tools as well as helping downstream
libraries make the shift to sparse arrays. We hope to enable the removal of
deprecated sparse matrix interfaces in favor of the array interface. For this
to happen we will need most downstream users to shift to the sparse array API.
We intend to help them do that.

Our work continues with a community call every [two weeks on Fridays.](https://scientific-python.org/calendars)
Near term work is to:

- Continue improving sparse creation functions: diags, eye, random and others.
- Deprecate some matrix-specific functionality
- General performance improvements
- Adapting scikit-learn to support sparse arrays (to be discussed with scikit-learn's maintainers)
