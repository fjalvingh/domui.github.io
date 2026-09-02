---
menu:
  sort: "70"
---
# ListShuttle

`ListShuttle` is two lists side by side with buttons between them: values move
from the left to the right and back, and the right-hand list can be put in
order. It is for choosing a handful of things out of many **and** deciding the
order they come in - the columns of a report, the steps of a procedure.

```java
ListShuttle shuttle = new ListShuttle();
cp.add(shuttle);
shuttle.setModel(new AlbumShuttleModel(albums));
shuttle.setSourceRenderer((node, album) -> node.add(((Album) album).getTitle()));
shuttle.setTargetRenderer((node, album) -> node.add(((Album) album).getTitle()));
```

!demo(to.etc.domuidemo.pages.components.tables.OtherTablesPage.ui, 100%, 900)

[TOC]

## What it needs

One `IShuttleModel<S,T>`, which is two table models and the moves between them:

```java
public interface IShuttleModel<S, T> {
    ITableModel<S> getSourceModel();
    ITableModel<T> getTargetModel();
    void moveSourceToTarget(int sourceIndex, int targetIndex) throws Exception;
    void moveTargetToSource(int targetIndex) throws Exception;
}
```

`IMovableShuttleModel<S,T>` adds `moveTargetItem(from, to)`, which is what makes
the up and down buttons work.

The model does the moving *and* tells both table models what changed - which is
what makes both sides of the screen follow. A model that moves the values but
does not call `add()` and `delete()` on its models leaves the screen unchanged.

!! `moveSourceToTarget` is called with a target index of **9999** when the
!! shuttle means "at the end". Clamp it to the size of the target list; taking
!! it literally throws.

## Using it

| Method | What it does |
| --- | --- |
| `setModel(IShuttleModel<?,?>)` | the two lists and the moves |
| `setSourceRenderer(IRenderInto<Object>)` / `setTargetRenderer(...)` | how an item is drawn on each side |
| `setSourceRendererClass(Class)` / `setTargetRendererClass(Class)` | the same as classes |

The renderers are typed `Object`, so a lambda casts to the value type - the
component predates the generics on the rest of this group.

Rows are selected by clicking them (the cell gets the css class `selected`) and
moved with the arrow buttons in the middle: single arrows move the selection,
double arrows the same. The order buttons on the right move a chosen item up or
down, and appear only for an `IMovableShuttleModel`.
