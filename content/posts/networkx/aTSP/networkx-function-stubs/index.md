---
title: "NetworkX Function Stubs"
date: 2021-05-24
draft: false
description: "Draft function stubs for the Asadpour method to use in the NetworkX API"
tags: ["gsoc", "networkx", "traveling-salesman-problem"]
displayInList: true
author: ["mjschwenne"]

resources:
  - name: featuredImage
    src: "mjschwenne_GSoc.png"
    params:
      description: "Google Summer of Code Logo with NetworkX logo"
      showOnTop: true
---

Now that my proposal was accepted by NetworkX for the 2021 Google Summer of Code (GSoC), I can get more into the technical details of how I plan to implement the Asadpour algorithm within NetworkX.

In this post I am going to outline my thought process for the control scheme of my implementation and create function stubs according to my GSoC proposal.
Most of the work for this project will happen in `netowrkx.algorithms.approximation.traveling_salesman.py`, where I will finish the last algorithm for the Traveling Salesman Problem so it can be merged into the project. The main function in `traveling_salesman.py` is

```python
def traveling_salesman_problem(G, weight="weight", nodes=None, cycle=True, method=None):
    """
    ...

    Parameters
    ----------
    G : NetworkX graph
        Undirected possibly weighted graph

    nodes : collection of nodes (default=G.nodes)
        collection (list, set, etc.) of nodes to visit

    weight : string, optional (default="weight")
        Edge data key corresponding to the edge weight.
        If any edge does not have this attribute the weight is set to 1.

    cycle : bool (default: True)
        Indicates whether a cycle should be returned, or a path.
        Note: the cycle is the approximate minimal cycle.
        The path simply removes the biggest edge in that cycle.

    method : function (default: None)
        A function that returns a cycle on all nodes and approximates
        the solution to the traveling salesman problem on a complete
        graph. The returned cycle is then used to find a corresponding
        solution on `G`. `method` should be callable; take inputs
        `G`, and `weight`; and return a list of nodes along the cycle.

        Provided options include :func:`christofides`, :func:`greedy_tsp`,
        :func:`simulated_annealing_tsp` and :func:`threshold_accepting_tsp`.

        If `method is None`: use :func:`christofides` for undirected `G` and
        :func:`threshold_accepting_tsp` for directed `G`.

        To specify parameters for these provided functions, construct lambda
        functions that state the specific value. `method` must have 2 inputs.
        (See examples).

    ...
    """
```

All user calls to find an approximation to the traveling salesman problem will go through this function.
My implementation of the Asadpour algorithm will also need to be compatible with this function.
`traveling_salesman_problem` will handle creating a new, complete graph using the weight of the shortest path between nodes $u$ and $v$ as the weight of that arc, so we know that by the time the graph is passed to the Asadpour algorithm it is a complete digraph which satisfies the triangle inequality.
The main function also handles the `nodes` and `cycles` parameters by only copying the necessary nodes into the complete digraph before calling the requested method and afterwards searching for and removing the largest arc within the returned cycle.
Thus, the parent function for the Asadpour algorithm only needs to deal with the graph itself and the weights or costs of the arcs in the graph.

My controlling function will have the following signature and I have included a draft of the docstring as well.

```python
def asadpour_tsp(G, weight="weight"):
    """
    Returns an O( log n / log log n ) approximate solution to the traveling
    salesman problem.

    This approximate solution is one of the best known approximations for
    the asymmetric traveling salesman problem developed by Asadpour et al,
    [1]_. The algorithm first solves the Held-Karp relaxation to find a
    lower bound for the weight of the cycle. Next, it constructs an
    exponential distribution of undirected spanning trees where the
    probability of an edge being in the tree corresponds to the weight of
    that edge using a maximum entropy rounding scheme. Next we sample that
    distribution $2 \\\\\\log n$ times and saves the minimum sampled tree once
    the direction of the arcs is added back to the edges. Finally,
    we argument then short circuit that graph to find the approximate tour
    for the salesman.

    Parameters
    ----------
    G : nx.DiGraph
        The graph should be a complete weighted directed graph.
        The distance between all pairs of nodes should be included.

    weight : string, optional (default="weight")
        Edge data key corresponding to the edge weight.
        If any edge does not have this attribute the weight is set to 1.

    Returns
    -------
    cycle : list of nodes
        Returns the cycle (list of nodes) that a salesman can follow to minimize
        the total weight of the trip.

    Raises
    ------
    NetworkXError
        If `G` is not complete, the algorithm raises an exception.

    References
    ----------
    .. [1] A. Asadpour, M. X. Goemans, A. Madry, S. O. Gharan, and A. Saberi,
       An o(log n/log log n)-approximation algorithm for the asymmetric
       traveling salesman problem, Operations research, 65 (2017),
       pp. 1043–1061
    """
    pass
```

