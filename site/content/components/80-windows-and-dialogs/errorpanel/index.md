---
menu:
  sort: "60"
---
# ErrorPanel

A titled block that shows the messages an error fence caught. It is the
component DomUI puts on a page that has nothing else to show them with.

```java
Div panel = new Div();
cp.add(panel);
panel.setErrorFence();                   // Messages from below stop here...
panel.add(new ErrorPanel());             // ...and this shows what was caught
```

!demo(to.etc.domuidemo.pages.components.dialog.ErrorDisplayPage.ui, 100%, 760)

[TOC]

## What it does

An `ErrorPanel` needs nothing but to be added: on the way into the page it looks
for the nearest error fence above it and registers itself as a listener of that
fence, and when it is removed it deregisters again. Everything after that is
automatic - it has no methods of its own worth calling.

- It is **invisible while there is nothing to show**, and appears the moment the
  first message arrives.
- Its **title follows the severest message in it**: "Errors on the page",
  "Warning(s) on the page" or the info header.
- Each message is written with its error location in bold in front of it, and the
  control a message belongs to gets the `ui-input-err` class - which is what
  makes the field turn red.

## Where it comes from by itself

A page usually never makes one. When a message arrives at a fence that has no
listener at all, the framework asks the application for a display component:

```java
@Override public void addDefaultErrorComponent(NodeContainer page) {
	ErrorPanel panel = new ErrorPanel();
	page.add(0, panel);
}
```

That is `DomApplication.addDefaultErrorComponent()`, and it is the reason a page
that does nothing about errors still shows them. Overriding that one method
changes how messages appear in the whole application - which is where an
application decides between this component and
[`ErrorMessageDiv`](../errormessagediv/index.md), and where in the page they land.

## Which of the two to use

`ErrorPanel` is a block with a caption around the messages: it is meant to be
noticed, and it fits at the top of a page or a dialog. `ErrorMessageDiv` writes
the bare lines with no title and no frame, which is what fits inside a panel, a
tab or a fragment that only has room for one line.
