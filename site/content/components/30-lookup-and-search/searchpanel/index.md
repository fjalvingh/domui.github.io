---
menu:
  sort: "40"
---
# SearchPanel

`SearchPanel<T>` is a search *screen*: a form of search fields, a button bar,
and one method that turns what the user filled in into a `QCriteria<T>`.

```java
SearchPanel<Invoice> sp = new SearchPanel<>(Invoice.class);
cp.add(sp);
sp.setClicked(a -> search(sp.getCriteria()));
```

!demo(to.etc.domuidemo.pages.components.lookup.SearchPanelPage.ui, 100%, 720)

That is a complete search screen: the fields, their labels and their controls
all come from the metadata of `Invoice`.

[TOC]

## What it is, and what it is not

It is **not** an `IControl`: it has no value. What it has is `getCriteria()`,
and what that returns is the question the user asked:

| `getCriteria()` returns | Meaning |
| --- | --- |
| a `QCriteria` with restrictions | search for this |
| a `QCriteria` with none | the user filled in nothing - show everything |
| `null` | at least one field holds something invalid; the errors are already on screen |

So a search handler starts by checking for `null` and doing nothing:

```java
private void search(QCriteria<Invoice> criteria) {
    if(null == criteria)
        return;                                   // Bad input: the panel said so already
    m_table.setModel(new SimpleSearchModel<>(this, criteria));
}
```

`hasUserDefinedCriteria()` tells the two non-null cases apart, for a screen that
refuses to list a whole table.

## Where the fields come from

Three ways, and they can be combined:

```java
new SearchPanel<>(Invoice.class);                                   // 1. metadata
new SearchPanel<>(Invoice.class, "customer", "billingCity");        // 2. these properties
sp.add().property(Invoice_.customer()).control();                   // 3. the builder
```

1. **Metadata.** With no fields added at all, the panel uses the
   `searchProperties` of the class's `@MetaObject` (or, failing that, properties
   marked `@MetaSearch`). This is the whole screen in the example above.
2. **A property list** in the constructor: the same controls, but the properties
   and their order are yours.
3. **The builder**, one `add()` per field, which is what the rest of this page
   is about.

!! Adding one field of your own means metadata is **not** consulted at all.
!! `addDefault()` puts the metadata fields back - after whatever was added
!! before it, skipping any property that is already on the form.

## The builder

!demo(to.etc.domuidemo.pages.components.lookup.SearchPanelItemsPage.ui, 100%, 760)

```java
sp.add().property(Invoice_.customer())
    .label("Invoiced to")
    .hint("The customer the invoice was made out to")
    .defaultValue(defaultCustomer)
    .control();
```

Each `add()` ends in a `control()` call - that is what finishes the line, and
forgetting it makes the next `add()` throw.

| Builder call | What it does |
| --- | --- |
| `property(QField)` / `property(String)` | which property this line searches; everything else defaults from it |
| `label(String)` / `label(Label)` | the label, instead of the property's own |
| `hint(String)` | tooltip on the label |
| `defaultValue(D)` | the value the line starts with, and returns to on **Reset** |
| `initialValue(D)` | a value for the first search only; Reset goes to `defaultValue` |
| `minLength(int)` | refuse a text search shorter than this |
| `ignoreCase(boolean)` | case-insensitive text search (the default) |
| `testID(String)` | a stable id for tests |
| `control()` | finish: build the control from the property |
| `control(IControl<D>)` | finish with a control of your own |
| `control(IControl<D>, ILookupQueryBuilder<T,D>)` | ...and a way to search with its value |
| `action(IExecute)` | run something while the form is being built, instead of adding a field |

A property may be a **path**: `property("customer.city")` searches invoices by a
property of their customer.

### A search value is not a property value

The default of a number field is not a number, and the default of a date field
is not a date:

```java
sp.add().property(Invoice_.total())
    .defaultValue(new NumberLookupValue(QOperation.GE, BigDecimal.valueOf(5.0)))
    .control();

sp.add().property(Invoice_.invoiceDate())
    .defaultValue(new DatePeriod(null, DateUtil.dateFor(2010, 0, 1)))
    .control();
```

The value of a search control is what the user may *express*: `>= 5` for the
total, "up to 1 January 2010" for the date. Hand `defaultValue()` the wrong type
and the line fails when it is built.

| Property type | Control | Its value type |
| --- | --- | --- |
| `String` | `Text2<String>` | `String` |
| number | `NumberLookupControl` | `NumberLookupValue` - from, to, and the operation of each |
| `Date` | `DateLookupControl` | `DatePeriod` - a from and a to |
| enum, boolean | `ComboFixed2` | the value itself |
| relation | [`LookupInput2`](../lookupinput2/index.md) | the record |
| relation, hinted `comboLookup` | [`ComboLookup2`](../../20-choice-input/combolookup2/index.md) | the record |

