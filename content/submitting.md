---
title: "Submitting a Post"
url: /submitting
---

## Scope

We publish quality blog posts covering packages part of the Scientific Python
Ecosystem. While we focus on showcasing great use of the packages, we are also
interested in the non-coding or technical side of projects.

We love code examples. While a fair quality is expected, we focus more on the
story than on the code and are less nitpicky that what you would expect
when submitting code to a major library. Still, best practices are to be
observed (both in terms of general Python construction, style and also
in terms of good practices using libraries) and the reviewers make sure of
this point.

We do not accept any sponsored or promotional article. It is accepted to
mention your organization, but it must not be the focus of the article.

At a bare minimum, submissions must:

- The main subject relates to at least one project affiliated to the
  Scientific Python Ecosystem.
- Authors have the right to publish the content under BSD 3-Clause
  License for the code and Creative Common CC-BY-4.0 License for the text.
- Respect our
  [code of conduct](https://scientific-python.org/code_of_conduct/).
- Be written in English.

## Submit a Post

Anyone is welcome to submit a blog post and very little technical
knowledge is required.

We use GitHub to manage post submissions. To create a submission, open a pull
request (PR) on our Git repository:

https://github.com/scientific-python/blog.scientific-python.org/pulls

If you are new to GitHub, see
[here](https://learn.scientific-python.org/contributors/setup/git-intro/)
for more information on how to make a PR.

A few extra notes.

- This project is using pre-commit hooks. The hooks will
  be installed automatically when you will build the blog.
- Do not rebase or force push on your branch. Only merge it with `main` if you
  need to get the latest version. This prevents past reviews to get out of
  sync with your branch.

## Create a Post

The blog uses [Hugo](https://gohugo.io/) to create and render the blog.
For a better experience, we recommend you to
[install it](https://gohugo.io/getting-started/quick-start/#step-1-install-hugo)
on your local machine. This will allow you to build the blog and see
how your post would look like.

**Note:** you will be able to see a rendered version of the blog with your
content when making a PR.

Type the following to create a new post, where `[library]` is one of the
affiliated project (see existing content for example):

```bash
hugo new content/posts/[library]/[title]/index.md
```

This command will create a new folder under `folder_repository/content/posts/[library]`.
This will be your working directory for the post. If you want to add external
content to your post (e.g., images), you will add it to this folder.

You can now open the file _index.md_ in your post folder with your favorite
text editor. It is filled with some basics to help you get started.

### Preamble

You will see a header section delimited by ---. Let us go through
all the headings you can configure:

```
title: "Your fancy title"
```

This is the title of your post that will appear at the beginning of the page.
Pick a catchy one.

```
date: 2019-09-01T21:37:03-04:00
```

The current date and time, you do not need to modify this.

```
draft: true
```

Specify if the post is a draft or not.

```
description: "This is my first post contribution."
```

This is a long description of the topic of your post. Modify it according to
your content.

```
tags: ["tutorials", [library]]
```

Pick the category you want your post to be added to. Reviewers will help with
that.

```
displayInList: true
```

Specify that you want your post to appear in the list of latest posts and in
the list of posts of the specified category.

```
author: ["Bob"]
```

Add your name as author. Multiple authors are separated by commas.

```
resources:
- name: featuredImage
  src: "my-image.png"
  params:
    description: "my image description"
    showOnTop: true
```

Select an image to be associated to your post, which will appear aside the
title in the homepage. Make sure to add _my-image.png_ to your post folder.
The parameter _showOnTop_ decides whether the image will also be shown
at the top of your post.

### Write!

Now, you can write the main text of your post. We fully support
[markdown](https://markdown-guide.readthedocs.io/en/latest/basics.html),
so use it to format your post.

To preview your new post, open a terminal and type:

```bash
make serve
```

Then open the browser and visit [http://localhost:1313](http://localhost:1313)
to make sure your post appears in the homepage. If you spot errors or something
that you want to tune, go back to your `index.md` file and modify it.
If you are editing notebooks, you need to run `make executed_notebooks`
before changes will appear.

### Images

Images must be in PNG and compressed using a tool like `pngcrush` or
`pngquant`. For instance:

```bash
pngquant --ext my_figure.png --force
```

Another important aspect is alt-text. All figures must include alt-text.
This is very important for inclusiveness.
