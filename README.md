## Authoring blog posts

Add a new directory to `./content` names as follows `2022-02-28-topic-of-your-choice`.

Use YYYY-MM-DD. The post will appear on the blog at:

```
/2022/02/28/topic-of-your-choice/
```

Inside the new folder, place an `index.md`:

```markdown
---
title: This is a test blog post
author: ["Your name here"]
---

Write your content here.

## A Heading

Some more content.
```

## Authoring using notebooks

Create the blog post directory as above.  Instead of `index.md`, add a
file called `notebook.md`.  In it, place:

```markdown
---
title: Example notebook post
author: ["Your Name Here"]

jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
  kernelspec:
    display_name: Python
    language: python
    name: python
---

Blog post content.

## Another heading

Some more content.
```

You can edit this notebook as a markdown file, or [edit it in Jupyter using Jupytext](https://jupytext.readthedocs.io/en/latest/install.html#jupytext-s-contents-manager).

To execute your notebook, type `make executed_notebooks`.

**NOTE:** **Do** commit `index.ipynb`, `index.md`, and
`index_files`—this is the generate blog post, and we'd like to store
those contents in the repository.

**NOTE:** Do not edit the resulting `index.ipynb`—this file will be overwritten during notebook execution.

## Previewing posts

While editing your posts, you can preview the results by running:

```
make serve
```

The server usually appears at http://localhost:1313 (unless port 1313
is already taken).

Remember, if you are editing notebooks, you need to run `make
executed_notebooks` before changes will appear.
