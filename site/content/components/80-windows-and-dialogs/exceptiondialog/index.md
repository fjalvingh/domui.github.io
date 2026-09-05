---
menu:
  sort: "50"
---
# ExceptionDialog

What the user sees when code threw. It shows a box with the message you passed
as its title, and what it puts inside depends on whether anything recognises the
exception.

```java
try {
	save();
} catch(Exception x) {
	ExceptionDialog.create(this, "Saving the order failed", x);
}
```

!demo(to.etc.domuidemo.pages.tutorial.messages.MsgExceptionPage.ui, 100%, 320)

[TOC]

## Showing one

| Method | What it does |
| --- | --- |
| `ExceptionDialog.create(NodeContainer, String message, Throwable)` | show the exception in a box |
| `ExceptionDialog.createIgnore(NodeContainer, String message, Throwable)` | the same, but a failure while *making* the box is logged instead of thrown |
| `node.executeWithDialog(String message, IExecute)` | run the code, show the dialog if it threw, and return `false` in that case |

`executeWithDialog` is on `NodeContainer`, so it is available on every page and
component; it is the try/catch above, written once:

```java
cp.add(new DefaultButton("Save", a -> executeWithDialog("Saving the order failed", () -> save())));
```

A `ValidationException` is ignored on purpose: the control that threw it has
already put its message on the screen, and a box on top of that would say the
same thing twice.

## What ends up in the box

The exception is unwrapped out of any `WrappedException` and offered to the
registered **translators** - functions from an exception to an
`ExceptionPresentation`, which is either a sentence or a piece of DOM. The first
one that returns something decides what is shown. If none of them recognise it,
the exception is logged as an error and the box shows its `toString()` and its
stack trace.

| Exception | What the user sees instead of a stack trace |
| --- | --- |
| `CodeException`, `MessageException` | the message of the exception, translated |
| `QConcurrentUpdateException`, JPA's `OptimisticLockException` | "somebody else changed this data" |
| a `SQLException` with SQL state 23505, `BetterSQLException` | the message of the database error |

Your own exceptions get the same treatment by registering a translator:

```java
ExceptionDialog.register(x -> x instanceof OutOfStockException osx
	? new ExceptionPresentation(Msg.orderOutOfStock.format(osx.getAlbum()))
	: null);
```

The list is global and the **last** translator registered is asked **first**, so
this belongs in the `initialize()` of your `DomApplication` - it is a decision of
the application, not of a page.

Exceptions that nobody catches at all do not reach this class; they are handled
by the exception listeners of the application, which
[telling something to a user](../../../building-pages/90-telling-the-user/index.md)
describes.
