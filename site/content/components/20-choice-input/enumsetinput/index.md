---
menu:
  sort: "50"
---
# EnumSetInput

`EnumSetInput<T>` is the control for choosing **several** values: what has been
chosen stands on screen as a row of labels, each with a cross to take it off,
and next to them a box that searches the rest as you type.

```java
List<Genre> genres = getSharedContext().query(QCriteria.create(Genre.class));

EnumSetInput<Genre> chosen = new EnumSetInput<>(Genre.class, genres, "name");
chosen.setValue(Set.of(genres.get(0)));

FormBuilder fb = new FormBuilder(cp);
fb.label("Genres to search in").control(chosen);
```

!demo(to.etc.domuidemo.pages.components.choice.EnumSetInputPage.ui, 100%, 640)

[TOC]

## The value is a Set

`EnumSetInput<T>` is an `IControl<Set<T>>`: the labels on screen *are* the set.
Adding a value that is already in it changes nothing, and a value already chosen
is dropped from the list the search box offers, so nothing can be picked twice.

The set the control hands back is its own - changing it does not change the
control. Give it a new set to change what is selected.

## Despite the name, not only enums

The name is historic; the control works on anything. What it needs is the class
of the values, the values themselves, and how to label one:

| Constructor | Use it for |
| --- | --- |
| `new EnumSetInput<>(Class<T>, List<T> data, String property)` | records: the label is that property of each value |
| `new EnumSetInput<>(Class<T>, List<T> data, null)` | enums and other values that label themselves through metadata |
| `new EnumSetInput<>(Class<T>, String property)` | the same, with the list handed over later by `setData()` |

With a property name the label is that property's value; without one the value
itself is looked up as a domain value - which is what gives an enum its label
from the `.properties` file next to it - falling back to `String.valueOf()`.

## The parts you can change

| Method | What it does |
| --- | --- |
| `setData(List<T>)` | the values that may be chosen (rebuilds the control) |
| `setValue(Set<T>)` / `getValue()` | what is chosen |
| `setConverter(Function<T,String>)` | the label of a value, worked out in code instead of from a property |
| `setRenderer(IRenderInto<T>)` | draw the whole label yourself - an icon, two lines, a colour |
| `setOnValueChanged(...)` | called on every add and every remove |
| `setReadOnly(boolean)` / `setDisabled(boolean)` | the labels lose their crosses; the search box stays but cannot be typed in |

The labels are kept sorted by their text, whichever order values were added in.

## What it is built out of

The search box is a [`SearchAsYouType`](../../30-lookup-and-search/searchasyoutype/index.md)
over the values not yet chosen. Every few keystrokes it sends what was typed to
the server, which filters the list it is holding and sends back the matches as a
small drop-down; picking one adds it to the set, clears the box and hands the box
the shortened list. The list is held in memory, so this is a control for a few
hundred values at most - for picking several *records* out of a table, the
searching controls are the ones to reach for.

The text it searches in is the same text the labels show, so a value found by
typing is a value the user can read back afterwards.

!! `setMatcher()` exists but does nothing: the matcher is stored and never
!! read. Leave it alone until it is either wired up or removed.
