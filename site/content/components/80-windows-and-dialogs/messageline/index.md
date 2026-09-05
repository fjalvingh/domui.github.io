---
menu:
  sort: "90"
---
# MessageLine

One line with an icon: a remark that is part of the screen rather than something
that just happened.

```java
cp.add(new MessageLine(MsgType.INFO, "The prices shown are <b>excluding</b> VAT."));
```

!demo(to.etc.domuidemo.pages.components.dialog.NoticePage.ui, 100%, 760)

[TOC]

## Making one

| Constructor | What it gives |
| --- | --- |
| `MessageLine(MsgType, String)` | the icon of that severity, and the text |
| `MessageLine(MsgType, IBundleCode, Object...)` | the same, translated |
| `MessageLine(String icon, String text)` | an icon of your own, by resource url |
| `MessageLine(MsgType, ConsumerEx<NodeContainer>)` | the icon, and a line you fill in yourself |

The text may contain simple html, and `setText(String)` or
`setText(IBundleCode, Object...)` replaces it afterwards - the line rebuilds
itself when it does.

The last form is for a line that is not just text: the consumer is handed the
span the text would have gone in, so it can add a link, a value, a button.

```java
cp.add(new MessageLine(MsgType.INFO, line -> {
	line.add("The stock is counted every night. ");
	line.add(link);
}));
```

## When to use it instead of a message

A `MessageLine` is written into the page like any other node. It is there because
you put it there, and it stays until the page is rebuilt - it is not posted, it
has no error location, no control turns red, and no error fence is involved.

So it is the component for a remark that belongs to the screen ("prices are
excluding VAT"), not for the answer to something the user did. That is a
`UIMessage`, and it ends up in an
[`ErrorMessageDiv`](../errormessagediv/index.md) or an
[`ErrorPanel`](../errorpanel/index.md).

For a whole paragraph rather than a line, use
[`InfoPanel`](../infopanel/index.md) or
[`Explanation`](../explanation/index.md).
