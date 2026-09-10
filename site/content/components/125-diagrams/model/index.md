---
menu:
  sort: "20"
---
# The model: nodes, edges and their style

The drawing itself. A `GraphModel` holds cells - `GraphNode` for a shape,
`GraphEdge` for a line between two of them - and everything about how the
drawing looks is set here, in Java.

```java
GraphModel model = new GraphModel();

GraphNode start = model.addNode("Order arrives", 60, 20, 160, 40)
    .styled(s -> s.shape(GraphShape.Ellipse).fillColor("#d5e8d4").strokeColor("#82b366"));
GraphNode check = model.addNode("In stock?", 60, 110, 160, 60)
    .styled(s -> s.shape(GraphShape.Rhombus).fillColor("#ffe6cc").strokeColor("#d79b00"));
GraphNode ship = model.addNode("Ship it", 320, 120, 140, 40)
    .styled(s -> s.rounded(true).fillColor("#dae8fc").strokeColor("#6c8ebf"));

model.addEdge(start, check);
model.addEdge(check, ship, "yes")
    .styled(s -> s.edgeStyle(GraphEdgeStyle.Orthogonal));
```

!demo(to.etc.domuidemo.pages.components.graph.BasicGraphPage.ui, 100%, 600)

[TOC]

## Building a drawing

| Method | What it does |
| --- | --- |
| `addNode(label, x, y, width, height)` | a shape at that place, in the drawing's own coordinates |
| `addNode(parent, label, x, y, w, h)` | the same, inside another node: its coordinates are then relative to that one |
| `addEdge(source, target)` | a line from one node to another |
| `addEdge(source, target, label)` | the same, with a label on it |
| `remove(cell)` | take a cell out - and with a node, its children and the edges that end on it |
| `clear()` | empty the drawing |
| `getCells()` / `getCell(id)` / `isEmpty()` | what is in it |

Coordinates are the drawing's own, not the screen's: what the user has zoomed to
or scrolled to has no effect on them. A node given a parent is positioned
relative to that parent, which is what makes a group of shapes move as one.

**Ids are the model's.** Every cell gets one when it is made - `n1`, `e1`, and so
on - and nothing outside the model ever invents one. It is worth knowing because
it is the reason the browser cannot add a cell by itself; see
[editing](../editing/index.md).

## Changing what is already there

A model that is on the screen is changed the same way it was built. Nothing has
to be redrawn or rebuilt: the change is sent to the browser at the end of the
request.

```java
node.setLabel("Renamed");
node.at(300, 40);                                // Move it
node.size(200, 60);                              // Resize it
node.style().fillColor("#f8cecc");               // Restyle it
edge.setTarget(otherNode);                       // Reconnect it
model.remove(node);                              // And it takes its edges with it
```

`at()`, `size()`, `label()` and `styled()` return the cell, so they chain;
`setLabel()`, `setSource()`, `setTarget()` and `style()` are the plain
setters. `style()` hands out the cell's own style, changed in place - a cell
restyled long after the drawing was sent is restyled in the browser too.

## Style

`GraphStyle` is a small set of named properties. Every one of them is optional,
and a cell with no style at all is a plain rectangle or a plain line.

| Method | For |
| --- | --- |
| `shape(GraphShape)` | what a node is drawn as |
| `fillColor(String)` / `strokeColor(String)` / `strokeWidth(double)` | the body and the outline |
| `dashed(boolean)` / `rounded(boolean)` | a dashed line, rounded corners |
| `opacity(double)` | 0 to 100 |
| `fontColor(String)` / `fontSize(int)` / `bold()` | the label |
| `edgeStyle(GraphEdgeStyle)` | how an edge is routed |
| `startArrow(String)` / `endArrow(String)` | the arrow heads |
| `raw(String name, Object value)` | anything maxGraph understands that the list above does not name |

`GraphShape` has `Rectangle` (the default), `Ellipse`, `DoubleEllipse`,
`Rhombus`, `Triangle`, `Hexagon`, `Cylinder`, `Actor`, `Cloud`, `Line`, `Label`,
`Swimlane`, `Image`, `Arrow`, `ArrowConnector` and `Connector`.

`GraphEdgeStyle` decides how a line gets from one node to the other:
`Orthogonal` (right angles - the flow-chart look), `Elbow`, `EntityRelation`,
`Loop`, `Manhattan`, `Segment`, `SideToSide` and `TopToBottom`. An edge without
one is drawn straight.

## Edges bend where they are told

```java
GraphEdge edge = model.addEdge(start, done);
edge.waypoint(240, 120).waypoint(240, 260);      // Through these two points
edge.clearWaypoints();                           // Straight again
```

`getWaypoints()` reads them back, and `setWaypoints(List<GraphPoint>)` replaces
the lot in one go.

## The user object stays here

```java
node.setUserObject(order);                       // The entity this shape stands for
```

`getUserObject()` / `setUserObject()` is a place to keep what the shape *means* -
the entity, the key, the enum. **It is never sent to the browser**, which is what
makes it the right place for it: it is the page's own data, and a handler that
has to decide something about a cell reads it there.
