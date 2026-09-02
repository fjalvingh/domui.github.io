---
menu:
  sort: "50"
---
# CheckboxButton

`CheckboxButton` is a two-sided button: it shows what "on" and "off" mean, and
its value is a `Boolean`.

```java
CheckboxButton inStock = new CheckboxButton()
    .setOnLabel("In stock")
    .setOffLabel("Sold out");

FormBuilder fb = new FormBuilder(cp);
fb.label("Availability").control(inStock);
```

!demo(to.etc.domuidemo.pages.components.buttons.ToggleButtonPage.ui, 100%, 660)

[TOC]

## It is a control

`CheckboxButton` is an `IControl<Boolean>`, so it goes in a form, it can be
bound, and it answers the same questions every control does. What it adds is the
two texts:

| Method | What it does |
| --- | --- |
| `setOnLabel(String)` / `setOffLabel(String)` | the two texts; both return the button |
| `setChecked(boolean)` / `isChecked()` | the value, said the way a checkbox says it |
| `setValue(Boolean)` / `getValue()` | the same as an `IControl<Boolean>` |
| `setDisabled(boolean)` / `setReadOnly(boolean)` | passed on to the checkbox inside |
| `css(String...)` | `is-small`, `is-medium`, `is-large`, `is-xlarge` for the size |
| `immediate()` | send the change even when there is no handler |

Without labels of its own it uses DomUI's own texts - **On** and **Off** in
English - so a control that is not about on and off should say what it *is*
about.

## Reacting to a change

```java
box.setClicked(a -> recompute());          // this one
box.setOnValueChanged(a -> recompute());   // deprecated, like on the plain Checkbox
```

Use `setClicked()`, as with the plain
[`Checkbox`](../../20-choice-input/checkbox/index.md): `getOnValueChanged()` on
this control is deprecated for the same reason.

## What it renders

```html
<div class="ui-chkbb">
    <input type="checkbox" id="...">
    <label for="...">
        <div class="ui-chkbb-sw" data-checked="In stock" data-unchecked="Sold out"></div>
    </label>
</div>
```

The two texts are **css content**, drawn from the `data-checked` and
`data-unchecked` attributes - which is why they can slide past each other
without a round trip. The checkbox itself is a real checkbox, so the control
keyboard-focuses and toggles the way a checkbox does.

A mandatory control adds `ui-mandatory`, a read-only one `ui-ro` and a disabled
one `ui-disabled`.
