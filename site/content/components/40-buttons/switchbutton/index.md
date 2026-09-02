---
menu:
  sort: "60"
---
# SwitchButton

`SwitchButton` is a plain on/off switch: the same value as a
[`CheckboxButton`](../checkboxbutton/index.md) with no texts on it at all.

```java
SwitchButton active = new SwitchButton();
active.setChecked(true);

FormBuilder fb = new FormBuilder(cp);
fb.label("Active").control(active);
```

!demo(to.etc.domuidemo.pages.components.buttons.ToggleButtonPage.ui, 100%, 660)

[TOC]

## The API

| Method | What it does |
| --- | --- |
| `setValue(Boolean)` / `getValue()` | the value, as an `IControl<Boolean>` |
| `setChecked(boolean)` / `isChecked()` | the same, said the way a checkbox says it |
| `setDisplayMode(DisplayMode)` | `Rounded` (the default) or `Square` |
| `setDisabled(boolean)` / `setReadOnly(boolean)` | passed on to the checkbox inside |
| `setClicked(...)` | what to do when it is flipped |

Like the `CheckboxButton`, `getOnValueChanged()` is deprecated on it: use
`setClicked()`.

## When to use it rather than a CheckboxButton

Use the switch where the label beside it already says what is being switched -
*Active*, *Send me the newsletter* - and the button only has to say yes or no.
Use a [`CheckboxButton`](../checkboxbutton/index.md) where the two states have
names of their own that are worth reading, like *In stock* and *Sold out*.

## What it renders

```html
<label class="ui-swtch">
    <input type="checkbox" id="...">
    <span class="ui-swtch-sl ui-swtch-rounded"></span>
</label>
```

The control itself is the `<label>`, so clicking anywhere on it flips the
checkbox inside; the span is the slider the theme draws.
