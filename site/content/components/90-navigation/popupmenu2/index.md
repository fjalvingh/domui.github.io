---
menu:
  sort: "30"
---
# PopupMenu2

A small menu that opens at a component, does one thing and disappears again.

```java
button.setClicked(a -> {
    PopupMenu2 pm = new PopupMenu2(a);                  // Opens at the button
    pm.text("Play it").icon(Icon.faMusic).click(() -> play(album)).append();
    pm.text("Add to the cart").icon(Icon.faShoppingCart).click(() -> order(album)).append();
    pm.show(a);
});
```

!demo(to.etc.domuidemo.pages.components.navigation.PopupMenu2Page.ui, 100%, 620)

[TOC]

## One item at a time

An item is described by chaining calls and then **appended**, which is what
actually adds it:

| Call | What it says about the next item |
| --- | --- |
| `text(String)` / `text(IBundleCode, Object...)` | its text |
| `icon(IIconRef)` | its icon |
| `hint(String)` / `hint(IBundleCode, Object...)` | its tooltip |
| `click(IExecute)` | what choosing it does |
| `disableReason(String)` | it cannot be chosen, and why |
| `testId(String)` | the test id on its row, for Selenium |
| `append()` | ...and now it is an item |

Every one of those refuses to overwrite a value that is already set, so a
forgotten `append()` throws instead of quietly merging two items into one. An
item needs at least a text or an icon; without either, `append()` throws as well.

A disabled item is drawn greyed out and does not answer a click. Its reason
becomes its tooltip - after the hint, if it has one.

**The menu adapts to what is in it.** An icon column is written only when some
item has an icon, and a text column only when some item has a text; a menu of
nothing but icons is a row of icons with tooltips, not a row of icons and empty
space.

## Showing it

| Call | What it does |
| --- | --- |
| `new PopupMenu2(NodeContainer owner)` | the menu opens at this component |
| `above()` / `below()` | which side of the owner it opens on; below by default |
| `show(NodeContainer)` | put it on the page |

`show()` adds the menu to the **page** rather than to whatever is around the
owner, and javascript then positions it against the owner and fades it in.

## It closes itself

The menu goes away when an item is chosen, and when the mouse is pressed anywhere
outside it - and *going away* means it removes itself from the page. There is
nothing to close, nothing to hide and nothing to clean up.

So a `PopupMenu2` is built in the click handler that opens it, every time, and is
never kept in a field:

```java
//-- Right: a new menu each time, thrown away when it closes
button.setClicked(a -> {
    PopupMenu2 pm = new PopupMenu2(a);
    ...
    pm.show(a);
});
```

## The shorter way to the same menu

Where the entries are [actions](../../40-buttons/actionbutton/index.md) - which
already know their name, their icon and the reason they cannot be used - an
`ActionButton` builds this menu for you:

```java
ActionButton b = new ActionButton(album, play);
b.addAction(album, order);
b.addAction(album, delete);
```

The chevron on the button opens a `PopupMenu2` filled from those actions. Build
the menu by hand when there are no actions to reuse, or when the entries are not
operations on one record.

The menu is written under `.ui-pome2`, one `.ui-pome2-r` per row.
