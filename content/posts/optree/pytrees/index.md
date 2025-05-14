---
title: "Pytrees for Scientific Python"
date: 2025-05-14T10:27:59-07:00
draft: false
description: "
Introducing PyTrees for Scientific Python. We discuss what PyTrees are, how they're useful in the realm of scientific python, and how to work _efficiently_ with them.
"
tags: ["PyTrees", "Functional Programming", "Tree-like data manipulation"]
displayInList: true
author: ["Peter Fackeldey", "Mihai Maruseac", "Matthew Feickert"]
---

### Manipulating tree-like data using functional programming paradigms

A "PyTree" is a nested collection of python containers (e.g. dicts, (named) tuples, lists, ...), where the leafs are of interest.
As you can imagine (or even experienced in the past), these arbitrary nested collections can become cumbersome to manipulate _efficiently_.
Often this requires complex recursive logic, and which usually does not generalize to other PyTree structures.

#### PyTree Origins

Originally, the concept of PyTrees was developed by the [JAX](https://docs.jax.dev/en/latest/) project to make nested collections of JAX arrays work transparently at the "JIT-boundary".
This was quickly adopted by AI researchers: semantically grouping layers of weights and biases in e.g. a list of named tuples (or dictionaries) is a common pattern in the JAX-AI-world, see the following pseudo-code:

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


pred = neural_network(layers=layers, x=jnp.array(...))
```

Here, `layers` is a PyTree - a `list` of multiple `Layer` - and the JIT compiled `neural_network` function _just works_ with this datastructure as input.

#### PyTrees in Scientific Python

Wouldn't it be nice to make workflows in the scientific python ecosystem _just work_ with any PyTree?
Enabling semantic meaning through PyTrees can be useful for applications outside of AI as well.
Consider the following minimization of the [Rosenbrock](https://en.wikipedia.org/wiki/Rosenbrock_function) function:

```Python
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
>> [0.99999569 0.99999137]
```

Now, let's turn it a minimization that uses a more complex type for the parameters - a NamedTuple that describes our fit parameters:

```Python
import optree as pt  # standalone PyTree library
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
    flat_params, PyTreeDef = pt.tree_flatten(params)

    # wrap fun to work with flat_params
    def wrapped_fun(flat_params):
    params = pt.tree_unflatten(PyTreeDef, flat_params)
    return fun(params)

    # actual minimization
    res = sp_minimize(wrapped_fun, flat_params)

    # re-wrap the bestfit values into Params with stored PyTree definition
    return pt.tree_unflatten(PyTreeDef, res.x)


# scipy minimize that works with any PyTree
x0 = Params(x=0.9, y=1.2)
bestfit_params = minimize(rosenbrock, x0)
print(bestfit_params)
>> Params(x=np.float64(0.999995688776513), y=np.float64(0.9999913673387226))
```

This new `minimize` function works with _any_ PyTree, e.g.:

```python
import numpy as np


def rosenbrock_modified(params: Params) -> float:
    """
    Modified Rosenbrock where the x and y parameters are determined by
    a non-linear transformations of two versions of each, i.e.:
      x = arcsin(min(x1, x2) / max(x1, x2))
      y = sigmoid(x1 - x2)
    """
    p1, p2 = params
    x = np.asin(min(p1.x, p2.x) / max(p1.x, p2.x))
    y = 1.0 / (1.0 + np.exp(-(p1.y / p2.y)))
    return (1 - x) ** 2 + 100 * (y - x**2) ** 2


x0 = (Params(x=0.9, y=1.2), Params(x=0.8, y=1.3))
bestfit_params = minimize(rosenbrock_modified, x0)
print(bestfit_params)
# >> (
#     Params(x=np.float64(4.686181110201706), y=np.float64(0.05129869722505759)),
#     Params(x=np.float64(3.9432263101976073), y=np.float64(0.005146110126174016)),
# )
```
