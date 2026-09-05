---
menu:
  sort: "20"
---
# AppPageTitleBar

The bar across the top of a page: an icon, the name of the screen, a way back,
and the buttons that belong to the screen as a whole.

```java
AppPageTitleBar bar = new AppPageTitleBar("Album maintenance", false);
add(bar);                                     // On the page, above everything else
bar.setShowBackButton(true);
bar.addButton(Icon.faSearch, "Find an album", a -> find());
```

!demo(to.etc.domuidemo.pages.components.navigation.PageTitleBarPage.ui, 100%, 700)

[TOC]

## Making one

| Constructor | What it gives |
| --- | --- |
| `AppPageTitleBar(boolean catchError)` | a bar whose title comes from the page |
| `AppPageTitleBar(String title, boolean catchError)` | ...with a title of your own |
| `AppPageTitleBar(String icon, String title, boolean catchError)` | ...and an image url for the icon |

The `catchError` argument is described [below](#the-bar-as-an-error-display); a
bar that is not the page's message display is made with `false`.

Without a title of its own the bar shows the page's title - the one
`setPageTitle()` sets, or the one the page's annotations and metadata compute -
so a screen normally passes no title at all. `setPageTitle(String)` on the bar
changes it afterwards, and a bar that is already on the screen redraws itself
when it does.

## The icon

`setIcon(String)` takes a **resource url**, not an icon reference:
`"img/logo.png"` for an image in the web application, `"THEME/something.png"` for
one from the current theme.

Given none, the bar looks for one itself, in this order:

1. the icon named in the page's `@UIMenu` annotation, if it has one;
2. a `.png` next to the page class with the same name as that class
   (`AlbumEditPage.java` and `AlbumEditPage.png` in the same package);
3. `getDefaultIcon()`, which returns null unless a subclass overrides it.

So a screen that follows the naming convention gets its own icon without saying
anything, and the bar shows no image at all when there is nothing to show.

## Going back

`setShowBackButton(true)` puts a button in front of the icon. Which button
depends on the page stack:

| The stack | The button |
| --- | --- |
| there is a page below this one | **back**, which does `UIGoto.back()` |
| this page is the bottom of the stack | **close**, which closes the window |

That is decided when the bar is built, so it is right for the route by which the
user actually arrived. What the two moves do to the page stack is described in
the walkthrough under
[page navigation](../../../building-pages/60-page-navigation/index.md).

## Buttons of your own

```java
bar.addButton(Icon.faSearch, "Find an album", a -> find());
bar.addButton(Icon.faPrint, "Print the catalogue", a -> print());
```

Each call adds one small image button at the right end of the bar, with the hint
as its tooltip. `getButtonpart()` is the cell they sit in, for anything that is
not a plain button.

An application whose every screen needs the same buttons overrides
`addDefaultButtons(NodeContainer)` in a subclass of the bar; the bar itself adds
none.

## The bar as an error display

A bar made with `catchError` set to `true` listens to the error fence above it
and shows the messages it catches, in a line under the title:

```java
AppPageTitleBar bar = new AppPageTitleBar("Order an album", true);
add(bar);
```

It registers itself when it is added to the page and deregisters when it is
removed, so nothing has to be cleaned up. What a message is and how it finds a
fence is one mechanism, described under
[telling something to a user](../../../building-pages/90-telling-the-user/index.md);
this is one of the components that can show the result.

!! One display per fence. A page whose title bar catches errors should not also
!! have an `ErrorPanel` or an `ErrorMessageDiv` on the same fence, or every
!! message appears twice.

## The rest of it

| Method | What it does |
| --- | --- |
| `setHint(String)` | a tooltip on the title itself |
| `setShowAsModified(boolean)` | put a `*` in front of the title: the screen has unsaved changes |
| `getTitlePart()` | the cell the title is in |
| `getButtonpart()` | the cell the buttons are in |
| `getBody()` | the bar's own table body - only after it has been built |

The bar writes itself under `.ui-atl`, with `.ui-atl-i` for the icon cell,
`.ui-atl-t` for the title and `.ui-atl-bb` for the buttons.
