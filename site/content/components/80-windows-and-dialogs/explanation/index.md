---
menu:
  sort: "110"
---
# Explanation

An [`InfoPanel`](../infopanel/index.md) with a severity: the same block of
explanation, but as a remark, a warning or an error.

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

The type picks both the large icon and the css class (`ui-expl ui-info`,
`ui-warning`, `ui-error`), so the colour of the block follows what is being said.
The text is xml text: html in it is rendered.

It is, like [`MessageLine`](../messageline/index.md), part of the page and not a
posted message - nothing puts it there but your own `createContent()`.
