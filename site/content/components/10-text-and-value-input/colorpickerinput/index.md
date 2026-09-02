---
menu:
  sort: "60"
---
# ColorPickerInput

`ColorPickerInput` is a text box holding the hex code, with a small swatch of
that colour beside it. Clicking in the box opens the picker; the code can also
just be typed.

```java
ColorPickerInput cover = new ColorPickerInput();
cover.setValue("c05a2a");
cover.setOnValueChanged(a -> repaintPreview(cover.getValue()));

FormBuilder fb = new FormBuilder(cp);
fb.label("Sleeve colour").control(cover);
```

!demo(to.etc.domuidemo.pages.components.input.ColorPickerInputPage.ui, 100%, 600)

[TOC]

## The value

Six hexadecimal digits in a `String`, without a `#`. This is the one colour
control that can be empty:

| Method | What it does |
| --- | --- |
| `setValue(String)` | the colour, and the swatch beside the box |
| `getValue()` | the six hex digits, or `null` when the box is empty and the control is not mandatory |
| `setMandatory(boolean)` | **defaults to true**; a mandatory control that is empty hands back `000000` rather than `null` |
| `setOnValueChanged(IValueChanged<?>)` | called when a colour is picked |
| `setDisabled(boolean)` / `setReadOnly(boolean)` | the box keeps its value and swatch, but the picker no longer opens |
| `setHint(String)` | the tooltip |

Mandatory defaulting to `true` is the opposite of every other control, and it
does not report an error the way a mandatory `Text2` does - it simply substitutes
black. Call `setMandatory(false)` when an unset colour has to stay unset.

## The swatch is a sibling

The control **is** the `<input>` element, and the swatch is a separate `div`
that the control appends *after itself* when it is built, and removes when it
leaves the page. It is not a child of the control: anything that moves the input
without moving what follows it leaves the swatch behind. Adding the control to a
form builder, a panel or a table cell - the ordinary cases - works as expected.

## When the change arrives

As with [`ColorPickerButton`](../colorpickerbutton/index.md), the change is only
posted when the control has a change handler at the time it is built, and the
picker is only attached when the control is neither disabled nor read only.

## Which one to use

| Control | Use it when |
| --- | --- |
| [`ColorPicker`](../colorpicker/index.md) | there is room for the picker to stand open, and nothing has to react |
| [`ColorPickerButton`](../colorpickerbutton/index.md) | a form field where the colour itself is the label |
| `ColorPickerInput` | a form field where the hex code has to be visible or typed |
