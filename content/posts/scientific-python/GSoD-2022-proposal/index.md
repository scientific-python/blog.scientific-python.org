---
title: "Scientific Python GSoD 2022 Proposal"
date: 2022-03-25
draft: false
tags: ["GSoD", "Scientific-Python", "proposal"]
description: "Create educational content for the Scientific Python Blog"
displayInList: true
author: ["Jarrod Millman"]
---

## Create educational content for the Scientific Python Blog

## About your organization

With an extensive and high-quality ecosystem of libraries, scientific Python
has emerged as the leading platform for data analysis.
This ecosystem is sustained largely by volunteers working on independent
projects with separate mailing lists, websites, roadmaps, documentation,
engineering and packaging solutions, and governance structures.

The Scientific Python project aims to better coordinate the ecosystem and
prepare the software projects in this ecosystem for the next decade of data
science.

## About your project

### Your project’s problem

There is no shortage of blog posts around the web about how to use and explore
different packages in the scientific Python ecosystem.
However, some of it is outdated or incomplete, and many times doesn't follow
the best practices that would be advocated for by the maintainers of these
packages.

In addition, we would like to create a central, _community-driven_ location where
Scientific Python projects can make announcements and share information.

Our project aims to be the definitive community blog---for people looking
to make use of these libraries in education, research and industry, contribute
to them, or maintain them---written, reviewed, and approved by the community
of developers and users.

While our core projects (NumPy, SciPy, Matplotlib, scikit-image, NetworkX, etc.)
will be regularly contributing content, we also would like to increase the number of
contributors by providing support to newer members to generate high-quality,
peer-reviewed blog posts.

### Your project’s scope

<!--
*Tell us about what documentation your organization will create, update, or improve. If some work is deliberately not being done, include that information as well. Include a time estimate, and whether you have already identified organization volunteers and a technical writer to work with your project.*
-->

Our goal is to populate the https://blog.scientific-python.org/ website with
high-quality content, reviewed and approved by the maintainers of the
libraries in the ecosystem.
The main goal of these documents is to centralize information relevant to all
(or most) projects in the ecosystem, at the reduced cost of being maintained in
one place.

This project aims to:

- Create content for the https://blog.scientific-python.org/ website

To ensure this project is successful, it is recommended that the technical
writer has some familiarity with at least a few of Scientific Python's
[core projects](https://scientific-python.org/specs/core-projects).

### Measuring your project’s success

<!--
*How will you know that your new documentation has helped solve your problem? What metrics will you use, and how will you track them?*
-->

We would consider the project successful if:

- At least 3 blog posts were published on blog.scientific-python.org,
  by each of the technical writers.
- Improved submission and review guide

### Timeline

We anticipate the project to be developed over six months including onboarding
five technical writers, reviewing existing material, developing blog post ideas with
the project mentors and blog editorial board, writing and revising the
blog posts, as well as providing feedback on the submission and review process.

<!-- prettier-ignore-start -->
{{< yamlToTable >}}
headers:
  - Dates
  - Action Items

format:
  - align: left
  - align: right

rows:
  - columns:
    - May
    - Onboarding

  - columns:
    - June
    - Review existing documentation

  - columns:
    - July
    - Update contributor guide

  - columns:
    - August--October
    - Create and edit content

  - columns:
    - November
    - Project completion
{{< /yamlToTable >}}
<!-- prettier-ignore-end -->

## Project budget

<!-- prettier-ignore-start -->
{{< yamlToTable >}}
headers:
  - Budget item
  - Amount
  - Running Total
  - Notes/justifications

rows:
  - columns:
    - Technical writers (5)
    - $15,000.00
    - $15,000.00
    - $3,000 / writer

  - columns:
    - TOTAL
    -
    - $15,000.00
    -

{{< /yamlToTable >}}
<!-- prettier-ignore-end -->

### Additional information

<!--
*Include here any additional information that is relevant to your proposal.*

*- Previous experience with technical writers or documentation: If you or any of your mentors have worked with technical writers before, or have developed documentation, mention this in your application. Describe the documentation that you produced and the ways in which you worked with the technical writer. For example, describe any review processes that you used, or how the technical writer's skills were useful to your project. Explain how this previous experience may help you to work with a technical writer in Season of Docs.*
*- Previous participation in Season of Docs, Google Summer of Code or others: If you or any of your mentors have taken part in Google Summer of Code or a similar program, mention this in your application. Describe your achievements in that program. Explain how this experience may influence the way you work in Season of Docs.*
-->

The Scientific Python project is a new initiative, and this is our first time
participating in Google Season of Docs.
However, both Jarrod Millman and Ross Barnowski are established members of the
Python community, with a vast collective experience in mentoring, managing and
maintaining large open source projects.

Jarrod cofounded the Neuroimaging in Python project. He was the NumPy and SciPy
release manager from 2007 to 2009. He cofounded NumFOCUS and served on its board
from 2011 to 2015. Currently, he is the release manager of NetworkX and cofounder
of the Scientific Python project.

Both mentors Jarrod and Ross have mentored many new
contributors on multiple projects including NumPy, SciPy, and NetworkX.
Ross has served as a co-mentor for three former GSoD students on the NumPy
project, largely related to generating new content for tutorials, as well as
refactoring existing user documentation.

Links:

- https://scientific-python.org/
- https://blog.scientific-python.org/
- https://github.com/scientific-python/
