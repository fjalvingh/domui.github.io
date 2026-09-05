---
menu:
  sort: "30"
---
# CaptionedPanel

`CaptionedPanel` is a box with a title bar above it. Both the title and the
content are nodes, so either can hold anything.

```java
CaptionedPanel panel = new CaptionedPanel("Delivery address", new Div());
cp.add(panel);
panel.getContent().add(addressForm);
```

!demo(to.etc.domuidemo.pages.components.layout.PanelsPage.ui, 100%, 620)

| Constructor | Gives |
| --- | --- |
| `new CaptionedPanel(String title, NodeContainer content)` | a title text and the content node |
| `new CaptionedPanel(NodeContainer title)` | a title node, with an empty div as content |
| `new CaptionedPanel(NodeContainer title, NodeContainer content)` | both as nodes |

| Method | What it does |
| --- | --- |
| `getContent()` | the content node - add to this, not to the panel |
| `getTitleContainer()` | the title node |
| `setTitle(String)` | replace the title text |
| `setContentContainer(NodeContainer)` | replace the content node wholesale |

!! Add to `getContent()`, not to the panel itself: the panel holds the title and
!! the content node, and anything added directly to it lands beside them.

The panel renders as `ui-pnl-outer` around a `ui-pnl-caption` and a
`ui-pnl-cont`, so a theme styles the three parts separately.
