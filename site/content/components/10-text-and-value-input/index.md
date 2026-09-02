# Text and value input

The controls in this group are the ones a user types a value into: a line of
text, a paragraph of it, a date, a colour. They are the simplest controls DomUI
has, and everything a control can do is visible on them - which is why the rest
of the component documentation compares back to this group.

[TOC]

## The components

| Component | What it is for |
| --- | --- |
| [`Text2<T>`](text2/index.md) | one line of text, converted to and from a `T`. The control almost every form is built out of. |
| [`TextArea`](textarea/index.md) | more than one line, always a `String`. |
| [`DateInput2`](dateinput2/index.md) | a date, or a date and a time, with a calendar to pick from. |
| [`ColorPicker`](colorpicker/index.md) | a colour picker that stands open on the page. |
| [`ColorPickerButton`](colorpickerbutton/index.md) | a swatch that opens the picker when pressed. |
| [`ColorPickerInput`](colorpickerinput/index.md) | the hex code in a text box, with a swatch beside it. |

## What they have in common

All of them are `IControl<T>`, so all of them answer the same five questions -
what is your value, are you read only, are you disabled, why, and are you
mandatory - and all of them can be bound and can be handed to a
`FormBuilder`:

```java
Text2<String> title = new Text2<>(String.class);
DateInput2 released = new DateInput2();

FormBuilder fb = new FormBuilder(cp);
fb.label("Album title").mandatory().control(title);
fb.label("Released").control(released);
```

`getValue()` is where a control checks its input before handing it over: it
reports what is wrong on the control itself and throws, so a click handler that
reads three fields stops at the first one that cannot deliver. That mechanism is
the same for every control and is described in
[using components](../../building-pages/20-using-components/index.md); the pages
below only say what *this* control checks.

The value type is a `Text2` speciality. `TextArea` is always a `String`,
`DateInput2` is always a `java.util.Date`, and the three colour controls are
always a `String` holding six hex digits without a `#`.

## Which one a form builder picks by itself

`fb.property(instance, property).control()` does not need to be told which
control to make: it asks the metadata. From this group it picks

- `Text2<T>` for a string, a number, or anything else with a converter,
- `TextArea` when the property's component type hint is `textarea`,
- `DateInput2` for a `Date`, with the time part switched on when the property's
  temporal presentation says `DATETIME`.

What decides that is described in
[metadata](../../building-pages/80-metadata/index.md). Making the control
yourself, as the examples here do, is what you do when metadata cannot know -
a value that is not a property of anything, or a screen that needs a control
configured differently from every other use of that property.
