---
_build:
  list: never
---

# NetworkX posts

This directory contains the posts related to NetworkX.

## Mentored projects

Mentored projects include programs like Google Summer of Code (GSoC) or
Outreachy.
Students are often encouraged to write blog posts for these projects, and (in
the case of NetworkX) are further encourage to host their blogs on this site!
There are blog series related to several projects, including:

- **aTSP** - the Asadpour algorithm for the traveling salesman problem, by
  @mjschwenne (GSoC 2021)
- **vf2pp** - and implementation of the VF2++ algorithm, by @kpetridis24
  (GSoC 2022)

### Quickstart: adding a new blog series for a mentored project

If you are working on a new mentored project (e.g. GSoC) that will have
multiple posts, please create a new directory (e.g. `mkdir <my-project-name>`).
All the posts related to the project should then be created within that
directory.
Don't forget to add a project-specific tag to the `tags` field for your posts,
e.g.

```yaml
tags: ["gsoc", "networkx", "<my-project-name>"]
```
