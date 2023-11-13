---
title: "Good practices with NumPy random number generators"
date: 2023-08-31T23:22:46+02:00
draft: false
description: "
Good practices with NumPy random number generators
"
tags: ["tutorials", numpy, rng]
displayInList: true
author: ["Albert Thomas"]
---

Unless you are working on a problem where you can afford a true Random Number Generator (RNG), which is basically never for most of us, implementing something random means relying on a pseudo Random Number Generator. I want to share here what I have learned about good practices with pseudo RNGs and especially the ones available in [NumPy](https://numpy.org/). I assume a certain knowledge of NumPy and that NumPy 1.17 or greater is used. The reason for this is that great new features were introduced in the [random](https://numpy.org/doc/stable/reference/random/index.html) module of version 1.17. As `numpy` is usually imported as `np`, I will sometimes use `np` instead of `numpy`. Finally, as I will not talk about true RNGs, RNG will always mean pseudo RNG in the rest of this blog post.

### The main messages
1. Avoid using the global NumPy RNG. This means that you should avoid using [`np.random.seed`](https://numpy.org/doc/stable/reference/random/generated/numpy.random.seed.html) and `np.random.*` functions, such as `np.random.random`, to generate random values.
2. Create a new RNG and pass it around using the [`np.random.default_rng`](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.default_rng) function.
3. Be careful with parallel random number generation and use the [strategies provided by NumPy](https://numpy.org/doc/stable/reference/random/parallel.html).

Note that, with the older NumPy <1.17, the way to create a new RNG is to use [`np.random.RandomState`](https://numpy.org/doc/stable/reference/random/legacy.html#numpy.random.RandomState) which is based on the popular Mersenne Twister 19937 algorithm. This is also how the global NumPy RNG is created. This function is still available in newer versions of NumPy, but it is now recommended to use `default_rng` instead, which returns an instance of the statistically better [PCG64](https://www.pcg-random.org) RNG. You might still see `np.random.RandomState` being used in tests as it has strong stability guarantees between different NumPy versions.

## Random number generation with NumPy
When you import `numpy` in your python script, an RNG is created behind the scenes. This RNG is the one used when you generate a new random value using a function such as `np.random.random`. I will here refer to this RNG as the global NumPy RNG.

Although not recommended, it is a common practice to reset the seed of this global RNG at the beginning of a script using the `np.random.seed` function. Fixing the seed at the beginning ensures that the script is reproducible: the same values and results will be produced each time you run it. However, although sometimes convenient, using the global NumPy RNG is considered a bad practice. A simple reason is that using global variables can lead to undesired side effects. For instance one might use `np.random.random` without knowing that the seed of the global RNG was set somewhere else in the codebase. Quoting [Numpy Enhancement Proposal (NEP) 19](https://numpy.org/neps/nep-0019-rng-policy.html) by Robert Kern:

> The implicit global RandomState behind the `np.random.*` convenience functions can cause problems, especially when threads or other forms of concurrency are involved. Global state is always problematic. We categorically recommend avoiding using the convenience functions when reproducibility is involved. [...] The preferred best practice for getting reproducible pseudorandom numbers is to instantiate a generator object with a seed and pass it around.

In short:
* Instead of using `np.random.seed`, which reseeds the already created global NumPy RNG, and then using `np.random.*` functions, you should create a new RNG.
* You should create an RNG at the beginning of your script (with a seed, if you want reproducibility) and use this RNG in the rest of the script.

To create a new RNG you can use the `default_rng` function as illustrated in the [introduction of the random module documentation](https://numpy.org/doc/stable/reference/random/index.html):

```python
import numpy as np

rng = np.random.default_rng()
rng.random()  # generate a floating point number between 0 and 1
```

If you want to use a seed for reproducibility, [the NumPy documentation recommends](https://numpy.org/doc/stable/reference/random/index.html#quick-start) using a very large and unique number to have a different seed than anyone else. Another reason is that using a small number for the seed could lead to a bad initialization of the RNG, although `default_rng` now takes care of creating a good initialization from a small number. To obtain a good, unique seed you can rely on the [secrets module](https://docs.python.org/3/library/secrets.html). The following code will return a 128 bit number that you can then use as a seed:

```python
import secrets

secrets.randbits(128)
```

When running this code I get `65647437836358831880808032086803839626` for the number to use as my seed. This number is randomly generated so you need to copy paste the value that is returned by `secrets.randbits(128)` otherwise you will have a different seed each time you run your code and thus break reproducibility:

```python
import numpy as np

seed = 65647437836358831880808032086803839626
rng = np.random.default_rng(seed)
rng.random()
```

The reason for seeding your RNG only once (and passing that RNG around) is that you can lose on the randomness and the independence of the generated random numbers by reseeding the RNG multiple times. Furthermore obtaining a good seed can be time consuming. Once you have a good seed to instantiate your generator, you might as well use it. With a good RNG such as the one returned by `default_rng` you will be ensured good randomness (and independence) of the generated numbers. It might be more dangerous to use generators derived from different seeds: how do you know that the streams of random numbers obtained from those are not correlated or, I should say, less independent than the ones created from the same seed? That being said, [as explained by Robert Kern](https://github.com/numpy/numpy/issues/15322#issuecomment-573890207), with the RNGs and seeding strategies introduced in NumPy 1.17, it is considered fairly safe to create RNGs using system entropy, i.e. using `default_rng(None)` multiple times. However as explained later be careful when running jobs in parallel and relying on `default_rng(None)`.


## Passing a NumPy RNG around

As you write functions that you will use on their own as well as in a more complex script it is convenient to be able to pass a seed or your already created RNG. The function `default_rng` allows you to do this very easily. As written above, this function can be used to create a new RNG from your chosen seed, if you pass a seed to it, or from system entropy when passing `None` but you can also pass an already created RNG. In this case the returned RNG is the one that you passed.

```python
import numpy as np


def stochastic_function(seed, high=10):
    rng = np.random.default_rng(seed)
    return rng.integers(high, size=5)
```
You can either pass an `int` seed or your already created RNG to `stochastic_function`. To be perfectly exact, the `default_rng` function returns the exact same RNG passed to it for certain kind of RNGs such at the ones created with `default_rng` itself. You can refer to the [`default_rng` documentation](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.default_rng) for more details on the arguments that you can pass to this function.

Before knowing about `default_rng`, and before NumPy 1.17, I was using the scikit-learn function [`check_random_state`](https://scikit-learn.org/stable/modules/generated/sklearn.utils.check_random_state.html) which is of course heavily used in the scikit-learn codebase. While writing this post I discovered that this function is now available in [scipy](https://github.com/scipy/scipy/blob/master/scipy/_lib/_util.py#L171). A look at the docstring and/or the source code of this function will give you a good idea about what it does. The differences with `default_rng` are that `check_random_state` currently relies on `np.random.RandomState` and that when `None` is passed to `check_random_state` then the function returns the already existing global NumPy RNG. The latter can be convenient because if you fix the seed of the global RNG before in your script using `np.random.seed`, `check_random_state` returns the generator that you seeded. However, as explained above, this is not the recommended practice and you should be aware of the risks and the side effects.

## Parallel processing

You must be careful when using RNGs in conjunction with parallel processing. I usually use the [joblib](https://joblib.readthedocs.io/en/latest/) library to parallelize my code and I will therefore mainly talk about it. However most of the discussion is not specific to joblib.

Let's consider the context of Monte Carlo simulation: you have a random function returning random outputs and you want to generate these random outputs a lot of times, for instance to compute an empirical mean. If the function is expensive to compute an easy solution to speed up the computation time is to resort to parallel processing. Depending on the parallel processing library or backend that you use different behaviors can be observed. For instance if you do not set the seed yourself it can be the case that forked Python processes use the same random seed, generated for instance from system entropy, and thus produce the exact same outputs which is a waste of computational resources. I learned this the hard way during my PhD. A very nice example illustrating this and other behaviors that one can obtain with joblib is available [here](https://joblib.readthedocs.io/en/latest/auto_examples/parallel_random_state.html).

If you fix the seed at the beginning of your main script for reproducibility and then pass the same RNG to each process to be run in parallel, most of the time this will not give you what you want as this RNG will be deep copied. The same results will thus be produced by each process. One of the solutions is to create as many RNGs as parallel processes with a different seed for each of these RNGs. The issue now is that you cannot choose the seeds as easily as you would think. When you choose two different seeds to instantiate two different RNGs how do you know that the numbers produced by these RNGs will appear as statistically independent? The design of independent RNGs for parallel processes has been an important research question. See, for example, [Random numbers for parallel computers: Requirements and methods, with emphasis on GPUs](https://www.sciencedirect.com/science/article/pii/S0378475416300829) by L'Ecuyer et al. (2017) for a good summary of different methods.

Starting with NumPy 1.17, it is now very easy to instantiate independent RNGs. Depending on the type of RNG you use, different strategies are available as documented in the [Parallel random number generation section](https://numpy.org/doc/stable/reference/random/parallel.html) of the NumPy documentation. One of the strategies is to use `SeedSequence` which is an algorithm that makes sure that poor input seeds are transformed into good initial RNG states. Additionally, it ensures that close seeds are mapped to very different initial states, resulting in RNGs that are, with very high probability, independent of each other. You can refer to the documentation of [SeedSequence Spawning](https://numpy.org/doc/stable/reference/random/parallel.html#seedsequence-spawning) for an example on how to generate independent RNGs from a user-provided seed. I here show how you can do this from an already existing RNG and apply it to the [joblib example](https://joblib.readthedocs.io/en/latest/auto_examples/parallel_random_state.html#fixing-the-random-state-to-obtain-deterministic-results) mentioned above.


```python
import numpy as np
from joblib import Parallel, delayed


def stochastic_function(seed, high=10):
    rng = np.random.default_rng(seed)
    return rng.integers(high, size=5)


seed = 319929794527176038403653493598663843656
# create the RNG that you want to pass around
rng = np.random.default_rng(seed)
# get the SeedSequence of the passed RNG.
# WARNING: note that this is using a private attribute of
# the RNG and the API might change in the future.
ss = rng.bit_generator._seed_seq
# create 5 initial independent states
child_states = ss.spawn(5)

# use 2 processes to run the stochastic_function 5 times with joblib
random_vector = Parallel(n_jobs=2)(
    delayed(stochastic_function)(random_state) for random_state in child_states
)
print(random_vector)

# rerun to check that we obtain the same outputs
random_vector = Parallel(n_jobs=2)(
    delayed(stochastic_function)(random_state) for random_state in child_states
)
print(random_vector)
```

By using a fixed seed you always get the same results and by using `SeedSequence.spawn` you have an independent RNG for each of the iterations. Note that I used the convenient `default_rng` function in `stochastic_function`. You can also see that the `SeedSequence` of the existing RNG is a private attribute. Accessing the `SeedSequence` might become easier in future versions of NumPy (more information [here](https://github.com/numpy/numpy/issues/15322#issuecomment-626400433)).

## Resources

### Numpy RNGs
* [The documentation of the NumPy random module](https://numpy.org/doc/stable/reference/random/index.html) is the best place to find information and where I found most of the information that I share here.
* [The Numpy Enhancement Proposal (NEP) 19 on the Random Number Generator Policy](https://numpy.org/neps/nep-0019-rng-policy.html) which lead to the changes introduced in NumPy 1.17
* A [NumPy issue](https://github.com/numpy/numpy/issues/15322) about the `check_random_state` function and RNG good practices, especially [this comment](https://github.com/numpy/numpy/issues/15322#issuecomment-573890207) by Robert Kern.
* [How do I set a random_state for an entire execution?](https://scikit-learn.org/stable/faq.html#how-do-i-set-a-random-state-for-an-entire-execution) from the scikit-learn FAQ.
* There are [ongoing discussions](https://github.com/scientific-python/specs/pull/180) about uniformizing the APIs used by different libraries to seed RNGs.

### RNGs in general
* [Random numbers for parallel computers: Requirements and methods, with emphasis on GPUs](https://www.sciencedirect.com/science/article/pii/S0378475416300829) by L'Ecuyer et al. (2017)
* To know more about the default RNG used in NumPy, named PCG, I recommend the [PCG paper](https://www.pcg-random.org/paper.html) which also contains lots of useful information about RNGs in general. The [pcg-random.org website](https://www.pcg-random.org) is also full of interesting information about RNGs.
