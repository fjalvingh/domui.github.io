---
menu:
  sort: "20"
---
# Traces: what kind of chart it is

A **trace** is one series of data, and its type decides what the chart looks
like. A dataset with two time-series traces is a chart with two lines; one with
a pie trace is a pie.

```java
PlotlyDataSet ds = new PlotlyDataSet();
PlTimeSeriesTrace sales = ds.addTimeSeries("Sales");
sales.mode(TraceMode.MarkersAndLines);
sales.line().shape(PlShape.Spline).smoothing(2.0);
```

[TOC]

## Time series

`addTimeSeries(String name)` returns a `PlTimeSeriesTrace`, whose points are a
date and a value.

| Method | What it does |
| --- | --- |
| `add(Date, double)` / `add(Date, double, String text)` | one point, with an optional label |
| `add(long millis, double, String)` | the same from a timestamp |
| `mode(TraceMode)` | `Lines`, `Markers`, `MarkersAndLines`, ... |
| `date()` / `dateTime()` | whether the x value is a day or a moment |
| `fill(PlFillType)` | fill the area under the line |
| `line()` | the line's own settings: `shape(PlShape.Spline)`, `smoothing()`, width, colour |
| `type(TraceType)` | the underlying Plotly type, when the default is not wanted |

!demo(to.etc.domuidemo.pages.components.charts.TimeSeriesChartPage.ui, 100%, 700)

## Bars and named categories

`addLabeledSeries(String name)` returns a `PlLabelValueTrace`: the same idea with
a **label** instead of a date, which is what a bar chart is.

| Method | What it does |
| --- | --- |
| `add(String label, double value)` | one bar, or one point |
| `mode(TraceMode)` | as above |
| `type(TraceType)` | `Bar` for bars, the scatter types for points |

Several such traces on one dataset become several bars per category; what happens
to them then is the dataset's `barMode(PlBarMode)` - side by side, or stacked.

!demo(to.etc.domuidemo.pages.components.charts.BarChartPage.ui, 100%, 700)

## Pies and donuts

`addPie()` returns a `PlPieTrace`, filled with label/value pairs.

| Method | What it does |
| --- | --- |
| `add(String label, double value)` | one slice |
| `hole(double)` | 0 is a pie; 0.4 is a donut |
| `textPosition(PlTextPosition)` | labels `Inside`, `Outside`, `Auto`, `None` |
| `textInfo(PlTextInfo...)` | what the label says: the name, the value, the percentage |
| `insideTextFont()` / `outsideTextFont()` | the fonts of those two |
| `autoMargin()` | let Plotly make room for labels that stick out |
| `domain(int x, int y)` | which cell of the dataset's grid this pie goes in |

`domain()` with the dataset's `grid(columns, rows)` is how several pies end up
next to each other on one graph.

!demo(to.etc.domuidemo.pages.components.charts.PieChartPage.ui, 100%, 700)

## Sunbursts

`addSunburst()` returns a `PlSunBurstTrace`: a hierarchy drawn as rings, where
each item names its parent.

| Method | What it does |
| --- | --- |
| `add(String id, String parentId, String label, double value)` | one item, under that parent |
| `add(String id, String parentId, String label)` | ...whose value is the sum of its children |
| `branchValues(PlBranchValues)` | whether a branch's value is its own or the total of its children |
| `maxDepth(int)` | how many rings to show at once |
| `leafOpacity(double)` | how solid the outer ring is |
| `textPosition()`, `textInfo()`, `insideTextOrientation()` | as on the pie |

The root is the item whose parent id is empty.

!demo(to.etc.domuidemo.pages.components.charts.SunburstChartPage.ui, 100%, 800)

## Gauges

A gauge shows one number on a dial, so it is not added to a dataset like the
others: `GaugeDataSource` **is** both the trace and the `IPlotlyDataSource`, and
is handed to the graph directly.

```java
GaugeDataSource speed = new GaugeDataSource(420, "Speed");
speed.gauge().axis().range(0, 500).tickColor("darkblue");
speed.gauge().step(0, 250, "cyan").step(250, 400, "royalblue");
speed.gauge().threshold().value(490).line().color("red").width(4);
graph.setSource(speed);
```

| Method | What it does |
| --- | --- |
| `value(double)` | the number the needle points at |
| `mode(PlIndicatorMode...)` | `Gauge`, `Number`, `Delta` - and combinations |
| `title()` | the text over the dial |
| `gauge()` | the dial itself: `axis()` for its range and ticks, `bar()` for the needle, `step(from, to, colour)` for its bands, `threshold()` for the red line |
| `dataSet()` | the dataset underneath, for a title or a margin around the dial |

The constructors do the common cases: `GaugeDataSource(value)` and
`GaugeDataSource(value, title)`. The mode is set to gauge-plus-number when the
dataset is asked for, so the number is printed under the dial by default.

!demo(to.etc.domuidemo.pages.components.charts.GaugeChartPage.ui, 100%, 700)
