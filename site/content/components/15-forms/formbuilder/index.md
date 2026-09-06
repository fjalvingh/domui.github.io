---
menu:
  sort: "10"
---
# Labels and controls

The plain form: controls made the ordinary way, each one handed to the builder
with the label that belongs in front of it.

```java
ContentPanel cp = new ContentPanel();
add(cp);

Text2<String> title = new Text2<>(String.class);
Text2<Integer> copies = new Text2<>(Integer.class);
Text2<BigDecimal> price = new Text2<>(BigDecimal.class);
DateInput2 released = new DateInput2();
Checkbox inPrint = new Checkbox();

FormBuilder fb = new FormBuilder(cp);
fb.label("Album title").mandatory().control(title);
fb.label("Copies in stock").control(copies);
fb.label("Price each").control(price);
fb.label("Released").control(released);
fb.label("Still in print").control(inPrint);
```

!demo(to.etc.domuidemo.pages.components.form.FormBasicsPage.ui, 100%, 500)

[TOC]

## The builder is handed a container

```java
FormBuilder fb = new FormBuilder(cp);
```

What goes in the constructor is the node the form is built **into** - the
`ContentPanel` of the page, a `Div`, a fragment. Not the page: a form built
straight into the `UrlPage` lands outside the content panel and loses the
padding the panel gives it.

The builder is a plain object with no place in the node tree, so it is made in
`createContent()`, used, and forgotten. More than one may be alive at a time;
each builds its own form into its own container.

## What the label can be

```java
Span own = new Span();
own.add("A label ");
own.add(new Span("dm-tut-hi", "of your own"));

fb.label("An ordinary label").control(plain);
fb.label("Mandatory").mandatory().control(marked);
fb.label(own).control(made);
fb.controlOnly().control(naked);
```

| Called as | What it does |
| --- | --- |
| `label(String)` | the ordinary case: a `<label>` with that text, pointing at the control. |
| `label(NodeContainer)` | a label you built yourself, put in the label's place as it is. |
| `label(IBundleCode, Object...)` | the text from a message bundle, formatted with the parameters. |
| `controlOnly()` | no label at all. |

`mandatory()` marks the label - it gets the `ui-f4-mandatory` class, which is
what puts the mark in front of it - and calls `setMandatory(true)` on the
control, so that `getValue()` starts refusing an empty value.

!! `controlOnly()` leaves the label **div** out too, not just its text. In a
!! vertical form the control then starts where the label would have been, out of
!! line with the rows above it. It is meant for a row that is not part of the
!! form's grid, not for a row with an empty label.

## Hints

A hint is the sentence that explains the field. It is the control's tooltip by
default:

```java
fb.label("Catalogue number").hint("The number on the spine of the box").control(code);
```

or an icon behind the label, which shows the text when it is clicked:

```java
fb.hintAsIcon(true);
fb.label("Catalogue number").hint("The number on the spine of the box").control(code);
```

`hintAsIcon()` is a property of the builder, not of the row: it decides how
every hint in *this* form is shown. `FormBuilder.setDefaultShowHintAsIcon(true)`
does the same for the whole application, and `hintRenderer()` replaces what the
icon is and does with a `BiConsumer<NodeContainer, String>` of your own.

A row with no `hint()` of its own still gets one when the property it is built
from has a default hint in its metadata.

## A row that is not a control

```java
Div note = new Div("dm-tut-q");
note.add("Anything can sit in the control position - this is a Div.");

fb.label("A remark").control(comment);
fb.label("Not a control").item(note);
```

`item()` takes any node, not just an `IControl`, and lays it out as a pair like
any other. Nothing is bound to it, nothing is read from it, and the things that
only a control understands - `mandatory()` and `readOnly()` - do nothing to it
beyond marking its label.

## What a row can be told

Between `label()` and `control()`:

| Method | What it does |
| --- | --- |
| `mandatory()`, `mandatory(boolean)` | mark the label and make the control require a value |
| `hint(String)`, `hint(IBundleCode)` | the explaining text, as tooltip or icon |
| `readOnly()`, `readOnly(boolean)` | the control shows its value but cannot be typed into |
| `readOnly(instance, property)` | bind `readOnly` to a boolean property - see [a form from properties](../from-a-property/index.md) |
| `cssLabel(String)`, `cssControl(String)` | a class on the label or the control part of this pair |
| `property(instance, property)` | continue as a property row, keeping everything set so far |

and the row ends in `control(control)` or `item(node)`.