Following my GSoC proposal, the next function is `held_karp`, which will solve the Held-Karp relaxation on the complete digraph using the ellipsoid method (See my last two posts [here]({{< relref "held-karp-relaxation" >}}) and [here]({{< relref "held-karp-separation-oracle" >}}) for my thoughts on why and how to accomplish this).
Solving the Held-Karp relaxation is the first step in the algorithm.

Recall that the Held-Karp relaxation is defined as the following linear program:

$$
\begin{array}{c l l}
\text{min} & \sum_{a} c(a)x_a \\\\\\
\text{s.t.} & x(\delta^+(U)) \geqslant 1 & \forall\ U \subset V \text{ and } U \not= \emptyset \\\\\\
& x(\delta^+(v)) = x(\delta^-(v)) = 1 & \forall\ v \in V \\\\\\
& x_a \geqslant 0 & \forall\ a
\end{array}
$$

and that it is a semi-infinite program so it is too large to be solved in conventional forms.
The algorithm uses the solution to the Held-Karp relaxation to create a vector $z^\*$ which is a symmetrized and slightly scaled down version of the true Held-Karp solution $x^\*$.
$z^\*$ is defined as

$$
z^\*\_{\{u, v\}} = \frac{n - 1}{n} \left(x^\*\_{uv} + x^\*\_{vu}\right)
$$

and since this is what the algorithm using to build the rest of the approximation, this should be one of the return values from `held_karp`.
I will also return the value of the cost of $x^\*$, which is denoted as $c(x^\*)$ or $OPT\_{HK}$ in the Asadpour paper [1].

Additionally, the separation oracle will be defined as an inner function within `held_karp`.
At the present moment I am not sure what the exact parameters for the separation oracle, `sep_oracle`, but it should be the the point the algorithm wishes to test and will need to access the graph the algorithm is relaxing.
In particular, I'm not sure _yet_ how I will represent the hyperplane which is returned by the separation oracle.

```python
def _held_karp(G, weight="weight"):
    """
    Solves the Held-Karp relaxation of the input complete digraph and scales
    the output solution for use in the Asadpour [1]_ ASTP algorithm.

    The Held-Karp relaxation defines the lower bound for solutions to the
    ATSP, although it does return a fractional solution. This is used in the
    Asadpour algorithm as an initial solution which is later rounded to a
    integral tree within the spanning tree polytopes. This function solves
    the relaxation with the ellipsoid method for linear programs.

    Parameters
    ----------
    G : nx.DiGraph
        The graph should be a complete weighted directed graph.
        The distance between all paris of nodes should be included.

    weight : string, optional (default="weight")
        Edge data key corresponding to the edge weight.
        If any edge does not have this attribute the weight is set to 1.

    Returns
    -------
    OPT : float
        The cost for the optimal solution to the Held-Karp relaxation
    z_star : numpy array
        A symmetrized and scaled version of the optimal solution to the
        Held-Karp relaxation for use in the Asadpour algorithm

    References
    ----------
    .. [1] A. Asadpour, M. X. Goemans, A. Madry, S. O. Gharan, and A. Saberi,
       An o(log n/log log n)-approximation algorithm for the asymmetric
       traveling salesman problem, Operations research, 65 (2017),
       pp. 1043–1061
    """

    def sep_oracle(point):
        """
        The separation oracle used in the ellipsoid algorithm to solve the
        Held-Karp relaxation.

        This 'black-box' takes a point and check to see if it violates any
        of the Held-Karp constraints, which are defined as

            - The out-degree of all non-empty subsets of $V$ is at lest one.
            - The in-degree and out-degree of each vertex in $V$ is equal to
              one. Note that if a vertex has more than one incoming or
              outgoing arcs the values of each could be less than one so long
              as they sum to one.
            - The current value for each arc is greater
              than zero.

        Parameters
        ----------
        point : numpy array
            The point in n dimensional space we will to test to see if it
            violations any of the Held-Karp constraints.

        Returns
        -------
        numpy array
            The hyperplane which was the most violated by `point`, i.e the
            hyperplane defining the polytope of spanning trees which `point`
            was farthest from, None if no constraints are violated.
        """
        pass

    pass
```

Next the algorithm uses the symmetrized and scaled version of the Held-Karp solution to construct an exponential distribution of undirected spanning trees which preserves the marginal probabilities.

