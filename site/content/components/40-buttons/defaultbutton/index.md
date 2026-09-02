---
menu:
  sort: "10"
---
# DefaultButton

`DefaultButton` is the ordinary button: a text, an icon, or both, and a handler
that runs when it is pressed.

```java
cp.add(new DefaultButton("Save", Theme.BTN_SAVE, a -> save()));
```

!demo(to.etc.domuidemo.pages.components.buttons.DefaultButtonPage.ui, 100%, 780)

[TOC]

## Making one

| Constructor | Gives |
| --- | --- |
| `new DefaultButton()` | an empty button to configure afterwards |
| `new DefaultButton(text)` | text only |
| `new DefaultButton(text, icon)` | text and icon |
| `new DefaultButton(text, click)` | text and a handler |
| `new DefaultButton(text, icon, click)` | all three - the usual one |
| `new DefaultButton(IBundleCode, ...)` | the same with a translated text |
| `new DefaultButton(instance, action)` | a button made from an [`IUIAction`](../actionbutton/index.md) |

The fluent form builds the same button and reads better when a button is
configured in pieces:

```java
DefaultButton b = new DefaultButton()
    .text("Save")
    .icon(Icon.faCheck)
    .clicked(a -> save());
```

`text()`, `icon()`, `clicked()`, `css()` and `mini()` all return the button.

## Text, icon and accelerator

| Method | What it does |
| --- | --- |
| `setText(String)` | the text; a `!` marks the accelerator, `\!` is a literal one |
| `setIcon(IIconRef)` | a font icon, an image or a themed resource |
| `setIconImage(Class, String)` | an image from a java resource next to a class |
| `setTitle(String)` | the tooltip |
| `setDisabled(boolean)` / `setDisabledBecause(String)` | off, with an optional reason as tooltip |

Setting the text or the icon rebuilds the button, so both can be changed from a
handler and the screen follows.

## What it looks like

The button is styled entirely through css classes, which `css()` adds:

| Class | Effect |
| --- | --- |
| `is-primary`, `is-info`, `is-success`, `is-warning`, `is-danger`, `is-link`, `is-dark`, `is-light`, `is-white`, `is-black` | the colour |
| `is-small`, `is-medium`, `is-large` | the size |
| `is-outlined`, `is-inverted`, `is-text` | outlined, inverted, or drawn as plain text |
| `is-fullwidth` | as wide as its container |
| `is-loading` | a spinner instead of the label |

```java
new DefaultButton("Delete", a -> delete()).css("is-danger", "is-outlined");
```

!! `mini()` is not one of these: it **replaces** the button's css classes with
!! `ui-sdbtn-mini` rather than adding one, so a mini button is not styled by the
!! `is-` classes at all. Use it for a button inside a table row.

## What it renders

```html
<button class="ui-button ui-control" type="button" onclick="...">
    <span class="ui-icon"><span class="fa fa-heart"></span></span>
    <span class="ui-sdbtn-txt">S<u>a</u>ve</span>
</button>
```

The icon and the text are separate spans, and the accelerator letter is wrapped
in a `<u>`. A button with no text renders no text span at all, which is what
makes an icon-only button come out square.
