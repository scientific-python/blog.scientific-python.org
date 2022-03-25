---
layout: post
usemathjax: true
---
In linear programming, we sometimes need to take what would be a integer program and 'relax' it, or unbound the values of the variables so that they are continuous.
One particular application of this process is Held-Karp relaxation used the first part of the Asadpour algorithm for the Asymmetric Traveling Salesman Problem, where we find the lower bound of the approximation.
Normally the relaxation is written as follows.

$$ 
\begin{array}{c l l}
\text{min} & \sum_{a} c(a)x_a \\
\text{s.t.} & x(\delta^+(U)) \geqslant 1 & \forall\ U \subset V \text{ and } U \not= \emptyset \\
& x(\delta^+(v)) = x(\delta^-(v)) = 1 & \forall\ v \in V \\
& x_a \geqslant 0 & \forall\ a
\end{array}
$$


This is a convenient way to write the program, but if we want to solve it, and we definitely do, we need it written in standard form for a linear program.
Standard form is represented using a matrix for the set of constraints and vectors for the objective function. 
It is shown below

$$
\begin{array}{c l}
\text{min} & Z = c^TX \\
\text{s.t.} & AX = b \\
& X \geqslant 0
\end{array}
$$

Where $$c$$ is the coefficient vector for objective function, $$X$$ is the vector for the values of all of the variables, $$A$$ is the coefficient matrix for the constraints and $$b$$ is a vector of what the constraints are equal to.
Once a linear program is in this form there are efficient algorithms which can solve it.

In the Held-Karp relaxation, the objective function is a summation, so we can expand it to a summation.
If there are $$n$$ edges then it becomes

$$
\sum_{a} c(a)x_a = c(1)x_1 + c(2)x_2 + c(3)x_3 + \dots + c(n)_n
$$

Where $$c(a)$$ is the weight of that edge in the graph.
From here it is easy to convert the objective function into two vectors which satisfies the standard form.

$$
\begin{array}{rCl}
c &=& \begin{bmatrix}
c_1 & c_2 & c_3 & \dots & c_n
\end{bmatrix}^T \\
X &=& \begin{bmatrix}
x_1 & x_2 & x_3 & \dots & x_n
\end{bmatrix}^T
\end{array}
$$

Now we have to convert the constraints to be in standard form.
First and foremost, notice that the Held-Karp relaxation contains $$x_a \geqslant 0\ \forall\ a$$ and the standard form uses $$X \geqslant 0$$, so these constants match already and no work is needed.
As for the others... well they do need some work.

Starting with the first constraint in the Held-Karp relaxation, $$x(\delta^+(U)) \geqslant 1\ \forall\ U \subset V$$ and $$U \not= \emptyset$$.
This constraint specifies that for every subset of the vertex set $$V$$, that subset must have at lest one arc with its tail in $$U$$ and its head not in $$U$$.
For any given $$\delta^+(U)$$, which is defined in the paper is $$\delta^+(U) = \{a = (u, v) \in A: u \in U, v \not\in U\}$$ where $$A$$ in this set is the set of all arcs in the graph, the coefficients on arcs not in $$U$$ are zero.
Arcs in $$\delta^+(U)$$ have a coefficient of $$1$$ as their full weight is counted as part of $$\delta^+(U)$$.
We know that there are about $$2^{|V|}$$ subsets of the vertex $$V$$, so this constraint adds that many rows to the constraint matrix $$A$$.

Moving to the next constraint, $$x(\delta^+(v)) = x(\delta^-(v)) = 1$$, we first need to split it in two.

$$
\begin{array}{rCl}
x(\delta^+(v)) &=& 1 \\
x(\delta^-(v)) &=& 1 
\end{array}
$$

Similar to the last constraint, each of these say that the number of arcs entering and leaving a vertex in the graph need to equal one.
For each vertex $$v$$ we find all the arcs which start at $$v$$ and those are the members of $$\delta^+(v)$$, so they have a weight of 1 and all others have a weight of zero.
The opposite is true for $$\delta^-(v)$$, every vertex which has a head on $$v$$ has a weight or coefficient of 1 while the rest have a weight of zero.
This adds $$2 \times |V|$$ rows to $$A$$, the coefficient matrix which brings the total to $$2^{|V|} + 2|V|$$ rows.

The Impossible Size of $$A$$
----------------------------

We already know that $$A$$ will have $$2^{|V|} + 2|V|$$ rows.
But how many columns will $$A$$ have?
We know that each arc is a variable so at lest $$|E|$$ rows, but in a traditional matrix form of a linear program, we have to introduce slack and surplus variables so that $$AX = b$$ and not $$AX \geqslant b$$ or any other inequality operation. 
The $$2|V|$$ rows already comply with this requirment, but the rows created with every subset of $$V$$ do *not*, those rows only require that $$x(\delta^+(U)) \geqslant 1$$, so we introduce a surplus variable for each of these rows bring the column count to $$|E| + 2^{|V|}$$.

Now, the Held-Karp relaxation performed in the Asadpour algorithm in is done on the complete bi-directed graph.
For a graph with $$n$$ vertices, there will be $$2 \times \binom{n}{2}$$ arcs in the graph.
The  updated value for the size of $$A$$ is then that it is a 

$$
\left(2^n + 2n \right)\times \left(2\binom{n}{2} + 2^n\right)
$$

matrix.
This is *very* large.
For $$n = 100$$ there are $$1.606 \times 10^{60}$$ elements in the matrix.
Allocating a measly 8 bits per entry sill consumes over $$1.28 \times 10^{52}$$ gigabytes of memory.

This is an impossible amount of memory for any computer that we could run NetworkX on.

Solution
--------

The Held-Karp relaxation *must* be solved in the Asadpour Asymmertic Traveling Salesman Problem Algorithm, but clearly putting it into standard form is not possible.
This means that we will not be able to use SciPy's linprog method which I was hoping to use.
I will instead have to research and write an ellipsoid method solver, which hopefully will be able to solve the Held-Karp relaxation in both polynomial time and a practical amount of memory.


