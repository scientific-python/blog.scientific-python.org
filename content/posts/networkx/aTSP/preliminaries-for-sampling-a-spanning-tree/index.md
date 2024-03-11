---
title: "Preliminaries for Sampling a Spanning Tree"
date: 2021-07-21
draft: false
description: "A close examination of the mathematics required to sample a random spanning tree from a graph"
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

In order to test the exponential distribution that I generate using `spanning_tree_distribution`, I need to be able to sample a tree from the distribution.
The primary citation used in the Asadpour paper is _Generating Random Combinatorial Objects_ by V. G. Kulkarni (1989).
While I was not able to find an online copy of this article, the Michigan Tech library did have a copy that I was able to read.

## Does the Kulkarni Algorithm work with Asadpour?

Kulkarni gave a general overview of the algorithm in Section 2, but Section 5 is titled `Random Spanning Trees' and starts on page 200.
First, let's check that the preliminaries for the Kulkarni paper on page 200 match the Asadpour algorithm.

> Let \\(G = (V, E)\\) be an undirected network of \\(M\\) nodes and \\(N\\) arcs...
> Let \\(\mathfrak{B}\\) be the set of all spanning trees in \\(G\\).
> Let \\(\alpha_i\\) be the positive weight of arc \\(i \in E\\).
> Defined the weight \\(w(B)\\) of a spanning tree \\(B \in \mathfrak{B}\\) as
>
> \\[w(B) = \prod\_{i \in B} \alpha\_i\\]
>
> Also define
>
> \\[n(G) = \sum\_{B \in \mathfrak{B}} w(B)\\]
>
> In this section we describe an algorithm to generate \\(B \in \mathfrak{B}\\) so that
>
> \\[P\\{B \text{ is generated}\\} = \frac{w(B)}{n(G)}\\]

Immediately we can see that \\(\mathfrak{B}\\) is the same as \\(\mathcal{T}\\) from the Asadpour paper, the set of all spanning trees.
The weight of each edge is \\(\alpha_i\\) for Kulkarni and \\(\lambda_e\\) to Asadpour.
As for the product of the weights of the graph being the probability, the Asadpour paper states on page 382

> Given \\(\lambda*e \geq 0\\) for \\(e \in E\\), a \\(\lambda\\)*-random tree\_ \\(T\\) of \\(G\\) is a tree \\(T\\) chosen from the set of all spanning trees of \\(G\\) with probability proportional to \\(\prod\_{e \in T} \lambda_e\\).

So this is not a concern.
Finally, \\(n(G)\\) can be written as

\\[\sum\_{T \in \mathcal{T}} \prod\_{e \in T} \lambda\_e\\]

which does appear several times throughout the Asadpour paper.
Thus the preliminaries between the Kulkarni and Asadpour papers align.

## The Kulkarni Algorithm

The specialized version of the general algorithm which Kulkarni gives is Algorithm A8 on page 202.

> \\(U = \emptyset,\\) \\(V = E\\)\
> Do \\(i = 1\\) to \\(N\\);\
> \\(\qquad\\)Let \\(a = n(G(U, V))\\)\
> \\(\qquad\qquad a'\\) \\(= n(G(U \cup \{i\}, V))\\)\
> \\(\qquad\\)Generate \\(Z \sim U[0, 1]\\)\
> \\(\qquad\\)If \\(Z \leq \alpha_i \times \left(a' / a\right)\\)\
> \\(\qquad\qquad\\)then \\(U = U \cup \{i\}\\),\
> \\(\qquad\qquad\\)else \\(V = V - \{i\}\\)\
> \\(\qquad\\)end.\
> Stop. \\(U\\) is the required spanning tree.

Now we have to understand this algorithm so we can create pseudo code for it.
First as a notational explanation, the statement "Generate \\(Z \sim U[0, 1]\\)" means picking a uniformly random variable over the interval \\([0, 1]\\) which is independent of all the random variables generated before it (See page 188 of Kulkarni for more information).
The built-in python module [`random`](https://docs.python.org/3/library/random.html) can be used here.
Looking at real-valued distributions, I believe that using `random.uniform(0, 1)` is preferable to `random.random()` since the latter does not have the probability of generating a '1' and that is explicitly part of the interval discussed in the Kulkarni paper.

The other notational oddity would be statements similar to \\(G(U, V)\\) which is this case does not refer to a graph with \\(U\\) as the vertex set and \\(V\\) as the edge set as \\(U\\) and \\(V\\) are both subsets of the full edge set \\(E\\).

\\(G(U, V)\\) is defined in the Kulkarni paper on page 201 as

> Let \\(G(U, V)\\) be a subgraph of \\(G\\) obtained by deleting arcs that are not in \\(V\\), and collapsing arcs that are in \\(U\\) (i.e., identifying the end nodes of arcs in \\(U\\)) and deleting all self-loops resulting from these deletions and collapsing.

This language seems a bit... clunky, especially for the edges in \\(U\\).
In this case, "collapsing arcs that are in \\(U\\)" would be contracting those edges without self loops.
Fortunately, this functionality is a part of NetworkX using [`networkx.algorithms.minors.contracted_edge`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.minors.contracted_edge.html#networkx.algorithms.minors.contracted_edge) with the `self_loops` keyword argument set to `False`.

As for the edges in \\(E - V\\), this can be easily accomplished by using [`networkx.MultiGraph.remove_edges_from`](https://networkx.org/documentation/stable/reference/classes/generated/networkx.MultiGraph.remove_edges_from.html).

Once we have generated \\(G(U, V)\\), we need to find \\(n(G(U, V)\\).
This can be done with something we are already familiar with: Kirchhoff's Tree Matrix Theorem.
All we need to do is create the Laplacian matrix and then find the determinant of the first cofactor.
This code will probably be taken directly from the `spanning_tree_distribution` function.
Actually, this is a place to create a broader helper function called `krichhoffs` which will take a graph and return the number of weighted spanning trees in it which would then be used as part of `q` in `spanning_tree_distribution` and in `sample_spanning_tree`.

From here we compare \\(Z\\) to \\(\alpha_i \left(a' / a\right)\\) so see if that edge is added to the graph or discarded.
Understanding the process of the algorithm gives context to the meaning of \\(U\\) and \\(V\\).
\\(U\\) is the set of edges which we have decided to include in the spanning tree while \\(V\\) is the set of edges yet to be considered for \\(U\\) (roughly speaking).

Now there is still a bit of ambiguity in the algorithm that Kulkarni gives, mainly about \\(i\\).
In the loop condition, \\(i\\) is an integer from 1 to \\(N\\), the number of arcs in the graph but it is later being added to \\(U\\) so it has to be an edge.
Referencing the Asadpour paper, it starts its description of sampling the \\(\lambda\\)-random tree on page 383 by saying "The idea is to order the edges \\(e_1, \dots, e_m\\) of \\(G\\) arbitrarily and process them one by one".
So I believe that the edge interpretation is correct and the integer notation used in Kulkarni was assuming that a mapping of the edges to \\(\{1, 2, \dots, N\}\\) has occurred.

## sample_spanning_tree pseudo code

Time to write some pseudo code!
Starting with the function signature

```
def sample_spanning_tree
    Input: A multigraph G whose edges contain a lambda value stored at lambda_key
    Output: A new graph which is a spanning tree of G
