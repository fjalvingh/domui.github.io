---
menu:
  sort: "80"
---
# ScrollableTabPanel

`ScrollableTabPanel` is a [`TabPanel`](../tabpanel/index.md) that keeps its tabs
on **one line** and puts scroll arrows at the ends, for when there are more tabs
than fit.

```java
ScrollableTabPanel tp = new ScrollableTabPanel();
cp.add(tp);
for(Period period : periodList) {
    tp.tab().label(period.getName()).content(panelFor(period)).lazy().build();
}
```

!demo(to.etc.domuidemo.pages.components.layout.TabPanelPage.ui, 100%, 900)

Everything on the [`TabPanel`](../tabpanel/index.md) page applies: the same tab
builder, the same `ITabHandle`, the same lazy tabs and the same error marking.
What differs is only the header - the labels are kept on one line, and the two
arrows scroll them.

| | `TabPanel` | `ScrollableTabPanel` |
| --- | --- | --- |
| tabs that do not fit | wrap onto another line | stay on one line, reached with the arrows |
| use it for | a handful of tabs, known in advance | as many as the data happens to produce |

The arrows disable themselves at the ends, and hide altogether when everything
fits. The panel recalculates that when the window is resized and when the page
is returned to.
