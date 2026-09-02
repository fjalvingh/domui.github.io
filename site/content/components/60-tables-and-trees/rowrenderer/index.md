---
menu:
  sort: "20"
---
# RowRenderer and ColumnDef

A `RowRenderer<T>` says what a row looks like. It is not a component: it is the
thing a table asks to draw each row, and it holds the column definitions.

```java
RowRenderer<Track> rr = new RowRenderer<>(Track.class);
rr.column(Track_.name()).label("Title").width(30).ascending().sortdefault();
rr.column(Track_.milliseconds()).label("Duration").width(10)
    .converter(new MsDurationConverter()).align(TextAlign.RIGHT);
```

!demo(to.etc.domuidemo.pages.components.tables.ColumnDefPage.ui, 100%, 900)

[TOC]

## Defining the columns

| Call | Gives a column for |
| --- | --- |
| `column(QField<T,V>)` | a typed property - the form to prefer |
| `column(String property)` | a property by name |
| `column(Class<V>, String property)` | the same with the value type stated |
| `column()` | **no property at all**: the column gets the row itself, and needs a renderer |

A renderer with no columns at all takes them from the class's `@MetaObject`
default columns; `addDefaultColumns()` asks for that explicitly.

!! Defining one column of your own drops the metadata columns entirely. It is
!! all or nothing.

## What a column can be told

Every method returns the column, so they chain.

**What it says**

| Method | Effect |
| --- | --- |
| `label(String)` / `label(IBundleCode)` | the header text; without one, metadata supplies it |
| `hint(String)` / `hint(IBundleCode)` | the header's tooltip |
| `valueHint(QField<T,String>)` | a property whose value becomes each *cell's* tooltip |
| `headerRenderer(IRenderInto<ColumnDef>)` | build the header cell yourself |

**How the value is shown**

| Method | Effect |
| --- | --- |
| `converter(IConverter<V>)` | turn the value into text yourself |
| `numeric(NumericPresentation)` | show a number as money, a percentage, and so on |
| `renderer(IRenderInto<V>)` | build the cell content yourself |
| `align(TextAlign)` | left, right or centre |
| `css(String)` / `cssHeader(String)` | a css class on the cells, or on the header |
| `wrap()` / `nowrap()` | whether text may wrap |

**How wide it is**

| Method | Effect |
| --- | --- |
| `width(int characters)` | the width in characters (see [DataTable](../datatable/index.md)) |
| `width(String css)` | an explicit css width |
| `maxWidth(int characters)` | truncate longer values, with the whole value as the cell's tooltip |

**Sorting**

| Method | Effect |
| --- | --- |
| `ascending()` / `descending()` | the column may be sorted, starting in that direction |
| `sortdefault()` | *this* column is the one the table is sorted on when it first appears |
| `sort(QField)` / `sort(String)` | sort on another property - needed when the column has a renderer, because there is then nothing to sort on |
| `sort(ISortHelper)` | sort in a way of your own |

**Clicking and editing**

| Method | Effect |
| --- | --- |
| `cellClicked(ICellClicked<T>)` | a handler for this column's cells; it wins over the row handler |
| `cellClicked(handler, Predicate<T>)` | the same, but only on the rows the predicate accepts |
| `editable()` | put a control in the cell, bound to the row's property |
| `factory(IRowControlFactory<T>)` | make that control yourself, per row - this implies `editable()` |
| `rerenderOnBind()` | redraw the cell when the bound value changes |
| `styleBinding(StyleBinder)` | bind a style to the cell |

!! A column cannot have both a renderer or converter *and* be editable: a cell
!! either shows a value or holds a control. Trying to do both throws.

## The whole row

| Method | What it does |
| --- | --- |
| `setRowClicked(ICellClicked<T>)` | what a click anywhere on the row does |
| `setRowButtonFactory(IRowButtonFactory<T>)` | add buttons to the end of each row |
| `addRenderListener(IRowRendered<T>)` | be told after each row is rendered - to colour it, for instance |
| `addHeaderBefore(TableHeader)` / `addHeaderAfter(...)` | extra header rows above or below the column headers |
| `emFactor(double)` | the character-to-em factor used for widths; 0.65 by default |
| `helper(IRowRenderHelper<T>)` | be handed each row before its cells are rendered |

`helper()` is for a row whose columns all need the same extra work: the helper
is given the row first, works out whatever the columns need, and the column
renderers then read it from the helper instead of each computing it again.

!! A renderer becomes **immutable the first time a table uses it**: changing a
!! column afterwards throws *This object has been USED and cannot be changed
!! anymore*. Build the renderer completely, then hand it to the table.

## A cell is a component

A cell holding a plain value is a `DisplaySpan` bound to that property, not a
piece of text - so changing the value on the row object updates the cell. That
is why an editable table needs no rebuilding, and why `rerenderOnBind()` exists
for the cells that are built by a renderer instead.

Binding in a table has enough of its own rules - which cells bind, what an
editable cell binds to, what a rebuilt row costs, and how an observable list
drives the rows - that they are collected in one place:
[data binding in a table](../datatable/index.md).
