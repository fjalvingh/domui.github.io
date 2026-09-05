---
menu:
  sort: "10"
---
# ContentPanel

`ContentPanel` is the panel a page's content goes in. It is a `Div` with the css
class `ui-cpnl` and nothing else - and that class is what supplies the padding
the theme prescribes.

```java
ContentPanel cp = new ContentPanel();
add(cp);
cp.add(new HTag(1, "Album"));
```

!demo(to.etc.domuidemo.pages.components.layout.PanelsPage.ui, 100%, 620)

The demo page adds one line to the page itself before the panel, so the
difference is visible: without a panel, content sits hard against the edge of
the window.

| Method | What it does |
| --- | --- |
| `new ContentPanel()` | the panel |
| `css(String...)` | extra css classes; returns the panel, so it chains |

Two rules go with it:

- **A page's content goes in one.** It is the only thing this group insists on.
- **Overlays do not.** A `MsgBox2`, a `Dialog` or a floating window is added to
  the *page*, because it is not part of the content and must not inherit its
  padding or its position.
