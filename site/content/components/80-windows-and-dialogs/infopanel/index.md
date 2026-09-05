---
menu:
  sort: "100"
---
# InfoPanel

A paragraph of explanation with a large icon beside it: the block at the top of a
screen that says what the screen is for.

```java
cp.add(new InfoPanel("The CD shop sells albums, not tracks.<br/>"
	+ "A track can only be bought as part of the album it is on."));
```

!demo(to.etc.domuidemo.pages.components.dialog.NoticePage.ui, 100%, 760)

[TOC]

| Method | What it does |
| --- | --- |
| `InfoPanel(String text)` | the text, with the theme's large info icon |
| `InfoPanel(String text, String icon)` | ...with an icon of your own, by resource url |
| `setIcon(String)` / `getIcon()` | change that icon afterwards |

The text may contain html, so it can hold more than one line, a list or a link.
The panel carries the `ui-ipa` class, which is where its width and its background
come from.

For the same thing with a severity - a warning or an error rather than a remark -
use [`Explanation`](../explanation/index.md); for a single line,
[`MessageLine`](../messageline/index.md).
