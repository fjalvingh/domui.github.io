---
menu:
  sort: "70"
---
# TabPanel

`TabPanel` puts several screens in the space of one. Tabs are made with the tab
builder, and each one hands back an `ITabHandle` - which is how it is addressed
afterwards.

```java
TabPanel tp = new TabPanel(true);           // true: mark the tab an error came from
cp.add(tp);

tp.tab().label("Details").content(detailsFragment).build();
tp.tab().label("Tracks").image(Icon.faMusic).content(trackTable).build();
ITabHandle history = tp.tab().label("History").content(historyPanel).lazy().build();
```

!demo(to.etc.domuidemo.pages.components.layout.TabPanelPage.ui, 100%, 900)

[TOC]

## The tab builder

`tab()` starts a tab; `build()` finishes it and returns its handle. Forgetting
`build()` throws when the panel renders.

| Call | What it does |
| --- | --- |
| `label(String)` / `label(IBundleCode)` / `label(NodeBase)` | the tab's label |
| `image(IIconRef)` | an icon in front of the label |
| `content(NodeBase)` | what the tab shows - **required** |
| `lazy()` / `lazy(boolean)` | build the content the first time the tab is opened |
| `closable()` | give the tab a cross the user can press |
| `position(int)` | where in the row it goes |
| `onDisplay(INotify<ITabHandle>)` | called when the tab is shown |
| `onHide(INotify<ITabHandle>)` | called when it is left |
| `onClose(INotify<ITabHandle>)` | called when it is closed |
| `testId(String)` | a stable id for tests |
| `build()` | finish, and return the `ITabHandle` |

## The handle

| Method | What it does |
| --- | --- |
| `select()` | show this tab |
| `updateLabel(String, IIconRef)` / `updateLabel(NodeBase, IIconRef)` | change the label |
| `updateContent(NodeContainer)` | replace the body |
| `close()` | close the tab; it is unusable afterwards |

Keep the handle of any tab the code has to touch later. There is no "give me tab
number three".

## Lazy tabs

A tab marked `lazy()` does not add its content to the page until it is first
opened, and never adds it at all if the user never goes there. That matters when
a tab costs a query: three tabs of which one is looked at is one query rather
than three.

The demo page has one, with a button that opens it from code - the content
appears on the page only at that moment.

## Errors on a tab nobody is looking at

`new TabPanel(true)` makes the panel an **error fence** and marks the tab an
error came from (`ui-tab-err`). Without it, a mandatory field on a tab that is
not open reports its error into nothing the user can see, and the screen simply
refuses to save with no visible reason.

Use it for any panel whose tabs hold input.

## Too many tabs

When the tabs no longer fit on a line, `TabPanel` wraps them onto a second line.
[`ScrollableTabPanel`](../scrollabletabpanel/index.md) keeps them on one line and
puts arrows at the ends instead; it takes exactly the same builder.
