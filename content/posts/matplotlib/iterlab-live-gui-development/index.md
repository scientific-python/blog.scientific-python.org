---
title: "Matplotlib GUIs drawn, not programmed, and edited without restarting: faster iteration for scientific research"
date: 2026-10-18T10:59:51-04:00
draft: false
description: "
Scientific coding runs in a loop: load the data, plot it, change something, plot it again.
iterlab is a small library built on matplotlib and Tk that shortens that loop: you draw the
interface instead of programming it, and the Python process never restarts when you edit your
code, so loaded data and drawn plots survive every change.
"
tags: ["tutorials", "matplotlib", "iterlab", "interactive"]
displayInList: true
authors: ["Alon"]

resources:
  - name: featuredImage
    src: "iterlab-loop.png"
    params:
      description: "Three panels linked by arrows: a running iterlab interface with three matplotlib plots (sine waves, a scatter plot and a bar chart) and input boxes; the same interface open in the layout editor as labelled rectangles; and the Python function that draws the scatter plot."
      showOnTop: true

summary: |
  [iterlab](https://github.com/alonhzn/iterlab) treats the GUI as a place to *develop* an
  algorithm rather than a wrapper added at the end. The layout is drawn on a canvas, every plot
  is a real matplotlib `Axes`, and edits to your code take effect in the open window without
  restarting Python or reloading your data.
---

Most of the time I spend on scientific code is not spent writing it. It goes into a loop that
looks something like this:

1. Edit a constant, a filter width, an axis label.
2. Re-run the script.
3. Wait for the data to load again.
4. Wait for the expensive preprocessing to run again.
5. Close the old figures, look at the new ones, and decide what to change next.

Steps 2 to 4 carry no information. They exist because the process that held my data died when I
changed one line. With a few gigabytes of spectra, or a fit that takes a minute, that dead time
becomes most of the working day.

An interactive interface ought to help, with a number box for the filter width and a button to
refit, but building one costs more than it saves. Writing Tk or Qt layout code for a figure you
will throw away next week is rarely worth it, so the parameters stay hard-coded and the loop goes
on.

[iterlab](https://github.com/alonhzn/iterlab) is my attempt to fix both halves of this at once. It
is a small library, built on matplotlib and Tk, for a way of working that MATLAB users will
recognise from GUIDE and App Designer but that is rare in Python: **the GUI is the development
environment for the algorithm**, not something added once the algorithm works.

## Three ideas

**The interface is drawn, not programmed.** You drag plot areas, buttons, text boxes and number
boxes onto a canvas and give each one a tag. No widget code is written.

**The code is live.** Your algorithm lives in an ordinary Python file. Edit a function and save it,
click a button in the window that is already open, and the new version runs.

**Python never restarts.** Data you loaded, results you computed and plots you drew all survive code
edits, mistakes included. A syntax error or an exception is reported in the window, and the session
carries on so you can fix it and continue.

If you would rather watch than read, this short introduction shows the whole loop in action:

{{< youtube id="G_HzmkInHAs" title="iterlab introduction: drawing an interface and editing its code without restarting" >}}

## A first interface

```console
pip install iterlab
iterlab demo
```

Because `demo` does not exist yet, iterlab creates two files side by side and opens the layout
editor:

```
demo_layout.py   what you drew (iterlab owns and rewrites this file)
demo.py          your code (you own this; iterlab only ever appends to it)
```

Keeping them separate is deliberate. Rearranging the interface cannot break your code, and editing
your code cannot break the interface. The only link between them is each element's tag.

Draw an axes tagged `spectrum` and a button tagged `run_fit`. iterlab appends a handler stub for the
button to `demo.py`, and you fill it in:

```python
import numpy as np


def on_startup(ev):
    # Runs once per session: put the expensive loading here.
    ev.x = np.linspace(0, 10, 500)
    ev.spectrum.plot(ev.x, np.sin(ev.x))


def on_clicked_run_fit(ev, event):
    ev.spectrum.clear()
    ev.spectrum.plot(ev.x, np.sin(2 * ev.x))
```

Click **Run it** and the canvas becomes your interface. Now comes the part that matters: **leave the
window open**, change the `2` to a `5`, save, and click the button again. The new curve appears, and
`ev.x` was never rebuilt. In a real project that line would be `np.load` on a large file or a
preprocessing step that takes minutes, and it still runs only once.

The model is small enough to fit in a table:

| | |
|---|---|
| `ev` | The session. Anything you assign to it lives until you reset or close the window. |
| `ev.<tag>` | The live element you drew, reached by its tag. |
| `on_<interaction>_<tag>(ev, event)` | A handler. Define it and it is wired; there is nothing to register. |

Handlers are optional. A button with no code behind it yet does nothing, quietly, so you can draw the
whole interface first and fill in behaviour as you go.

## Where matplotlib comes in

Every plot area in an iterlab interface **is** a `matplotlib.axes.Axes`. It is not a wrapper around
one or an imitation of the API. Under the hood each one lives in a `FigureCanvasTkAgg` with a
`NavigationToolbar2Tk`, so:

```python
import matplotlib

isinstance(ev.spectrum, matplotlib.axes.Axes)  # True


def on_clicked_run_fit(ev, event):
    ax = ev.spectrum
    ax.clear()
    ax.plot(ev.wavelength, ev.counts, lw=1, label="measured")
    ax.plot(ev.wavelength, model(ev.wavelength, *ev.params), label="fit")
    ax.set_xlabel("wavelength (nm)")
    ax.legend()
```

Everything you already know from matplotlib works, and so does any library that accepts an `ax=`
argument (seaborn, xarray's plotting, mplhep and many others). You never call `plt.show()` or
`draw()`: after a handler runs, iterlab checks matplotlib's own `figure.stale` flag and calls
`canvas.draw_idle()` on any figure that changed, so twenty artists still cost one repaint. Pan and
zoom come from the standard toolbar with no code, and they survive a trip back into the layout
editor.

Mouse events on an axes arrive in **data coordinates**. Click a spectrum at 512 nm and `event.x` is
`512.0`, not a pixel offset. Picking a peak, setting a fit window or marking a background region
becomes a few lines in an `on_clicked_` handler.

matplotlib is used for plots only, and that is a lesson I learned the hard way. iterlab began
as an earlier prototype that built *every* control out of `matplotlib.widgets`. It stalled for two
reasons. matplotlib has no dropdown, list box or real label, so the set of controls could not grow.
And a figure crowded with widgets got slower with every control added, so the tool degraded just as
the interface became useful. The rewrite splits the work cleanly: **Tk provides every control,
matplotlib draws every plot**, and each library does what it was designed for.

## How the live reload works

The mechanism is simple, and knowing it helps you predict what will and will not survive an edit.

- **Handlers are resolved by name each time they are invoked.** The earlier prototype looked up
  handler functions once at startup and cached them, so edits never reached the running window.
  iterlab never holds on to a function object. When you click `run_fit`, it looks up
  `on_clicked_run_fit` in the current version of your module.
- **The module is reloaded when the file changes.** iterlab stamps the file with its modification
  time, size *and* a content hash. The hash is there because Windows file times can be coarse enough
  that two quick saves of the same size, such as an editor formatting on save, look identical
  without it. When the file changes, iterlab builds a fresh module object from it with
  `importlib.util`.
- **State lives on `ev`, not in module globals.** Reloading the module re-executes its top level.
  That is the one rule to remember: load data in `on_startup`, not at the top of the file.

```python
import numpy as np                      # fine: cheap

data = np.loadtxt("huge.csv")           # bad: re-runs on every edit


def on_startup(ev):
    ev.data = np.loadtxt("huge.csv")    # good: runs once per session
```

- **"Not defined" and "broken" are different.** A missing handler is normal and silent. A module that
  fails to import, or a handler that raises, is reported with its traceback in the window, and the
  process keeps running. The earlier prototype wrapped everything in a bare `except:`, so a syntax
  error looked exactly like a button with no code behind it: you clicked and nothing happened.

Some edits do need more than a reload, and iterlab says so rather than guessing. When you change
`on_startup` itself, it notices within a second and offers **Re-run startup**, which runs the new
version over the session you already have. If you edit a separate module that your code imports, or
want to start cold, **Hard reset** throws the session away. Upgrading a library such as NumPy still
means closing and reopening.

## A worked example

The repository ships with a
[showcase](https://github.com/alonhzn/iterlab/blob/main/examples/showcase.py) that puts three plots,
a few input boxes and some buttons together (shown in the image at the top of this post). Its
structure is the pattern I recommend for real work: one function builds the data, and every other
function only draws.

```python
def on_startup(ev):
    """Runs once, when the interface opens. The expensive half lives here."""
    ev.rng = np.random.default_rng(7)
    ev.t = np.linspace(0, SPAN, 1200)
    ev.reading = ev.rng.normal(1.0, 0.25, size=len(CATEGORIES))
    redraw(ev)


def draw_scatter(ev):
    """A cloud whose spread is the noise control, coloured by distance."""
    ax = ev.ax_scatter
    ax.clear()
    count = samples(ev)
    x = ev.rng.normal(0, 1, count)
    y = 0.7 * x + ev.rng.normal(0, noise(ev) + 0.05, count)
    ax.scatter(x, y, c=np.hypot(x, y), cmap="viridis", s=16, alpha=0.8)
    ax.set_title("Scatter", fontsize=10, loc="left")
```

Change the colormap, the marker size or the model inside `draw_scatter`, save, and press **Redraw**.
The plot updates in place against data that is already in memory. That is the whole idea: the slow
part runs once, and the part you are actually thinking about can change as fast as you can type.

## Status and what's next

iterlab is young. The full loop (draw, run, edit, keep going) is implemented and tested, with seven
element types: axes, button, label, text box, number box, file selector and folder selector.
Checkboxes, radio buttons, dropdowns, lists and sliders are next. On Linux you will need your
distribution's Tk package (`python3-tk` or `python3-tkinter`), since tkinter cannot be installed
from PyPI.

If you want to try it:

- `pip install iterlab`, then `iterlab demo`
- the [user guide](https://github.com/alonhzn/iterlab/blob/main/GUIDE.md) walks through the editor
  and the handler API for every element
- the [introduction video](https://www.youtube.com/watch?v=G_HzmkInHAs) (embedded above) shows the loop from start to finish

Feedback and issues are very welcome on
[GitHub](https://github.com/alonhzn/iterlab/issues), especially from anyone whose day is mostly
spent waiting for data to reload.
