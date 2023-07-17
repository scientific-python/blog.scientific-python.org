---
title: "Finalizing the Held-Karp Relaxation"
date: 2020-07-07
draft: false
description: "Picking which method to use for the final implementation of the Asadpour algorithm in NetworkX"
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

This _should_ be my final post about the Held-Karp relaxation!
Since my last post titled [Implementing The Held Karp Relaxation]({{< relref "implementing-the-held-karp-relaxation" >}}), I have been testing both the ascent method as well as the branch and bound method.

My first test was to use a truly asymmetric graph rather than a directed graph where the cost in each direction happened to be the same.
In order to create such a test, I needed to know the solution to any such proposed graphs.
I wrote a python script called `brute_force_optimal_tour.py` which will generate a random graph, print its adjacency matrix and then check every possible combination of edges to find the optimal tour.

```python
import networkx as nx
from itertools import combinations
import numpy as np
import math
import random


def is_1_arborescence(G):
    """
    Returns true if `G` is a 1-arborescence
    """
    return (
        G.number_of_edges() == G.order()
        and max(d for n, d in G.in_degree()) <= 1
        and nx.is_weakly_connected(G)
    )


# Generate a random adjacency matrix
size = (7, 7)
G_array = np.empty(size, dtype=int)
random.seed()
for r in range(size[0]):
    for c in range(size[1]):
        if r == c:
            G_array[r][c] = 0
            continue
        G_array[r][c] = random.randint(1, 100)

# Print that adjacency matrix
print(G_array)

G = nx.from_numpy_array(G_array, create_using=nx.DiGraph)
num_nodes = G.order()

combo_count = 0
min_weight_tour = None
min_tour_weight = math.inf
test_combo = nx.DiGraph()
for combo in combinations(G.edges(data="weight"), G.order()):
    combo_count += 1
    test_combo.clear()
    test_combo.add_weighted_edges_from(combo)
    # Test to see if test_combo is a tour.
    # This means first that it is an 1-arborescence
    if not is_1_arborescence(test_combo):
        continue
    # It also means that every vertex has a degree of 2
    arborescence_weight = test_combo.size("weight")
    if (
        len([n for n, deg in test_combo.degree if deg == 2]) == num_nodes
        and arborescence_weight < min_tour_weight
    ):
        # Tour found
        min_weight_tour = test_combo.copy()
        min_tour_weight = arborescence_weight

print(
    f"Minimum tour found with weight {min_tour_weight} from {combo_count} combinations of edges\n"
)
for u, v, d in min_weight_tour.edges(data="weight"):
    print(f"({u}, {v}, {d})")
```

## Everything is Cool with the Ascent Method

This is useful information as every though the ascent method returns a vector, because if the ascent method returns this solution (a.k.a \\(f(\pi) = 0\\)) we can calculate that vector off of the edges in the solution without having to explicitly enumerate the dict returned by `held_karp_ascent()`.

The first output from the program was a six vertex graph and is presented below.

```
~ time python3 brute_force_optimal_tour.py
[[ 0 45 39 92 29 31]
 [72  0  4 12 21 60]
 [81  6  0 98 70 53]
 [49 71 59  0 98 94]
 [74 95 24 43  0 47]
 [56 43  3 65 22  0]]
Minimum tour found with weight 144.0 from 593775 combinations of edges

(0, 5, 31)
(5, 4, 22)
(1, 3, 12)
(3, 0, 49)
(2, 1, 6)
(4, 2, 24)

real	0m9.596s
user	0m9.689s
sys     0m0.241s
```

First I checked that the ascent method was returning a solution with the same weight, 144, which it was.
Also, every entry in the vector was \\(0.866\overline{6}\\) which is \\(\frac{5}{6}\\) or the scaling factor from the Asadpour paper so I know that it was finding the exact solution.
Because if this, my test in `test_traveling_salesman.py` checks that for all edges in the solution edge set both \\((u, v)\\) and \\((v, u)\\) are equal to \\(\frac{5}{6}\\).

