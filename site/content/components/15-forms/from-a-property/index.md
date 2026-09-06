---
menu:
  sort: "20"
---
# A form from properties

A row that names a **property** instead of a control does not need a control, a
label, or a value: the builder makes the control from the property's metadata,
labels it from the metadata, and binds it to the property.

```java
Track track = getSharedContext().get(Track.class, 1L);

FormBuilder fb = new FormBuilder(cp);
fb.property(track, Track_.name()).control();
fb.property(track, Track_.composer()).control();
fb.property(track, Track_.unitPrice()).control();
fb.property(track, Track_.genre()).control();
```

!demo(to.etc.domuidemo.pages.components.form.FormPropertyPage.ui, 100%, 560)

[TOC]

## What the four lines did

`control()` with no argument is what asks for a control to be made. For each
row, the builder

- reads the property's metadata - `Track.name` is a mandatory `String` of 200
  characters whose label is "Title", `Track.unitPrice` is money, `Track.genre`
  is a relation to another entity,
- asks the `ControlCreatorRegistry` for the control that fits it, which is a
  `Text2<String>` for the first, a `Text2<BigDecimal>` with a money converter
  for the third and a `LookupInput2<Genre>` for the last,
- labels it with the property's label and marks it mandatory when the property
  is,
- and binds the control's value to that property of that instance.

Which control comes out of which property is decided by the registry and is
described with the controls themselves - see
[text and value input](../../10-text-and-value-input/index.md) and
[metadata](../../../building-pages/80-metadata/index.md). The binding is the
ordinary [data binding](../../../building-pages/50-data-binding/index.md):
typing in the box changes the `Track` instance, and changing the instance
changes the box.

## Naming the property

```java
fb.property(track, Track_.name()).control();          // the generated QField
fb.property(track, "name").control();                 // by name
```

The `QField` form is the one to use: `Track_` is generated from the entity, so a
renamed property is a compile error rather than a runtime one, and the chain
knows the property's type - which is what lets `control(control)` check that the
control fits the property. See
[typed properties](../../../building-pages/40-typed-properties/index.md).

Naming the property as a `String` gives a chain that does not know the type: it
takes any `IControl`, and it is the chain that has `converter()` on it, because
the converter cannot be checked against the property's type either way.

In Kotlin a property reference does the same as the `QField`:

```kotlin
fb.property(track, Track::name).control()
```

## Overriding what the metadata says

```java
fb.property(track, Track_.composer()).label("A label of my own").control();
fb.property(track, Track_.unitPrice()).mandatory().hint("What the shop charges").control();
fb.property(track, Track_.genre()).control(ComboLookup2.class);
fb.property(track, Track_.name()).label("A control of my own").control(ownControl);
```

Every step of the chain overrules the metadata for that one row.

| Ending the row with | What you get |
| --- | --- |
| `control()` | the control the registry picks for the property |
| `control(Class)` | the control the registry picks *of that class* - `genre` is a relation, which becomes a `LookupInput2` by default and a `ComboLookup2` when asked for one |
| `control(control)` | a control you made yourself, bound and laid out the same way |
| `control(control, converter)` | the same, with an `IBidiBindingConverter` between the control's type and the property's |

!! `control(Class)` only works where a control creator can deliver that class for
!! that property. Asking for a class no creator makes for the property - a
!! `TextArea` for a property with no textarea hint, say - ends in *No control
!! factory found*.

## readOnly and disabled

Both can be set outright, bound to a property, or set for a run of rows:

```java
FormBuilder fb = new FormBuilder(cp);
fb.readOnlyAll(this, "locked");                       // from here on: bound to page.locked
fb.property(track, Track_.name()).control();
fb.property(track, Track_.composer()).control();
fb.readOnlyAllClear();                                // and no longer
fb.property(track, Track_.unitPrice()).control();
```

| On the builder | On one row |
| --- | --- |
| `readOnlyAll(instance, property)` / `readOnlyAllClear()` | `readOnly()`, `readOnly(boolean)`, `readOnly(instance, property)` |
| `disabledAll(instance, property)` / `disabledAllClear()` | `disabled()`, `disabled(boolean)`, `disabled(instance, property)` |
| `disabledBecauseAll(instance, property)` / `disabledBecauseClear()` | `disabledBecause(String)`, `disabledBecause(instance, property)` |

The row wins over the builder: a `readOnly()` on the row is used even when
`readOnlyAll()` is in force. The bound forms are ordinary bindings, so the
control follows the property as it changes - tick the box on the demo page above
and the two controls under it become read only while the third does not.

`disabledBecause()` disables the control *and* says why, which the control shows
as its tooltip. It is set on the control's own `disabledBecause` property; a
control that has no such property is simply disabled.

## The rest of the chain

| Method | What it does |
| --- | --- |
| `mandatory()`, `mandatory(boolean)` | override the metadata's idea of whether a value is required |
| `hint(String)`, `hint(IBundleCode)` | the explaining text, over the property's default hint |
| `errorLocation(String)` | where errors on this control are reported; the label text by default |
| `testId(String)` | the test id for [Selenium tests](../../../testing/index.md); the property's name by default |
| `cssLabel(String)`, `cssControl(String)` | a class on the label or the control part of this pair |
