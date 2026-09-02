---
menu:
  sort: "30"
---
# ComboFixed2

`ComboFixed2<T>` is a drop-down over a list of values you state yourself, each
with the label to show for it.

```java
ComboFixed2<String> medium = new ComboFixed2<>(List.of(
    new ValueLabelPair<>("cd", "Compact disc"),
    new ValueLabelPair<>("lp", "Vinyl LP"),
    new ValueLabelPair<>("dl", "Download")
));

FormBuilder fb = new FormBuilder(cp);
fb.label("Medium").control(medium);
```

!demo(to.etc.domuidemo.pages.components.choice.ComboFixed2Page.ui, 100%, 700)

[TOC]

## Value and label

The list is a `List<ValueLabelPair<T>>`: the pair carries the value the control
hands back and the text the user reads. That is the whole difference with
[`ComboLookup2`](../combolookup2/index.md), which takes the values themselves and
works out their labels from metadata.

`ComboFixed2<T>` therefore has two types inside it - it extends
`ComboComponentBase2<ValueLabelPair<T>, T>` - but from the outside it is an
`IControl<T>`: `getValue()` hands back a `T`.

## Building one from an enum

```java
ComboFixed2<Medium> medium = ComboFixed2.createEnumCombo(Medium.class);
```

| Method | What you get |
| --- | --- |
| `createEnumCombo(Class, exceptions...)` | every constant except the exceptions, **sorted by label** |
| `createEnumCombo(Class, boolean sorted, exceptions...)` | the same, in declaration order when `sorted` is false |
| `createEnumCombo(List<T>)` / `createEnumCombo(T...)` | exactly these constants, in that order |
| `createCombo(T... items)` | any objects at all, labelled by their domain label or `toString()` |
| `createCombo(List<T>, QField<T,?> labelField)` | any objects, labelled by one of their properties |
| `createComboFor(PropertyMetaModel, editable)` | a combo for a property, from its domain values and metadata |

The enum labels come from the `.properties` file next to the enum
(`Vinyl.label=Vinyl LP`). A combo built from a *property* can do better: it uses
that property's own bundle first, so the same enum value can read differently in
two places.

## The empty choice

A combo that is not mandatory renders an extra, empty option at the top - that
is how it can hand back `null`. What that option says is up to you:

```java
combo.setEmptyText("- pick a medium -");
```

A **mandatory** combo renders the empty option only while it has no valid value
*at the moment it is built*: build it with a value and the user cannot
un-choose. Picking a value in the browser does not take the empty choice away -
the option list is only rewritten when the control is rebuilt. `getValue()` on
an empty mandatory combo reports *Mandatory field* and throws.

## The rest of the control

| Method | What it does |
| --- | --- |
| `setValue(T)` / `getValue()` | the value; it must be one of the list |
| `setData(List<ValueLabelPair<T>>)` | replace the whole list (this rebuilds the control) |
| `setMandatory(boolean)` | see above; it rebuilds, because the empty option changes |
| `setReadOnly(boolean)` | renders as the **label of its value**, no select element at all |
| `setDisabled(boolean)` / `setDisabledBecause(String)` | a greyed-out select |
| `setOnValueChanged(...)` | called when another option is picked |
| `immediate()` | post the change even without a handler |
| `addExtraButton(icon, title, click)` | a small button right of the combo |
| `setRenderer(IRenderInto<ValueLabelPair<T>>)` | draw the options yourself instead of showing the label |

A read-only combo is worth calling out: it is not a disabled select but plain
text, so a read-only form reads as a form rather than as a wall of grey boxes.

## From a property

`fb.property(shipment, Shipment_.state()).control()` gives a `ComboFixed2` for a
boolean or an enum property with **more than five** domain values, and a
[`RadioGroup`](../radiogroup/index.md) for one with five or fewer. Asking for
`control(ComboFixed2.class)` overrides the count. A boolean property gets Yes/No
from DomUI's own bundle, and a **primitive** `boolean` one is made mandatory as
well - it has no third state to offer.
