---
menu:
  sort: "80"
---
# MessageFlare

A message that shows itself over the page and then goes away by itself. It says
that something happened; it asks nothing and there is nothing to press.

```java
MessageFlare.display(this, MsgType.INFO, "The album has been saved.");
```

!demo(to.etc.domuidemo.pages.components.dialog.FlarePage.ui, 100%, 520)

[TOC]

## Showing one

| Call | What it shows |
| --- | --- |
| `MessageFlare.display(NodeContainer, String)` | a message of the default severity (error) |
| `MessageFlare.display(NodeContainer, MsgType, String)` | a message of that severity |
| `MessageFlare.display(NodeContainer, UIMessage)` | the message and severity of a `UIMessage` |

There is nothing to add to the page: the flare is created on the page body,
shown, and removed again after the request. The severity picks the colour and
the icon - `MsgType.INFO`, `WARNING` or `ERROR`.

## One flare per request

`display()` does not make a new flare every time; it finds the one this request
already has, or makes it. So several messages in one request end up **in the same
flare, under each other**, and the severest of them decides what the flare looks
like:

```java
MessageFlare flare = MessageFlare.display(this, MsgType.INFO, "212 albums were read.");
flare.addMessage("3 albums were skipped: they have no artist.", MsgType.WARNING);
flare.addMessage("1 album was refused: it has no title.", MsgType.ERROR);
//-- ...and the flare is an error flare.
```

`addMessage(String)`, `addMessage(String, MsgType)` and `addMessage(UIMessage)`
add a line to a flare you already have.

## How long it stays

By default the flare **stays until the user moves the mouse**. A flare
constructed with `new MessageFlare(type, true)` vanishes by itself after about a
second and a half instead.

!! `setAutoVanish()` only counts while the flare is being made. The javascript
!! that makes it disappear is written when the flare is created, so setting it on
!! the flare that `display()` handed back changes nothing.

A flare is not for something the user has to act on: it is gone before it can be
read twice, and it says nothing about which field it is about. For that, post a
message - see [`ErrorMessageDiv`](../errormessagediv/index.md) - or ask in a
[`MsgBox2`](../msgbox2/index.md).
