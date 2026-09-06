# Forms

A form is not a component in DomUI. There is no `Form` class to add to a page and
no form node to put controls in: a form is what the **`FormBuilder`** leaves
behind after it has been handed a panel and a series of controls.

```java
ContentPanel cp = new ContentPanel();
add(cp);

Text2<String> title = new Text2<>(String.class);
Text2<Integer> copies = new Text2<>(Integer.class);
DateInput2 released = new DateInput2();

FormBuilder fb = new FormBuilder(cp);
fb.label("Album title").mandatory().control(title);
fb.label("Copies in stock").control(copies);
fb.label("Released").control(released);
```

!demo(to.etc.domuidemo.pages.components.form.FormBasicsPage.ui, 100%, 500)

[TOC]

## The three things it does

The builder takes the controls of the [component groups](../index.md) around it
and

- puts a **label** in front of each one and lines the pairs up,
- creates the control **for** you when you name a property instead of a control,
  and binds it to that property,
- carries the things a whole form shares - read only, disabled, the width of the
  labels - so that they are not repeated on every row.

| Page | What it covers |
| --- | --- |
| [Labels and controls](formbuilder/index.md) | the pair the form is made of: `label()`, `control()`, `mandatory()`, hints, and rows that are not controls at all. |
| [A form from properties](from-a-property/index.md) | `property()`: the control made from metadata and bound to the property, and the `readOnly`/`disabled` bindings around it. |
| [Laying the form out](form-layout/index.md) | vertical and horizontal, where a form ends, more than one control in a pair, and the css of a row. |

## The shape of the call

Every row is one chain, and the chain always ends in `control()` or `item()`:

```java
fb.label("Album title").mandatory().hint("As it is on the sleeve").control(title);
fb.property(album, Album_.title()).readOnly().control();
```

Between the two ends sit the things this row is to be told - the label, whether
it is mandatory, whether it is read only, what css it carries. The builder holds
that row while it is being described, so the chain must be finished before the
next one starts; a `label()` that is never followed by a `control()` makes the
next row fail with *You need to end the builder pattern with a call to
'control()'*.

`control()` with no argument only exists on a `property()` chain, where the
metadata says what to make. Everywhere else the control is made first and handed
over.

## What ends up on the page

The builder does not put the controls into the panel directly. It builds a `div`
per form, a `div` per pair, and a `div` for the label and the control of that
pair:

```html
<div class="ui-f5 ui-f5-v">
    <div class="ui-f5-pair ui-f5-pair-v">
        <div class="ui-f5-lbl ui-f5-lbl-v"><label for="...">Album title</label></div>
        <div class="ui-f5-ctl ui-f5-ctl-v">...the control...</div>
    </div>
    ...
</div>
```

Those divs are flexbox: the pair is a row in a vertical form and an inline block
in a horizontal one, and the label div has a minimum width, which is what makes
the controls line up under each other. Nothing about it is a table.

!i The class names say `ui-f5` while the package says `form4`. The builder is
!i `component2.form4.FormBuilder`; `ui-f5` is the fifth generation of the css it
!i emits. The two numbers are not related to each other.
