---
menu:
  sort: "40"
---
# ComboLookup2

`ComboLookup2<T>` is a drop-down over records: its value is an entity, and its
list comes from a query or from a list you already have.

```java
QCriteria<Artist> q = QCriteria.create(Artist.class).ascending(Artist_.name()).limit(20);
ComboLookup2<Artist> artist = new ComboLookup2<>(q);

FormBuilder fb = new FormBuilder(cp);
fb.label("Artist").control(artist);
```

!demo(to.etc.domuidemo.pages.components.choice.ComboLookup2Page.ui, 100%, 720)

[TOC]

## Where the list comes from

| Constructor | The list is |
| --- | --- |
| `new ComboLookup2<>(QCriteria<T>)` | the result of that query, run when the combo is built |
| `new ComboLookup2<>(List<T>)` | a list you have already |
| `new ComboLookup2<>(IListMaker<T>)` | a cached list, shared between pages and requests |
| `new ComboLookup2<>(Class<? extends IComboDataSet<T>>)` | whatever that data set class produces |
| `setData(List<T>)` / `setQuery(QCriteria<T>)` | the same afterwards; both rebuild the control |

A query is only run when the control is built, so its size is your
responsibility: everything in the list is rendered as an `<option>`, and the
user scrolls through all of it. A few dozen rows is a combo box; more than that
is a [`LookupInput2`](../../30-lookup-and-search/lookupinput2/index.md), which
searches instead of listing.

`ComboLookup2` also implements `IComboBox<T>`, whose `data()`, `query()` and
`renderer()` return the control, so the three can be chained.

## What each option says

In order:

1. a **renderer** set on the control, if there is one;
2. the **properties** named in the constructor;
3. the **metadata** of the value's class - `@MetaCombo`'s display properties;
4. `toString()`.

```java
//-- Name the properties to show
ComboLookup2<Artist> byProperty = new ComboLookup2<>(artists, Artist_.name());

//-- Or render each option yourself
ComboLookup2<Artist> rendered = new ComboLookup2<>(artists);
rendered.setRenderer((node, artist) -> {
    node.add(new Span("hi", artist.getName()));
    node.add(" (#" + artist.getId() + ")");
});
```

An entity with a `@MetaCombo` needs neither: `new ComboLookup2<>(genres)`
renders the genre's name because `Genre` says so. An entity with *no* combo
metadata falls back to `toString()`, which is how a combo ends up showing
`to.etc.domui.derbydata.db.MediaType#1 @1491...` - the fix for that is
`@MetaCombo` on the class, not a renderer on every screen.

## The value is the record

`getValue()` hands back the entity, not its id. Finding the current value back
in the list is done with `MetaManager.areObjectsEqual`, which compares entities
on their **primary key** - so a value that was read in another persistence
session is still found and selected. Two different objects with the same id
count as the same value, which also means `setValue()` with a stale copy of a
record changes nothing on screen.

## The rest of the control

| Method | What it does |
| --- | --- |
| `setValue(T)` / `getValue()` | the record; it must be in the list |
| `setMandatory(boolean)` | without it the combo carries an empty choice and can hand back `null` |
| `setEmptyText(String)` | what that empty choice says |
| `setReadOnly(boolean)` | renders as the rendered label of its value, without a select |
| `setDisabled(boolean)` / `setDisabledBecause(String)` | a greyed-out select |
| `setOnValueChanged(...)` / `immediate()` | report the change |
| `addExtraButton(icon, title, click)` | a small button right of the combo |

## From a property

A property that points at another entity - a many-to-one relation - gets a
[`LookupInput2`](../../30-lookup-and-search/lookupinput2/index.md) by default: with
nothing said either way the lookup outscores the combo, because a table can be
of any size. Say which one you want with the property's **component type hint**:

```java
@MetaProperty(componentTypeHint = Constants.COMPONENT_COMBO)     // "comboLookup"
public Genre getGenre() { … }
```

The same hint on the *class* makes every relation pointing at it a combo. Either
way the control is built by `createLookup(PropertyMetaModel)`, which reads the
combo data set, the query manipulator and the sort order from the metadata, so
`fb.property(track, Track_.genre()).control()` is then all a screen needs.
Handing `control(ComboLookup2.class)` in does the same for one screen.
