# The body document (UrlPage)

Every DomUI page extends `UrlPage`, and a `UrlPage` **is** the `<body>` of the
rendered document. It is an ordinary `NodeContainer` - a `Div` subclass, in fact
- so everything true of a node is true of it, and this page is only about the
things that are true of it *alone*.

[TOC]

## The title in the browser

```java
setTitle("Album - " + album.getTitle());        // the browser's title bar
setPageTitle("Album");                          // the title bar on the page
```

On every other node, `title` is the html `title` **attribute** - the tooltip. On
a `UrlPage` it is the `<title>` element of the document instead, because the
page is the body and the head is rendered from it.

`pageTitle` is a different property with a confusingly similar name: it is the
page's name as [`AppPageTitleBar`](../../components/90-navigation/index.md) and
the breadcrumb show it, and it never reaches the head.

A page that sets no title gets one from
`DomApplication.getDefaultPageTitle(body)`, which is
`"DomUI Application - " + the class's simple name` unless the application
overrides it.

## Lifecycle hooks

`createContent()` builds the page and is called again after every
`forceRebuild()`. Around it, `UrlPage` adds hooks that only a page has:

| Method | When it runs |
| --- | --- |
| `onReload()` | the page is being reloaded - a root page only |
| `onDestroy()` | the page is being thrown away, by navigation or by the conversation ending |
| `onAfterRequest()` | at the end of every request that touched this page |
| `afterCreateContent()` | after `createContent()` has run, for a base class that has to act on the finished tree |
| `onForceRebuild()` | the tree is about to be discarded and rebuilt |

`onShelve()` and `onUnshelve()` come from `NodeContainer` and fire when the page
is put aside for another page and brought back;
[state management](../state-management/index.md) is where that story is told.

## The database context of the page

```java
QDataContext dc = getSharedContext();
```

A page has a **shared** `QDataContext`: created when first asked for, held by the
page's conversation, released when that conversation ends. Every component on
the page that asks gets the same one, which is what makes an entity loaded in
one part of the page the same object as in another.

`getSharedContext(key)` gives a second, independent context under a name of your
own, for work that must not sit in the same transaction.
`resetAllSharedContexts()` throws them all away. `forceReloadData()` does that,
re-injects the page's URL parameters and rebuilds - the way to make a page
re-read everything it shows.

`lc()` returns the `ILogicContext` for the page's shared context - the entry
point to the logic classes, when an application uses them.

## Odds and ends

- `redirectIn(url, milliseconds)` schedules a browser redirect, for a page that
  shows something and then moves on.
- `closeWindow()` closes the browser window the page is in.
- `postbox()` is the page's `AsyncMessageLink`: how work on another thread hands
  results back to the page (see
  [asynchronous work](../../components/130-async/index.md)).
- `setThemeVariant()` puts this page on a variant of the current theme.
