---
menu:
  sort: "06"
---
# Using components

[Your first page](../first-page/index.md) was built out of tags: a `Div`, a
`Para`, a `Span`. Screens are not written that way. They are written with
**components** - input fields, buttons, comboboxes, tables - and this page is
about what a component actually is, what state each input control has, and how
a control tells you what the user typed.

The examples use `Text2<T>`, `DateInput2`, `ComboFixed2<T>` and `DefaultButton`,
and they set and read every value by hand. That is not how a real screen moves
data around - [data binding](../../data/data-binding/index.md) does that - but
doing it by hand once is the clearest way to see what a control does.

## A component is a node that builds itself

A component is not a separate kind of thing. `Text2<T>` extends `Div`,
`DefaultButton` extends `Button`, `ComboFixed2<T>` is a div as well. A component
*is* a node, so it goes into the tree like any other node - `add()` it to the
page, to a panel, to a table cell.

What makes it a component is that it fills itself in. It implements
`createContent()` - the same method your page implements, called by the same
mechanism, once, just before the node is rendered for the first time. A `Text2`
builds a div holding an `<input>`, followed by any buttons that were added to
it. A `DefaultButton` builds a `<button>` with a span for its icon and a span
for its text. Nothing else happens: the html a component becomes is a small tree
of the same tags you wrote by hand on the previous page.

This is what "layer 0" and "layer 1" mean. Layer 0 is `to.etc.domui.dom.html`:
the tags, one class per html element, with no behaviour of their own. Layer 1 is
the components, built out of layer 0. Your own screen fragments are the same
kind of thing - a class extending `Div` with a `createContent()` - so there is no
line between "framework component" and "your code".

Because the content is built late, setting a property on a component is just
setting a field; the html follows when the component builds. A property that
changes what the component *looks* like makes it drop its content and build
again (`forceRebuild()`): `ComboFixed2` does exactly that when you switch it to
read-only, and comes back as plain text instead of a `<select>`. Either way you
never render anything yourself - DomUI compares the built tree with what the
browser has and sends the difference.

## A form of components

```java
public class ComponentFormPage extends UrlPage {
	private final Text2<String> m_title = new Text2<>(String.class);

	private final Text2<Integer> m_copies = new Text2<>(Integer.class);

	private final Text2<BigDecimal> m_price = new Text2<>(BigDecimal.class);

	private final DateInput2 m_released = new DateInput2();

	private final ComboFixed2<String> m_medium = new ComboFixed2<>(List.of(
		new ValueLabelPair<>("cd", "Compact disc"),
		new ValueLabelPair<>("lp", "Vinyl LP"),
		new ValueLabelPair<>("dl", "Download")
	));

	@Override
	public void createContent() throws Exception {
		setPageTitle("A form of components");

		ContentPanel cp = new ContentPanel();
		add(cp);
		cp.add(new HTag(1, "A form of components"));

		FormBuilder fb = new FormBuilder(cp);
		fb.label("Album title").mandatory().control(m_title);
		fb.label("Copies in stock").control(m_copies);
		fb.label("Price each").control(m_price);
		fb.label("Released").control(m_released);
		fb.label("Medium").control(m_medium);
		...
	}
}
```

!demo(to.etc.domuidemo.pages.tutorial.components.ComponentFormPage.ui, 100%, 420)

The type parameter is what the control hands you back: `Text2<Integer>` returns
an `Integer`, `DateInput2` a `Date`, `ComboFixed2<String>` one of the `String`s
you put in it. A `Text2` for a numeric type also refuses non-numeric keystrokes
in the browser, but that is a convenience, not the check that matters.

The controls are laid out by
[FormBuilder](../../components/forms-and-input/form4-formbuilder/index.md) from
`to.etc.domui.component2.form4`. `fb.label("Album title").control(control)` puts
a label in front of a control; `mandatory()` marks the label and makes the
control mandatory. The label is used for one more thing: it becomes the
control's **error location**, the name that error messages are prefixed with.

## The state every control has

Whatever it looks like, an input control is an `IControl<T>` and has the same
handful of properties:

- **value** - `setValue(T)` and `getValue()`, in the control's own type. Setting
  a value only presents it; it is not checked.
- **readOnly** - the value stays visible and stays part of the page, but cannot
  be changed. Every control decides for itself how to show that: `Text2` renders
  its input read-only, `DateInput2` hides its calendar buttons as well, and
  `ComboFixed2` rebuilds itself and shows the chosen label as plain text instead
  of a `<select>`.
