# Windows, dialogs and messages

Saying something the screen itself does not say. The components here differ in
one thing: how much they interrupt. A **window** covers the page and, when it is
modal, has to be dealt with before anything else can happen. A **message** is a
line of text that appears next to what it is about and waits to be read. A
**flare** shows itself for a second and is gone.

[TOC]

## The components

The overlays - a window over the page, with or without buttons:

| Component | What it is for |
| --- | --- |
| [`Window`](window/index.md) | a floating window: a title bar, a content area and nothing else |
| [`Dialog`](dialog/index.md) | the same window with a button bar and save/cancel handling |
| [`InputDialog`](inputdialog/index.md) | a dialog that asks for exactly one value |
| [`MsgBox2`](msgbox2/index.md) | the message box: a sentence, some buttons, an answer |
| [`ExceptionDialog`](exceptiondialog/index.md) | what the user sees when code threw |

...and the things that appear inside the page itself:

| Component | What it is for |
| --- | --- |
| [`ErrorPanel`](errorpanel/index.md) | a titled block showing the messages a fence caught |
| [`ErrorMessageDiv`](errormessagediv/index.md) | the same, as bare lines instead of a block |
| [`MessageFlare`](messageflare/index.md) | a message that shows itself over the page and vanishes |
| [`MessageLine`](messageline/index.md) | one line with an icon: a remark that is part of the screen |
| [`InfoPanel`](infopanel/index.md) | a paragraph of explanation with a large icon |
| [`Explanation`](explanation/index.md) | the same, with a severity |

## An overlay is added to the page

Everything in the first table is a floating window, and a floating window is
added to the **page**, never to the `ContentPanel` the content lives in:

```java
Window w = new Window("The album");
add(w);                                   // add() on the page, not on the panel
w.add(new Para().add("...the content of the window..."));
```

`MsgBox2` and `ExceptionDialog` do that themselves - `MsgBox2.on(node)` only
needs a node to find the page from - so for those there is nothing to add.

!! A window does not stop the code that opened it. The handler that made the
!! window runs to its end, and the window appears on the next screen the user
!! sees. Everything that has to happen *after* the user answers belongs in a
!! close handler, an answer handler or an `onSave()` - never on the line after
!! the window was made.

## Where messages come from

The second table is only the display side. What is displayed - a `UIMessage`,
where it is posted, and the error fence that decides which component shows it -
is one mechanism, described in the walkthrough under
[telling something to a user](../../building-pages/90-telling-the-user/index.md).
The pages here say what each component looks like and when to pick it; that page
says how a message finds them.
