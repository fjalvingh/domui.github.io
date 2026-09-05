---
menu:
  sort: "40"
---
# MsgBox2

The message box: a sentence, an icon, a few buttons, and an answer. It is a
window like any other, but it is built with one chained call and it adds itself
to the page.

```java
MsgBox2.on(this).info("The album has been saved.");

MsgBox2.on(this)
	.question()
	.text("Delete the album \"Big Ones\"? This cannot be undone.")
	.yesNo()
	.onAnswer(button -> {
		if(button == MsgBoxButton.YES) {
			delete();
		}
	});
```

!demo(to.etc.domuidemo.pages.components.dialog.MsgBox2Page.ui, 100%, 700)

[TOC]

`MsgBox2.on(node)` makes the box and hangs it on the page that `node` belongs to,
so there is nothing to `add()`. Everything after it describes the box, and the
box appears when the request is finished.

## What it says

| Call | What it does |
| --- | --- |
| `info()`, `warning()`, `error()`, `question()` | the type: the icon and the default title |
| `info(String)`, `warning(String)`, `error(String)` | the same, plus the text, in one call |
| `type(Type)` | the type as a value: `INFO`, `WARNING`, `ERROR`, `DIALOG`, `INPUT` |
| `title(String)` / `title(IBundleCode, Object...)` | a title of your own instead of the one the type gives |
| `text(String)` / `text(IBundleCode, Object...)` | the message; simple html in it is rendered |
| `content(NodeContainer)` | a piece of DOM instead of a sentence |
| `renderer(IRenderInto<String>)` | render the text yourself |
| `icon(IIconRef)` | an icon of your own |
| `size(int width, int height)` | a fixed size; `-1` for a height that follows the content |

## The buttons

| Call | What it adds |
| --- | --- |
| `button(MsgBoxButton)` | one of the standard buttons: `OK`, `YES`, `NO`, `CANCEL`, `CONTINUE`, `RETRY`, `IGNORE`, `MORE`, `BUGGEROFF` |
| `button(MsgBoxButton, MsgBoxButtonPrio)` | ...with a priority of your own |
| `buttonDefault(MsgBoxButton, MsgBoxButtonPrio)` | ...and give it the focus when the box opens, so enter presses it |
| `yesNo()`, `continueCancel()` | the two usual pairs |
| `button(String label, Object value)` | a button of your own carrying the value it answers with |
| `button(String label, IClicked<DefaultButton>)` | a button that runs its own handler instead of answering |
| `button(String label, MsgBoxButtonPrio, IClicked<DefaultButton>)` | ...with a priority |

**Add no buttons at all and the box gets `CONTINUE`** - plus a `CANCEL` when it
carries an input. Closing the box with the cross counts as `CANCEL`.

The **priority** decides two things: the colour of the button (`Primary` and
`PrimaryDanger` are coloured, `Secondary`, `Default` and `Cancel` are not) and
where it ends up. When no button was given a priority of its own, each standard
button takes the priority of its kind and the bar is sorted by it: `Primary`
(`OK`, `YES`, `CONTINUE`) on the right, `Cancel` (`CANCEL`, `NO`) on the left. As
soon as one button is added *with* a priority, that sorting is off and the
buttons stand in the order they were added - so either let the box order them, or
add them in the order you want them.

## The answer

| Handler | When it is called, and with what |
| --- | --- |
| `onAnswer(IAnswer)` | a standard button was pressed: the `MsgBoxButton` |
| `onAnswer2(IAnswer2)` | the same, but for `button(label, value)`: the value |
| `onClicked(IClicked<MsgBox2>)` | any button was pressed: the box |
| `input(label, control, IInput<T>)` | the box has an input and it was accepted: the value of the control |
| `onValidate(IValidate)` | *before* the answer handler, with the button; `false` keeps the box open |

```java
Text2<Integer> copies = new Text2<>(Integer.class);
copies.setMandatory(true);

MsgBox2.on(this)
	.title("Order")
	.input("Copies", copies, value -> order(value))
	.onValidate(button -> {
		if(button != MsgBoxButton.CONTINUE) {
			return true;                              // Cancelling is always allowed
		}
		Integer value = copies.getValueSafe();        // Empty: reports "mandatory" itself
		if(null == value) {
			return false;
		}
		if(value.intValue() > 10) {
			MsgBox2.on(this).error("At most 10 copies can be ordered at once.");
			return false;                             // Keeps the box open
		}
		return true;
	});
```

The control in an input box is an ordinary control: it converts, validates and
reports the way it would on a page. `input(String label, NodeBase control)` adds
one without a handler, for a box that reads its controls itself.

!! The call returns at once - a message box does not block. The rest of the
!! handler runs, and the box is only on the screen the user sees next. Everything
!! that has to happen after the answer belongs in the answer handler.

`autoClose(boolean)` decides whether clicking next to the box closes it, as on
any [window](../window/index.md).

Boxes stack: a box opened from inside a box - a validation error over an input
box, say - is put on top of it and closed first.
