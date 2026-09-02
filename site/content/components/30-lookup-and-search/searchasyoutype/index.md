---
menu:
  sort: "30"
---
# SearchAsYouType

`SearchAsYouType<T>` is an input box whose value is one of a list: the user
*types* the value rather than picking it, and the control shows whether what has
been typed is a value yet.

```java
List<Genre> genres = getSharedContext().query(QCriteria.create(Genre.class));

SearchAsYouType<Genre> genre = new SearchAsYouType<>(Genre.class, "name");
genre.setData(genres);
genre.setMandatory(true);

FormBuilder fb = new FormBuilder(cp);
fb.label("Genre").control(genre);
```

!demo(to.etc.domuidemo.pages.components.lookup.SearchAsYouTypePage.ui, 100%, 660)

[TOC]

## Why type instead of pick

It is a `ComboLookup2` for people who would rather use the keyboard: same
contract - an `IControl<T>` over a `List<T>` - different interaction. It pays
off when the list is long enough to be annoying in a drop-down but short enough
to keep in memory, and when the users know what they are looking for.

The marker at the end of the box is the point of the control: it says whether
what is typed **is** a value. Typing `roc` shows the matches but leaves the
control empty; the moment the text is `rock` the control holds Rock, and says so.

## The value must be typeable

Everything else follows from one requirement: the user has to be able to type
the value, so a `T` must have an obvious, unique text. The control gets that
text in one of three ways:

| The values are | Give it |
| --- | --- |
| strings, numbers, enums | nothing - their own text is used |
| records with a text property | `new SearchAsYouType<>(Genre.class, "name")`, or `setSearchProperty("name")` |
| anything else | `setConverter((locale, value) -> ...)` |

The property must be a `String`, an `Enum` or a `Number`; anything else needs
the converter. The same text is used to display a value and to search it, which
is what keeps the control honest: nothing can be found by typing something the
user cannot see.

`setRenderer(...)` changes the drop-down *only*, so a row can show more than the
text that is matched against.

## How the text is matched

| `setMode(...)` | Matches |
| --- | --- |
| `MatchMode.CONTAINS_CI` | the text appears anywhere in the value, ignoring case - **the default** |
| `MatchMode.CONTAINS` | the same, case-sensitive |
| `MatchMode.STARTS_CI` | the value starts with the text, ignoring case |
| `MatchMode.STARTS` | the same, case-sensitive |

`setComparator(ICompare<T>)` replaces the matching altogether when none of those
is what a user would expect.

## The rest of the control

| Method | What it does |
| --- | --- |
| `setData(List<T>)` | the values that may be found |
| `setValue(T)` / `getValue()` | the value; `null` while what is typed is not one |
| `setMandatory(boolean)` | `getValue()` on an empty control reports *Mandatory field* and throws |
| `setOnValueChanged(...)` | called when the value becomes something, or nothing |
| `setOnEnter(FunctionEx<String,T>)` | make a value out of what was typed when it matches nothing - for a control that may also *create* |
| `setReadOnly(boolean)` / `setDisabled(boolean)` | the usual states |

`setData()`, `setConverter()`, `setMode()`, `setComparator()` and
`setSearchProperty()` all return the control, so they chain.

## It searches a list, not a table

The data is a `List<T>` the control holds: the filtering happens on the server,
over that list, not in the database. For finding a record in a table that is too
big to hold, the control is [`LookupInput2`](../lookupinput2/index.md).

It is also what [`EnumSetInput`](../../20-choice-input/enumsetinput/index.md) is
built out of - that control is a `SearchAsYouType` plus the labels of everything
picked so far.
