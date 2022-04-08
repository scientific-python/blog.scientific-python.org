---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: false
description: "
This post is awesome read it!
"
tags: ["tutorials", [library]]
displayInList: true
author: ["Bob"]

resources:
- name: featuredImage
  src: "my-image.png"
  params:
    description: "my image description"
    showOnTop: true
---

Some cool description before jumping in maybe?

## New cool Post

[Link](https://blog.scientific-python.org).

Here is some code

```python
import numpy as np
...
```

And maybe you need inline maths like $A=\pi r^2$, or more prominent equations:

$$ \sum_0^1 x $$

### Images

Images must be in PNG and compressed using a tool like `pngcrush` or
`pngquant`. For instance:

```bash
pngquant --ext .png --force my_figure.png
```

Another important aspect is alt-text. All figures must include alt-text.
This is very important for inclusiveness.

![my image description](my-image.png)
