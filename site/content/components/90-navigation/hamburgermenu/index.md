---
menu:
  sort: "40"
---
# HamburgerMenu

The list of actions behind the three-bar button: everything that can be done to
what the button belongs to, without any of it taking up room on the screen.

```java
ExpandHeader header = new ExpandHeader("Led Zeppelin IV");
cp.add(header);
header.addAction(play);
header.addAction(order);
```

!demo(to.etc.domuidemo.pages.components.navigation.HamburgerMenuPage.ui, 100%, 560)

[TOC]

## Where it comes from

Usually you do not make one. An
[`ExpandHeader`](../../70-layout/expandheader/index.md) given a list of
[actions](../../40-buttons/actionbutton/index.md) grows the three-bar button at
its right, and pressing it opens a `HamburgerMenu` of those actions just under
it. That is the whole of the API most screens need:

| Call on the header | What it does |
| --- | --- |
| `addAction(IUIAction<?>)` | one more entry in the menu |
| `setActionList(List<IUIAction<?>>)` | the whole menu at once |
| `clearActions()` | no menu, and no button either |
| `closeMenu()` | close it from code |

With no actions the header has no button, so a header that needs no menu costs
nothing.

## Making one yourself

```java
HamburgerMenu menu = new HamburgerMenu(actions);
button.appendAfterMe(menu);
menu.setOnSelection(action -> action.execute(button, null));
```

| Method | What it does |
| --- | --- |
| `new HamburgerMenu(List<IUIAction<?>>)` | the menu, from the actions it shows |
| `setOnSelection(INotify<IUIAction<?>>)` | told which action was chosen |
| `close()` / `isClosed()` | close it, and ask whether it is gone |

Each entry takes its name, its icon and its reason to be disabled from its own
action, exactly as a button made from that action does. A disabled entry is
greyed out, shows its reason as a tooltip and does not answer a click.

!! The menu does not appear *under the button*. It is positioned absolutely at
!! `right: 0` of the block it is added to, so it lines up with the right edge of
!! that block wherever the button happens to be. It therefore belongs to a
!! button that is itself at the right - which is where `ExpandHeader` puts its
!! three-bar button, and why it looks right there and lopsided anywhere else.

!! The menu does **not** run the action. It closes itself and hands the chosen
!! action to the `onSelection` notify, and that is where `execute()` is called.
!! Without a notify, choosing an entry does nothing at all.

## Closing

A `HamburgerMenu` is a *close on click* panel: it removes itself from the page
when something is chosen, when the mouse is pressed anywhere else, and when
escape is pressed. Opening one also closes every other one that is still up, so
two of these are never open at the same time.

Like a [`PopupMenu2`](../popupmenu2/index.md) it is therefore built when the
button is pressed and never kept in a field.

## Which of the two menus

Both are a small menu that opens at a component and closes itself, and both are
made of actions. The difference is what opens them:

| | Opened by | Filled with |
| --- | --- | --- |
| [`PopupMenu2`](../popupmenu2/index.md) | anything, or the chevron of an `ActionButton` | actions **or** items built by hand |
| `HamburgerMenu` | the hamburger button of an `ExpandHeader` | actions only |

New code that needs a menu of its own is better off with `PopupMenu2`: it is the
newer of the two, it takes items that are not actions, and it opens **at** the
component that owns it instead of at the right edge of a block.

The menu is written under `.ui-hmbrg-menu`, one `.ui-hmbrg-item` per entry.