- **disabled** - the control is switched off: it cannot be focused or changed,
  and the theme greys it out.
- **disabledBecause** - the same as disabled, plus the reason.
  `setDisabledBecause("This album is no longer for sale")` disables the control
  and makes that text its hover title; `setDisabledBecause(null)` enables it
  again. Prefer it over a bare `setDisabled(true)`: a control that is off for no
  stated reason is a puzzle for the user.
- **mandatory** - `setMandatory(true)` states that a value must be present. It is
  checked when the value is read, not while typing.

```java
private void state(boolean readOnly, boolean disabled, @Nullable String because) {
	m_title.setReadOnly(readOnly);
	m_released.setReadOnly(readOnly);
	m_medium.setReadOnly(readOnly);

	//-- A reason both disables the control and becomes its hover text; null enables it again.
	m_title.setDisabledBecause(because);
	m_released.setDisabledBecause(because);
	m_medium.setDisabledBecause(because);

	if(because == null) {
		m_title.setDisabled(disabled);
		m_released.setDisabled(disabled);
		m_medium.setDisabled(disabled);
	}
}
```

!demo(to.etc.domuidemo.pages.tutorial.components.ComponentStatePage.ui, 100%, 320)

Press the buttons and watch the three controls: read-only and disabled are not
the same thing, and they do not look the same either.

## getValue() is where the input is checked

The browser sends back the raw text of every input with each request. Turning
that text into a value is what `getValue()` does, and it does it in three steps:
the mandatory check, then conversion to the control's type, then any validators
on the control. That gives three possible outcomes:

- a value;
- `null`, when the control is empty and not mandatory;
- a `ValidationException`.

On that last one the control puts itself in error state, and posts a message to
the nearest **error fence** - the page body is always one, so a message always
lands somewhere. If nothing on the page handles messages, DomUI inserts an
`ErrorPanel` as the first node of the page, which is the red bar the demo above
shows. The message is prefixed with the error location, so it reads
**Album title:** Mandatory field, and the field itself turns red.

Only then does the exception leave `getValue()` - and you are not expected to
catch it. The framework catches it around your handler, stops the handler there,
and renders the page as it now stands: with the message that was just posted. So
a handler can simply read what it needs:

```java
String title = m_title.getValue();
Integer copies = m_copies.getValue();
BigDecimal price = m_price.getValue();
```

The first field that cannot deliver ends the handler and reports itself. Nothing
after it runs, which is exactly what you want - the handler never sees
half-valid input.

When you *do* want to look without that happening, use `getValueSafe()`, which
returns `null` instead of throwing, and `hasError()`, which tells you whether
that `null` was an error rather than an empty field.

Two messages the demo page will show you: **Mandatory field** for an empty
mandatory control, and **The field content "abc" is invalid** when the text
cannot be converted to the control's type.

## Reacting to a change: setOnValueChanged

While the user types, nothing goes to the server; the typed values travel with
the next action, such as a button click. Registering a change handler on a
control changes that for that control:

```java
m_copies.setOnValueChanged(c -> showTotal());
m_price.setOnValueChanged(c -> showTotal());
```

DomUI then renders an `onchange` handler on the input, so leaving the field
after changing it causes a request of its own. In every request, whatever
triggered it, DomUI does the same three things in order:

1. it pushes the raw values from the browser into all controls;
2. it calls the change handlers of the controls whose value actually changed;
3. it runs the action, if the request was one.

That order is why a Save button always sees the value that was typed
immediately before it was pressed - the field's own change handler has already
run by then.

```java
private void showTotal() {
	Integer copies = m_copies.getValueSafe();
	BigDecimal price = m_price.getValueSafe();

	m_total.removeAllChildren();
	if(copies == null || price == null) {
		m_total.add("Fill in both fields to see the total");
	} else {
		m_total.add("Total: " + price.multiply(new BigDecimal(copies)));
	}
}
```

!demo(to.etc.domuidemo.pages.tutorial.components.ComponentChangePage.ui, 100%, 300)

Change either field and leave it: the total follows, without a button. Note the
`getValueSafe()` - a change handler runs while the user is still filling the
form in, so it should look at what is there rather than complain about what is
not.

## Next

Setting and reading every control by hand, as these three pages do, is fine for
a handful of fields and tiring for a screen. The next step is
[data binding](../../data/data-binding/index.md): you say which property of
which object a control shows, and DomUI keeps the two in step in both
directions.

All three pages above are in the demo application, under "Tutorial pages" on its
home page; the source icon in the top bar shows the Java source of the screen
you are looking at.