For my next test, I created a \\(7 \times 7\\) matrix to test with, and as expected the running time of the python script was much slower.

```
~ time python3 brute_force_optimal_tour.py
[[ 0 26 63 59 69 31 41]
 [62  0 91 53 75 87 47]
 [47 82  0 90 15  9 18]
 [68 19  5  0 58 34 93]
 [11 58 53 55  0 61 79]
 [88 75 13 76 98  0 40]
 [41 61 55 88 46 45  0]]
Minimum tour found with weight 190.0 from 26978328 combinations of edges

(0, 1, 26)
(1, 3, 53)
(3, 2, 5)
(2, 5, 9)
(5, 6, 40)
(4, 0, 11)
(6, 4, 46)

real	7m28.979s
user	7m29.048s
sys     0m0.245s
```

Once again, the value of \\(f(\pi)\\) hit 0, so the ascent method returned an exact solution and my testing procedure was the same as for the six vertex graph.

## Trouble with Branch and Bound

The branch and bound method was not working well with the two example graphs I generated.
First, on the seven vertex matrix, I programmed the test and let it run... and run... and run... until I stopped it at just over an hour of execution time.
If it took one eight of that time to brute force the solution, then the branch and bound method truly is not efficient.

I moved to the six vertex graph with high hopes, I already had a six vertex graph which was correctly executing in a reasonable amount of time.
The six vertex graph created a large number of exceptions and errors when I ran the tests.
I was able to determine why the errors were being generated, but the context did not conform which my expectations for the branch and bound method.

Basically, `direction_of_ascent_kilter()` was finding a vertex which was out-of-kilter and returning the corresponding direction of ascent, but `find_epsilon()` was not finding any valid cross over edges and returning a maximum direction of travel of \\(\infty\\).
While I could change the default value for the return value of `find_epsilon()` to zero, that would not solve the problem because the value of the vector \\(\pi\\) would get stuck and the program would enter an infinite loop.

I do have an analogy for this situation.
Imagine that you are in an unfamiliar city and you have to meet somebody at the tallest building in that city.
However, you don't know the address and have no way to get a GPS route to that building.
Instead of wandering around aimlessly, you decide to scan the skyline for the tallest building you can see and start walking down the street which is the closest to matching that direction.
Additionally, you have the ability to tell at any given direction how far down the chosen street to go before you need to re-evaluate and pick a new street.

This hypothetical is a better approximation of the ascent method, but the problem here can be demonstrated non the less.

- Determining if you are at the tallest building is running the linear program to see if the direction of ascent still exists.
- Picking the street to go down is the same as finding the direction of ascent.
- Finding out how far to go down that street is the same as finding epsilon.

After this procedure works for a while, you suddenly find yourself in an unusual situation.
You can still see the tallest building, so you know you are not there yet.
You know what street will take you closer to the building, but for some reason you cannot move down that street.

From my understanding of the ascent and branch and bound methods, if the direction of ascent exists, then we have to be able to move some amount in that direction without fail, but the branch and bound method was failing to provide an adequate distance to move.

Considering the trouble with the branch and bound method, and that it is not going to be used in the final Asadpour algorithm, I plan on removing it from the NetworkX pull request and moving onwards using only the ascent method for the rest of the Ascent method.

## References

A. Asadpour, M. X. Goemans, A. Mardry, S. O. Ghran, and A. Saberi, _An o(log n / log log n)-approximation algorithm for the asymmetric traveling salesman problem_, Operations Research, 65 (2017), pp. 1043-1061.

M. Held, R. M. Karp, _The traveling-salesman problem and minimum spanning trees_. Operations research, 1970-11-01, Vol.18 (6), p.1138-1162. [https://www.jstor.org/stable/169411](https://www.jstor.org/stable/169411)
