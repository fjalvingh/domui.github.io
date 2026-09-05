# Layout and page structure

The shape around the content: the panel a page's content sits in, the headers
that divide it into sections, the tabs that put three screens in the space of
one, and the fragment that shows the children of a record.

[TOC]

## The components

| Component | What it is for |
| --- | --- |
| [`ContentPanel`](contentpanel/index.md) | the panel a page's content goes in - the one rule of this group |
| [`Panel`](panel/index.md) | a plain box to group things in |
| [`CaptionedPanel`](captionedpanel/index.md) | the same box with a title bar above it |
| [`Caption2`](caption2/index.md) | a title bar of its own, with an icon and buttons |
| [`GenericHeader`](genericheader/index.md) | a header line in one of six styles, with optional buttons |
| [`ExpandHeader`](expandheader/index.md) | a header that folds what is under it away |
| [`TabPanel`](tabpanel/index.md) | several screens in the space of one |
| [`ScrollableTabPanel`](scrollabletabpanel/index.md) | the same with more tabs than fit on a line |
| [`SplitterPanel`](splitterpanel/index.md) | two panels with a bar the user can drag |
| [`VerticalSpacer`](verticalspacer/index.md) | a gap of exactly so many pixels |
| [`ChildFragment`](childfragment/index.md) | the children of a record, in a table that follows it |

## The one rule

**A page's content goes inside a `ContentPanel`.** The page body has no padding
of its own, so anything added straight to the page sits hard against the edge of
the window. Everything else in this group is optional; that is not.

```java
ContentPanel cp = new ContentPanel();
add(cp);
cp.add(new HTag(1, "Album"));
```

Overlays are the exception: a message box or a floating window is added to the
**page**, not to the panel, because it is not part of the content.

## Writing a piece of screen yourself

Most of what a screen is made of is not a component from this list but a
**fragment** of your own: a `Div` that fills itself in `createContent()` - a
`UrlPage` minus the url. That is how a card, a summary block or a panel of your
own is written, and it is described in the walkthrough under
[layout](../../building-pages/100-layout/index.md), together with `ContentPanel`,
`ButtonBar2` and the tab builder.

[`ChildFragment`](childfragment/index.md) is the one such fragment the framework
ships, because "show the children of this record" is a screen everybody writes.
