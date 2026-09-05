---
menu:
  sort: "60"
---
# ExpandHeader

`ExpandHeader` is a header that owns what is under it: pressing it folds that
content away, pressing it again brings it back.

```java
ExpandHeader header = new ExpandHeader("Sales history");
cp.add(header);
header.setContent(salesTable);
```

!demo(to.etc.domuidemo.pages.components.layout.HeadersPage.ui, 100%, 700)

[TOC]

## The API

| Method | What it does |
| --- | --- |
| `new ExpandHeader(String title)` | a normal-sized header |
| `new ExpandHeader(Type, String)` | `NORMAL` or `SMALL` |
| `setContent(NodeBase)` | what the header folds away - **give it this**, or it has nothing to do |
| `setExpanded(boolean)` / `isExpanded()` / `toggleExpansion()` | open and close from code |
| `setCaption(String)` / `setCaptionNode(NodeBase)` | the title, as a text or as a node |
| `setActionList(List<IUIAction<?>>)` / `clearActions()` | a hamburger menu of [actions](../../40-buttons/actionbutton/index.md) at the right |

The difference with the other two headers is exactly that ownership: a
[`GenericHeader`](../genericheader/index.md) or a
[`Caption2`](../caption2/index.md) is a line above whatever happens to follow it,
while this one is given the content and shows or hides it.

## What folding costs

The content node stays on the page and is hidden, so folding is a css change
rather than a rebuild: the state of everything inside it - a half-filled form, a
table's scroll position - survives. It also means the content is built even
while it is closed. Where that is the expensive part, put the content in a
[`TabPanel`](../tabpanel/index.md) tab marked `lazy()` instead, which is not
built until it is first shown.