What a user may type in the two special ones is worth repeating on screen:
`> 1000`, `<= 50`, `10%` or a plain amount in a number field; a from date, a to
date, or both.

## Controls of your own

!demo(to.etc.domuidemo.pages.components.lookup.SearchPanelControlPage.ui, 100%, 780)

A search line is a **control** plus a **query builder** - two separate things,
and that is what makes the panel extensible:

```java
//-- A control whose value is a Genre: the default builder handles that.
sp.add().property(Track_.genre()).control(new ComboLookup2<>(genres));

//-- A control whose value is a Set<Genre>: it brings its own builder.
sp.add().property(Track_.genre())
    .control(new EnumSetInput<>(Genre.class, genres, "name"),
             new EnumSetQueryBuilder<>("genre"));
```

Hand in only a control and the panel uses `ObjectLookupQueryBuilder`, which
compares the property with the value - and for a `String` value does an `ilike`
with a trailing `%`. Anything else needs a builder:

```java
public class EnumSetQueryBuilder<Q, V> implements ILookupQueryBuilder<Q, Set<V>> {
    private final String m_propertyName;

    @Override
    public LookupQueryBuilderResult appendCriteria(QCriteria<Q> criteria, @Nullable Set<V> value) {
        if(value == null || value.isEmpty())
            return LookupQueryBuilderResult.EMPTY;      // Nothing filled in: not an error
        QRestrictorImpl<Q> or = criteria.or();
        value.forEach(v -> or.eq(m_propertyName, v));
        return LookupQueryBuilderResult.VALID;
    }
}
```

The three results it may return are the whole contract: `EMPTY` (this line adds
nothing), `VALID` (it did), and `INVALID` (the input is wrong - which is what
makes `getCriteria()` return `null`). A `ValidationException` out of the
control's `getValue()` counts as `INVALID` too.

Because a search control is an ordinary `IControl`, everything that works on a
control works here: a change handler on one search field can fill in or clear
another.

## Which control a property gets

`LookupControlRegistry2` decides, by asking every registered factory to score
the property and taking the highest:

| Factory | Scores 10 for |
| --- | --- |
| `DateLookupFactory2` | a `Date` |
| `EnumAndBoolLookupFactory2` | an enum or a boolean |
| `NumberLookupFactory2` | any numeric type |
| `RelationLookupFactory2` | an upward relation |
| `RelationComboLookupFactory2` | an upward relation hinted `comboLookup` |
| `StringLookupFactory2` | - scores 1 for everything, so it is the fallback |

Registering one of your own is two lines in the application's `initialize()`:

```java
LookupControlRegistry2.INSTANCE.register(new MyLookupFactory(),
    pmm -> MyType.class.isAssignableFrom(pmm.getActualType()) ? 10 : 0);
```

## The form and the buttons

!demo(to.etc.domuidemo.pages.components.lookup.SearchPanelFormPage.ui, 100%, 780)

The panel does not lay the form out itself - an `ISearchFormBuilder` does, and
the default one puts every label/control pair on its own line using an ordinary
`FormBuilder`. It has one extra: `addBreak()` starts a new column, reached
through an `action()` in the middle of the field list:

```java
DefaultSearchFormBuilder builder = new DefaultSearchFormBuilder();
sp.setFormBuilder(builder);

sp.add().property(Invoice_.billingAddress()).control();
sp.add().action(() -> builder.addBreak());          // Everything after this: second column
sp.addDefault();
```

Actions run while the form is being built, in the order the lines were added.
For a different layout altogether, implement `ISearchFormBuilder` and either
hand it to one panel with `setFormBuilder()` or make it the default for the
application with `SearchPanel.setDefaultSearchFormBuilder(...)`.

The button bar:

| Button | When it is there |
| --- | --- |
| **Search** | always; also triggered by pressing return in a field |
| **Reset** | always; puts every field back to its `defaultValue` |
| **Hide** / **Show** | when `setShowHideButton(true)` - folds the form away, leaving the buttons |
| **Add** | when `setOnNew(...)` is set |
| **Cancel** | when `setOnCancel(...)` is set |
| anything else | `addButtonItem(node, order, mode)`, where the mode says whether it shows while the form is folded |

`setCollapsed(true)` folds the form from the code, and `setOnAfterCollapse()` /
`setOnAfterRestore()` report it.

## Running the query

The panel produces a `QCriteria`; showing the result is the page's own job, and
is described under [showing rows](../../../building-pages/70-showing-rows/index.md).
The short version is one model and one table:

```java
SimpleSearchModel<Invoice> model = new SimpleSearchModel<>(this, criteria);
DataTable<Invoice> table = new DataTable<>(model, new RowRenderer<>(Invoice.class));
cp.add(table);
cp.add(new DataPager(table));
```
