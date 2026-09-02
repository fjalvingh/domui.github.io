---
menu:
  sort: "10"
---
# LookupInput2

`LookupInput2<T>` holds one record as its value. The user finds that record
either by typing a few letters into the control itself, or by pressing the
lookup button and searching in a dialog.

```java
LookupInput2<Customer> customer = new LookupInput2<>(Customer.class);
customer.setMandatory(true);

FormBuilder fb = new FormBuilder(cp);
fb.label("Customer").control(customer);
```

!demo(to.etc.domuidemo.pages.components.lookup.LookupInput2Page.ui, 100%, 820)

[TOC]

## The three things it can show

| State | What is on screen |
| --- | --- |
| **empty, with quick search** | an input box plus a lookup and a clear button |
| **empty, without quick search** | the text *(no selection)* plus those two buttons |
| **a value** | the record, rendered; the clear button becomes usable |

Which of the first two it is depends on whether the control *has* a quick
search - it needs to know which properties to search on. It gets those from the
`KEYWORD` (or `BOTH`) search properties of the class, or from
`addKeywordProperty()`; with neither, the button is the only way in.
`setAllowKeyWordSearch(false)` turns the box off even when metadata offers one.

A read-only control with a value shows just the value (`ui-lui-selected-ro`) and
drops both buttons; a disabled one keeps them, greyed.

## What the quick search does

Typing in the box searches after a short pause, and **what comes back decides
what happens**:

| Records found | What the control does |
| --- | --- |
| none | shows *no matches* under the box |
| exactly one | **selects it**, without asking |
| 2 to 100 | drops down the list to pick from |
| more than 100 | shows *n record(s)* instead of a list |

!! The single-match rule is the one to remember: a search precise enough to
!! match one record fills the control straight away, change handler and all.
!! `setDisableSelectOne(true)` switches that off for one control, and
!! `LookupInputBase2.setDisableSelectOneGlobal(true)` for a whole application.

The query itself is built by an `IStringQueryFactory`. The default one ors a
`like` over every keyword property, anchored at the start (`ilike 'abc%'` for a
string, `=` for a number), and skips any property whose minimum length the typed
text has not reached yet - which is what `addKeywordProperty("artist.name", 2)`
sets. It understands two prefixes of its own:

| Typed | Searches |
| --- | --- |
| `$$3` | the record whose **primary key** is 3 |
| `$$city=Oslo` | the record whose `city` property is exactly `Oslo` |
| `*` anywhere | as a wildcard - it becomes `%` |

Pressing the lookup button instead of picking from the list opens the dialog,
carrying whatever was typed into it as its first search.

## Saying what may be searched

| Method | What it does |
| --- | --- |
| `addKeywordProperty(name)` | a property the quick search covers - **replaces** the metadata list |
| `addKeywordProperty(name, minlen)` | the same, but only once that many characters are typed |
| `setAllowKeyWordSearch(boolean)` | switch the box off entirely |
| `setKeySearchHint(String)` | the tooltip of the box; the default names the properties being searched |
| `setStringQueryFactory(...)` | build the quick-search query yourself |

A keyword property may be a **path**: `addKeywordProperty("artist.name", 2)`
searches albums by the name of their artist.

## Limiting what can be found at all

!demo(to.etc.domuidemo.pages.components.lookup.LookupInput2QueryPage.ui, 100%, 640)

| Way | When to use it |
| --- | --- |
| `new LookupInput2<>(QCriteria<T>)` | a fixed limit for the life of the control: every search is anded with this |
| `setQueryManipulator(...)` | a limit that changes: it is asked on **every** search, and may return `null` to refuse one |
| `new LookupInput2<>(Class<T>, List<T>)` | no database at all - the control searches the list it was given |

The root criteria and the manipulator stack: the manipulator runs first, then
the root criteria is merged in.

## What it shows for a value

!demo(to.etc.domuidemo.pages.components.lookup.LookupInput2LookPage.ui, 100%, 620)

Three different things are rendered, and each has its own hook:

| What | How to change it |
| --- | --- |
| the **selected value** in the control | `new LookupInput2<>(clz, "lastName", "city")`, or `setValueRenderer(...)` for full control |
| the **drop-down** under the search box | `setKeywordSearchResultsDropDownRenderer(...)` |
| the **table** in the lookup dialog | `setFormRowRenderer(...)` |

Without any of them, all three come from the class's `@MetaObject` display
properties. The dialog is configurable too:

| Method | What it does |
| --- | --- |
| `setSearchProperties(QField...)` | which fields the dialog's own search form offers |
| `setDefaultTitle(String)` | the dialog's title |
| `setPopupSearchImmediately(true)` | search at once when the dialog opens, rather than waiting |
| `setPopupInitiallyCollapsed(true)` | open with the search form folded away |
| `setOnPopupOpen(INotify<Dialog>)` | get at the dialog itself as it opens |
| `setPopupOpener(IPopupOpener)` | replace the dialog wholesale |

!! The dialog fills most of the window. That is fine on a page, but a
!! `LookupInput2` inside a small frame - a documentation page embedding a demo,
!! for instance - has no room for it. The quick search works in any size.

## Value, states and changes

| Method | What it does |
| --- | --- |
| `setValue(T)` / `getValue()` | the record; `getValue()` on an empty mandatory control reports *Mandatory field* and throws |
| `setMandatory(boolean)` | see above |
| `setReadOnly(boolean)` / `setDisabled(boolean)` / `setDisabledBecause(String)` | the usual three states |
| `setOnValueChanged(...)` | called when a record is picked or cleared - including by the single-match rule |
| `getWorkValue()` | the value without the mandatory check |

Selecting a record moves the value into the model straight away
(`OldBindingHandler.controlToModel`), so a bound page sees the new value in the
same request that selected it - not on the next one.

## From a property

A relation property gets a `LookupInput2` from the form builder by default:

```java
fb.property(invoice, Invoice_.customer()).control();
```

The alternative for a small table is a
[`ComboLookup2`](../../20-choice-input/combolookup2/index.md), chosen by putting
`componentTypeHint = Constants.COMPONENT_COMBO` on the property.
