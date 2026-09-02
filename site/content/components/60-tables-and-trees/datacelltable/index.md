---
menu:
  sort: "60"
---
# DataCellTable

`DataCellTable<T>` shows the rows of a model as a **grid of cells** rather than
as lines: one item per cell, so many per row. An index of album covers, a wall
of photographs, a month of days.

```java
DataCellTable<Album> grid = new DataCellTable<>(new SimpleListModel<>(albums));
grid.setColumns(4);
grid.setContentRenderer((node, album) -> {
    Div title = new Div("title");
    node.add(title);
    title.add(album.getTitle());
    node.add(album.getArtist().getName());
});
cp.add(grid);
```

!demo(to.etc.domuidemo.pages.components.tables.OtherTablesPage.ui, 100%, 900)

[TOC]

## The API

| Method | What it does |
| --- | --- |
| `new DataCellTable<>(ITableModel<T>)` | the rows to show - the same models a `DataTable` takes |
| `setColumns(int)` / `setRows(int)` | the shape of the grid |
| `setContentRenderer(IRenderInto<T>)` | how one item is drawn; **required** |
| `setContentRendererClass(Class)` | the same as a class to instantiate |
| `setRenderEmptyCells(boolean)` | draw the cells that have no item, to keep the grid rectangular |
| `setRenderEmptyRows(boolean)` | the same for whole rows |

There is no `RowRenderer` and there are no columns: a cell is whatever the
content renderer puts in it.

Like a `DataTable` it is a pageable component, so a
[`DataPager`](../datapager/index.md) works with it; the grid's own rows and
columns decide how many items a page holds.
