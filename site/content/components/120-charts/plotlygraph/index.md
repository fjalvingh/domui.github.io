---
menu:
  sort: "10"
---
# PlotlyGraph

The component: a box on the page that fetches its own data and lets Plotly draw
a chart in it.

```java
PlotlyGraph.initialize(this);                 // Puts Plotly's javascript on the page

PlotlyGraph graph = new PlotlyGraph();
graph.setHeight("400px");
graph.setSource(new SalesPerMonth());
cp.add(graph);
```

!demo(to.etc.domuidemo.pages.components.charts.TimeSeriesChartPage.ui, 100%, 700)

[TOC]

## The API

| Method | What it does |
| --- | --- |
| `PlotlyGraph.initialize(NodeContainer)` | put Plotly's javascript on the page - **call it once per page** |
| `setSource(IPlotlyDataSource)` | where the data comes from; the graph rebuilds |
| `size(int width, int height)` | width and height in pixels, chained |
| `setWidth(String)` / `setHeight(String)` | the same in css, when a percentage or `100%` is wanted |

There is no `getValue()` and no `setValue()`: a graph is not a control. It has a
source, and the source is asked for a dataset whenever the graph is drawn.

!! **Give it a height.** The component is a `div`, and a `div` with nothing in it
!! yet is zero pixels high, so a graph without a height is invisible. A width is
!! optional - Plotly fills what it is given.

## The source

```java
public interface IPlotlyDataSource {
    IPlotlyDataset createDataset(QDataContext dc) throws Exception;
}
```

One method, and it is called **outside the page's request** - see
[the group page](../index.md) for the round trip. The `QDataContext` it is handed
is created for that call and closed after it, so the source queries with that one
and with nothing else.

`PlotlyDataSet` is the implementation of `IPlotlyDataset` you almost always
return: it collects [traces](../traces/index.md) and
[layout](../layout/index.md) and renders itself as the json Plotly expects.

```java
static final class SalesPerMonth implements IPlotlyDataSource {
    @Override
    public IPlotlyDataset createDataset(QDataContext dc) throws Exception {
        PlotlyDataSet ds = new PlotlyDataSet();
        PlTimeSeriesTrace sales = ds.addTimeSeries("Sales");
        for(Invoice i : dc.query(QCriteria.create(Invoice.class))) {
            sales.add(i.getInvoiceDate(), i.getTotal().doubleValue());
        }
        ds.title("Sales over time");
        return ds;
    }
}
```

A source that needs parameters gets them as constructor arguments - it is an
ordinary object, and making it a static nested class rather than a lambda over
page fields is what keeps it out of trouble.

## Which Plotly

The library is served from the framework's own resources
(`$js/plotly/plotly-1.58.5.min.js`), not from a content delivery network. That is
what `initialize()` registers, and it is why a page that has a graph on it needs
that one line.
