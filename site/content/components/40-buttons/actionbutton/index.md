---
menu:
  sort: "70"
---
# Actions: IUIAction and ActionButton

An `IUIAction` is one description of something that may be done to an instance:
its name, its tooltip, its icon, the reason it cannot be done right now, and the
code that does it. Buttons are then made *from* the action, and none of them
repeats any of that.

```java
IUIAction<Album> ship = new UIAction<>("Ship it", "Send this album to the customer",
    Icon.faTruck, null, (node, album) -> shipTo(album));

cp.add(new DefaultButton(album, ship));
bar.addAction(album, ship);
```

!demo(to.etc.domuidemo.pages.components.buttons.ActionButtonPage.ui, 100%, 620)

[TOC]

## The interface

```java
public interface IUIAction<T> {
    String getName(T instance) throws Exception;            // the button's text
    String getTitle(T instance) throws Exception;            // its tooltip
    IIconRef getIcon(T instance) throws Exception;            // its icon
    String getDisableReason(T instance) throws Exception;    // null when it may be done
    void execute(NodeBase component, T instance) throws Exception;
}
```

Every method gets the instance, so the same action can answer differently for
different records: an order that is already shipped returns a disable reason, a
draft one returns `null`.

A button built from an action asks it all five questions when it is built:

| The action says | The button becomes |
| --- | --- |
| `getName()` | its text |
| `getIcon()` | its icon |
| `getDisableReason()` returns null | enabled, with `getTitle()` as tooltip |
| `getDisableReason()` returns a text | **disabled**, with that reason as tooltip |
| `execute()` | what its click handler calls |

`UIAction<T>` is the ready-made implementation: name, title, icon, an optional
disable reason and a lambda.

```java
IUIAction<Album> reprint = new UIAction<>("Reprint", "Have the sleeve printed again",
    Icon.faPrint, "The printer is out of ink", (node, album) -> reprint(album));
```

## Where an action can be used

| Where | Call |
| --- | --- |
| a button | `new DefaultButton(instance, action)` |
| a button bar | `bar.addAction(instance, action)` |
| a button with a menu | `new ActionButton(instance, action)` |
| a popup menu | `PopupMenu2.text(...)...` built from the action's parts |

!! `LinkButton(IUIAction<Void>)` and `ButtonBar2.addButton(IUIAction<Void>)`
!! take an action over `Void` only - an action with an instance goes through
!! `DefaultButton(instance, action)` or `bar.addAction(instance, action)`.

## ActionButton: more actions behind one button

`ActionButton` is a `DefaultButton` for the main action plus a chevron that
opens a menu of the others:

```java
ActionButton b = new ActionButton(album, ship);
b.addAction(album, reprint);
b.addAction(album, cancel);
cp.add(b);
```

| Method | What it does |
| --- | --- |
| `addAction(instance, action)` | one more entry in the menu |
| `removeActions()` | empty the menu (the main action stays) |
| `above()` / `below()` | which way the menu opens; below by default |

Each menu entry takes its name, tooltip, icon and disable reason from its own
action, exactly as the button does. With no extra actions added, the chevron is
not rendered at all and an `ActionButton` is just a button.

## Why bother

The point is that "may this be done, and what is it called" lives in one place.
A screen with the same operation on a button bar, in a row menu and on a detail
page states it once; when the rule changes - a new reason to disable it, a
different icon - every button that uses it follows.
