---
menu:
  sort: "50"
---
# Img

The plain html image tag: a picture that is part of the screen, fetched by the
browser from wherever the source points.

```java
Img logo = new Img("img/logo-small.png");
logo.setAlt("The company logo");
cp.add(logo);
```

!demo(to.etc.domuidemo.pages.components.images.ImgPage.ui, 100%, 800)

[TOC]

## Where the picture comes from

| Constructor | The source |
| --- | --- |
| `new Img()` | nothing yet; `setSrc()` later |
| `new Img(String src)` | a path inside the web application, or `THEME/...` for one from the current theme |
| `new Img(Class<?> base, String name)` | a java resource beside that class - how a jar ships its own pictures |

`setSrc(String)` and `setSrc(Class<?>, String)` do the same afterwards. A
`THEME/` path is resolved against whatever theme the application is running, so
the same code shows a different picture under a different theme.

## What can be said about it

| Method | What it does |
| --- | --- |
| `setAlt(String)` | the `alt` text - **write one**: it is what a screen reader reads |
| `setImgWidth(String)` / `setImgHeight(String)` | the tag's width and height; giving one keeps the ratio |
| `setImgBorder(int)` | the border; the constructors that take a source already set it to 0 |
| `setAlign(ImgAlign)` | the old html alignment |
| `setTitle(String)` / `setHint(String)` | the tooltip |
| `setUseMap(String)` | an image map, for the rare screen that needs one |

Width and height are strings because the html attributes are. They tell the
browser how big to draw the picture; they do not resize the file, so a 4000-pixel
photo shown at 64 pixels still costs the user 4000 pixels of download. When the
picture is stored by the application rather than shipped with it,
[`DisplayImage`](../displayimage/index.md) is the component that resizes on the
server.

## An image that answers a click

```java
Img button = new Img("img/reload.png");
button.setClicked(a -> reload());
```

Giving an `Img` a click handler adds the `ui-clickable` class, so the cursor
changes over it. `setDisabled(true)` greys the picture out and stops the handler
being called.

!! An image with a click handler is not a button: it has no focus, no keyboard,
!! and nothing tells the user it can be pressed. For an actual button with a
!! picture on it use [`SmallImgButton`](../../40-buttons/smallimgbutton/index.md)
!! or [`HoverButton`](../../40-buttons/hoverbutton/index.md), which are exactly
!! that.

## Img or an icon?

Both put a picture on the screen, and the difference is what the picture is
*for*. An [`ImgIcon`](../imgicon/index.md) is what a component makes out of an
[icon reference](../icons/index.md) - it marks a button, a row, a header, and it
is interchangeable with a font or an svg icon. An `Img` is a picture in its own
right: a logo, a photograph, a diagram.
