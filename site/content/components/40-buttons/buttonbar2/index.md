---
menu:
  sort: "80"
---
# ButtonBar2

`ButtonBar2` is the bar a screen's buttons sit on: a left group, a right group,
and a set of methods for the *kinds* of button a screen usually needs.

```java
ButtonBar2 bb = new ButtonBar2();
cp.add(bb);
bb.addButton("Save", Theme.BTN_SAVE, a -> save());
bb.addConfirmedButton("Delete", Theme.BTN_DELETE, "Delete this album?", a -> delete());
bb.addBackButton();
bb.right();                                    // Everything after this goes right
bb.addLinkButton("Help", Icon.faQuestionCircle, a -> help());
```

!demo(to.etc.domuidemo.pages.components.buttons.ButtonBar2Page.ui, 100%, 700)

[TOC]

## What you add to it

You do not add buttons so much as ask for one:

| Call | What it adds |
| --- | --- |
| `addButton(text, icon, click)` | an ordinary `DefaultButton` |
| `addButton(text, click)` | the same without an icon |
| `addLinkButton(text, icon, click)` | a `LinkButton` |
| `addConfirmedButton(text, icon, question, click)` | a button that asks the question first and only calls the handler on yes |
| `addConfirmedLinkButton(text, icon, question, click)` | the same as a link |
| `addBackButton()` | go back to the page you came from |
| `addBackButtonConditional()` | the same, but nothing at all when there is nowhere to go back to |
| `addCloseButton()` | close the window |
| `addAction(instance, action)` | a button made from an [`IUIAction`](../actionbutton/index.md) |
| `addButton(node, order)` | any node at all, for what the list above does not cover |

Every one of them also has a form taking an `order` number, and the bar sorts on
it - so where a button ends up does not depend on the order the code happened to
run in, which is what a base class adding buttons around a subclass's needs.

`addBackButton()` reads the page shelf that
[page navigation](../../../building-pages/60-page-navigation/index.md)
describes: with nothing to go back to it quietly renders a **Close** button
instead.

## Left, right and direction

| Method | What it does |
| --- | --- |
| `right()` | everything added after this goes in the right group |
| `new ButtonBar2(Direction.VERTICAL)` | a column instead of a row |
| `new ButtonBar2(String css)` | an extra css class on the bar |
| `clearButtons()` / `removeButton(node)` | take them out again |

## What it renders

```html
<div class="ui-bbar2 ui-bbar2-horizontal">
    <div class="ui-bbar2-l">
        <div class="ui-bbar2-bc"><button ...>Save</button></div>
        <div class="ui-bbar2-bc"><button ...>Delete</button></div>
    </div>
    <div class="ui-bbar2-r">
        <div class="ui-bbar2-bc"><a ...>Help</a></div>
    </div>
</div>
```

Each button sits in its own cell, and the two groups are separate elements -
which is what lets the theme push them to the two ends of the bar.
