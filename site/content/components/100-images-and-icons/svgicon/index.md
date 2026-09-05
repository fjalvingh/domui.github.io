---
menu:
  sort: "30"
---
# SvgIcon

An svg file, written **into** the page rather than fetched by the browser. That
is what makes it different from an image: because the svg's own tags are part of
the document, css reaches inside it and can recolour it.

```java
cp.add(new SvgIcon("img/checkmark.svg"));
cp.add(Icon.of("img/checkmark.svg").createNode());     // The same, through a reference
```

!demo(to.etc.domuidemo.pages.components.images.IconsPage.ui, 100%, 900)

[TOC]

## Making one

| Method | What it does |
| --- | --- |
| `new SvgIcon(String src)` | a resource path, or the svg source itself when it starts with `<` |
| `new SvgIcon(ISvgIconRef)` | the icon of a reference that carries svg |
| `setSrc(String)` / `getSrc()` | change it; the icon rebuilds |
| `css(String...)` | add classes, and return the icon, so it chains |

The path is resolved through the application's resource system, so it can be a
file in the web application, `THEME/...` for one from the current theme, or a
java resource. A path that does not resolve throws when the icon is built, rather
than rendering a broken picture.

## Size and colour

```java
Icon.of("img/checkmark.svg").css("is-size-1", "is-danger")
```

The `is-size-*` and colour classes are the same list as for a
[`FontIcon`](../fonticon/index.md). Size works by font size: the stylesheet gives
the embedded `svg` a width and height of `1em`, so the icon follows the text
around it.

!! Colour works by filling the svg's **paths**, so it recolours a single-colour
!! icon and ruins a multi-coloured one. An svg meant to be recoloured should be
!! one colour to begin with.

## What it costs

The svg's source is read and written into the page every time the icon is
rendered, so the same icon on a hundred rows is a hundred copies of it in the
html. For an icon that is a handful of paths that is nothing; for a detailed
drawing it is not, and an [`Img`](../img/index.md) pointing at the same file -
which the browser fetches once and caches - is the better component.
