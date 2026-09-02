---
menu:
  sort: "40"
---
# HoverButton

`HoverButton` is an image button whose normal, hover and disabled appearance all
come from **one** image: three pictures of the same size, side by side.

```java
HoverButton close = new HoverButton("THEME/72x24_close.png", a -> closeWindow());
```

!demo(to.etc.domuidemo.pages.components.buttons.ButtonKindsPage.ui, 100%, 620)

[TOC]

## The image is the button

The control reads the image's dimensions at build time, divides the width by
three, and sizes itself to one of them - so a 72x24 image is a 24x24 button
showing its left third, its middle third on hover, and its right third when
disabled. Getting that wrong is reported: an image whose width is not a multiple
of three, or whose parts are far from square, is logged as an error.

| Method | What it does |
| --- | --- |
| `new HoverButton(rurl)` / `(rurl, click)` | the image, and optionally the handler |
| `setSrc(String)` | a different image; rebuilds the button |
| `setDisabled(boolean)` / `setDisabledBecause(String)` | off, with the reason as tooltip |

The url is an ordinary web resource path, with `THEME/` in front of it meaning
"from the current theme's directory".

## When to use it

This is the button of the framework's own furniture: the back and close buttons
of `AppPageTitleBar` and the expander of `ExpandHeader` are all `HoverButton`s,
and their images live in the theme.

For anything else, prefer [`SmallImgButton`](../smallimgbutton/index.md): it
takes an `IIconRef`, so it works with font icons, needs no image to be drawn in
three states, and scales with the page rather than with a bitmap.
