---
title: "GSoC 2022: NetworkX VF2++ Implementation"
date: 2022-06-09
draft: false
description: "This is the first blog of my GSoC-2022 journey. It includes general information about me, and a superficial
description of the project."
tags: ["gsoc", "networkx"]
displayInList: true
author: ["Konstantinos Petridis"]

resources:
- name: featuredImage
  src: "GSoC_networkx_logo.png"
  params:
  description: "Google Summer of Code Logo with NetworkX logo"
  showOnTop: true

---

# Intro

I got accepted as a **GSoC** contributor, and I am so excited to spend the summer working on such an incredibly
interesting project. The mentors are very welcoming, communicative, fun to be around, and I really look forward to
collaborating with them. My application for GSoC 2022 can
be found [here](https://summerofcode.withgoogle.com/programs/2022/projects/V1hY83XG).

# About me

My name is Konstantinos Petridis, and I am an **Electrical Engineering** student at the Aristotle University of
Thessaloniki. I am currently on my 5th year of studies, with a **Major in Electronics & Computer Science**. Although a
wide range of scientific fields fascinate me, I have a strong passion for **Computer Science**, **Physics** and
**Space**. I love to study, learn new things and don't hesitate to express my curiosity by asking a bunch of questions
to the point of being annoying. You can find me on GitHub [@kpetridis24](https://github.com/kpetridis24).

# Project

The project I'll be working on, is the implementation of **VF2++**, a state-of-the-art algorithm used for the
[**Graph Isomorphism**](https://en.wikipedia.org/wiki/Graph_isomorphism) problem, which lies in the
[complexity class](https://en.wikipedia.org/wiki/Complexity_class) [**NP**](<https://en.wikipedia.org/wiki/NP_(complexity)>).
The functionality of the algorithm is similar to a regular, but
more complex form of a
[**DFS**](https://en.wikipedia.org/wiki/Depth-first_search), but performed on the possible solutions rather than the
graph nodes. In order to verify/reject the isomorphism between two graphs, we examine every possible candidate pair of
nodes
(one from the first and one from the second graph) and check whether going deeper into the DFS tree is feasible using
specific rules. In case of feasibility establishment, the DFS tree is expanded, investigating deeper pairs. When one
pair is not feasible, we go up the tree and follow a different branch, just like in a regular **DFS**. More details
about the algorithm can be found [here](https://doi.org/10.1016/j.dam.2018.02.018).

# Motivation

The major reasons I chose this project emanate from both my love for **Graph Theory**, and the fascinating nature of
this individual project. The algorithm itself is so recent, that **NetworkX** is possibly going to hold one of the first
implementations of it. This might become a reference that is going to help to further develop and optimize future
implementations of the algorithm by other organisations. Regarding my personal gain, I will become more familiar with
the open source communities and their philosophy, I will collaborate with highly skilled individuals and cultivate a
significant amount of experience on researching, working as a team, getting feedback and help when needed, contributing
to an actual scientific library.
