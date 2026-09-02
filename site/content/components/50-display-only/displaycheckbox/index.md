---
menu:
  sort: "30"
---
# DisplayCheckbox

`DisplayCheckbox` shows a `Boolean` as a tick box that cannot be pressed. It is
an image, not an input.

```java
DisplayCheckbox paid = new DisplayCheckbox(invoice.isPaid());

FormBuilder fb = new FormBuilder(cp);
fb.label("Paid").control(paid);
```

!demo(to.etc.domuidemo.pages.components.display.DisplayBooleanPage.ui, 100%, 620)

[TOC]

## The API

| Method | What it does |
| --- | --- |
| `new DisplayCheckbox()` / `new DisplayCheckbox(Boolean)` | empty, or with a value |
| `setValue(Boolean)` / `getValue()` | the value |
| `setChecked(boolean)` / `isChecked()` | the same, said the way a checkbox says it |

It has **two** pictures, not three: `null` and `false` both show the unticked
one. A screen that has to tell "no" apart from "not known" needs something else -
a [`DisplaySpan<Boolean>`](../displayspan/index.md) with an empty string, for
instance, which shows the metadata labels Yes and No and can show a third text
for `null`.

## What it renders

```html
<img class="ui-dspcb" src="THEME/dspcb-on.png">
```

The component *is* an `Img`, and setting the value swaps the `src` between the
theme's `dspcb-on.png` and `dspcb-off.png`. Because it is an image, it cannot be
focused, tabbed to or pressed - which is the whole difference with a disabled
`Checkbox`, something a user may still read as "not allowed *yet*".
