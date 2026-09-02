---
menu:
  sort: "50"
---
# ExpandingEditTable

`ExpandingEditTable<T>` shows a small list read-only and opens one row at a time
for editing, in place. It is the table for a list that is edited *as a whole* -
the lines of an order, the members of a group - rather than for a page of search
results.

```java
ExpandingEditTable<BasketLine> table = new ExpandingEditTable<>(model, renderer);
cp.add(table);
table.setEnableExpandItems(true);
table.setEnableDeleteButton(true);
table.setNewAtStart(true);
```

!demo(to.etc.domuidemo.pages.components.tables.TableEditPage.ui, 100%, 900)

[TOC]

## What it does

It takes the same `ITableModel<T>` and `IRowRenderer<T>` a
[`DataTable`](../datatable/index.md) takes, and adds three things: a row can be
opened into an editor, rows can be deleted, and a new row can be added. It does
**not** page: everything the model holds is on screen, which is why it is for
small lists.

| Method | What it does |
| --- | --- |
| `setEnableExpandItems(boolean)` | a row can be opened for editing by clicking it |
| `setEnableDeleteButton(boolean)` | each row gets a delete button |
| `setEnableAddingItems(boolean)` | a new row can be added |
| `setNewAtStart(boolean)` | a new row appears at the top rather than the bottom |
| `setEditorFactory(IRowEditorFactory<T,?>)` | what the opened row looks like - a fragment of your own |
| `setOnRowChangeCompleted(IRowEditorEvent<T,?>)` | called when an opened row is closed, to save or validate it |
| `addNew(T)` | add a row and open it for editing |
| `collapseRow(int)` | close an open row from code |

Without an editor factory the row opens as the editable form of its own columns;
with one, the factory returns a `NodeContainer` that gets the row instance and
lays out whatever it likes.

## Editable columns, or an expanding editor?

Both put controls in a table, and they answer different questions:

| | Editable columns on a `DataTable` | `ExpandingEditTable` |
| --- | --- | --- |
| how many rows are editable | all of them at once | one at a time |
| what the editor looks like | one control per cell | anything, through an editor factory |
| paging | yes | no |
| use it for | a grid of values to correct | rows with more fields than fit on a line |

Editable columns are described on the
[RowRenderer page](../rowrenderer/index.md):
`column(...).editable()`, and `factory(...)` when the control has to be made by
hand.
