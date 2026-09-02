---
menu:
  sort: "10"
---
# Checkbox

`Checkbox` is one box that is either ticked or not. Its value is a `Boolean`,
and it is never `null`.

```java
Checkbox newsletter = new Checkbox();
newsletter.setChecked(true);
newsletter.setClicked(a -> shown.add("Newsletter is now " + newsletter.getValue()));

FormBuilder fb = new FormBuilder(cp);
fb.label("Send me the newsletter").control(newsletter);
```

!demo(to.etc.domuidemo.pages.components.choice.CheckboxPage.ui, 100%, 620)

[TOC]

## The value

| Method | What it does |
| --- | --- |
| `setChecked(boolean)` / `isChecked()` | tick it, ask whether it is ticked |
| `setValue(Boolean)` / `getValue()` | the same thing as an `IControl<Boolean>` |
| `setDisabled(boolean)` / `setDisabledBecause(String)` | greyed out, with the reason as its tooltip |
| `setMandatory(boolean)` | stored, and nothing checks it - see below |
| `setHint(String)` | the tooltip |

`setValue(null)` unticks the box, and `getValue()` on an unticked box is
`Boolean.FALSE`. There is no third state and nothing to convert, so `getValue()`
can never report an error the way a `Text2` does - which also means a mandatory
checkbox is not enforced. When a box *must* be ticked, check it yourself in the
handler and post the message.

## No read-only state

`setReadOnly(true)` calls `setDisabled(true)`, and `isReadOnly()` returns
`isDisabled()`: a checkbox has no way to show a value that cannot be changed
other than being disabled. Where a page wants a tick that reads as text rather
than as a dead control, `DisplayCheckbox` is the display-only component for it.

## Use the click handler, not the change handler

```java
box.setClicked(a -> recompute());          // this one
box.setOnValueChanged(a -> recompute());   // not this one - it is deprecated
```

`setOnValueChanged()` and `getOnValueChanged()` are deprecated on `Checkbox`.
Use `setClicked()`: it fires on the click that changed the box, and the value is
already in the control by the time the handler runs.

`immediate()` is the other way to have the value posted - it makes the box send
its state even when it has no handler at all, which is what a bound checkbox
whose model is read by *another* control needs.

## What it renders

A `Checkbox` is a bare `<input type="checkbox">` - it is one of the few controls
that is a single html element rather than a div around one. `getForTarget()`
returns the checkbox itself, so a `<label>` told to point at the control
(`Label.setForTarget(box)`) ends up pointing at the box, and clicking the label
ticks it.
