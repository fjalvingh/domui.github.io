---
menu:
  sort: "30"
---
# Layout: everything around the data

The same `PlotlyDataSet` that collects the [traces](../traces/index.md) carries
the layout: the title, the axes, the legend, the colours and whatever is drawn on
top. All of it chains.

```java
PlotlyDataSet ds = new PlotlyDataSet();
ds.title("Sales over time").titleFont().size(25).color("#663399");
ds.xAxis().title("Month");
ds.yAxis().title("Invoices");
ds.showLegend(true).legendHorizontal();
```

[TOC]

## The dataset's own settings

| Method | What it does |
| --- | --- |
| `title(String)` | the chart's title; `titleFont()` styles it |
| `xAxis()` / `yAxis()` | the axes - see below |
| `showLegend(boolean)` / `legendHorizontal()` | whether there is a legend, and which way it runs |
| `size(int, int)`, `width(int)`, `height(int)` | the drawing's size in pixels, rather than the component's |
| `margin()` | the white space around the drawing |
| `barMode(PlBarMode)` | what several bar traces do to each other: side by side, or stacked |
| `grid(int columns, int rows)` | split the graph into cells, for several pies on one drawing |
| `colorWay(String...)` | the colours the traces are given, in order |
| `sunburstColorWay(String...)` / `extendSunburstColorway()` | the same for a sunburst |
| `addTrace(IPlotlyTrace)` | a trace built by hand rather than by `addPie()` and friends |

## Axes

`xAxis()` and `yAxis()` return a `PlAxis`, which is the usual list: a title, a
type, a range, the tick marks and their format, grid lines, and whether the axis
is shown at all. An `AxisTick` says how the ticks are spaced and written.

## Annotations and images

```java
ds.addAnnotation(0.5, 0.5, "Team").font().size(20).color("#99aaff");
ds.image().bgImage("img/logo.png", 0.3, 1.0, 0.1);
```

| Method | What it does |
| --- | --- |
| `addAnnotation(x, y, text)` | a `PlAnnotation` at that position; chain `font()`, and more |
| `annotation(x, y, text)` | the same, returning the dataset so it chains on |
| `image()` | a `PlImage`, for a picture behind or over the drawing |

An annotation in the middle of a donut is how a donut gets a label in its hole,
which is what the demo does.

## The pieces

The layout classes live in `component.plotly.layout` and are all small, all
fluent, and all named after what Plotly calls them:

| Class | For |
| --- | --- |
| `PlAxis`, `AxisTick` | an axis and its ticks |
| `PlFont` | a font: family, size, colour |
| `PlMargin` | the margins around the drawing |
| `PlLine`, `PlDash`, `PlShape` | a line's width, colour, dashing and shape |
| `PlAnnotation` | a text at a position |
| `PlImage`, `PlImageRef`, `PlImageAnchor`, `PlImageLayer` | a picture on the drawing |
| `PlBarMode` | grouped or stacked bars |
| `PlSizing` | how the drawing fills its box |

They map onto Plotly's own layout options, so
[Plotly's documentation](https://plotly.com/javascript/reference/layout/) is the
reference for what each one does to the picture.
