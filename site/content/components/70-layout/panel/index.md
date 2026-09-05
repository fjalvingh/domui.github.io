---
menu:
  sort: "20"
---
# Panel

`Panel` is a plain box: a `Div` with the css class `ui-spnl`, for grouping
things that belong together.

```java
Panel panel = new Panel();
cp.add(panel);
panel.add("Everything about the delivery goes in here.");
```

!demo(to.etc.domuidemo.pages.components.layout.PanelsPage.ui, 100%, 620)

| Constructor | Gives |
| --- | --- |
| `new Panel()` | a box with the standard `ui-spnl` class |
| `new Panel(String css)` | a box with a class of your own instead |

That is the whole component. It exists so that a screen says *panel* rather than
*div with a particular class*, and so that the class is decided in one place.

For a box that says what is in it, use
[`CaptionedPanel`](../captionedpanel/index.md); for the panel a page's content
lives in, [`ContentPanel`](../contentpanel/index.md).
