---
title: "Pytrees for Scientific Python"
date: 2025-05-14T10:27:59-07:00
draft: false
description: "
Introducing PyTrees for Scientific Python. We discuss what PyTrees are, how they're useful in the realm of scientific Python, and how to work _efficiently_ with them.
"
tags: ["PyTrees", "Functional Programming", "Tree-like data manipulation"]
displayInList: true
author: ["Peter Fackeldey", "Mihai Maruseac", "Matthew Feickert"]
summary: |
  This blog introduces PyTrees &mdash; nested Python data structures (such as lists, dicts, and tuples) with numerical leaf values &mdash; designed to simplify working with complex, hierarchically organized data.
  While such structures are often cumbersome to manipulate, PyTrees make them more manageable by allowing them to be flattened into a list of leaves along with a reusable structure blueprint in a _generic_ way.
  This enables flexible, generic operations like mapping and reducing from functional programming.
  By bringing those functional paradigms to structured data, PyTrees let you focus on what transformations to apply, not how to traverse the structure &mdash; no matter how deeply nested or complex it is.
---

## Manipulating Tree-like Data using Functional Programming Paradigms

A "PyTree" is a nested collection of Python containers (e.g. dicts, (named) tuples, lists, ...), where the leaves are of interest.
In the scientific world, such a PyTree could consist of experimental measurements of different properties at different timestamps and measurement settings resulting in a highly complex, nested and not necessarily rectangular data structure.
Such collections can be cumbersome to manipulate _efficiently_, especially if they are nested any depth.
It often requires complex recursive logic which usually does not generalize to other nested Python containers (PyTrees), e.g. for new measurements.

