---
menu:
  sort: "20"
---
# SearchInput2

`SearchInput2` is the search box itself: an input with a magnifier marker that
reports what is typed to the server while the user is still typing.

```java
SearchInput2 box = new SearchInput2();
box.setHint("Type part of a name");
box.setOnLookupTyping(a -> showMatches(box.getValue()));
box.setReturnPressed(a -> takeTheFirstMatch());
cp.add(box);
```

[TOC]

## What it is for

It is the box inside a [`LookupInput2`](../lookupinput2/index.md), and that is
where most applications meet it. It is worth knowing on its own for the case
where a screen needs the typing behaviour without the value: a filter above a
list, a box that narrows a tree.

It is **not** an `IControl`: it has no value of type `T`, no mandatory state and
no binding. What it has is the text typed so far.

| Method | What it does |
| --- | --- |
| `getValue()` | the raw text currently in the box |
| `setOnLookupTyping(IValueChanged<SearchInput2>)` | called while typing, a short pause after each burst |
| `setReturnPressed(...)` | called when the user presses return in the box |
| `setHint(String)` | the tooltip |
| `setPopupWidth(int)` | the width for whatever is dropped down under it |
| `setFocus()` | put the cursor in it |

## How the typing gets to the server

The control renders an ordinary input and attaches `WebUI.SearchPopup` to it in
the browser. That watches the keyboard and posts what has been typed after a
short idle - so the server is asked once per burst of typing rather than once
per keystroke, and a fast typist causes one round trip rather than ten.

The handler is free to do anything with the text. `LookupInput2` runs a query
with it and hangs a `SelectOnePanel` - the drop-down list - inside the box; a
screen of your own can do the same, or nothing at all.
