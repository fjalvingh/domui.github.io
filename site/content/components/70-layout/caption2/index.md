---
menu:
  sort: "40"
---
# Caption2

`Caption2` is a title **bar**: it fills its width, it can carry an icon, and its
buttons sit at the right-hand end.

```java
Caption2 caption = new Caption2(CaptionType.Default, "Invoice lines");
cp.add(caption);
caption.addButton(Icon.faPlus, "Add a line", a -> addLine());
```

!demo(to.etc.domuidemo.pages.components.layout.HeadersPage.ui, 100%, 700)

[TOC]

## The API

| Constructor | Gives |
| --- | --- |
| `new Caption2(CaptionType)` | a bar in one of the two standard styles, without a text yet |
| `new Caption2(CaptionType, String)` | the same with its text |
| `new Caption2(String cssClass)` / `(String cssClass, String title)` | a bar with a css class of your own |

| Method | What it does |
| --- | --- |
| `setCaption(String)` / `getCaption()` | the text; setting it rebuilds the bar |
| `setIcon(String)` | an image at the left of the bar |
| `addButton(IIconRef, String hint, IClicked<NodeBase>)` | a small button at the right |
| `addButton(IIconRef, String hint, String onClickJs)` | the same, handled in the browser |

`CaptionType` decides the look: `Default` is a bar standing on its own
(`ui-cptn2-alg`), `Panel` is one meant to sit on top of a panel
(`ui-cptn2-pnl`).

## Which header to use

| | Use |
| --- | --- |
| a line of text above a section | [`GenericHeader`](../genericheader/index.md) |
| a bar across the width, with buttons in it | `Caption2` |
| a header that folds its content away | [`ExpandHeader`](../expandheader/index.md) |
| the title of a box | [`CaptionedPanel`](../captionedpanel/index.md) |
