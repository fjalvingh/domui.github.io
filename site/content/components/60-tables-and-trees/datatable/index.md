---
menu:
  sort: "10"
---
# DataTable

`DataTable<T>` shows the rows of a model as a table, one page at a time.

```java
SimpleSearchModel<Album> model = new SimpleSearchModel<>(this,
    QCriteria.create(Album.class).ascending(Album_.title()));

RowRenderer<Album> rr = new RowRenderer<>(Album.class);
rr.column(Album_.title()).label("Album").width(40).ascending().sortdefault();
rr.column(Album_.artist().name()).label("Artist").width(30).ascending();

DataTable<Album> table = new DataTable<>(model, rr);
cp.add(table);
table.setPageSize(10);
cp.add(new DataPager(table));
```

!demo(to.etc.domuidemo.pages.components.tables.DataTablePage.ui, 100%, 800)

[TOC]

## The table itself

| Method | What it does |
| --- | --- |
| `new DataTable<>(model, renderer)` | the usual form; both can also be set afterwards |
| `setModel(ITableModel<T>)` | show other rows - this is how a search screen shows its result |
| `setRowRenderer(IRowRenderer<T>)` | show them differently |
| `setPageSize(int)` | how many rows a page holds; `0` means all of them, and then a pager is pointless |
| `setEmptyMessage(String)` / `setEmptyMessage(NodeBase)` | what to show when the model has no rows |
| `setShowHeaderAlways(boolean)` | keep the header when there is nothing to show |
| `setTableWidth(String)` | the css width of the table |
| `setPreventRowHighlight(boolean)` | stop the hover highlight on rows |
| `setResizeMode(DataTableResize)` | whether, and how, the user may drag column borders |

Setting a new model is the normal way to run a new search: the table redraws
itself from the new rows and the pager follows. The renderer stays.

## Clicking

A click handler is set on the **renderer**, not on the table:

```java
rr.setRowClicked(album -> UIGoto.moveSub(AlbumDetailPage.class, "id", album.getId()));
rr.column(Album_.title()).cellClicked(album -> rename(album));
```

A cell handler wins over the row handler for its own column, and cells that have
one are marked (`ui-cellsel`) so the user can see that they do something.

## Selecting rows

!demo(to.etc.domuidemo.pages.components.tables.TableSelectionPage.ui, 100%, 820)

A table gets a selection column as soon as it has a **selection model**:

```java
InstanceSelectionModel<Album> selection = new InstanceSelectionModel<>(true);
table.setSelectionModel(selection);
table.setSelectionAllHandler(new DefaultSelectAllHandler());
table.setShowSelection(true);
```

| Part | What it decides |
| --- | --- |
| `ISelectionModel<T>` | whether more than one row may be selected, which rows are, and who is told when that changes |
| `InstanceSelectionModel<T>` | the usual implementation: it holds the selected *instances* in a set, and is `Iterable` over them |
| `KeySelectionModel<T,K>` | the same by primary key, for rows that arrive as different objects between requests |
| `ISelectionAllHandler` | what the tick in the header does; `DefaultSelectAllHandler` selects **everything the model holds**, not just the page on screen |
| `IAcceptable<T>` | which rows may be selected at all - hand one to the `InstanceSelectionModel` constructor |

A row the acceptor refuses still gets a checkbox, but a dead one: DomUI turns a
read-only checkbox into a disabled one, because html has no read-only checkbox.
Select-all respects the acceptor too - in the demo it selects two albums out of
347.

`selection.addListener(...)` reports every change, through
`selectionChanged(row, on)` and `selectionAllChanged()`; the table itself
listens as well, which is how the checkboxes follow a selection made in code.

## Column widths

Every column can be given a width in one of two ways, and the table treats them
differently:

- `width(int characters)` - the default, and what metadata supplies. The
  renderer multiplies the character count by its `emFactor` (0.65) and renders
  an `em` width, because text is not all Ms.
- `width(String css)` - an explicit css width. **If one column uses this, all of
  them should**: only the css widths are then used.

The last column is special: in a table with `setTableWidth("100%")` it gets no
width at all, so it takes up whatever is left. In a table with no width it does
get one, and the table is then as wide as its columns.

!! Give the columns realistic widths. Without them the browser sizes each page
!! of rows on its own content, so the columns jump about every time the user
!! pages.

## Letting the user resize columns

| `setResizeMode(...)` | What dragging a column border does |
| --- | --- |
| `NONE` | nothing - resizing is off |
| `FIXED` | the table keeps its width: column X grows, column X+1 shrinks |
| `OVERFLOW` | the table grows with the column, possibly past its container - the default |
| `FLEX` | as `OVERFLOW`, with the columns after it sharing the space |

A resize is reported to the server so an application can remember it, per
renderer with `rr.setColumnListener(...)`, or once for the whole application:

```java
//-- In DomApplication.initialize()
setAttribute(RowRenderer.COLUMN_LISTENER, (IColumnListener<Object>) (tbl, newWidths) -> saveWidths(tbl, newWidths));
```
