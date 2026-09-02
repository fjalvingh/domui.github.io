---
menu:
  sort: "20"
---
# RadioGroup

`RadioGroup<T>` is one value out of a handful, with all the choices on screen at
once. The group is the control; the buttons inside it are not.

```java
RadioGroup<Medium> medium = new RadioGroup<>();
medium.addButton("Compact disc", Medium.Cd);
medium.addButton("Vinyl LP", Medium.Vinyl);
medium.addButton("Download", Medium.Download);
medium.setValue(Medium.Cd);

FormBuilder fb = new FormBuilder(cp);
fb.label("Medium").control(medium);
```

!demo(to.etc.domuidemo.pages.components.choice.RadioGroupPage.ui, 100%, 760)

[TOC]

## The group is the control

`RadioGroup<T>` implements `IControl<T>`: it has the value, the mandatory state,
the disabled and read-only states, and it is the thing that gets bound. A
`RadioButton<T>` inside it carries the value that button stands for and nothing
else.

The group renders itself from the list of buttons it was given -
`createContent()` draws one `div.ui-rbb-item` per button with its label - so
buttons are added to the *group*, never to the page:

| Method | What it adds |
| --- | --- |
| `addButton(String text, T value)` | a button with the label you give it |
| `addButton(String text, T value, String title)` | the same, plus a tooltip on the label |
| `addButton(T value)` | a button labelled from metadata - the enum's label, or `toString()` |
| `removeButton(T value)` | takes one out; if it was selected the value becomes null |
| `clearButtons()` | empties the group |

Adding a second button with a value the group already has throws: the value is
what identifies a button.

!! A `RadioGroup` that is not added to the page cannot be bound. Add the group,
!! not its buttons.

## Building one from an enum

```java
RadioGroup<Medium> sorted = RadioGroup.createEnumRadioGroup(Medium.class);
RadioGroup<Medium> inOrder = RadioGroup.createEnumRadioGroupUnsorted(Medium.class, Medium.Cassette);
```

| Method | What you get |
| --- | --- |
| `createEnumRadioGroup(Class, exceptions...)` | every constant except the exceptions, **sorted by label** |
| `createEnumRadioGroupUnsorted(Class, exceptions...)` | the same in declaration order |
| `createEnumRadioGroup(List<T>)` / `createEnumRadioGroup(T...)` | exactly these values, in that order |
| `createGroupFor(PropertyMetaModel, editable, asButtons)` | a group for a property, configured from its metadata |

The labels come from the metadata of the enum: `Vinyl.label=Vinyl LP` in the
`.properties` file next to it, falling back to the constant's own name. A hint
in the same bundle becomes the tooltip of that choice.

## How it looks

```java
group.asButtons();          // a row of buttons rather than a column of circles
```

`asButtons()` adds the css class `ui-rbb-buttons` and returns the group, so it
chains onto a factory call. A group with no value carries `ui-rbb-empty`, which
is what lets a theme mark an untouched mandatory group.

For anything more than a text next to the circle, hand the group a renderer:

```java
group.setValueRenderer((node, item) -> {
    node.add(new Span("hi", item.getLabelText()));
    node.add(" (" + item.getValue() + ")");
});
```

The renderer is called with a `RadioButtonInstance<T>`, which carries the button,
its label text, its tooltip and its value. Setting one rebuilds the group.

## Value, states and changes

| Method | What it does |
| --- | --- |
| `setValue(T)` / `getValue()` | the value of the selected button, `null` when nothing is selected |
| `setMandatory(boolean)` | `getValue()` on an empty group reports *Mandatory field* and throws |
| `setReadOnly(boolean)` / `setDisabled(boolean)` | passed on to every button in the group |
| `setOnValueChanged(...)` | called when another button is picked |
| `immediate()` | post the change even without a handler |
| `getName()` | the html `name` the buttons share, generated per group |

`setValue()` with a value that no button carries selects nothing and leaves the
group empty rather than throwing.

## From a property

`fb.property(shipment, Shipment_.method()).control()` gives a `RadioGroup` by
itself when the property's type has **five or fewer** domain values, and a
[`ComboFixed2`](../combofixed2/index.md) when it has more. Asking for one
explicitly overrides that count:

```java
fb.property(shipment, Shipment_.state()).control(RadioGroup.class);
```
