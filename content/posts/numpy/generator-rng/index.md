---
title: "Random numbers done right"
date: 2022-12-28
draft: false
description: "
Use `np.random.Generator` and don't seed! A quick explainer on random number
generation with NumPy.
"
tags: ["NumPy", "tutorials", "random-numbers"]
displayInList: true
author: ["Pamphile Roy"]

---

Do you need random numbers? You use NumPy? NumPy has a canonical way to
produce random numbers with
[`np.random.Generator`](https://numpy.org/doc/stable/reference/random/index.html).
There is a say in Python, "global variables are bad". And you guessed correctly,
it's also bad to use `np.random.random()` or other generators that rely on a
global state! I finish with some discussion on using a seed.

In the following, we assume that _NumPy_, _SciPy_ and _Matplotlib_ are
installed and imported:

```python
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
```

## Random done wrong

```python
# the following is wrong and only exists for demonstration purposes!
np.random.seed(123456)
sample = np.random.random(1_024)
```

Aoutch! Two lines of codes and things can be said on both. This is a simple
snippet to generate 1024 points using NumPy's random number generator that is
very common in codes and tutorials online. Sadly/surprisingly even on famous
blogs.

There are 2 problems I want to talk about:

1. [global state](#global-id),
2. [seed](#seed-id).

## Goodbye global state {#global-id}

Behind `np.random.random` a number generator is used. This generator has an
internal state which is _global_. This state is shared and as new points/samples
are requested, this state is used and updated. The state can be set with a
_seed_ value.

As with any global variable, it means that it can be changed by other
subprocesses, threads, other libraries, etc. Take the following code. It uses
4 threads to call `np.random.random` 10 times and then prints the last value.
We execute this 5 times to see how the value changes.

```python
# the following is wrong and only exists for demonstration purposes!
import concurrent.futures

for _ in range(5):
    np.random.seed(123456)  # fix the state of the global generator

    sample = []
    with concurrent.futures.ThreadPoolExecutor(4) as executor:
        futures = [executor.submit(np.random.random, 1) for _ in range(10)]
        for future in concurrent.futures.as_completed(futures):
            sample.append(future.result())

    print(sample[-1])

# [0.33622174]
# [0.5430262]
# [0.96671784]
# [0.37674972]
# [0.96671784]
```

As you can see, although we started with the same state, this program is not
deterministic anymore.

NumPy came up with a solution: `np.random.RandomState`. The idea is,
knowing random number generators have a state, let's define them as
objects. This way, each object can have it's internal state instead of relying
on a global one. This API is more explicit and prevents any "contamination"
of state. See this example.

```python
# value of the seed only for illustrative purposes
# see bellow to use SeedSequence
seed = 123456

# reference value
rng = np.random.RandomState(seed)
print(rng.random(6)[-1])

np.random.seed(seed)
rng = np.random.RandomState(seed)

for _ in range(5):
    # try to introduce some unwanted noise on the global state
    np.random.random(1)
    # call we want to control
    rng.random(1)

print(rng.random(1)[0])

# 0.33622174433445307
# 0.33622174433445307
```

It sets the global seed and defines a `rng` using the object based API.

> RNG stands for Random Number Generator. This abbreviation is commonly used.

Then `np.random.random` and `np.random.RandomState` calls 5 times. The global
state is getting updated, but it does not impact our `rng` stream of numbers.

A lot of packages already migrated their code to move away from the global
generator in favour of an object one. In this case, setting the global state
would have absolutely no effect and you will end up in a broken state.

## Welcome to `np.random.Generator`

Now you might have read that `np.random.RandomState` is deprecated and
`np.random.Generator` should be used instead. It's true, but a bit more nuanced
as we will see. What is true though is that in any case, a global state
generator must not be used.

So why this new interface `np.random.Generator`? The main reason is to break
away from backward compatibilities concerns. `np.random.RandomState` was
advertised as providing a constant bit-stream for a given seed. The problem
is that this is extremely hard to guarantee for a wide range of
platform/architecture. Even more if you want to change underlying methods,
improve speed, fix bugs, etc. This is why NumPy decided with the policy
described in
[NEP19](https://numpy.org/neps/nep-0019-rng-policy.html)
to create a new interface.

> Did you know? `rand`, `randn`, etc. were just added to accommodate Matlab
> users. These names match similar functions from Matlab to help code porting.
> But you should check the documentation and use other recommended methods.

Hence, for new code, `np.random.Generator` should be
used. It does not provide a strong guarantee of reproducibility across
different versions. But it's fine as we will see in the next section about
[seed](#seed-id). To create a new instance of `np.random.Generator`, the
canonical way is to use:

```python
rng = np.random.default_rng()
```

When you have to write tests `np.random.RandomState` is still recommended.
Yes it's slower and has known issues, but it guarantees the bit-stream.
Something you might need if you have sensitive tests.

For more details have a look at the documentation of
[`np.random`](https://numpy.org/doc/stable/reference/random/index.html)
and at the policy document
[NEP19](https://numpy.org/neps/nep-0019-rng-policy.html).

## Digression on using a seed {#seed-id}

A quick note about using a seed. When you use a seed, you are using a fixed
sequence of points which effectively has no guarantee over the quality of the
points.

Consider a few statistical distributions to illustrate this.

_Note that I used 1024 points which is fairly reasonable for a 1 dimensional
problem._

```python
from collections import namedtuple

seed = 123456  # Please do NOT use a seed: this is to illustrate a wrong usage
rng = np.random.default_rng(seed)

# samples
ns = 1_024

dist_ = namedtuple("dist", ["name", "sample", "pdf"])
dists = [
    dist_("uniform", rng.random(ns), stats.uniform),
    dist_("normal", rng.standard_normal(ns), stats.norm),
    dist_("gamma", rng.gamma(2.0, size=ns), stats.gamma(2.0)),
]

# visualization
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

for i, dist in enumerate(dists):
    _, bins, _ = axs[i].hist(dist.sample, bins=64, density=True)
    x = np.linspace(min(bins), max(bins), 100)
    axs[i].plot(x, dist.pdf.pdf(x), "r-", lw=5, alpha=0.6, label=dist.name)
    axs[i].legend()
```

![
Histograms for uniform, normal and gamma distribution using 1024 samples.
They are compared with the underlying distributions and a poor match.
](distributions_seeded.png)

Does that look good to you? It is not. If you need to have a determined
sequence of points, there are other techniques that would generate almost
perfect histograms only using a fraction of the number of points which is used
here. See [this article]({{< relref "../../scipy/qmc-basics" >}})
for more information on this.

Be mindful of that in your application and know why you are using a seed
and how it impacts your results and analysis.

Bellow we will see how we can use seed in tests and also how to generate
a good seed value. Because yes, all values are not created equal and it's
not a good idea to reuse common values such as 0, 12345 or 42. Seed should
also be randomly generated for various reasons. Again, the
[NEP19](https://numpy.org/neps/nep-0019-rng-policy.html) has good insights.

## Testing with random numbers

Before showing any code though, ask yourself if you actually need ot use
random numbers to write your test. You might just need a small matrix with
hard-coded numbers. Not only you don't need to run the code to know the values,
but you will be 100% certain that this is stable on any platform/architecture
and future-proof. You have more advanced needs, ok then maybe using known
sequences (quasi-random numbers) is a good alternative (again see
[here]({{< relref "../../scipy/qmc-basics" >}})
).

If you want or need to use NumPy for that, then either use
`np.random.Generator` or the legacy `np.random.RandomState`. Aside from
backward compatibility concerns, `np.random.RandomState` is still present in
NumPy for testing.

```python
rng = np.random.default_rng()
# or
rng = np.random.RandomState()
```

[NEP19](https://numpy.org/neps/nep-0019-rng-policy.html) actually
recommends `np.random.RandomState` for testing as the byte stream is not
guaranteed as strongly as before with the new generators. In practice, changes
are not happening often though. What matters in both cases is that you use the
object based API and not the legacy approach with global state.

Now, one thing with tests is that we want them to be reproducible so that
we can inspect our code and find issues. Here you want to use a seed.
This is one of the few valid use for a seed. (Sure if you are an expert in
Monte Carlo sampling, you can probably find your way... Just don't try this at
home).

But because you can use a seed doesn't mean you can resort to our old friends
0, 123456, etc. NumPy proposes a canonical way to randomly give you a seed.

```python
import numpy as np

print(np.random.SeedSequence().entropy)
```

Use this snippet to generate seed values for your tests.

## Conclusion

Use `np.random.Generator`: it is better in every way. If you see code using
the global state, spread the word and help us move forward.

```python
# this is right!
rng = np.random.default_rng()
sample = rng.random(1_024)
```

```python
# this is right!
def test_something():
    # generate a seed using `print(np.random.SeedSequence().entropy)`
    seed = ...
    rng = np.random.RandomState(seed)
    sample = rng.random(1_024)
```
