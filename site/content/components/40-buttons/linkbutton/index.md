---
menu:
  sort: "20"
---
# LinkButton

`LinkButton` is a button that looks like a link. It does exactly what a
[`DefaultButton`](../defaultbutton/index.md) does - it calls a handler - and
asks for attention more quietly.

```java
cp.add(new LinkButton("Forgot your password?", a -> resetPassword()));
cp.add(new LinkButton("Delete", Icon.faTrash, a -> delete()));
```

!demo(to.etc.domuidemo.pages.components.buttons.ButtonKindsPage.ui, 100%, 620)

[TOC]

## Making one

| Constructor | Gives |
| --- | --- |
| `new LinkButton(text)` | text only |
| `new LinkButton(text, click)` | text and a handler |
| `new LinkButton(text, icon)` | text and an icon |
| `new LinkButton(text, icon, click)` | all three |
| `new LinkButton(IBundleCode, ...)` | the same with a translated text |
| `new LinkButton(IUIAction<Void>)` | a link made from an [action](../actionbutton/index.md) |

`icon()` and `click()` are the fluent forms and return the button.

| Method | What it does |
| --- | --- |
| `setText(String)` | the text |
| `setImage(IIconRef)` | the icon in front of it |
| `setDisabled(boolean)` / `setDisabledBecause(String)` | off, with the reason as tooltip |
| `setTitle(String)` | the tooltip |

## It is an ATag, not a button

`LinkButton extends ATag`, so it renders as an `<a>` and flows with the text
around it - which is what makes it right for "and by the way you can also do
this" and wrong for the action a screen is about. A disabled one gets the css
class `ui-disabled` and stops calling its handler; it stays visible.

The rendered structure is the link, the icon node when there is one, and the
text in its own span:

```html
<a class="ui-lbtn ui-lbtn-i" onclick="...">
    <span class="fa fa-trash ui-lbtn-icon"></span>
    <span class="ui-lbtn-txt">Delete</span>
</a>
```

A link without an icon gets `ui-lbtn-noi` instead of `ui-lbtn-i`, so the two can
be spaced differently.

## Not a navigation link

A `LinkButton` runs a handler. For a link that *goes somewhere* - another page,
with parameters - the component is `ALink`, which renders a real `href` the
browser can open in a new tab. Use `LinkButton` when pressing it does something,
`ALink` when pressing it goes somewhere.
