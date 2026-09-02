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

## Data binding in a table

Binding in a table is not the same subject as binding on a form, because a table
has many rows, only some of them on screen, and it builds their cells itself.
This section is what that changes.

!demo(to.etc.domuidemo.pages.components.tables.TableBindingPage.ui, 100%, 780)

### Every value cell is already bound

A column that shows a property does not render text: it renders a
`DisplaySpan` **bound to that property of that row object**. So this is all it
takes for the screen to follow the data:

```java
rr.column("copies").label("Copies");        // A bound cell, like every other one
…
line.setCopies(line.getCopies() + 1);       // The cell updates. Nothing else is called.
```

No `forceRebuild()`, no telling the table, no re-query. The binding was made when
the row was rendered and lives inside the cell, and the page's binding pass moves
the value on every request.

### A cell built by a renderer is not

A renderer builds content from whatever it likes, so there is no single value the
binding could watch, and nothing updates it. Say `rerenderOnBind()` and the cell
is redrawn once per request instead:

```java
rr.column().label("Line total")
    .renderer((node, line) -> node.add(line.getCopies() + " x 14.95"))
    .rerenderOnBind();                       // ...or the cell keeps its first text
```

The demo above has the same column twice, with and without it: after pressing a
button the bound one follows and the other still shows what it rendered when the
page was built.

`valueHint(QField)` works the same way for the cell's tooltip - it binds the
cell's `title` to a property of the row.

### Editable cells

`editable()` puts a **control** in the cell and binds it to the row's property,
which is what makes a table of input boxes work with no code at all:

```java
rr.column("copies").label("Copies").editable();
```

Which control it is comes from the metadata of the property, exactly as in a
form. `factory(row -> …)` makes the control yourself, and is asked once per row
so the control can depend on what is in it.

!! Whichever way the control is made, the binding is always
!! `control.bind().to(row, theColumnProperty)`. A control made by a factory is
!! bound to that same property, so its value type must be the property's type -
!! a factory returning a control over something else fails when the binding
!! moves a value.

An editable column cannot also have a renderer or a converter: a cell either
shows a value or holds a control, and asking for both throws.

### Style bound to the row

A column can bind a css class to a property of the row, which is how a table
colours the rows that need attention:

```java
rr.column("copies").label("Copies")
    .styleBinding(new StyleBinder()
        .define(Boolean.TRUE, "row-warning")
        .define(Boolean.FALSE, ""))
    .to("bulk");                              // A property of the row object
```

### The footer binds to anything

`getFooterBody()` hands back an ordinary `TBody` under the rows, so a total is
just a control bound to whatever holds it - usually the page or a controller
rather than a row:

```java
Text2<Integer> total = new Text2<>(Integer.class);
total.setReadOnly(true);
total.bind().to(this, "totalCopies");         // A property of the page

TR tr = table.getFooterBody().addRow();
tr.addCell().add("Copies in total");
tr.addCell().add(total);
```

### Binding the rows themselves: an observable list

A table can be given an `IObservableList<T>` instead of a model:

```java
DataTable<Album> table = new DataTable<>(rr);
table.setList(artist.getAlbumList());         // A Hibernate relation list is observable
```

The table then listens to the list, and **changing the list changes the table**:
adding an album to the artist's list adds a row. What the table does with an
event depends on how many changes arrive at once:

| The list reports | The table |
| --- | --- |
| one add, delete or modify | updates that one row |
| an assign (the whole list replaced) | rebuilds itself |
| more than one change in one event | rebuilds itself |

That is the natural way to write a master/detail screen: the detail table is
bound to the relation of the master record, and nothing has to be told when the
relation changes.

### The special cases

!! **A modified row is thrown away and rebuilt.** `model.modified(index)`
!! removes the row's cells and renders them again, so the controls in that row
!! are new ones: an unsaved keystroke, a validation error and the focus are all
!! gone. Update the object and let the *cell* bindings follow it where you can,
!! and reserve `modified()` for changes the cells cannot show by themselves.

!! **Only the rows on screen have bindings.** A table renders one page; the rows
!! of the other pages do not exist as components, so nothing binds them.
!! Changing an object that is not on screen is not lost - it is simply picked up
!! when that page is rendered.

!! **A cell compares values the way every binding does**, with
!! `MetaManager.areObjectsEqual`. Two entities with the same primary key are the
!! same value, and an object changed *in place* is still the same object - so
!! putting a mutated copy back does not move anything. That trap is the same one
!! [writing a component](../../../building-pages/110-writing-a-component/index.md)
!! describes, and it bites hardest in a table because the cells are made for you.

The binding pass walks every control on the page once per request, so an
editable table is that many comparisons per request: a hundred rows of five
editable columns is five hundred. That is cheap, but it is not free, and it is a
reason to page a large table rather than show it whole.

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
