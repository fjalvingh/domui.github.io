---
menu:
  sort: "30"
---
# Laying the form out

A form is vertical unless it is told otherwise: the label sits in front of the
control and every pair is a line of its own. `horizontal()` turns the pairs
sideways - the label above the control, the pairs running across the page.

```java
FormBuilder fb = new FormBuilder(cp);
fb.label("Street").control(street);
fb.label("Town").control(town);

FormBuilder fb2 = new FormBuilder(cp);
fb2.horizontal();
fb2.label("Day").control(day);
fb2.label("Month").control(month);
fb2.label("Year").control(year);
```

!demo(to.etc.domuidemo.pages.components.form.FormLayoutPage.ui, 100%, 560)

[TOC]

## Where one form ends

One builder normally builds one form: every pair goes into the same `ui-f5`
div, however much else is added to the panel in between. `nl()` ends that div,
so what is added next lands *between* the two forms and the pair after it starts
a new one:

```java
FormBuilder fb = new FormBuilder(cp);
fb.label("Before the break").control(first);
fb.nl();
cp.add(new Para().add("This paragraph is not part of either form."));
fb.label("After the break").control(second);
```

Changing the direction does the same by itself: the pair after a
`horizontal()` or `vertical()` starts a new form div, because a form div is
either horizontal or vertical and cannot be both.

## More than one thing in a pair

```java
fb.label("Price").control(amount);
fb.append().label("in").control(currency);      // a second control in the same pair

fb.label("Catalogue code").control(code);
fb.appendAfterControl(help);                    // a node behind the control
```

`append()` puts the next row inside the previous pair's control div instead of
on a line of its own - label and all, which is how two controls come to share
one label. `appendAfterControl()` adds a node there without a row around it,
which is what a button belonging to the control before it wants.

Both work on the pair the builder made last, so they only make sense directly
after one.

## How wide the labels are

The label divs of a vertical form share a minimum width - 150px - which is what
lines the controls up under each other. A form whose labels are longer than that
is put inside a div that says so:

```java
Div wide = new Div("ui-label-wide");            // 230px
cp.add(wide);

FormBuilder fb = new FormBuilder(wide);
fb.label("Inside a ui-label-wide div").control(control);
```

`ui-label-wide` and `ui-label-extrawide` (300px) work from anywhere above the
form, so a page can be put in one and every form on it follows. The widths
themselves are the `$form-label-width` and `$form-label-width-wide` variables of
the [theme](../../../look-and-feel/index.md).

## The css of one row

```java
fb.label("A highlighted row").cssLabel("dm-tut-hi").cssControl("dm-tut-hi").control(marked);
```

`cssLabel()` and `cssControl()` add a class to the label div and the control div
of that one pair - for the row that has to look different from the rest of the
form. The form's own divs cannot be reached that way; style `.ui-f5` inside a
class of your own instead.

## What builds the divs

The builder decides *what* a row holds; an `IFormLayouter` decides what html it
becomes. The one it uses is `ResponsiveFormLayouter`: flexbox, one div per form,
one per pair, one for the label and one for the control.

```java
FormBuilder fb = new FormBuilder(new MyOwnLayouter(cp));
```

A layouter of your own, handed to the constructor, is the way to change that
html - what it is handed for each row is the control, the label, the hint and
the css that row was given. Everything else - the chain, the
bindings, the direction, `append()` - is the builder's and does not change with
it.
