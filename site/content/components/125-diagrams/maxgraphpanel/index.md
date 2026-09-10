---
menu:
  sort: "10"
---
# MaxGraphPanel

The component: a box on the page that maxGraph draws a diagram in.

```java
MaxGraphPanel.initialize(this);               // Puts maxGraph's javascript on the page

MaxGraphPanel panel = new MaxGraphPanel();
cp.add(panel);
panel.size("100%", "420px").setModel(model);
```

!demo(to.etc.domuidemo.pages.components.graph.BasicGraphPage.ui, 100%, 600)

[TOC]

## The API

| Method | What it does |
| --- | --- |
| `MaxGraphPanel.initialize(NodeContainer)` | put maxGraph's javascript and stylesheets on the page - **call it once per page** |
| `setModel(GraphModel)` | the drawing to show; another model rebuilds the panel |
| `getModel()` | the model it is showing |
| `size(String width, String height)` | both dimensions in css, chained |
| `setPanning(boolean)` | whether dragging the background moves the drawing; on by default |
| `setEditable(boolean)` | whether the user may change the drawing; off by default - see [editing](../editing/index.md) |
| `setChangeHandler(IGraphChangeHandler)` | who decides about the changes the user makes |
| `setCreateHandler(IGraphCreateHandler)` | who makes the cells the user asks for |
| `addPaletteItem(GraphPaletteItem)` | what the user can drag into the drawing |
| `layout(GraphLayoutType)` | arrange the drawing, now - see [arranging](../arranging/index.md) |
| `download(GraphExportFormat, String)` / `export(GraphExportFormat, IGraphExportHandler)` | a picture of the drawing - see [pictures](../pictures/index.md) |

A panel with no model of its own shows an empty drawing; `setModel()` is what
usually follows the constructor.

!! **Give it a size.** The component renders one empty `div`, and an empty div is
!! zero pixels high - a diagram without a height is a diagram you cannot see.
!! `size("100%", "420px")` is the usual answer.

## What the user can do without being allowed anything

A drawing is read-only unless [editing](../editing/index.md) is switched on, but
read-only is not the same as inert. The user can

- **pan**: drag the background to move the drawing, unless `setPanning(false)`;
- **zoom**: ctrl and the mouse wheel. A plain wheel scrolls the page, which is
  what a reader of a page that happens to contain a diagram expects;
- **select** a node, which draws a border around it and does nothing else.

None of that reaches the server, and none of it changes the model: what is
zoomed and where the drawing is scrolled to is the browser's business.

## The panel is never a field

```java
public class OrderFlowPage extends UrlPage {
    private final GraphModel m_model = createModel();     // State: a field

    @Override
    public void createContent() throws Exception {
        MaxGraphPanel.initialize(this);
        MaxGraphPanel panel = new MaxGraphPanel();        // Component: a local
        cp.add(panel);
        panel.size("100%", "420px").setModel(m_model);
    }
}
```

This is the ordinary DomUI rule and it bites harder here than elsewhere: a
`forceRebuild()` builds a new panel, the browser throws its drawing away and asks
the new panel for the model, and a panel kept in a field would leave the page
holding one that nothing on the screen belongs to any more.

Because the model is the state, nothing is lost by that: the new panel is given
the same model, and the drawing that comes back is the drawing that was there.
