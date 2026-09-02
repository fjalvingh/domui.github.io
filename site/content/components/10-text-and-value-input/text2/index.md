---
menu:
  sort: "10"
---
# Text2

`Text2<T>` is one line of input, converted to and from a `T`. It is the control
most of a DomUI application is built out of: a string, a number, an amount of
money and a date all arrive through it.

```java
Text2<String> title = new Text2<>(String.class);
Text2<Integer> copies = new Text2<>(Integer.class);
Text2<BigDecimal> price = new Text2<>(BigDecimal.class);

FormBuilder fb = new FormBuilder(cp);
fb.label("Album title").control(title);
fb.label("Copies in stock").control(copies);
fb.label("Price").control(price);
```

!demo(to.etc.domuidemo.pages.components.input.Text2Page.ui, 100%, 620)

[TOC]

## The type is the point

The class handed to the constructor is what the control converts to, and what
`getValue()` hands back:

```java
Text2<Integer> copies = new Text2<>(Integer.class);
copies.setValue(12);
Integer number = copies.getValue();      // an Integer, not a String
```

`new Text2<>()` with no argument is `Text2<String>`.

The type decides three things at once:

| The type | What it changes |
| --- | --- |
| The converter | which `IConverter` turns the typed text into a `T` and back - found in the `ConverterRegistry` for that class |
| The keyboard filter | an integer type only accepts digits, a real type also accepts a decimal separator; anything else accepts everything |
| The error message | an unconvertible value reports what is wrong with *that* type: "Unexpected character (a) in number abc" |

The keyboard filter is the `NumberMode`, set from the constructor's type and
overridable with `setNumberMode()`. It only stops keys in the browser; nothing
depends on it, and the conversion happens on the server regardless.

## What getValue() checks

```java
Text2<String> email = new Text2<>(String.class);
email.setMandatory(true);
email.addValidator(new EmailValidator());
```

!demo(to.etc.domuidemo.pages.components.input.Text2ValidatePage.ui, 100%, 760)

`getValue()` runs the whole chain, in this order, and stops at the first thing
that fails:

1. **mandatory** - an empty box on a mandatory control is `Mandatory field`.
   An empty box on a control that is not mandatory is simply `null`, and nothing
   else is checked.
2. **the regular expression**, when one is set - it is applied to the raw text,
   before any conversion.
3. **the converter** - the one set with `setConverter()`, otherwise the one the
   registry has for the type.
4. **the validators**, in the order they were added, each getting the *converted*
   value.

A failure is reported on the control (the box goes red, the message becomes its
tooltip and appears in the page's error display) and thrown as a
`ValidationException`, which the framework catches - so a handler reading three
fields simply stops at the first one that cannot deliver. `hasError()` asks the
same question without the exception, and `getValueSafe()` returns `null` instead
of throwing.

The result of one validation is remembered until the raw text changes, so
calling `getValue()` five times costs one check.

| Method | What it adds |
| --- | --- |
| `setMandatory(boolean)` | the box may not be left empty |
| `setValidationRegexp(String)` | a pattern the raw text must match |
| `setRegexpUserString(String)` | what to say when it does not: *Input format must be `9999 AA`* instead of a generic message |
| `addValidator(IValueValidator<?>)` | any check of your own, on the converted value |
| `addValidator(Class<? extends IValueValidator<T>>)` | the same, made by the `ValidatorRegistry` |
| `setConverter(IConverter<T>)` | convert text to `T` differently from the default - a money format, for instance |

## The three states

```java
control.setReadOnly(true);                       // shows the value, cannot be changed
control.setDisabled(true);                       // greyed out
control.setDisabledBecause("Already shipped");   // greyed out, and says why on hover
```

`setDisabledBecause()` is `setDisabled()` plus a tooltip, and passing `null`
enables the control again. A read-only `Text2` keeps its box but refuses input;
a disabled one is grey and sends nothing back.

## How the box looks

!demo(to.etc.domuidemo.pages.components.input.Text2LookPage.ui, 100%, 700)

| Method | Effect |
| --- | --- |
| `setSize(int)` | the width of the box, in characters |
| `setMaxLength(int)` | the longest text that may be typed |
| `setPlaceHolder(String)` | the browser's own placeholder text |
| `setMarkerText(String)` | a marker *image* DomUI renders behind an empty box, from `MarkerImagePart` |
| `setMarker()` / `setMarker(icon)` / `setMarker(icon, caption)` | the same with the search icon, an icon of your own, or both |
| `password()` | renders `type="password"`, and tells the browser not to fill it with a stored password |
| `setHint(String)` | the tooltip of the control |
| `setUntrimmed(true)` | keep leading and trailing spaces; by default they are stripped |
| `immediate()` | send the value to the server when the field is left, even when the control has no change handler |

Both `setSize()` and `setMaxLength()` return the control, so they chain:
`new Text2<>(String.class).setSize(10).setMaxLength(6)`.

## Buttons inside the control

```java
Text2<String> search = new Text2<>(String.class);
search.addButtonSmall(Icon.faSearch, a -> doSearch(search.getValue()));
search.addButtonSmall(Icon.faEraser, a -> search.setValue(null));
```

A button added this way is rendered *inside* the control, right of the box, so
it travels with the control wherever it is put and lines up with it. The control
gets the css class `ctl-has-addons` while it has any.

| Method | What it adds |
| --- | --- |
| `addButtonSmall(icon, click)` | a `SmallImgButton` - the usual choice |
| `addButton(icon, click)` | a full `DefaultButton` |
| `addButton()` | an empty `DefaultButton` to configure yourself |
| `addButton(NodeBase)` | anything at all |
| `clearButtons()` | remove them all (this rebuilds the control) |

`DateInput2` is built exactly this way: it *is* a `Text2<Date>` with a calendar
button and a today button added.

## What it renders

```html
<div class="ui-txt2 ctl-has-addons">
    <div class="ui-control">
        <input class="ui-input" type="text" value="Yesterday">
    </div>
    <button class="ui-button ui-sib2">…</button>
</div>
```

The control is a `Div`, not an `<input>`: that is what lets it carry buttons and
an error state of its own. `getForTarget()` returns the inner input, which is
what a `<label>` has to point at - `Label.setForTarget(control)` follows it, and
keeps following it when the control rebuilds.

## Making one from a property

The static methods build a control already configured from the metadata of a
property - its length, its converter, its validators, the display size computed
from precision and scale:

| Method | Makes |
| --- | --- |
| `createText(Class, PropertyMetaModel, editable)` | a control for any property |
| `createIntInput(clz, property, editable)` | `Text2<Integer>`, right aligned |
| `createLongInput` / `createDoubleInput` / `createBigDecimalInput` | the same for the other numeric types |
| `createDoubleMoneyInput` / `createBDMoneyInput` | a monetary control, with the currency converter assigned |

A form builder does this for you: `fb.property(album, Album_.title()).control()`
asks the [control factory registry](../../../building-pages/80-metadata/index.md)
and gets a configured `Text2` back. Use the static methods when you build a
control outside a form.
