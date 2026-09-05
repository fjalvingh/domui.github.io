---
menu:
  sort: "90"
---
# SplitterPanel

`SplitterPanel` puts two panels either side of a bar the user can drag.

```java
Div left = new Div();
Div right = new Div();

SplitterPanel split = new SplitterPanel(left, right, true);   // true: a vertical bar
split.setHeight("300px");
split.setMinASize(100);
cp.add(split);
```

!demo(to.etc.domuidemo.pages.components.layout.SplitterPanelPage.ui, 100%, 640)

[TOC]

## The two directions

!! The boolean is the orientation of the **bar**, not of the split. `true` is a
!! vertical bar, and therefore two panels **side by side**; `false` is a
!! horizontal bar, and therefore one panel **above** the other. It is easy to
!! read the wrong way round.

| `vertical` | The bar | The panels | Css |
| --- | --- | --- | --- |
| `true` | vertical | A left, B right | `ui-splt-vert`, `ui-splt-left`, `ui-splt-right` |
| `false` | horizontal | A on top, B below | `ui-splt-horz`, `ui-splt-top`, `ui-splt-bottom` |

## Limits

| Method | What it does |
| --- | --- |
| `setMinASize(int)` / `setMaxASize(int)` | how far the bar may move, in pixels, for panel A |
| `setMinBSize(int)` / `setMaxBSize(int)` | the same for panel B |
| `setClosableToPerc(int)` | below this percentage the panel snaps shut |
| `getPanelA()` / `getPanelB()` | the two panels |

!! Give the splitter a **height**. It has none of its own, and without one there
!! is nothing to divide - the panels collapse to nothing.

The dragging itself is done in the browser by a jQuery splitter; the server is
not involved, so moving the bar costs no round trip and the position is not
remembered across a page load.
