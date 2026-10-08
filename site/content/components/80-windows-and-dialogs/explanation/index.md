---
menu:
  sort: "110"
---
# Explanation

A block of explanation with a severity - a remark, a warning or an error - drawn
as a callout: a bar on the left and a round marker in the severity's colour, on
that severity's tint, with the text beside the marker.

```java
cp.add(new Explanation("Search is on the album title, and it is case insensitive."));
cp.add(new Explanation(MsgType.WARNING, "Deleting an artist deletes its albums with it."));
```

!demo(to.etc.domuidemo.pages.components.dialog.NoticePage.ui, 100%, 760)

[TOC]

| Method | What it does |
| --- | --- |
| `Explanation(String text)` | an explanation of type `INFO` |
| `Explanation(MsgType type, String text)` | ...of that type |
| `setText(String)` | replace the text |

The type picks the css class (`ui-expl ui-info`, `ui-warning`, `ui-error`), and
the theme draws the rest - there is no image - so the colour of the block follows
what is being said, and the [colour scheme](../../../look-and-feel/themes/index.md)
it is said in. The text is xml text: html in it is rendered, as one paragraph.

It is, like [`MessageLine`](../messageline/index.md), part of the page and not a
posted message - nothing puts it there but your own `createContent()`.
