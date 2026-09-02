---
menu:
  sort: "20"
---
# TextArea

`TextArea` is the multi-line input: a review, a note, an address. Its value is
always a `String`, newlines and all.

```java
TextArea review = new TextArea(60, 6);       // columns, rows
review.setValue("The best album they made.\nSide two especially.");
review.setMandatory(true);

FormBuilder fb = new FormBuilder(cp);
fb.label("Review").control(review);
```

!demo(to.etc.domuidemo.pages.components.input.TextAreaPage.ui, 100%, 720)

[TOC]

## Size and value

| Method | What it does |
| --- | --- |
| `new TextArea(cols, rows)` | the size of the box; `new TextArea()` leaves it to the css |
| `setCols(int)` / `setRows(int)` | the same afterwards |
| `setValue(String)` | put text in the box |
| `getValue()` | the text; a box the user left empty arrives as `null` |
| `setReadOnly(boolean)` | shown but not editable (css class `ui-textarea-ro`) |
| `setDisabled(boolean)` / `setDisabledBecause(String)` | greyed out, with the reason as its tooltip |
| `setHint(String)` | the tooltip |

`TextArea` is a `NodeContainer` whose text *is* its value, so unlike `Text2` it
renders as a real `<textarea>` element rather than a div around one.

## The two length limits

```java
TextArea note = new TextArea(60, 3);
note.setMaxLength(4000);          // at most 4000 characters
note.setMaxByteLength(4000);      // ...and at most 4000 UTF-8 bytes
```

`setMaxLength()` counts characters. Because `<textarea>` has no `maxlength`
attribute that browsers enforce the way they do for an `<input>`, DomUI renders
it as `mxlength` (Chrome gets `maxlength` on a textarea wrong) and enforces it in
javascript - and again on the server, where
incoming text longer than the limit is truncated rather than trusted.

`setMaxByteLength()` is the second limit, and it exists for one reason: an
Oracle `varchar2` holds 4000 *bytes*, not 4000 characters, so a note full of
accented characters overflows a column that a character count says fits. When
both are set the character limit is applied first, and the byte limit then
removes characters until the text fits.

## Validation

`TextArea` checks less than a `Text2` does, because there is nothing to convert:

- `setMandatory(true)` makes an empty box an error (`Mandatory field`),
- `addValidator(...)` adds checks of your own on the string, in the same forms
  `Text2` takes.

`getValue()` reports a failure on the control and throws, `getValueSafe()`
returns `null` instead, and `hasError()` asks without throwing - the same
contract every control has.

## What comes back

The value that arrives from the browser is normalised before it is compared with
what the control held: `\r\n` becomes `\n`, and an empty box is `null` rather
than an empty string. That is what keeps a text area from reporting itself as
modified merely because a browser sent its line endings back differently.

## When a form builder makes one

`fb.property(...)` gives a `TextArea` instead of a `Text2` when the property's
component type hint says `textarea`:

```java
@MetaProperty(componentTypeHint = TextArea.HINT)
public String getReview() { … }
```

That is the only way metadata selects it, so a long `String` column gets a
one-line box until it is told otherwise. See
[metadata](../../../building-pages/80-metadata/index.md).