```python
def _spanning_tree_distribution(z_star):
    """
    Solves the Maximum Entropy Convex Program in the Asadpour algorithm [1]_
    using the approach in section 7 to build an exponential distribution of
    undirected spanning trees.

    This algorithm ensures that the probability of any edge in a spanning
    tree is proportional to the sum of the probabilities of the trees
    containing that edge over the sum of the probabilities of all spanning
    trees of the graph.

    Parameters
    ----------
    z_star : numpy array
        The output of `_held_karp()`, a scaled version of the Held-Karp
        solution.

    Returns
    -------
    gamma : numpy array
        The probability distribution which approximately preserves the marginal
        probabilities of `z_star`.
    """
    pass
```

Now that the algorithm has the distribution of spanning trees, we need to sample them.
Each sampled tree is a $\lambda$-random tree and can be sampled using algorithm A8 in [2].

```python
def _sample_spanning_tree(G, gamma):
    """
    Sample one spanning tree from the distribution defined by `gamma`,
    roughly using algorithm A8 in [1]_ .

    We 'shuffle' the edges in the graph, and then probabilistically
    determine whether to add the edge conditioned on all of the previous
    edges which were added to the tree. Probabilities are calculated using
    Kirchhoff's Matrix Tree Theorem and a weighted Laplacian matrix.

    Parameters
    ----------
    G : nx.Graph
        An undirected version of the original graph.

    gamma : numpy array
        The probabilities associated with each of the edges in the undirected
        graph `G`.

    Returns
    -------
    nx.Graph
        A spanning tree using the distribution defined by `gamma`.

    References
    ----------
    .. [1] V. Kulkarni, Generating random combinatorial objects, Journal of
       algorithms, 11 (1990), pp. 185–207
    """
    pass
```

At this point there is only one function left to discuss, `laplacian_matrix`.
This function already exists within NetworkX at `networkx.linalg.laplacianmatrix.laplacian_matrix`, and even though this is relatively simple to implement, I'd rather use an existing version than create duplicate code within the project.
A deeper look at the function signature reveals

```python
@not_implemented_for("directed")
def laplacian_matrix(G, nodelist=None, weight="weight"):
    """Returns the Laplacian matrix of G.

    The graph Laplacian is the matrix L = D - A, where
    A is the adjacency matrix and D is the diagonal matrix of node degrees.

    Parameters
    ----------
    G : graph
       A NetworkX graph

    nodelist : list, optional
       The rows and columns are ordered according to the nodes in nodelist.
       If nodelist is None, then the ordering is produced by G.nodes().

    weight : string or None, optional (default='weight')
       The edge data key used to compute each value in the matrix.
       If None, then each edge has weight 1.

    Returns
    -------
    L : SciPy sparse matrix
      The Laplacian matrix of G.

    Notes
    -----
    For MultiGraph/MultiDiGraph, the edges weights are summed.

    See Also
    --------
    to_numpy_array
    normalized_laplacian_matrix
    laplacian_spectrum
    """
```

Which is exactly what I need, _except_ the decorator states that it does not support directed graphs and this algorithm deals with those types of graphs.
Fortunately, our distribution of spanning trees is for trees in a directed graph _once the direction is disregarded_, so we can actually use the existing function.
The definition given in the Asadpour paper [1], is

$$
L\_{i,j} = \left\\{
\begin{array}{l l}
-\lambda\_e & e = (i, j) \in E \\\\\\
\sum\_{e \in \delta(\{i\})} \lambda\_e & i = j \\\\\\
0 & \text{otherwise}
\end{array}
\right.
$$

Where $E$ is defined as "Let $E$ be the support of graph of $z^\*$ when the direction of the arcs are disregarded" on page 5 of the Asadpour paper.
Thus, I can use the existing method without having to create a new one, which will save time and effort on this GSoC project.

In addition to being discussed here, these function stubs have been added to my fork of `NetworkX` on the `bothTSP` branch.
The commit, [`Added function stubs and draft docstrings for the Asadpour algorithm`](https://github.com/mjschwenne/networkx/commit/d3a3db8823804faa3edbf8bfa0f4b12459143ac8) is visible on my GitHub using that link.

## References

[1] A. Asadpour, M. X. Goemans, A. Mardry, S. O. Ghran, and A. Saberi, _An o(log n / log log n)-approximation algorithm for the asymmetric traveling salesman problem_, Operations Research, 65 (2017), pp. 1043-1061, [https://homes.cs.washington.edu/~shayan/atsp.pdf](https://homes.cs.washington.edu/~shayan/atsp.pdf).

[2] V. Kulkarni, _Generating random combinatorial objects_, Journal of algorithms, 11 (1990), pp. 185–207
