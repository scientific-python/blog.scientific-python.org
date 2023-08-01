---
title: "Entropy Distribution Setup"
date: 2020-07-13
draft: false
description: "Preliminaries for the entropy distribution over spanning trees"
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

Finally moving on from the Held Karp relaxation, we arrive at the second step of the Asadpour asymmetric traveling salesman problem algorithm.
Referencing the Algorithm 1 from the Asadpour paper, we are now _finally_ on step two.

> ---
>
> **Algorithm 1** An \\(O(\log n / \log \log n)\\)-approximation algorithm for the ATSP
>
> ---
>
> **Input:** A set \\(V\\) consisting of \\(n\\) points and a cost function \\(c\ :\ V \times V \rightarrow \mathbb{R}^+\\) satisfying the triangle inequality.
>
> **Output:** \\(O(\log n / \log \log n)\\)-approximation of the asymmetric traveling salesman problem instance described by \\(V\\) and \\(c\\).
>
> 1. Solve the Held-Karp LP relaxation of the ATSP instance to get an optimum extreme point solution \\(x^\*\\).
>    Define \\(z^\*\\) as in (5), making it a symmetrized and scaled down version of \\(x^\*\\).
>    Vector \\(z^\*\\) can be viewed as a point in the spanning tree polytope of the undirected graph on the support of \\(x^\*\\) that one obtains after disregarding the directions of arcs (See Section 3.)
> 2. Let \\(E\\) be the support graph of \\(z^\*\\) when the direction of the arcs are disregarded.
>    Find weights \\(\{\tilde{\gamma}\}\_{e \in E}\\) such that the exponential distribution on the spanning trees, \\(\tilde{p}(T) \propto \exp(\sum\_{e \in T} \tilde{\gamma}\_e)\\) (approximately) preserves the marginals imposed by \\(z^\*\\), i.e. for any edge \\(e \in E\\),
>    \\[\sum\_{T \in \mathcal{T} : T \ni e} \tilde{p}(T) \leq (1 + \epsilon) z^\*\_e\\]
>    for a small enough value of \\(\epsilon\\).
>    (In this paper we show that \\(\epsilon = 0.2\\) suffices for our purpose. See Section 7 and 8 for a description of how to compute such a distribution.)
> 3. Sample \\(2\lceil \log n \rceil\\) spanning trees \\(T_1, \dots, T\_{2\lceil \log n \rceil}\\) from \\(\tilde{p}(.)\\).
>    For each of these trees, orient all its edges so as to minimize its cost with respect to our (asymmetric) cost function \\(c\\).
>    Let \\(T^\*\\) be the tree whose resulting cost is minimal among all of the sampled trees.
> 4. Find a minimum cost integral circulation that contains the oriented tree \\(\vec{T}^\*\\).
>    Shortcut this circulation to a tour and output it. (See Section 4.)
>
> ---

Sections 7 and 8 provide two different methods to find the desired probability distribution, with section 7 using a combinatorial approach and section 8 the ellipsoid method.
Considering that there is no ellipsoid solver in the scientific python ecosystem, and my mentors and I have already decided not to implement one within this project, I will be using the method in section 7.

The algorithm given in section 7 is as follows:

