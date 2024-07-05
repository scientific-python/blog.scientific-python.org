---
title: "PyPalettes: all the colors you'll ever need"
description: "In matplotlib, when you create a chart, you can somehow becomes quite limited in terms of colors. Libraries such as matplotlib and seaborn have some built-in colormaps (like viridis, inferno etc), but it gives all the charts outside the exact same look. And that's where PyPalettes appears: thousands of pre-made palettes with good color matching and a web app to browse and preview all of them!"
date: 2024-07-10T21:37:03-04:00
tags: ["matplotlib", "color", "colormap"]
displayInList: true
author: ["Joseph Barbier", "Yan Holtz"]
draft: false
resources:
  - name: featuredImage
    src: "preview.png"
    params:
      description: "pypalettes library"
      showOnTop: false
---

## Finding the right color has never been easier

Recently (June 2024), the [pypalettes library](https://github.com/JosephBARBIERDARNAL/pypalettes), a Python tool for working with colormaps, was released. It provides mainly 2 things:

- a [super-easy-to-use library](https://github.com/JosephBARBIERDARNAL/pypalettes) that litteraly requires 1 line of code (in 99.99% cases, 2 otherwise 🙃) to have access to thousands of pre-defined and good looking palettes
- a [web app](https://python-graph-gallery.com/color-palette-finder/) to browse, filter, search and preview all the available palettes (and **bonus**: copy-pastable code to reproduce the charts)

_A small sample of the available palettes_[![Preview and try all the palettes](https://github.com/holtzy/The-Python-Graph-Gallery/raw/master/static/asset/pypalettes.gif)](https://python-graph-gallery.com/color-palette-finder/)

<br>

## How it happened

In R, there are dozens of packages dedicated to colors for data visualization. Then [Paletteer](https://emilhvitfeldt.github.io/paletteer/) came out to **aggregate** every color palette from those packages into a single one, meaning you **only need one package** to access almost all the color palettes people have created!

While re-crafting the [colors section of the Python Graph Gallery](https://python-graph-gallery.com/python-colors/), I started thinking of a way to have a similar tool to Paletteer but for Python.

<center><h3 style="color: lightgray;">That's where PyPalettes comes in.</h3></center>

Basically, I scraped 2 websites:

- the [Paletteer gallery](https://pmassicotte.github.io/paletteer_gallery/), which contains all palettes from Paletteer with hexadecimal colors, palette names, and package sources.
- [coolors.co](https://coolors.co/), another website with cool palettes.

With these, I was able to create a dataset with around **2500 different palettes**, each with a name and a list of hexadecimal colors.

At this point, the hardest part was already done. I just had to create a simple API to make them usable in a Python environment and add some additional simple features.

<br>

## How to use it

The goal was to make the simplest API possible, and I'm quite satisfied with the result. For example, I really like the [Ingres palette](https://python-graph-gallery.com/color-palette-finder/?palette=ingres), and I want to make a chart with it.

First, you import the `load_cmap()` function (the main function of the library):

```python
from pypalettes import load_cmap
```

And then you just have to call this function with `name="Ingres"`

```python
cmap = load_cmap("Ingres")
```

The output of `load_cmap()` is either a [matplotlib.colors.ListedColormap](https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.ListedColormap.html) or a [matplotlib.colors.LinearSegmentedColormap](https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html), depending on the value of the `type` argument (default is `"discrete"`, so it's `ListedColormap` in this case).

Finally, you can create your chart as you normally would:

```python
# load libraries
import geopandas as gpd
import matplotlib.pyplot as plt
from pypalettes import load_cmap

# load the world dataset
df = gpd.read_file(
    "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/all_world.geojson"
)
df = df[~df["name"].isin(["Antarctica"])]

fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
ax.set_axis_off()
df.plot(
    ax=ax,
    cmap=cmap,  # here we pass the colormap loaded before
    edgecolor="white",
    linewidth=0.3,
)

plt.show()
```

<center>

![](map.png)

</center>

And once the code is working, you can change the color map name and see straight away what it would look like!

<br>

## Other usages

PyPalettes is primarily designed for `matplotlib` due to its **high compatibility** with the `cmap` argument, but one can imagine **much more**.

For example, it also provides the `get_hex()` and `get_rgb()` functions that return a list of hexadecimal colors or RGB values that can then be used in any context: other Python visualization libraries (plotly, plotnine, altair), colorimetry, image processing, or anything that requires color!

<br>

## Learn more

The main links to find out more about this project are as follows:

- the [web app](https://python-graph-gallery.com/color-palette-finder/) to browse the palettes
- the [Github repo](https://github.com/JosephBARBIERDARNAL/pypalettes) with source code and palettes (give us a star! ⭐)
- this [introduction to PyPalettes](https://python-graph-gallery.com/introduction-to-pypalettes/) for a more in-depth code explanation
