---
menu:
  sort: "50"
---
# ColorPickerButton

`ColorPickerButton` is a small square showing the current colour; pressing it
opens the picker over the page and closes it again when a colour is chosen.

```java
ColorPickerButton cover = new ColorPickerButton();
cover.setValue("c05a2a");
cover.setOnValueChanged(a -> repaintPreview(cover.getValue()));

FormBuilder fb = new FormBuilder(cp);
fb.label("Sleeve colour").control(cover);
```

!demo(to.etc.domuidemo.pages.components.input.ColorPickerButtonPage.ui, 100%, 560)

[TOC]

## The value

Six hexadecimal digits in a `String`, without a `#` - the same value
[`ColorPicker`](../colorpicker/index.md) has, and with the same rules: a `#` is
stripped, `null` becomes `000000`, and there is no empty state.

| Method | What it does |
| --- | --- |
| `setValue(String)` / `getValue()` | the colour |
| `setOnValueChanged(IValueChanged<?>)` | called when a colour is picked |
| `setMandatory(boolean)` | stored, but nothing checks it: the control always has a colour |
| `setDisabled(boolean)` / `setReadOnly(boolean)` | the square still shows its colour, but pressing it opens nothing |
| `setHint(String)` | the tooltip |

## When the change arrives

Unlike the open picker, this one **does** report back: give it a change handler
and picking a colour posts the new value and calls the handler, so the rest of
the screen can follow it. Without a handler nothing is posted, and the colour
simply waits on the server until the next request.

That is decided when the control is built, so a change handler set after the
control has rendered does not start the reporting - set it before, as the
example does.

## It is an IControl

`ColorPickerButton` implements `IControl<String>`, so a form builder takes it and
it can be bound:

```java
fb.property(sleeve, Sleeve_.colour()).control(new ColorPickerButton());
```

Nothing in the metadata picks this control by itself: a `String` property gets a
`Text2`, so a colour field is one you hand to the form builder yourself.
