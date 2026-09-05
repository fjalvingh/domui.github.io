---
menu:
  sort: "70"
---
# ErrorMessageDiv

The messages an error fence caught, as bare lines: no caption, no frame. It is
what a piece of a screen uses to keep its own complaints inside itself.

```java
Div panel = new Div();
cp.add(panel);
ErrorMessageDiv emd = new ErrorMessageDiv(panel);   // Makes the panel a fence and listens to it
panel.add(emd);
```

!demo(to.etc.domuidemo.pages.components.dialog.ErrorDisplayPage.ui, 100%, 760)

[TOC]

## Making one

| Constructor | What it does |
| --- | --- |
| `ErrorMessageDiv(NodeContainer parent)` | makes `parent` an error fence and registers itself as its listener |
| `ErrorMessageDiv(NodeContainer parent, boolean propagate)` | the same, but with `true` the fence also hands what it catches to the fence above it |
| `ErrorMessageDiv()` | neither; use `setAsErrorFence(parent)` later, or register it on a component as an external error listener |

The one-argument constructor is two things in one call - the fence *and* the
component that shows what it catches - which is why it is the usual way to give a
panel messages of its own. Note that it only registers the div; adding it to the
panel is still up to you, and where you add it is where the messages appear.

**Propagating** is for a message that has to be visible in two places at once: a
panel deep in a page that shows its own errors, on a screen where the page as a
whole also lists everything that is wrong. It is a
`PropagatingErrorFenceHandler` on the panel; the message is shown here and then
travels on.

## What it does with the messages

- It is **hidden while empty** (`visibility: hidden`) and shows itself when a
  message arrives.
- The border class follows the severest message in it (`ui-emd-brd-error`,
  `-warning`, `-info`), and each line carries the type of that one message.
- **An info message makes way for a real one**: when a warning or an error
  arrives, the info messages already on display are dropped. The other way round
  they are not - an info message never replaces a warning.
- The control a message belongs to gets `ui-input-err`, and loses it when the
  message is removed.

For the block with a caption, and for what the application shows by default, see
[`ErrorPanel`](../errorpanel/index.md).
