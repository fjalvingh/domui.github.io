---
menu:
  sort: "40"
---
# DataPager

`DataPager` is the bar that walks a table through its pages, and says how many
records there are.

```java
DataTable<Album> table = new DataTable<>(model, rr);
cp.add(table);
table.setPageSize(10);
cp.add(new DataPager(table));
```

!demo(to.etc.domuidemo.pages.components.tables.DataTablePage.ui, 100%, 800)

[TOC]

## What it is

`DataPager` is a wrapper: it renders whichever pager the application has chosen
as its default, and proxies to it. That is what lets an application change the
look of every pager it has in one place, without any screen mentioning a
particular one.

The two it can be:

| | Looks like |
| --- | --- |
| `DataPager1` | first / previous / next / last buttons with *Record 50-75* beside them |
| `DataPager2` | numbered page buttons - 1 2 3 ... 45 46 - with the record count at the end |

`DataPager2` is the default. An application changes that once, in its
`initialize()`:

```java
DataPager.setPagerFactory(table -> new DataPager1(table));
```

after which every `new DataPager(table)` in every screen renders the other one.

## Using it

| Method | What it does |
| --- | --- |
| `new DataPager(IPageableComponent)` | the pager for that table |
| `setPageSize(int)` on the **table** | how many rows a page holds - the pager reads it |

The pager takes what it needs from the table: how many rows the model has, which
page is showing, whether the result was truncated. A table whose model finds
1000 rows and reports itself truncated is shown as *> 1000 records*, so the user
knows the count is a floor rather than the truth.

Paging asks the model for another slice; it does **not** re-run the query. See
[table models](../tablemodels/index.md).
