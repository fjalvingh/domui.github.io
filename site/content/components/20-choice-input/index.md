# Choice input

These controls do not let the user type a value: they offer the values there
are, and the user picks one of them - or, in one case, several.

[TOC]

## The components

| Component | What it is for |
| --- | --- |
| [`Checkbox`](checkbox/index.md) | one box: yes or no. Its value is a `Boolean`. |
| [`RadioGroup<T>`](radiogroup/index.md) | one value out of a handful, with every choice on screen. |
| [`ComboFixed2<T>`](combofixed2/index.md) | a drop-down over a list of values you state yourself, each with its label. |
| [`ComboLookup2<T>`](combolookup2/index.md) | a drop-down over records, with the list coming from the database. |
| [`EnumSetInput<T>`](enumsetinput/index.md) | several values at once, each shown as a label that can be taken off again. |

## Which one to use

The question is how many values there are, and where they come from:

| How many | Where they come from | Control |
| --- | --- | --- |
| two, and the second one is "no" | - | `Checkbox` |
| up to about five | an enum, or a list in the code | `RadioGroup` |
| five to a few dozen | an enum, or a list in the code | `ComboFixed2` |
| five to a few dozen | a table | `ComboLookup2` |
| more than fits in a drop-down | a table | [`LookupInput2`](../30-lookup-and-search/lookupinput2/index.md) |
| more than one at a time | a list or a table | `EnumSetInput` |

The line between a radio group and a combo box is what the metadata layer draws
at **five values**: a property whose type has five or fewer domain values gets a
`RadioGroup`, more than that gets a `ComboFixed2`. Making the control yourself,
which is what the pages here do, means you decide.

## What they have in common

All five are `IControl`, so they answer the same questions every control does -
value, read only, disabled, mandatory - and they can be bound and handed to a
`FormBuilder`. Two things are worth knowing before the individual pages:

**The value is the thing itself.** A `ComboLookup2<Artist>` hands back an
`Artist`, not an id; a `RadioGroup<Medium>` hands back a `Medium`. Finding the
value back in the list is done with `MetaManager.areObjectsEqual`, which
compares two entities on their **primary key** - so a value read in one
persistence session is found in a list read in another.

**Mandatory is what "empty" means.** A combo that is not mandatory renders an
extra empty choice at the top, and that is how it can hand back `null`. A
mandatory one keeps that choice only until a real value is picked, and
`getValue()` on an empty one reports *Mandatory field* and throws - except on a
`Checkbox`, which is never empty.

## Where the labels come from

None of these controls invent their texts:

- an **enum** value is labelled from the `.properties` file next to the enum
  (`Vinyl.label=Vinyl LP`), or by the owning property's own bundle, falling back
  to the constant's name;
- an **entity** is labelled by its `@MetaCombo` display properties, falling back
  to `toString()`;
- a **`ValueLabelPair`** carries its own label, which is what makes it useful
  when there is no metadata to ask.

This is the metadata mechanism described under
[metadata](../../building-pages/80-metadata/index.md); the pages below only say
which of it each control uses.
