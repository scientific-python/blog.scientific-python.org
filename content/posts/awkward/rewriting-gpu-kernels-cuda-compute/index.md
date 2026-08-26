---
title: "Rewriting Awkward Array's GPU kernels in Python with NVIDIA's cuda.compute"
date: 2026-08-26
draft: false
description: "How the Awkward Array and NVIDIA teams replaced thousands of lines of hand-written CUDA C++ with Python built on cuda.compute — ending up with less code that runs faster."
tags: ["Awkward Array", "GPU", "CUDA", "cuda.compute", "Scikit-HEP"]
displayInList: true
authors: ["Ianna Osborne", "Ashwin Srinath"]
---

_Thousands of lines of hand-written CUDA C++, now Python. Less code, and it runs faster._

A single collision event in a particle detector holds a variable number of particles, each with a variable number of measurements:

```
[[1.1, 2.2, 3.3], [], [4.4, 5.5]]
```

[Awkward Array](https://awkward-array.org/) is a Python library for manipulating nested, variable-length ("ragged") data like this with NumPy-like idioms. It stores that data flat, as one `content` buffer holding every value contiguously plus an `offsets` array marking where each sublist begins and ends:

```
content:  [1.1, 2.2, 3.3, 4.4, 5.5]
offsets:  [0, 3, 3, 5]        # the empty middle list spans no elements
```

Nothing is wasted on padding, but _every_ operation must then be written in terms of those two buffers rather than a simple shape. That is where dense GPU tensor frameworks stop helping: they want rectangles. For several years, Awkward's answer was a dictionary of hand-written CUDA C++ kernels compiled at runtime with CuPy.

The Awkward Array and NVIDIA teams have now rebuilt that layer on [`cuda.compute`](https://nvidia.github.io/cccl/unstable/python/compute/index.html), which brings the CUDA C++ parallel-algorithm libraries CUB and Thrust (the reductions, scans, and sorts that power production GPU software) into Python as ordinary callables. Instead of writing a kernel, the backend now composes ones that already exist. Four results stand out.

## 1. The GPU code is Python now

`ak.min`, the minimum over each ragged sublist, took _three_ kernel launches in CUDA C++: initialize a scratch buffer, reduce within each block using shared memory and explicit thread synchronization, and copy the result out. Each communicated with the next through global memory.

It is now a single call to a library primitive:

```python
import cupy as cp, numpy as np
from cuda.compute import OpKind, segmented_reduce


def awkward_reduce_min(
    toptr: cp.ndarray,
    fromptr: cp.ndarray,
    offsets: cp.ndarray,
    outlength: int,
    identity: float,
) -> None:

    toptr[:outlength] = identity
    segmented_reduce(
        fromptr,
        toptr,
        offsets[:-1],
        offsets[1:],
        OpKind.MINIMUM,
        np.asarray(identity, dtype=fromptr.dtype),
        outlength,
    )
```

`segmented_reduce` performs one reduction per segment, and `offsets[:-1]` and `offsets[1:]` hand it the start and end of each sublist directly. No CUDA C++, no synchronization, no scratch buffers: the library handles all of it.

Awkward's user-facing API is unchanged. Underneath, 2.10.0 routes **106 of its 133 GPU kernels (80%)** through `cuda.compute`, up from none in 2.8.11. Every reduction and the sort now run through it with no hand-written implementation remaining. The 27 still in CUDA C++ handle structural work like jagged indexing, padding, and validity checks. Their control flow depends on the ragged layout itself, which fits the segmented primitives less naturally. That migration is ongoing. Counting only code that must actually be maintained, the switch to `cuda.compute` has so far cut hand-written CUDA C++ from **8,288 lines to 2,170 — a 74% reduction**.

## 2. The abstraction made it faster

We might expect to pay something for the abstraction.

Over 5,000,000 ragged sublists, `ak.argmin` takes **0.96 ms per call** as a hand-written CUDA kernel and **0.39 ms** through `cuda.compute`: **2.5x faster, with identical output**.

That speedup is inherited rather than hand-tuned, which is exactly the point of building on CUB: segmented reductions are difficult to write well by hand, and CUB's have been tuned per architecture for years. Awkward gets that tuning now, and the next architecture's when it ships, without changing its own code.

## 3. A whole physics formula can collapse into one kernel

The first two results came from the migration. For this one, a user drops down to `cuda.compute` and composes the primitives by hand.

Awkward evaluates eagerly: every operation returns a real array, so a chain of them writes an intermediate to global memory at each step and reads it back at the next. `cuda.compute` algorithms instead accept **iterators** that are evaluated lazily as the algorithm runs, letting many logical steps ride along inside a single pass. That is [kernel fusion](https://developer.nvidia.com/blog/kernel-fusion-in-nvidia-cuda-optimizing-memory-traffic-and-launch-overhead/), and it saves both the memory traffic and the launch overhead.

### Example: di-muon invariant mass

The opposite-sign di-muon invariant mass, a standard reconstruction in particle physics, combines a few measured quantities for every pair of particles in an event. In Awkward, it is one line:

```python
mu1, mu2 = ak.unzip(ak.combinations(muons, 2))
mass = np.sqrt(
    2 * mu1.pt * mu2.pt * (np.cosh(mu1.eta - mu2.eta) - np.cos(mu1.phi - mu2.phi))
)
```

Evaluated step by step, that chain of arithmetic and trigonometric operations becomes one or more kernels per step, with every intermediate written out as a full-length array and read back.

Written by hand as one `cuda.compute` call, the whole formula becomes a single operator: a `gpu_struct` keeps each particle's fields together, a `ZipIterator` combines them, and a `PermutationIterator` produces each pair on demand. The operator sees one complete pair at a time, and no intermediate is ever built.

Over all such pairs in a CMS open-data sample:

|                     | **kernel launches** | **memory operations** | **GPU time** |
| ------------------- | ------------------- | --------------------- | ------------ |
| step by step        | 88                  | 212                   | 25.7 ms      |
| fused into one call | **1**               | 45                    | **10.2 ms**  |

2.5x faster, with nothing allocated in between.

## 4. At analysis scale, the gap widens

We ran the [ADL benchmark queries](https://github.com/CoffeaTeam/coffea-benchmarks) (a standard set of physics-analysis tasks) on CMS 2012 open data, against released Awkward 2.8.11 on its hand-written CuPy backend, the last version before `cuda.compute`. For the two combinatoric queries below, the Awkward expression is **unchanged**; only the backend underneath differs, so the comparison isolates the migration itself.

Measured on the **GPU compute stage** at 100k, 1M, and 10M events, both speed up by margins that grow with the data:

- the di-muon reconstruction from section 3: **60x → 422x → 3634x**
- a second combinatoric query: **45x rising to 250x**

`cuda.compute`'s time stays approximately constant across those sizes while the hand-written implementation grows super-linearly, so the gap widens as data grows rather than closing.

## The result that isn't a number

A stated goal of the Awkward Array project is to let physicists and data analysts write high-performance code in Python without GPU expertise. The old backend required contributors to understand CUDA thread hierarchies, atomics, and shared-memory behavior before they could add or fix a kernel. The new one asks for an ordinary Python function and a call to the right primitive. Domain scientists can read it, review it, and unit-test its logic without a GPU.

Awkward knows the problem. `cuda.compute` knows the hardware. The result is Python that's simpler and faster than the CUDA C++ it replaced.

_Full methodology, per-query results, and the code-counting rules are in "GPU-Accelerated Awkward Arrays with CUDA Python" by Ashwin Srinath (NVIDIA) and Ianna Osborne (Princeton University), Proceedings of the 24th Python in Science Conference (SciPy 2026). All measurements were taken on an NVIDIA RTX PRO 6000 Blackwell Server Edition with CUDA 13.2, `cuda.compute` 1.1.0, and CuPy 14.1.1; every benchmark was run twice on independent machines, with structural counts identical and timings agreeing to within a few percent. Migration progress is tracked in [scikit-hep/awkward#3793](https://github.com/scikit-hep/awkward/issues/3793)._

_Much of the kernel migration was implemented by Maxym Naumchyk. Thanks also to the `cuda.compute` and CUB/Thrust developers at NVIDIA and to the Scikit-HEP community. This work was supported in part by NSF grants OAC-1450377, OAC-1836650, OAC-2103945, PHY-2121686, and PHY-2323298._
