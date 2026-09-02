---
menu:
  sort: "30"
---
# SmallImgButton

`SmallImgButton` is a small button showing only an icon. It is the button that
lives *inside* something else: the calendar and today buttons of a
[`DateInput2`](../../10-text-and-value-input/dateinput2/index.md), the search
button of a [`Text2`](../../10-text-and-value-input/text2/index.md), a row
button in a table.

```java
SmallImgButton search = new SmallImgButton(Icon.faSearch, a -> doSearch());
search.setTitle("Search for a customer");
```

!demo(to.etc.domuidemo.pages.components.buttons.ButtonKindsPage.ui, 100%, 620)

[TOC]

## The API

| Method | What it does |
| --- | --- |
| `new SmallImgButton(icon)` / `(icon, click)` | the icon, and optionally the handler |
| `setSrc(IIconRef)` / `icon(IIconRef)` | a different icon; `icon()` returns the button |
| `setTitle(String)` / `setHint(String)` | the tooltip - **give it one** |
| `css(String...)` | extra css classes; returns the button |
| `setDisabled(boolean)` | off |

It has no text at all, so the tooltip is the only thing telling a user what the
button does. `setTitle()` also gives the button a stable test id derived from
that text, which is what the Selenium page objects use to find it.

## What it renders

```html
<button class="ui-button ui-sib2" type="button" onclick="...">
    <div class="ui-icon"><span class="fas fa-search ui-fnti"></span></div>
</button>
```

The icon sits in a `ui-icon` div, exactly as in a `DefaultButton` - the two
differ in their own class (`ui-sib2` against `ui-control`) and therefore in
their padding and size, not in their structure.
