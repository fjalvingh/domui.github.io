---
menu:
  sort: "40"
---
# ImgIcon

An icon that is really a picture: a small `img` tag in a span, for a png, gif or
jpg used where a component wants an icon.

```java
cp.add(Icon.of("img/logo-small.png").createNode());    // ...which is an ImgIcon
```

!demo(to.etc.domuidemo.pages.components.images.IconsPage.ui, 100%, 900)

[TOC]

## Making one

| Method | What it does |
| --- | --- |
| `new ImgIcon(String src)` | that resource path |
| `new ImgIcon(ImageIconRef)` | the icon of a reference |
| `setSrc(String)` / `getSrc()` | change the picture |
| `css(String...)` | add classes, and return the icon, so it chains |

`Icon.of(path)` returns a reference that makes one of these for any extension
that is not `.svg`, so an `ImgIcon` is almost never constructed by hand. It
renders a span of class `ui-imgi` containing the `img`, with the border switched
off.

## What it cannot do

An image is a picture: **the colour classes do nothing to it**. `is-danger` on an
`ImgIcon` changes the colour of nothing, because css does not repaint a png.

That is the one real argument between the three kinds of icon. An icon that has
to follow the theme - to be red when it means danger, grey when it is disabled -
must be a [`FontIcon`](../fonticon/index.md) or an
[`SvgIcon`](../svgicon/index.md). An `ImgIcon` is for a picture that is what it
is: a logo, a flag, a screenshot-like thing that no palette applies to.

The framework's own [`Theme`](../icons/index.md) icons are image icons, which is
why restyling them means replacing the files or repointing the constants rather
than adding a class.