The core concept of PyTrees is being able to flatten them into a flat collection of leaves and a "blueprint" of the tree structure, and then being able to unflatten them back into the original PyTree.
This allows for the application of generic transformations.
In this blog post, we use [`optree`](https://github.com/metaopt/optree/tree/main/optree) &mdash; a standalone PyTree library &mdash; that enables these transformations. It focuses on performance, is feature rich, has minimal dependencies, and has been adopted by [PyTorch](https://pytorch.org), [Keras](https://keras.io), and [TensorFlow](https://github.com/tensorflow/tensorflow) (through Keras) as a core dependency.
For example, on a PyTree with NumPy arrays as leaves, taking the square root of each leaf with `optree.tree_map(np.sqrt, tree)`:

```python
import optree as pt
import numpy as np

# tuple of a list of a dict with an array as value, and an array
tree = ([[{"foo": np.array([4.0])}], np.array([9.0])],)

# sqrt of each leaf array
sqrt_tree = pt.tree_map(np.sqrt, tree)
print(f"{sqrt_tree=}")
# >> sqrt_tree=([[{'foo': array([2.])}], array([3.])],)

# reductions
all_positive = all(np.all(x > 0.0) for x in pt.tree_iter(tree))
print(f"{all_positive=}")
# >> all_positive=True

summed = np.sum(pt.tree_reduce(sum, tree))
print(f"{summed=}")
# >> summed=np.float64(13.0)
```

The trick here is that these operations can be implemented in three steps, e.g. `tree_map`:

```python
# step 1:
leaves, treedef = pt.tree_flatten(tree)

# step 2:
new_leaves = tuple(map(fun, leaves))

# step 3:
result_tree = pt.tree_unflatten(treedef, new_leaves)
```

### PyTree Origins

Originally, the concept of PyTrees was developed by the [JAX](https://docs.jax.dev/en/latest/) project to make nested collections of JAX arrays work transparently at the "JIT-boundary" (the JAX JIT toolchain does not know about Python containers, only about JAX Arrays).
However, PyTrees were quickly adopted by AI researchers for broader use-cases: semantically grouping layers of weights and biases in a list of named tuples (or dictionaries) is a common pattern in the JAX-AI-world, as shown in the following (pseudo) Python snippet:

```python
from typing import NamedTuple, Callable
import jax
import jax.numpy as jnp


class Layer(NamedTuple):
    W: jax.Array
    b: jax.Array


layers = [
    Layer(W=jnp.array(...), b=jnp.array(...)),  # first layer
    Layer(W=jnp.array(...), b=jnp.array(...)),  # second layer
    ...,
]


@jax.jit
def neural_network(layers: list[Layer], x: jax.Array) -> jax.Array:
    for layer in layers:
        x = jnp.tanh(layer.W @ x + layer.b)
    return x


prediction = neural_network(layers=layers, x=jnp.array(...))
```

Here, `layers` is a PyTree &mdash; a `list` of multiple `Layer` &mdash; and the JIT compiled `neural_network` function _just works_ with this data structure as input.

### PyTrees in Scientific Python

Wouldn't it be nice to make workflows in the scientific Python ecosystem _just work_ with any PyTree?

Giving semantic meaning to numeric data through PyTrees can be useful for applications outside of AI as well.
Consider the following minimization of the [Rosenbrock](https://en.wikipedia.org/wiki/Rosenbrock_function) function:

```python
from scipy.optimize import minimize


def rosenbrock(params: tuple[float]) -> float:
    """
    Rosenbrock function. Minimum: f(1, 1) = 0.

    https://en.wikipedia.org/wiki/Rosenbrock_function
    """
    x, y = params
    return (1 - x) ** 2 + 100 * (y - x**2) ** 2


x0 = (0.9, 1.2)
res = minimize(rosenbrock, x0)
print(res.x)
# >> [0.99999569 0.99999137]
```

Now, let's consider a minimization that uses a more complex type for the parameters &mdash; a NamedTuple that describes our fit parameters:

```python
import optree as pt
from typing import NamedTuple, Callable
from scipy.optimize import minimize as sp_minimize


class Params(NamedTuple):
    x: float
    y: float


def rosenbrock(params: Params) -> float:
    """
    Rosenbrock function. Minimum: f(1, 1) = 0.

    https://en.wikipedia.org/wiki/Rosenbrock_function
    """
    return (1 - params.x) ** 2 + 100 * (params.y - params.x**2) ** 2


def minimize(fun: Callable, params: Params) -> Params:
    # flatten and store PyTree definition
    flat_params, treedef = pt.tree_flatten(params)

    # wrap fun to work with flat_params
    def wrapped_fun(flat_params):
        params = pt.tree_unflatten(treedef, flat_params)
        return fun(params)

    # actual minimization
    res = sp_minimize(wrapped_fun, flat_params)

    # re-wrap the bestfit values into Params with stored PyTree definition
    return pt.tree_unflatten(treedef, res.x)


# scipy minimize that works with any PyTree
x0 = Params(x=0.9, y=1.2)
bestfit_params = minimize(rosenbrock, x0)
print(bestfit_params)
# >> Params(x=np.float64(0.999995688776513), y=np.float64(0.9999913673387226))
```

This new `minimize` function works with _any_ PyTree!

Let's now consider a modified and more complex version of the Rosenbrock function that relies on two sets of `Params` as input &mdash; a common pattern for hierarchical models (e.g. a superposition of various probability density functions):

```python
import numpy as np


def rosenbrock_modified(two_params: tuple[Params, Params]) -> float:
    """
    Modified Rosenbrock where the x and y parameters are determined by
    a non-linear transformations of two versions of each, i.e.:
      x = arcsin(min(x1, x2) / max(x1, x2))
      y = sigmoid(x1 - x2)
    """
    p1, p2 = two_params

    # calculate `x` and `y` from two sources:
    x = np.asin(min(p1.x, p2.x) / max(p1.x, p2.x))
    y = 1 / (1 + np.exp(-(p1.y / p2.y)))

    return (1 - x) ** 2 + 100 * (y - x**2) ** 2


x0 = (Params(x=0.9, y=1.2), Params(x=0.8, y=1.3))
bestfit_params = minimize(rosenbrock_modified, x0)
print(bestfit_params)
# >> (
#     Params(x=np.float64(4.686181110201706), y=np.float64(0.05129869722505759)),
#     Params(x=np.float64(3.9432263101976073), y=np.float64(0.005146110126174016)),
# )
```

The new `minimize` still works, because a `tuple` of `Params` is just _another_ PyTree!

### Final Thought

Working with nested data structures doesn’t have to be messy.
PyTrees let you focus on the data and the transformations you want to apply, in a generic manner.
Whether you're building neural networks, optimizing scientific models, or just dealing with complex nested Python containers, PyTrees can make your code cleaner, more flexible, and just nicer to work with.
