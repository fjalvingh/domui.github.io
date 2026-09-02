---
menu:
  sort: "40"
---
# DisplayRadiobutton

`DisplayRadiobutton` shows a `Boolean` as a radio button icon. It is the
round-icon counterpart of
[`DisplayCheckbox`](../displaycheckbox/index.md), for a value that reads as one
choice out of several rather than as a tick.

```java
DisplayRadiobutton chosen = new DisplayRadiobutton();
chosen.setValue(Boolean.TRUE);
```

!demo(to.etc.domuidemo.pages.components.display.DisplayBooleanPage.ui, 100%, 620)

[TOC]

## The API

| Method | What it does |
| --- | --- |
| `new DisplayRadiobutton()` | the default icons: an open circle and a filled one |
| `new DisplayRadiobutton(iconTrue, cssTrue, iconFalse, cssFalse)` | icons of your own, each with a css class |
| `setValue(Boolean)` / `getValue()` | the value; setting it rebuilds |
| `setChecked(boolean)` / `isChecked()` | the same as a boolean |

The icons are `IIconRef`s, so anything that can be an icon can be a state:
thumbs up and down, a lock and an open lock, a tick and a cross. That makes this
the component to reach for whenever a yes/no should be shown as *two pictures*
rather than as text.

## What it renders

A `<span class="ui-dsprb">` with the icon node of the matching state inside it,
each carrying the css class given for that state. Unlike a real radio button it
has no name, no group and no input element - it is a picture of a state.
