---
menu:
  sort: "30"
---
# Table models

A table model is where the rows come from. Every table-shaped component in this
group takes an `ITableModel<T>`, and none of them care which one it is.

```java
//-- A query
SimpleSearchModel<Album> queried = new SimpleSearchModel<>(this,
    QCriteria.create(Album.class).ascending(Album_.title()));

//-- A list you hold yourself
SortableListModel<BasketLine> held = new SortableListModel<>(BasketLine.class, lines);
```

!demo(to.etc.domuidemo.pages.components.tables.TableModelPage.ui, 100%, 900)

[TOC]

## What a model must answer

`ITableModel<T>` is small: how many rows are there (`getRows()`), give me rows
*a* to *b* (`getItems(a, b)`), and tell these listeners when something changes.
Everything else is added by the interfaces a model may also implement:

| Interface | Adds |
| --- | --- |
| `IModifyableTableModel<T>` | `add()`, `delete()`, `modified()` - changing the data *through* the model |
| `ISortableTableModel` | `sortOn(property, descending)` - what a header click calls |
| `ITruncateableDataModel` | `isTruncated()` - "there were more rows than I fetched" |
| `IKeyedTableModel<T>` | rows can be found by primary key |
| `IShelvedListener` | the model is told when its page is shelved and returned to |

## The models that ship

| Model | Rows come from | Sorts |
| --- | --- | --- |
| `SimpleSearchModel<T>` | a `QCriteria`, an `IQuery` or a query functor | in the **database**, by re-running the query |
| `SimpleListModel<T>` | a `List<T>` you give it | not at all |
| `SortableListModel<T>` | the same | in **memory**, with a comparator per property |
| `DefaultTableModel<T>` | a `List<T>`, kept modifiable | in memory |
| `SimpleKeyModel<T,K>` | a list, addressed by key | - |

Where the sorting happens matters as soon as the result is bigger than one
page: the query model sorts **before** the row limit, so sorting 20,000 tracks
gives the first page of all of them. A list model can only sort the list it
holds.

## SimpleSearchModel

The model most list screens use. It runs its query **once**, keeps the result,
and hands out the slice each page needs - paging costs nothing.

| Method | What it does |
| --- | --- |
| `new SimpleSearchModel<>(NodeBase, QCriteria<T>)` | the usual form: the query, run in the page's own context |
| `new SimpleSearchModel<>(NodeBase, IQuery<T>)` | a lambda that runs the query itself, given the data context, the sort property and the row limit |
| `setRefreshAfterShelve(boolean)` | re-query when the page is returned to |
| `getQuery()` | the criteria it holds |
| `setMaxRowCount(int)` | how many rows to fetch at most; `ITableModel.DEFAULT_MAX_SIZE` (1000) when unset |
| `isTruncated()` | whether the result hit that maximum |

It fetches at most **1000** rows by default and reports `isTruncated()` when
there were more, which the table shows as a truncation marker. It is also an
`IShelvedListener`: when its page is shelved it drops the result, so returning
to the screen re-runs the query rather than showing what was true an hour ago.

## Changing rows

For a list model, every change goes through the model:

```java
listModel.add(new BasketLine("Let It Be", 1));   // appears in the table
line.setCopies(line.getCopies() + 1);
listModel.modified(0);                          // that one cell updates
listModel.delete(0);                            // that row disappears
```

Each of those tells the table exactly what changed, and the table updates
exactly that - no rebuild, no flicker, and the scroll position and selection
survive. Changing the list itself and *not* telling the model leaves the screen
showing the old rows.

An `IObservableList<T>` can be handed to the table directly with `setList()`;
the table then listens to the list and no model is written at all.
