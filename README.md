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

## Previewing posts

While editing your posts, you can preview the results by running:

```
make serve
```

The server usually appears at http://localhost:1313 (unless port 1313
is already taken).

Remember, if you are editing notebooks, you need to run `make executed_notebooks`
before changes will appear.
