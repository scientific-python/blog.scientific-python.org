---
title: "Held-Karp Seperation Oracle"
date: 2020-05-08
draft: false
description: "Considering creating a seperation oracle for the Held-Karp relaxation"
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

Continuing the theme of my last post, we know that the Held-Karp relaxation in the Asadpour Asymmetric Traveling Salesman Problem cannot be practically written into the standard matrix form of a linear program.
Thus, we need a different method to solve the relaxation, which is where the ellipsoid method comes into play.
The ellipsoid method can be used to solve semi-infinite linear programs, which is what the Held-Karp relaxation is.

One of the keys to the ellipsoid method is the separation oracle.
From the perspective of the algorithm itself, the oracle is a black-box program which takes a vector and determines

- Whether the vector is in the linear program's feasible region.
- If not, it returns a hyperplane with the given point on one side and the linear program's feasible region on the other.

In the most basic form, the ellipsoid method is a decision algorithm rather than an optimization algorithm, so it terminates once a single, but almost certainly nonoptimal, vector within the feasible region is found.
However, we can convert the ellipsoid method into an algorithm which is truly an optimization one.
What this means for us is that we can assume that the separation oracle will return a hyperplane.

The hyperplane that the oracle returns is then used to construct the next ellipsoid in the algorithm, which is of smaller volume and contains a half-ellipsoid from the originating ellipsoid.
This is, however, a topic for another post.
Right now I want to focus on this 'black-box' separation oracle.

The reason that the Held-Karp relaxation is semi-infinite is because for a graph with \\(n\\) vertices, there are \\(2^n + 2n\\) constraints in the program.
A naive approach to the separation oracle would be to check each constraint individually for the input vector, creating a program with \\(O(2^n)\\) running time.
While it would terminate eventually, it certainly would take a _long_ time to do so.

So, we look for a more efficient way to do this.
Recall from the Asadpour paper [1] that the Held-Karp relaxation is the following linear program.

\\[
\begin{array}{c l l}
\text{min} & \sum_{a} c(a)x_a \\\\\\
\text{s.t.} & x(\delta^+(U)) \geqslant 1 & \forall\ U \subset V \text{ and } U \not= \emptyset \\\\\\
& x(\delta^+(v)) = x(\delta^-(v)) = 1 & \forall\ v \in V \\\\\\
& x_a \geqslant 0 & \forall\ a
\end{array}
\\]

The first set of constraints ensures that the output of the relaxation is connected.
This is called _subtour elimination_, and it prevents a solution with multiple disconnected clusters by ensuring that every set of vertices has at least one total outgoing arc (we are currently dealing with fractional arcs).
From the perspective of the separation oracle, we do not care about all of the sets of vertices for which \\(x(\delta^+(U)) \geqslant 1\\), only trying to find one such subset of the vertices where \\(x(\delta^+(U)) < 1\\).

In order to find such a set of vertices \\(U \in V\\) where \\(x(\delta^+(U)) < 1\\) we can find the subset \\(U\\) with the smallest value of \\(\delta^+(x)\\) for all \\(U \subset V\\).
That is, find the _global minimum cut_ in the complete digraph using the edge capacities given by the input vector to the separation oracle.
Using lecture notes by Michel X. Goemans (who is also one of the authors of the Asadpour algorithm this project seeks to implement), [2] we can find such a minimum cut with \\(2(n - 1)\\) maximum flow calculations.

The algorithm described in section 6.4 of the lecture notes [2] is fairly simple.
Let \\(S\\) be a subset of \\(V\\) and \\(T\\) be a subset of \\(V\\) such that the \\(s-t\\) cut is the global minimum cut for the graph.
First, we pick an arbitrary \\(s\\) in the graph.
By definition, \\(s\\) is either in \\(S\\) or it is in \\(T\\).
We now iterate through every other vertex in the graph \\(t\\), and compute the \\(s-t\\) and \\(t-s\\) minimum cut.
If \\(s \in S\\) than we will find that one of the choices of \\(t\\) will produce the global minimum cut and the case where \\(s \not\in S\\) or \\(s \in T\\) is covered by using the \\(t-s\\) cuts.

According to Geoman [2], the complexity of finding the global min cut in a weighted digraph, using an effeicent maxflow algorithm, is \\(O(mn^2\log(n^2/m))\\).

The second constraint can be checked in \\(O(n)\\) time with a simple loop.
It makes sense to actually check this one first as it is computationally simpler and thus if one of these conditions are violated we will be able to return the violated hyperplane faster.

Now we have reduced the complexity of the oracle from \\(O(2^n)\\) to the same as finding the global min cut, \\(O(mn^2\log(n^2/m))\\) which is substantially better.
For example, let us consider an initial graph with 100 vertices.
Using the \\(O(2^n)\\) method, that is \\(1.2677 \times 10^{30}\\) subsets \\(U\\) that we need to check _times_ whatever the complexity of actually determining whether the constraint violates \\(x(\delta^+(U)) \geqslant 1\\).
For that same complete digraph on 100 vertices, we know that there \\(n = 100\\) and \\(m = \binom{100}{2} = 4950\\).
Using the global min cut approach, the complexity which includes finding the max flow as well as the number of times it needs to be found, is \\(15117042\\) or \\(1.5117 \times 10^7\\) which is faster by a factor of \\(10^{23}\\).

## References

[1] A. Asadpour, M. X. Goemans, A. Mardry, S. O. Ghran, and A. Saberi, _An o(log n / log log n)-approximation algorithm for the asymmetric traveling salesman problem_, Operations Research, 65 (2017), pp. 1043-1061, [https://homes.cs.washington.edu/~shayan/atsp.pdf](https://homes.cs.washington.edu/~shayan/atsp.pdf).

[2] M. X. Goemans, _Lecture notes on flows and cuts_, Handout 18, Massachusetts Institute of Technology, Cambridge, MA, 2009 [http://www-math.mit.edu/~goemans/18433S09/flowscuts.pdf](http://www-math.mit.edu/~goemans/18433S09/flowscuts.pdf).