```

Next up is a bit of initialization

```
    U = set()
    V = set(G.edges)
    shuffled_edges = shuffle(G.edges)
```

Now the definitions of `U` and `V` come directly from Algorithm A8, but `shuffled_edges` is new.
My thoughts are that this will be what we use for \\(i\\).
We shuffle the edges of the graph and then in the loop we iterate over the edges within `shuffled_edges`.
Next we have the loop.

```
    for edge e in shuffled_edges
        G_total_tree_weight = kirchhoffs(prepare_graph(G, U, V))
        G_i_total_tree_weight = kirchhoffs(prepare_graph(G, U.add(e), V))
        z = uniform(0, 1)
        if z <= e[lambda_key] * G_i_total_tree_weight / G_total_tree_weight
            U = U.add(e)
            if len(U) == G.number_of_edges - 1
                # Spanning tree complete, no need to continue to consider edges.
                spanning_tree = nx.Graph
                spanning_tree.add_edges_from(U)
                return spanning_tree
        else
            V = V.remove(e)
```

The main loop body does use two other functions which are not part of the standard NetworkX libraries, `krichhoffs` and `prepare_graph`.
As I mentioned before, `krichhoffs` will apply Krichhoff's Theorem to the graph.
Pseudo code for this is below and strongly based off of the existing code in `q` of `spanning_tree_distribution` which will be updated to use this new helper.

```
def krichhoffs
    Input: A multigraph G and weight key, weight
    Output: The total weight of the graph's spanning trees

    G_laplacian = laplacian_matrix(G, weight=weight)
    G_laplacian = G_laplacian.delete(0, 0)
    G_laplacian = G_laplacian.delete(0, 1)

    return det(G_laplacian)
```

The process for the other helper, `prepare_graph` is also given.

```
def prepare_graph
    Input: A graph G, set of contracted edges U and edges which are not removed V
    Output: A subgraph of G in which all vertices in U are contracted and edges not in V are
			removed

    result = G.copy
    edges_to_remove = set(result.edges).difference(V)
    result.remove_edges_from(edges_to_remove)

    for edge e in U
        nx.contracted_edge(e)

    return result
```

There is one other change to the NetworkX API that I would like to make.
At the moment, [`networkx.algorithms.minors.contracted_edge`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.minors.contracted_edge.html) is programmed to always return a copy of a graph.
Since I need to be contracting multiple edges at once, it would make a lot more sense to do the contraction in place.
I would like to add an optional keyword argument to `contracted_edge` called `copy` which will default to `True` so that the overall functionality will not change but I will be able to perform in place contractions.

## Next Steps

The most obvious one is to implement the functions that I have laid out in the pseudo code step, but testing is still a concerning area.
My best bet is to sample say 1000 trees and check that the probability of each tree is equal to the product of all of the lambda's on it's edges.

That actually just caused me to think of a new test of `spanning_tree_distribution`.
If I generate the distribution and then iterate over all of the spanning trees with a `SpanningTreeIterator` I can sum the total probability of each tree being sampled and if that is not 1 (or very close to it) than I do not have a valid distribution over the spanning trees.

## References

A. Asadpour, M. X. Goemans, A. Mardry, S. O. Ghran, and A. Saberi, _An o(log n / log log n)-approximation algorithm for the asymmetric traveling salesman problem_, SODA ’10,
Society for Industrial and Applied Mathematics, 2010, pp. 379-389, [https://dl.acm.org/doi/abs/10.5555/1873601.1873633](https://dl.acm.org/doi/abs/10.5555/1873601.1873633).

V. G. Kulkarni, _Generating random combinatorial objects_, Journal of algorithms, 11 (1990), pp. 185–207.
