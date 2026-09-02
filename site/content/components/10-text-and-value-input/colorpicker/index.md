---
menu:
  sort: "40"
---
# ColorPicker

`ColorPicker` is the colour picker itself, standing open on the page: a colour
field, a hue bar and the hex, RGB and HSB values.

```java
ColorPicker picker = new ColorPicker();
picker.setValue("c05a2a");
cp.add(picker);

//-- somewhere later
String colour = picker.getValue();           // "c05a2a"
```

!demo(to.etc.domuidemo.pages.components.input.ColorPickerPage.ui, 100%, 560)

[TOC]

## The value

The value is a `String` of six hexadecimal digits **without** a leading `#`. A
`#` handed to `setValue()` is stripped, and `null` becomes `000000` - the
control has no empty state.

| Method | What it does |
| --- | --- |
| `setValue(String)` | set the colour; also updates the open picker |
| `getValue()` | the six hex digits currently picked |
| `setOnValueChanged(IValueChanged<?>)` | stored, but see below |

## How the value gets back

Every move in the picker writes the new colour straight into a hidden input, in
the browser. That input travels with the next request like any other, so by the
time a click handler runs the control already holds what the user picked -
without a round trip per movement.

The consequence is that a change handler on this control does **not** fire when
the colour changes: nothing tells the server it happened.
[`ColorPickerButton`](../colorpickerbutton/index.md) and
[`ColorPickerInput`](../colorpickerinput/index.md) do report a change, and are
the ones to use when something on the screen has to follow the colour.

## What it is not

`ColorPicker` implements `IHasChangeListener`, not `IControl<String>`: it has no
mandatory, read-only or disabled state, and it cannot be bound or handed to a
form builder. It is a picker on a page, not a form field. For a form field use
one of the other two.

The picker takes about 356 by 176 pixels and is always open, so it belongs on a
screen with room for it - a settings page, a panel of its own.
