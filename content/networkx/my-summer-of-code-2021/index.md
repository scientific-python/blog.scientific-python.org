---
title: "My Summer of Code 2021"
date: 2020-08-16 
draft: false
description: "Review of my entire summer implementing the Asadpour ATSP Algorithm"
tags: ["gsoc", "networkx"] 
displayInList: true 
author: ["mjschwenne"] 

resources:
- name: featuredImage
  src: "mjschwenne_GSoc.png"
  params:
    description: "Google Summer of Code Logo with NetworkX logo"
    showOnTop: true 
---
Welcome! This post is not going to be discussing technical implementation details or theortical work for my Google Summer of Code project, but rather serve as a summary and recap for the work that I did this summer.

I am very happy with the work I was able to accomplish and believe that I successfully completed my project.

## Overview

My project was titled NetworkX: Implementing the Asadpour Asymmetric Traveling Salesman Problem Algorithm.
The updated abstract given on the Summer of Code project [project page](https://summerofcode.withgoogle.com/dashboard/project/5352909442646016/details/) is below.

> This project seems to implement the asymmetric traveling salesman problem developed by Asadpour et al, originally published in 2010 and revised in 2017. 
> The project is broken into multiple methods, each of which has a set timetable during the project. 
> We start by solving the Held-Karp relaxation using the Ascent method from the original paper by Held and Karp. 
> Assuming the result is fractional, we continue into the Asadpour algorithm (integral solutions are optimal by definition and immediately returned). 
> We approximate the distribution of spanning trees on the undirected support of the Held Karp solution using a maximum entropy rounding method to construct a distribution of trees. 
> Roughly speaking, the probability of sampling any given tree is proportional to the product of all its edge lambda values. 
> We sample 2 log *n* trees from the distribution using an iterative approach developed by V. G. Kulkarni and choose the tree with the smallest cost after returning direction to the arcs. 
> Finally, the minimum tree is augmented using a minimum network flow algorithm and shortcut down to an *O(log n / log log n)* approximation of the minimum Hamiltonian cycle.

My proposal PDF for the 2021 Summer of Code can be [found here](https://drive.google.com/file/d/1XGrjupLYWioz-Nf8Vp63AeuBVApdkwSa/view?usp=sharing).

All of my changes and additions to NetworkX are part of [this pull request](https://github.com/networkx/networkx/pull/4740) and can also be found on [this branch](https://github.com/mjschwenne/networkx/tree/bothTSP) in my fork of the GitHub repository, but I will be discussing the changes and commits in more detail later.
Also note that for the commits I listed in each section, this is an incomplete list only hitting on focused commits to that function or its tests.
For the complete list, please reference the pull request or the `bothTSP` GitHub branch on my fork of NetworkX.

My contributions to NetworkX this summer consist predominantly of the following functions and classes, each of which I will discuss in their own sections of this blog post.
Functions and classes which are front-facing are also linked to the [developer documentation](https://networkx.org/documentation/latest/index.html) for NetworkX in the list below and for their section headers.

* [`SpanningTreeIterator`](https://networkx.org/documentation/latest/reference/algorithms/generated/networkx.algorithms.tree.mst.SpanningTreeIterator.html)
* [`ArborescenceIterator`](https://networkx.org/documentation/latest/reference/algorithms/generated/networkx.algorithms.tree.branchings.ArborescenceIterator.html)
* `held_karp_ascent`
* `spanning_tree_distribution`
* `sample_spanning_tree`
* [`asadpour_atsp`](https://networkx.org/documentation/latest/reference/algorithms/generated/networkx.algorithms.approximation.traveling_salesman.asadpour_atsp.html)

These functions have also been unit tested, and those tests will be integrated into NetworkX once the pull request is merged.

## References

The following papers are where all of these algorithms originate form and they were of course instrumental in the completion of this project.

[1] A. Asadpour, M. X. Goemans, A. Madry, S. O. Gharan, and A. Saberi, *An O (log n / log log n)-approximation algorithm for the asymmetric traveling salesman problem*, SODA ’10, Society for Industrial and Applied Mathematics, 2010, p. 379 - 389 [https://dl.acm.org/doi/abs/10.5555/1873601.1873633](https://dl.acm.org/doi/abs/10.5555/1873601.1873633).

[2] J. Edmonds, *Optimum Branchings*, Journal of Research of the National Bureau of Standards, 1967, Vol. 71B, p.233-240, [https://archive.org/details/jresv71Bn4p233](https://archive.org/details/jresv71Bn4p233)

[3] M. Held, R.M. Karp, *The traveling-salesman problem and minimum spanning trees*. Operations research, 1970-11-01, Vol.18 (6), p.1138-1162. [https://www.jstor.org/stable/169411](https://www.jstor.org/stable/169411)

[4] G.K. Janssens, K. Sörensen, *An algorithm to generate all spanning trees in order of increasing cost*, Pesquisa Operacional, 2005-08, Vol. 25 (2), p. 219-229, [https://www.scielo.br/j/pope/a/XHswBwRwJyrfL88dmMwYNWp/?lang=en](https://www.scielo.br/j/pope/a/XHswBwRwJyrfL88dmMwYNWp/?lang=en)

[5] V. G. Kulkarni, *Generating random combinatorial objects*, Journal of algorithms, 11 (1990), p. 185–207.

## [`SpanningTreeIterator`](https://networkx.org/documentation/latest/reference/algorithms/generated/networkx.algorithms.tree.mst.SpanningTreeIterator.html)

The `SpanningTreeIterator` was the first contribution I completed as part of my GSoC project.
This class takes a graph and returns every spanning tree in it in order of increasing cost, which makes it a direct implementation of [4].

The interesting thing about this iterator is that it is not used as part of the Asadpour algorithm, but served as an intermediate step so that I could develop the `ArborescenceIterator` which is required for the Held Karp relaxation. 
It works by partitioning the edges of the graph as either included, excluded or open and then finding the minimum spanning tree which respects the partition data on the graph edges. 
In order to get this to work, I created a new minimum spanning tree function called `kruskal_mst_edges_partition` which does exactly that.
To prevent redundancy, all kruskal minimum spanning trees now use this function (the original `kruskal_mst_edges` function is now just a wrapper for the partitioned version).
Once a spanning tree is returned from the iterator, the partition data for that tree is split so that the union of the newly generated partitions is the set of all spanning trees in the partition except the returned minimum spanning tree.

As I mentioned earlier, the `SpanningTreeIterator` is not directly used in my GSoC project, but I still decided to implement it to understand the partition process and be able to directly use the examples from [4] before moving onto the `ArborescenceIterator`.
This class I'm sure will be useful to the other users of NetworkX and provided a strong foundation to build the `ArborescenceIterator` off of.

**Blog Posts about `SpanningTreeIterator`**

5 Jun 2021 - *[Finding All Minimum Arborescences](fhttps://blog.scientific-python.org/posts/networkx/inding-all-minimum-arborescences.html)*

10 Jun 2021 - *[Implementing The Iterators](https://blog.scientific-python.org/posts/networkx/implementing-the-iterators.html)*

**Commits about `SpanningTreeIterator`**

Now, at the beginning of this project, my commit messages were not very good...
I had some problems about merge conflicts after I accidentally committed to the wrong branch and this was the first time I'd used a pre-commit hook.

I have not changed the commit messages here, so that you may be assumed by my troughly unhelpful messages, but did annotate them to provide a more accurate description of the commit.

[Testing](https://github.com/mjschwenne/networkx/commit/495458842d3ec798c6ea52dc1c8089b9a5ce3de5) - *Rewrote Kruskal's algorithm to respect partitions and tested that while stubbing the iterators in a separate file*

[I'm not entirly sure how the commit hook works...](https://github.com/mjschwenne/networkx/commit/3d81e36c8313013a3ae4c4dfc6517c3bde8d826e) - *Added test cases and finalized implementation of Spanning Tree Iterator in the incorrect file*

[Moved iterators into the correct files to maintain proper codebase visibility](https://github.com/mjschwenne/networkx/commit/d481f757125a699f69bf5c16790d2e727e3cc159) - *Realized that the iterators need to be in `mst.py` and `branchings.py` respectively to keep private functions hidden*

[Documentation update for the iterators](https://github.com/mjschwenne/networkx/commit/5503203433bc875df8c0de5d827bda7bed1589e2) - *No explanation needed*

[Update mst.py to accept suggestion](https://github.com/mjschwenne/networkx/commit/337804ee38b2c1ac3964447a39d67184081deb01) - *Accepted doc string edit from code review*

[Review suggestions from dshult](https://github.com/mjschwenne/networkx/commit/5f97de07821e49cc9ba4f9996ec6d1495eb268b7) - *Implemented code review suggestions from one of my mentors*

[Cleaned code, merged functions if possible and opened partition functionality to all](https://github.com/mjschwenne/networkx/commit/97b2da1b5499ecbfd15ef2abd385e50f94c6ba97)

[Implement suggestions from boothby](https://github.com/mjschwenne/networkx/commit/aef90dfcbb8b8424c6ed887311b4825559d0a398)

## [`ArborescenceIterator`](https://networkx.org/documentation/latest/reference/algorithms/generated/networkx.algorithms.tree.branchings.ArborescenceIterator.html)

The `ArborescenceIterator` is a modified version of the algorithm discussed in [4] so that it iterates over the spanning arborescences. 

This iterator was a bit more difficult to implement, but that is due to how the minimum spanning arborescence algorithm is structured rather than the partition scheme not being applicable to directed graphs.
In fact the partition scheme is identical to the undirected `SpanningTreeIterator`, but Edmonds' algorithm is more complex and there are several edge cases about how nodes can be contracted and what it means for respecting the partition data.
In order to fully understand the NetworkX implementation, I had to read the original Edmonds paper, [2].

The most notable change was that when the iterator writes the next partition onto the edges of the graph just before Edmonds' algorithm is executed, if any incoming edge is marked as included, all of the others are marked as excluded. 
This is an implicit part of the `SpanningTreeIterator`, but needed to be explicitly done here so that if the vertex in question was merged during Edmonds' algorithm we could not choose two of the incoming edges to the same vertex once the merging was reversed.

As a final note, the `ArborescenceIterator` has one more initial parameter than the `SpanningTreeIterator`, which is the ability to give it an initial partition and iterate over all spanning arborescence with cost greater than the initial partition.
This was used as part of the branch and bound method, but is no longer a part of the my Asadpour algorithm implementation.

**Blog Posts about `ArborescenceIterator`**

5 Jun 2021 - *[Finding All Minimum Arborescences](https://blog.scientific-python.org/posts/networkx/finding-all-minimum-arborescences)*

10 Jun 2021 - *[Implementing The Iterators](https://blog.scientific-python.org/posts/networkx/implementing-the-iterators)*

**Commits about `ArborescenceIterator`**

My commits listed here are still annotated and much of the work was done at the same time.

[Testing](https://github.com/mjschwenne/networkx/commit/495458842d3ec798c6ea52dc1c8089b9a5ce3de5) - *Rewrote Kruskal's algorithm to respect partitions and tested that while stubbing the iterators in a separate file*

[Moved iterators into the correct files to maintain proper codebase visibility](https://github.com/mjschwenne/networkx/commit/d481f757125a699f69bf5c16790d2e727e3cc159) - *Realized that the iterators need to be in `mst.py` and `branchings.py` respectivly to keep private functions hidden*

[Including Black reformat](https://github.com/mjschwenne/networkx/commit/73cade29568f9e10303fb901c97ac52b1d45b8aa) - *Modified Edmonds' algorithm to respect partitions*

[Modified the ArborescenceIterator to accept init partition](https://github.com/mjschwenne/networkx/commit/ae1c1031980f7e3c3854d718c8813b226d2e8d42) - *No explanation needed*

[Documentation update for the iterators](https://github.com/mjschwenne/networkx/commit/5503203433bc875df8c0de5d827bda7bed1589e2) - *No explanation needed*

[Update branchings.py accept doc string edit](https://github.com/mjschwenne/networkx/commit/b44a5ab9c8d5ac86db446213d7b9712e5b9aac81) - *No explanation needed*

[Review suggestions from dshult](https://github.com/mjschwenne/networkx/commit/5f97de07821e49cc9ba4f9996ec6d1495eb268b7) - *Implemented code review suggestions from one of my mentors*

[Cleaned code, merged functions if possible and opened partition functionality to all](https://github.com/mjschwenne/networkx/commit/97b2da1b5499ecbfd15ef2abd385e50f94c6ba97)

[Implemented review suggestions from rossbar](https://github.com/mjschwenne/networkx/commit/55688deb9a84bc7a77aecc556a63ff80dc41c56f)

[Implement suggestions from boothby](https://github.com/mjschwenne/networkx/commit/aef90dfcbb8b8424c6ed887311b4825559d0a398)

## `held_karp_ascent`

The Held Karp relaxation was the most difficult part of my GSoC project and the part that I was the most worried about going into this May.

My plans on how to solve the relaxation evolved over the course of the summer as well, finally culminating in `held_karp_ascent`. 
In my GSoC proposal, I discuss using `scipy` to solve the relaxation, but the Held Karp relaxation is a semi-infinite linear problem (that is, it is finite but exponential) so I would quickly surpass the capabilities of virtually any computer that the code would be run on. 
Fortunately I realized that while I was still writing my proposal and was able to change it.
Next, I wanted to use the ellipsoid algorithm because that is the suggested method in the Asadpour paper [1]. 

As it happens, the ellipsoid algorithm is not implemented in `numpy` or `scipy` and after discussing the practicality of implementing the algorithm as part of this project, we decided that a robust ellipsoid solver was a GSoC project onto itself and beyond the scope of the Asadpour algorithm. 
Another method was needed, and was found.
In the original paper by Held and Karp [3], they present three different algorithms for solving the relaxation, the column-generation technique, the ascent method and the branch and bound method.
After reading the paper and comparing all of the methods, I decided that the branch and bound method was the best in terms of performance and wanted to implement that one.

The branch and bound method is a modified version of the ascent method, so I started by implementing the ascent method, then the branch and bound around it. 
This had the extra benefit of allowing me to compare the two and determine which is actually better. 

Implementing the ascent method proved difficult. 
There were a number of subtle bugs in finding the minimum 1-arborescences and finding the value of epsilon by not realizing all of the valid edge substitutions in the graph.
More information about these problems can be found in my post titled *Understanding the Ascent Method*.
Even after this the ascent method was not working proper, but I decided to move onto the branch and bound method in hopes of learning more about the process so that I could fix the ascent method.

That is exactly what happened!
While debugging the branch and bound method, I realized that my function for finding the set of minimum 1-arborescences would stop searching too soon and possibly miss the minimum 1-arborescences.
Once I fixed that bug, both the ascent as well as the branch and bound method started to produce the correct results.

But which one would be used in the final project?

Well, that came down to which output was more compatible with the rest of the Asadpour algorithm.
The ascent method could find a fractional solution where the edges are not totally in or out of the solution while the branch and bound method would take the time to ensure that the solution was integral.
As it would happen, the Asadpour algorithm expects a fractional solution to the Held Karp relaxation so in the end the ascent method one out and the branch and bound method was removed from the project.

All of this is detailed in the (many) blog posts I wrote on this topic, which are listed below.

**Blog posts about the Held Karp relaxation**

My first two posts were about the `scipy` solution and the ellipsoid algorithm.

11 Apr 2021 - *[Held Karp Relaxation](https://blog.scientific-python.org/posts/networkx/held-karp-relaxation)*

8 May 2021 - *[Held Karp Separation Oracle](https://blog.scientific-python.org/posts/networkx/held-karp-separation-oracle)*

This next post discusses the merits of each algorithm presenting in the original Held and Karp paper [3].

3 Jun 2021 - *[A Closer Look At Held Karp](https://blog.scientific-python.org/posts/networkx/a-closer-look-at-held-karp)*

And finally, the last three Held Karp related posts are about the debugging of the algorithms I did implement.

22 Jun 2021 - *[Understanding The Ascent Method](https://blog.scientific-python.org/posts/networkx/understanding-the-ascent-method)*

28 Jun 2021 - *[Implementing The Held Karp Relaxation](https://blog.scientific-python.org/posts/networkx/implementing-the-held-karp-relaxation)*

7 Jul 2021 - *[Finalizing Held Karp](https://blog.scientific-python.org/posts/networkx/finalizing-held-karp)*

**Commits about the Held Karp relaxation**

Annotations only provided if needed.

[Grabbing black reformats](https://github.com/networkx/networkx/pull/4740/commits/716437f6ccbbd6c77a7a01b38d330f899c333f0a) - *Initial Ascent method implementation*

[Working on debugging ascent method plus black reformats](https://github.com/mjschwenne/networkx/commit/cd28eb71676ecc34c7af6f2e0f8980ad6ae89f00)

[Ascent method terminating, but at non-optimal solution](https://github.com/mjschwenne/networkx/commit/660e4d3f04a0b4ce28e152af7f8c7df84e1961b3)

[minor edits](https://github.com/mjschwenne/networkx/commit/8314c3c28d205ed5a7d6316904f4db0265d93942) - *Removed some debug statements*

[Fixed termination condition, still given non-optimal result](https://github.com/mjschwenne/networkx/commit/f7dcb54ce17ec3646e7d3c33f909f6b382608532)

[Minor bugfix, still non-optimal result](https://github.com/mjschwenne/networkx/commit/beccc98c362eb8bdddc42b72af0d669ad082e468) - *Ensured reported answer is the cycle if multiple options*

[Fixed subtle bug in find\_epsilon()](https://github.com/mjschwenne/networkx/commit/68ffad5c70811a702ade569817a1f3a14c33a1af) - *Fixed the improper substitute detection bug*

[Cleaned code and tried something which didn't work](https://github.com/mjschwenne/networkx/commit/a4f1442dcf2c6f69dcf03dacf0ed38183cdc7ddb)

[Black formats](https://github.com/mjschwenne/networkx/commit/644d14ac6ce327ce577592e566153c0117c6dcb6) - *Initial branch and bound implementation*

[Branch and bound returning optimal solution](https://github.com/mjschwenne/networkx/commit/288bb5324cceb11e94396e435616c70b87926f69)

[black formatting changes](https://github.com/mjschwenne/networkx/commit/242b53da0e00326ece75304a4ad8fb89e9ba8a25) - *Split ascent and branch and bound methods into different functions*

[Performance tweaks and testing fractional answers](https://github.com/mjschwenne/networkx/commit/adbf930c23271c17a4d2fed6fbcd03552799793c)

[Fixed test bug, I hope](https://github.com/mjschwenne/networkx/commit/d3a45122bba3240d933a2b4275173f7e8a987cfa)

[Asadpour output for ascent method](https://github.com/mjschwenne/networkx/commit/37d6219887bff444d9f29e38526965ec4cc0687d)

[Removed branch and bound method. One unit test misbehaving](https://github.com/mjschwenne/networkx/commit/bcfb0ebcbe552524e44f9c85e353b53b1711e028)

[Added asymmetric fractional test for the ascent method](https://github.com/mjschwenne/networkx/commit/b529389be5263144b5755f8e4589216606e37484)

[Removed printn statements and tweaked final test to be more asymmetric](https://github.com/mjschwenne/networkx/commit/c6cedc1f9d53a0c486c0196041188ae1b9c740d4)

[Changed HK to only report on the support of the answer](https://github.com/mjschwenne/networkx/commit/b6bec0dada9ff67dc1cf28f5ae0fe3b1df490dc5)

[documentation update](https://github.com/mjschwenne/networkx/commit/837d0448d38936278cfa9fdb7d8cb636eb8552c3)

## `spanning_tree_distribution`

Once we have the support of the Held Karp relaxation, we calculate edge weights \\(\gamma\\) for support so that the probability of any tree being sampled is proportional to the product of \\(e^{\gamma}\\) across its edges.
This is called a maximum entropy distribution in the Asadpour paper.
This procedure was included in the Asadpour paper [1] on page 386.

> 1. Set \\(\gamma = \vec{0}\\).
> 2. While there exists an edge \\(e\\) with \\(q\_e(\gamma) > (1 + \epsilon)z\_e\\):
>   * Compute \\(\delta\\) such that if we define \\(\gamma'\\) ad \\(\gamma\_e' = \gamma\_e - \delta\\) and \\(\gamma\_f' = \gamma\_e\\) for all \\(f \in E \backslash \{e\}\\), then \\(q\_e(\gamma') = (1 + \epsilon / 2)z\_e\\)
>   * Set \\(\gamma \leftarrow \gamma'\\)
> 3. Output \\(\tilde{\gamma} := \gamma\\).

Where \\(q\_e(\gamma)\\) is the probability that any given edge \\(e\\) will be in a sampled spanning tree chosen with probability proportional to \\(\exp(\gamma(T))\\).
\\(\delta\\) is also given as 

\\[
\delta = \frac{q\_e(\gamma)(1-(1+\epsilon/2)z\_e)}{(1-q\_e(\gamma))(1+\epsilon/2)z\_e}
\\]

so the Asadpour paper did almost all of the heavy lifting for this function.
However, they were not very clear on how to calculate \\(q\_e(\gamma)\\) other than that Krichhoff's Tree Matrix Theorem can be used.

My original method for calculating \\(q\_e(\gamma)\\) was to apply Krichhoff's Theorem to the original laplacian matrix and the laplacian produced once the edge \\(e\\) is contracted from the graph.
Testing quickly showed that once the edge is contracted from the graph, it cannot affect the value of the laplacian and thus after subtracting \\(\delta\\) the probability of that edge would increase rather than decrease. 
Multiplying my original value of \\(q\_e(\gamma)\\) by \\(\exp(\gamma\_e)\\) proved to be the solution here for reasons extensively discussed in my blog post *The Entropy Distribution* and in particular the "Update! (28 July 2021)" section.

**Blog posts about `spanning_tree_distribution`**

13 Jul 2021 - *[Entropy Distribution Setup](https://blog.scientific-python.org/posts/networkx/entropy-distribution-setup)*

20 Jul 2021 - *[The Entropy Distribution](https://blog.scientific-python.org/posts/networkx/the-entropy-distribution)*

**Commits about `spanning_tree_distribution`**

[Draft of spanning\_tree\_distribution](https://github.com/mjschwenne/networkx/commit/da1f5cf688277426575115e3328e16d8f5b29a3c)

[Changed HK to only report on the support of the answer](https://github.com/mjschwenne/networkx/commit/b6bec0dada9ff67dc1cf28f5ae0fe3b1df490dc5) - *Needing to limit \\(\gamma\\) to only the support of the Held Karp relaxation is what caused this change*

[Fixed contraction bug by changing to MultiGraph. Problem with prob > 1](https://github.com/mjschwenne/networkx/commit/0fcf0b3ecfc3704db17830eeeae72a67b4182ffb) - *Because the probability is only* proportional *to the product of the edge weights, this was not actually a problem*

[Black reformats](https://github.com/mjschwenne/networkx/commit/e820d4f921268ff0d55f913624bcd402c90244b2) - *Rewrote the test and cleaned the code*

[Fixed pypi test error](https://github.com/mjschwenne/networkx/commit/2195002e9394bcb2c47876809cfbbec3c05b1008) - *The pypi tests do not have `numpy` or `scipy` and I forgot to flag the test to be skipped if they are not available*

[Further testing of dist fix](https://github.com/mjschwenne/networkx/commit/e4cd4f17311e8d908f016cea45f03b1b3e35822e) - *Fixed function to multiply \\(q\_e(\gamma)\\) by \\(\exp(\gamma\_e)\\) and implemented exception if \\(\delta\\) ever misbehaves*

[Can sample spanning trees](https://github.com/mjschwenne/networkx/commit/68f0cf95565bcdce0aec4678e3af9815e23b494e) - *Streamlined finding \\(q\_e(\gamma)\\) using new helper function*

[documentation update](https://github.com/mjschwenne/networkx/commit/837d0448d38936278cfa9fdb7d8cb636eb8552c3)

[Review suggestions from dshult](https://github.com/mjschwenne/networkx/commit/5f97de07821e49cc9ba4f9996ec6d1495eb268b7) - *Implemented code review suggestions from one of my mentors*

[Implement suggestions from boothby](https://github.com/mjschwenne/networkx/commit/aef90dfcbb8b8424c6ed887311b4825559d0a398)

## `sample_spanning_tree`

What good is a spanning tree distribution if we can't sample from it?

While the Asadpour paper [1] provides a rough outline of the sampling process, the bulk of their methodology comes from the Kulkarni paper, *Generating random combinatorial objects* [5]. 
That paper had a much more detailed explanation and even this pseudo code from page 202.

> \\(U = \emptyset,\\) \\(V = E\\)\
> Do \\(i = 1\\) to \\(N\\);\
> \\(\qquad\\)Let \\(a = n(G(U, V))\\)\
> \\(\qquad\qquad a'\\) \\(= n(G(U \cup \{i\}, V))\\)\
> \\(\qquad\\)Generate \\(Z \sim U[0, 1]\\)\
> \\(\qquad\\)If \\(Z \leq \alpha\_i \times \left(a' / a\right)\\)\
> \\(\qquad\qquad\\)then \\(U = U \cup \{i\}\\),\
> \\(\qquad\qquad\\)else \\(V = V - \{i\}\\)\
> \\(\qquad\\)end.\
> Stop. \\(U\\) is the required spanning tree.

The only real difficulty here was tracking how the nodes were being contracted.
My first attempt was a mess of `if` statements and the like, but switching it to a merge-find data structure (or disjoint set data structure) proved to be a wise decision.

Of course, it is one thing to be able to sample a spanning tree and another entirely to know if the sampling technique matches the expected distribution.
My first iteration test for `sample_spanning_tree` just sampled a large number of trees (50000) and they printed the percent error from the normalized distribution of spanning tree.
With a sample size of 50000 all of the errors were under 10%, but I still wanted to find a better test.

From my AP statistics class in high school I remembered the \\(X^2\\) (Chi-squared) test and realized that it would be perfect here.
`scipy` even had the ability to conduct one.
By converting to a chi-squared test I was able to reduce the sample size down to 1200 (near the minimum required sample size to have a valid chi-squared test) and use a proper hypothesis test at the \\(\alpha = 0.01\\) significance level.
Unfortunately, the test would still fail 1% of the time until I added the `@py_random_state` decorator to `sample_spanning_tree`, and then the test can pass in a `Random` object to produce repeatable results.

**Blog posts about `sample_spanning_tree`**

21 Jul 2021 - *[Preliminaries For Sampling A Spanning Tree](https://blog.scientific-python.org/posts/networkx/preliminaries-for-sampling-a-spanning-tree)*

28 Jul 2021 - *[Sampling A Spanning Tree](https://blog.scientific-python.org/posts/networkx/sampling-a-spanning-tree)*

**Commits about `sample_spanning_tree`**

[Can sample spanning trees](https://github.com/mjschwenne/networkx/commit/68f0cf95565bcdce0aec4678e3af9815e23b494e)

[Developing test for sampling spanning tree](https://github.com/mjschwenne/networkx/commit/3cca2b5bfdf001b1613f8e803f78c9fb380adc59)

[Changed sample_spanning_tree test to Chi squared test](https://github.com/mjschwenne/networkx/commit/274e2c5908f337941ee5234d727fd307257a9b85)

[Adding test cases](https://github.com/mjschwenne/networkx/commit/7ebc6d874ec703a46dfc40f195fa84594bb9582c) - *Implemented `@py_random_state` decorator*

[documentation update](https://github.com/mjschwenne/networkx/commit/837d0448d38936278cfa9fdb7d8cb636eb8552c3)

[Review suggestions from dshult](https://github.com/mjschwenne/networkx/commit/5f97de07821e49cc9ba4f9996ec6d1495eb268b7) - *Implemented code review suggestions from one of my mentors*

## [`asadpour_atsp`](https://networkx.org/documentation/latest/reference/algorithms/generated/networkx.algorithms.approximation.traveling_salesman.asadpour_atsp.html)

This function was the last piece of the puzzle, connecting all of the others together and producing the final result!

Implementation of this function was actually rather smooth.
The only technical difficulty I had was reading the support of the `flow_dict` and the theoretical difficulties were adapting the `min_cost_flow` function to solve the minimum circulation problem.
Oh, and that if the flow is greater than 1 I need to add parallel edges to the graph so that it is still eulerian.

A brief overview of the whole algorithm is given below:

1. Solve the Held Karp relaxation and symmertize the result to made it undirected.
2. Calculate the maximum entropy spanning tree distribution on the Held Karp support graph.
3. Sample \\(2 \lceil \ln n \rceil\\) spanning trees and record the smallest weight one before reintroducing direction to the edges.
4. Find the minimum cost circulation to create an eulerian graph containing the sampled tree.
5. Take the eulerian walk of that graph and shortcut the answer.
6. return the shortcut answer.

**Blog posts about `asadpour_atsp`**

29 Jul 2021 - *[Looking At The Big Picture](https://blog.scientific-python.org/posts/networkx/looking-at-the-big-picture.html)*

10 Aug 2021 - *[Completing The Asadpour Algorithm](https://blog.scientific-python.org/posts/networkx/completing-the-asadpour-algorithm.html)*

**Commits about `asadpour_atsp`**

[untested implementation of asadpour\_tsp](https://github.com/mjschwenne/networkx/commit/2c1dc57542cc9651b5443f6015fb94b94bc2f7cd)

[Fixed issue reading flow\_dict](https://github.com/mjschwenne/networkx/commit/454c82ca61ab4746b57c6681449f8ea08f96d557)

[Fixed runtime errors in asadpour\_tsp](https://github.com/mjschwenne/networkx/commit/328a4f3b2669fa9890d2c08a4d72f0f9bb7573dc) - *General traveling salesman problem function assumed graph were undirected. This is not work with an atsp algorithm*

[black reformats](https://github.com/mjschwenne/networkx/commit/1d345054a20a88b3115af900972a0145d708d8b5) - *Fixed parallel edges from flow support bug*

[Adding test cases](https://github.com/mjschwenne/networkx/commit/7ebc6d874ec703a46dfc40f195fa84594bb9582c)

[documentation update](https://github.com/mjschwenne/networkx/commit/837d0448d38936278cfa9fdb7d8cb636eb8552c3)

[One new test and check](https://github.com/mjschwenne/networkx/commit/11fef147246eb3374568515a4b29aeee5a9f469d)

[Fixed rounding error with tests](https://github.com/mjschwenne/networkx/commit/6db9f7692fc5294ac206fa331242fe679cbfb7d7)

[Review suggestions from dshult](https://github.com/mjschwenne/networkx/commit/5f97de07821e49cc9ba4f9996ec6d1495eb268b7) - *Implemented code review suggestions from one of my mentors*

[Implemented review suggestions from rossbar](https://github.com/mjschwenne/networkx/commit/55688deb9a84bc7a77aecc556a63ff80dc41c56f)

## Future Involvement with NetworkX

Overall, I really enjoyed this Summer of Code.
I was able to branch out, continue to learn python and more about graphs and graph algorithms which is an area of interest for me.

Assuming that I have any amount of free time this coming fall semester, I'd love to stay involved with NetworkX.
In fact, there are already some things that I have in mind even though my current code works as is.

* Move `sample_spanning_tree` to `mst.py` and rename it to `random_spanning_tree`.
  The ability to sample random spanning trees is not a part of the greater NetworkX library and could be useful to others.
  One of my mentors mentioned it being relevant to [Steiner trees](https://en.wikipedia.org/wiki/Steiner_tree_problem) and if I can help other developers and users out, I will.
* Adapt `sample_spanning_tree` so that it can use both additive and multiplicative weight functions.
  The Asadpour algorithm only needs the multiplicative weight, but the Kulkarni paper [5] does talk about using an additive weight function which may be more useful to other NetworkX users.
* Move my Krichhoff's Tree Matrix Theorem helper function to `laplacian_matrix.py` so that other NetworkX users can access it.
* Investigate the following article about the Held Karp relaxation.
  While I have no definite evidence for this one, I do believe that the Held Karp relaxation is the slowest part of my implementation of the Asadpour algorithm and thus is the best place for improving it.
  The ascent method I am using comes from the original Held and Karp paper [3], but they did release a part II which may have better algorithms in it.
  The citation is given below.
  
  M. Held, R.M. Karp, *The traveling-salesman problem and minimum spanning trees: Part II*. Mathematical Programming, 1971, 1(1), p. 6–25. [https://doi.org/10.1007/BF01584070](https://doi.org/10.1007/BF01584070)
* Refactor the `Edmonds` class in `branchings.py`.
  That class is the implementation for Edmonds' branching algorithm but uses an iterative approach rather than the recursive one discussed in Edmonds' paper [2].
  I did also agree to work with another person, [lkora](https://github.com/lkora) to help rework this class and possible add a `minimum_maximal_branching` function to find the minimum branching which still connects as many nodes as possible. 
  This would be analogous to a spanning forest in an undirected graph.
  At the moment, neither of us have had time to start such work.
  For more information please reference issue [#4836](https://github.com/networkx/networkx/issues/4836).

While there are areas of this problem which I can improve upon, it is important for me to remember that this project was still a complete success. 
NetworkX now has an algorithm to approximate the traveling salesman problem in asymmetric or directed graphs.


