---
menu:
  sort: "100"
---
# VerticalSpacer

`VerticalSpacer` is a gap of exactly so many pixels.

```java
cp.add(new VerticalSpacer(20));
```

!demo(to.etc.domuidemo.pages.components.layout.PanelsPage.ui, 100%, 620)

It is a `Div` of the given height holding a non-breaking space, with its
overflow hidden. That is all it is.

Use it where a gap is a one-off - between two panels on one screen, above a
button bar. Where the same gap belongs everywhere, it belongs in the theme
instead: a css class on the components around it says *why* there is space, and
a spacer only says that there is.
