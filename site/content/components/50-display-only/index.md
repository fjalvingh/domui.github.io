# Display-only components

These show a value and nothing else: no input, no focus, no change event. They
exist because a screen that may not be edited should not look like a screen that
may be - a row of greyed-out input boxes reads as "you are not allowed to",
where plain text reads as "this is what it is".

[TOC]

## The components

| Component | Shows |
| --- | --- |
| [`DisplaySpan<T>`](displayspan/index.md) | any value, converted or rendered, as a span |
| [`DisplayControl<T>`](displaycontrol/index.md) | the same as a div, so it lines up in a form |
| [`DisplayCheckbox`](displaycheckbox/index.md) | a `Boolean` as a tick box picture |
| [`DisplayRadiobutton`](displayradiobutton/index.md) | a `Boolean` as a radio button icon |
| [`DisplayHtml`](displayhtml/index.md) | html, with the parts it does not allow taken out |
| [`PercentageCompleteRuler2`](percentagecompleteruler2/index.md) | how far something got, as a bar |
| [`EmbeddedCode`](embeddedcode/index.md) | a piece of code, as code |

## What a display control is

All of them except the last two implement `IDisplayControl<T>`, which is nothing
but `IControl<T>` with a marker on it. That means they fit everywhere a control
fits - a form builder takes them, a table cell holds them - while behaving as
you would expect of something that cannot be edited:

| Asked | A display control answers |
| --- | --- |
| `getValue()` | exactly what `setValue()` was given |
| `getValueSafe()` | the same - it cannot fail |
| `isReadOnly()` | `true`, always; `setReadOnly()` does nothing |
| `isDisabled()`, `isMandatory()` | `false`; their setters do nothing |
| `getOnValueChanged()` | `null` - the value only changes when the code changes it |

There is nothing to validate, so nothing can report an error, and nothing
arrives from the browser: a display control renders and that is all.

## Read-only control, or display control?

Most input controls have a read-only state of their own, and several of them
already render as plain text when they are in it - a
[`ComboFixed2`](../20-choice-input/combofixed2/index.md) shows the label of its
value, a [`LookupInput2`](../30-lookup-and-search/lookupinput2/index.md) shows
the record. Prefer that when a screen switches between editing and viewing: one
control, one binding, one line of code deciding.

Reach for a display component when the value is *never* editable on this screen:
a total that is computed, a state the user cannot change, a review written by
somebody else. The result reads better, and nothing about the control suggests
otherwise.
