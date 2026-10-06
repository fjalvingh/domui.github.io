---
menu:
  sort: "60"
---
# ExpandHeader

`ExpandHeader` is a header that owns what is under it: pressing it - its arrow or
its title - folds that content away, pressing it again brings it back.

```java
ExpandHeader header = new ExpandHeader("Sales history");
cp.add(header);
header.setContent(salesTable);
header.setExpanded(true);				// it starts folded
```

!demo(to.etc.domuidemo.pages.components.layout.HeadersPage.ui, 100%, 700)

[TOC]

## The API

| Method | What it does |
| --- | --- |
| `new ExpandHeader(String title)` | a normal-sized header |
| `new ExpandHeader(Type, String)` | `NORMAL` or `SMALL` |
| `setContent(NodeBase)` | what the header shows and folds away; it is kept while folded |
| `setOnExpand(INotify<Div>)` | instead of `setContent()`: fills the content afresh every time the header is opened, and folding drops it |
| `setExpanded(boolean)` / `isExpanded()` / `toggleExpansion()` | open and close from code; a new header starts folded |
| `setCaption(String)` / `setCaptionNode(NodeBase)` | the title, as a text or as a node |
| `setActionList(List<IUIAction<?>>)` / `clearActions()` | a hamburger menu of [actions](../../40-buttons/actionbutton/index.md) at the right |

The difference with the other two headers is exactly that ownership: a
[`GenericHeader`](../genericheader/index.md) or a
[`Caption2`](../caption2/index.md) is a line above whatever happens to follow it,
while this one is given the content and shows or hides it.

## What folding costs

Content given with `setContent()` stays on the page and is hidden, so folding is a
css change rather than a rebuild: the state of everything inside it - a half-filled
form, a table's scroll position - survives. It also means the content is built even
while it is closed. Where that is the expensive part, use `setOnExpand()` instead:
the content is then only made when the header is opened, and dropped again when it
is folded.
