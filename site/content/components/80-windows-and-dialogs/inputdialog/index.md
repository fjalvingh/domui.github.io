---
menu:
  sort: "30"
---
# InputDialog

A [`Dialog`](../dialog/index.md) that asks for exactly one value: one label, one
control, a save button and a cancel button. What comes back is the value, not
the control.

```java
Text2<String> title = new Text2<>(String.class);
title.setMandatory(true);
title.setValue("Big Ones");

InputDialog<String, Text2<String>> dlg = new InputDialog<>(title, "Rename the album", "New title") {
	@Override protected boolean onValidateData(String value) throws Exception {
		return value.length() >= 2;              // Refused: the dialog stays open
	}

	@Override protected boolean onSaveData(String value) throws Exception {
		album.setTitle(value);
		return true;
	}
};
add(dlg);
```

!demo(to.etc.domuidemo.pages.components.dialog.InputDialogPage.ui, 100%, 560)

[TOC]

## The two type parameters

`InputDialog<T, C extends NodeBase & IControl<T>>` - `T` is the type of the value
being asked for and `C` the control that asks for it. Any control will do, since
every one of them is an `IControl<T>`: a `Text2<Integer>` for a number, a
`ComboFixed2<Genre>` for a choice, a `DateInput2` for a date.

| Constructor | What it gives |
| --- | --- |
| `InputDialog(C control, String title)` | modal, not resizable, no label above the control |
| `InputDialog(C control, String title, String label)` | ...with a label |
| `InputDialog(C control, boolean resizable, String title)` | ...and a say in resizing |
| `InputDialog(C control, boolean modal, boolean resizable, String title, String label)` | ...and in modality |
| `InputDialog(C control, int width, int height, String title)` | of that size |
| `InputDialog(C control, boolean modal, boolean resizable, int width, int height, String title, String label)` | all of it |

The buttons are made for you: unlike a bare `Dialog`, an `InputDialog` calls
`createButtons()` itself and puts the bar at the bottom.

## What to override

| Method | What belongs in it |
| --- | --- |
| `onValidateData(T value)` | decide whether the value is acceptable; `false` keeps the dialog open |
| `onSaveData(T value)` | do something with it; `false` keeps the dialog open |
| `createContent()` | a layout of your own instead of label-above-control |
| `createButtons()` | a different set of buttons |

`onValidate()` and `onSave()` are final here: they read the control and hand the
value to the two methods above, which is the whole point of the class. The value
is read *before* validation, so both methods see the same thing;
`getInputControl()` is there for the rare case where the control itself is needed.

## Confirming something

Two ready-made dialogs use the same machinery to make an action hard to do by
accident. Both are static methods returning a `Dialog`, which still has to be
added to the page:

```java
//-- The user has to type the name of the thing being deleted.
add(InputDialog.confirmDeleteInBlood("Delete \"Big Ones\"?", "Big Ones",
	"Type the album title to confirm", value -> {
		delete();
		return true;
	}));

//-- The user has to say why.
add(InputDialog.confirmWithReason("Cancel the order", 80, 40,
	"Cancel the order", Icon.faTimes, reason -> {
		cancel(reason);
		return true;
	}));
```

| Method | What it asks |
| --- | --- |
| `confirmDeleteInBlood(title, confirmValue, controlLabel, onConfirm)` | the answer must equal `confirmValue`; the action button is a delete button in the danger colour, with a skull on it |
| `confirmWithReason(title, maxLen, size, buttonText, icon, onConfirm)` | the answer only has to be filled in, and is handed to the handler |
| `confirmInBlood(title, message, control, confirmValue, check, label, buttonText, icon, onConfirm)` | the general form of both: your control, your comparison |

The handler is a predicate: returning `false` keeps the dialog open, exactly as
`onSaveData` does.
