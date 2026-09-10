---
menu:
  sort: "40"
---
# Arranging the drawing

A drawing whose nodes were never placed by hand - one built from a database, a
dependency tree, a workflow - can be laid out instead:

```java
bb.addButton("Arrange", () -> panel.layout(GraphLayoutType.Hierarchical));
```

!demo(to.etc.domuidemo.pages.components.graph.ChangingGraphPage.ui, 100%, 700)

[TOC]

## A command, not a property

`layout()` arranges the drawing **now**. It is what a button does, not something
a drawing *is*: a diagram arranged on every render would put a node the user had
dragged back where the layout wants it.

The arranging is done in the browser, because that is where the drawing is - but
where it puts things comes back here as ordinary geometry changes, and the model
ends up holding the arranged drawing. So the arrangement survives: a page that is
rendered again draws it as it was left.

Two things follow from that:

- a [change handler](../editing/index.md) is asked about those changes like any
  other, and where the model keeps a history, one arrangement is one step to undo;
- it works on a read-only drawing too. The user cannot move anything there, but
  the page can, and the positions have to come back or the arrangement would be
  lost on the next render.

## Which layouts there are

```java
panel.layout(GraphLayoutType.Hierarchical, GraphLayoutDirection.West);
```

| `GraphLayoutType` | What it does | Fits |
| --- | --- | --- |
| `Hierarchical` | layers, in the direction given | flow charts, and anything with a direction to it - the one to try first |
| `Organic` | force-directed, spreading a connected drawing out evenly | connected drawings; nodes without edges are left alone |
| `Circle` | everything on a circle | anything, connected or not - the edges are not looked at |
| `Tree` | a compact tree, growing in the direction given | trees only; a cycle is left alone |
| `RadialTree` | the same tree, around its root | trees only |
| `ParallelEdges` | pulls apart edges that run between the same two nodes | a touch-up of a drawing that is otherwise fine |

`GraphLayoutDirection` is `North` (the default), `South`, `East` or `West`, and
only `Hierarchical` and the two tree layouts look at it - it says which way the
drawing grows.

!! A layout that does not suit a drawing does nothing rather than something
!! wrong: a tree layout ignores a drawing with a cycle in it, and the ones that
!! work along the edges ignore a node that has none.