> 1. Set \\(\gamma = \vec{0}\\).
> 2. While there exists an edge \\(e\\) with \\(q_e(\gamma) > (1 + \epsilon) z_e\\):
>    - Compute \\(\delta\\) such that if we define \\(\gamma'\\) as \\(\gamma_e' = \gamma_e - \delta\\), and \\(\gamma_f' = \gamma_f\\) for all \\(f \in E\ \backslash \{e\}\\), then \\(q_e(\gamma') = (1 + \epsilon/2)z_e\\).
>    - Set \\(\gamma \leftarrow \gamma'\\).
> 3. Output \\(\tilde{\gamma} := \gamma\\).

This structure is fairly straightforward, but we need to know what \\(q_e(\gamma)\\) is and how to calculate \\(\delta\\).

Finding \\(\delta\\) is very easy, the formula is given in the Asadpour paper
(Although I did not realize this at the time that I wrote my GSoC proposal and re-derived the equation for delta. Fortunately my formula matches the one in the paper.)

\\[
\delta = \ln \frac{q\_e(\gamma)(1 - (1 + \epsilon / 2)z\_e)}{(1 - q\_e(\gamma))(1 + \epsilon / 2) z\_e}
\\]

Notice that the formula for \\(\delta\\) is reliant on \\(q_e(\gamma)\\).
The paper defines \\(q_e(\gamma)\\) as

\\[
q\_e(\gamma) = \frac{\sum\_{T \ni e} \exp(\gamma(T))}{\sum\_{T \in \mathcal{T}} \exp(\gamma(T))}
\\]

where \\(\gamma(T) = \sum\_{f \in T} \gamma_f\\).

The first thing that I noticed is that in the denominator the summation is over all spanning trees for in the graph, which for the complete graphs we will be working with is exponential so a `brute force' approach here is useless.
Fortunately, Asadpour and team realized we can use Kirchhoff's matrix tree theorem to our advantage.

As an aside about Kirchhoff's matrix tree theorem, I was not familiar with this theorem before this project so I had to do a bit of reading about it.
Basically, if you have a laplacian matrix (the adjacency matrix minus the degree matrix), the absolute value of any cofactor is the number of spanning trees in the graph.
This was something completely unexpected to me, and I think that it is very cool that this type of connection exists.

The details of using Kirchhoff's theorem are given in section 5.3.
We will be using a weighted laplacian \\(L\\) defined by

\\[
L\_{i, j} = \left\\{
\begin{array}{l l}
-\lambda\_e & e = (i, j) \in E \\\\\\
\sum\_{e \in \delta(\{i\})} \lambda\_e & i = j \\\\\\
0 & \text{otherwise}
\end{array}
\right.
\\]

where \\(\lambda_e = \exp(\gamma_e)\\).

Now, we know that applying Krichhoff's theorem to \\(L\\) will return

\\[
\sum\_{t \in \mathcal{T}} \prod\_{e \in T} \lambda\_e
\\]

but which part of \\(q_e(\gamma)\\) is that?

If we apply \\(\lambda_e = \exp(\gamma_e)\\), we find that

\\[
\begin{array}{r c l}
\sum\_{T \in \mathcal{T}} \prod\_{e \in T} \lambda\_e &=& \sum\_{T \in \mathcal{T}} \prod\_{e \in T} \exp(\gamma\_e) \\\\\\
&& \sum\_{T \in \mathcal{T}} \exp\left(\sum\_{e \in T} \gamma\_e\right) \\\\\\
&& \sum\_{T \in \mathcal{T}} \exp(\gamma(T)) \\\\\\
\end{array}
\\]

So moving from the first row to the second row is a confusing step, but essentially we are exploiting the properties of exponents.
Recall that \\(\exp(x) = e^x\\), so could have written it as \\(\prod\_{e \in T} e^{\gamma_e}\\) but this introduces ambiguity as we would have multiple meanings of \\(e\\).
Now, for all values of \\(e\\), \\(e_1, e_2, \dots, e\_{n-1}\\) in the spanning tree \\(T\\) that product can be expanded as

\\[
\prod\_{e \in T} e^{\gamma\_e} = e^{\gamma\_{e\_1}} \times e^{\gamma\_{e\_2}} \times \dots \times e^{\gamma\_{e\_{n-1}}}
\\]

Each exponential factor has the same base, so we can collapse that into

\\[
e^{\gamma\_{e\_1} + \gamma\_{e\_2} + \dots + \gamma\_{e\_{n-1}}}
\\]

which is also

\\[
e^{\sum\_{e \in T} \gamma\_e}
\\]

but we know that \\(\sum\_{e \in T} \gamma_e\\) is \\(\gamma(T)\\), so it becomes

\\[
e^{\gamma(T)} = \exp(\gamma(T))
\\]

Once we put that back into the summation we arrive at the denominator in \\(q_e(\gamma)\\), \\(\sum\_{T \in \mathcal{T}} \exp(\gamma(T))\\).

Next, we need to find the numerator for \\(q_e(\gamma)\\).
Just as before, a `brute force' approach would be exponential in complexity, so we have to find a better way.
Well, the only difference between the numerator and denominator is the condition on the outer summation, which the \\(T \in \mathcal{T}\\) being changed to \\(T \ni e\\) or every tree containing edge \\(e\\).

There is a way to use Krichhoff's matrix tree theorem here as well.
If we had a graph in which every spanning tree could be mapped in a one-to-one fashion onto every spanning tree in the original graph which contains the desired edge \\(e\\).
In order for a spanning tree to contain edge \\(e\\), we know that the endpoints of \\(e\\), \\((u, v)\\) will be directly connected to each other.
So we are then interested in every spanning tree in which we reach vertex \\(u\\) and then leave from vertex \\(v\\).
(As opposed to the spanning trees where we reach vertex \\(u\\) and then leave from that same vertex).
In a sense, we are treating vertices \\(u\\) and \\(v\\) is the same vertex.
We can apply this literally by _contracting_ \\(e\\) from the graph, creating \\(G / \{e\}\\).
Every spanning tree in this graph can be uniquely mapped from \\(G / \{e\}\\) onto a spanning tree in \\(G\\) which contains the edge \\(e\\).

From here, the logic to show that a cofactor from \\(L\\) is actually the numerator of \\(q_e(\gamma)\\) parallels the logic for the denominator.

At this point, we have all of the needed information to create some pseudo code for the next function in the Asadpour method, `spanning_tree_distribution()`.
Here I will use an inner function `q()` to find \\(q_e\\).

```
def spanning_tree_distribution
    input: z, the symmetrized and scaled output of the Held Karp relaxation.
    output: gamma, the maximum entropy exponential distribution for sampling spanning trees
           from the graph.

    def q
        input: e, the edge of interest

        # Create the laplacian matrices
        write lambda = exp(gamma) into the edges of G
        G_laplace = laplacian(G, lambda)
        G_e = nx.contracted_edge(G, e)
        G_e_laplace = laplacian(G, lambda)

        # Delete a row and column from each matrix to made a cofactor matrix
        G_laplace.delete((0, 0))
        G_e_laplace.delete((0, 0))

        # Calculate the determinant of the cofactor matrices
        det_G_laplace = G_laplace.det
        det_G_e_laplace = G_e_laplace.det

        # return q_e
        return det_G_e_laplace / det_G_laplace

    # initialize the gamma vector
    gamma = 0 vector of length G.size

    while true
        # We will iterate over the edges in z until we complete the
        # for loop without changing a value in gamma. This will mean
        # that there is not an edge with q_e > 1.2 * z_e
        valid_count = 0
        # Search for an edge with q_e > 1.2 * z_e
        for e in z
            q_e = q(e)
            z_e = z[e]
            if q_e > 1.2 * z_e
                delta = ln(q_e * (1 - 1.1 * z_e) / (1 - q_e) * 1.1 * z_e)
                gamma[e] -= delta
            else
                valid_count += 1
        if valid_count == number of edges in z
            break

    return gamma
```

## Next Steps

The clear next step is to implement the function `spanning_tree_distribution` using the pseudo code above as an outline.
I will start by writing `q` and testing it with the same graphs which I am using to test the Held Karp relaxation.
Once `q` is complete, the rest of the function seems fairly straight forward.

One thing that I am concerned about is my ability to test `spanning_tree_distribution`.
There are no examples given in the Asadpour research paper and no other easy resources which I could turn to in order to find an oracle.

The only method that I can think of right now would be to complete this function, then complete `sample_spanning_tree`.
Once both functions are complete, I can sample a large number of spanning trees to find an experimental probability for each tree, then run a statistical test (such as an h-test) to see if the probability of each tree is near \\(\exp(\gamma(T))\\) which is the desired distribution.
An alternative test would be to use the marginals in the distribution and have to manually check that

\\[
\sum\_{T \in \mathcal{T} : T \ni e} p(T) \leq (1 + \epsilon) z^\*\_e,\ \forall\ e \in E
\\]

where \\(p(T)\\) is the experimental data from the sampled trees.

Both methods seem very computationally intensive and because they are sampling from a probability distribution they may fail randomly due to an unlikely sample.

## References

A. Asadpour, M. X. Goemans, A. Mardry, S. O. Ghran, and A. Saberi, _An o(log n / log log n)-approximation algorithm for the asymmetric traveling salesman problem_, Operations Research, 65 (2017), pp. 1043-1061.
