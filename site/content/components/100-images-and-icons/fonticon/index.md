---
menu:
  sort: "20"
---
# FontIcon

A glyph from an icon font. Because it is a character in a font it is *text*: it
takes the colour of text, scales with font size, and costs nothing to draw.

```java
cp.add(FaIcon.faMusic.createNode());
```

!demo(to.etc.domuidemo.pages.components.images.IconsPage.ui, 100%, 900)

[TOC]

## What it renders

A `span` with the class `ui-fnti` and whatever css classes the font needs — that
is the whole component. The font's own stylesheet turns those classes into a
glyph.

| Method | What it does |
| --- | --- |
| `new FontIcon(IFontIconRef)` | the icon of that font-pack constant |
| `new FontIcon(String cssClass)` | the same by class name, when there is no constant |
| `setIconName(IFontIconRef)` / `setIconName(String)` | change it; the span swaps its class |
| `css(String...)` | add classes, and return the icon, so it chains |

You rarely construct one. A font pack's enum constant *is* an
[`IIconRef`](../icons/index.md), and every component that takes an icon takes the
reference:

```java
new DefaultButton("Delete", FaIcon.faTrash, a -> delete());   // Makes the FontIcon itself
```

## Size and colour

Both are css classes on the span, and both work because it is text:

```java
FaIcon.faTrash.css("is-size-2", "is-danger")
```

| Classes | What they do |
| --- | --- |
| `is-size-1` … `is-size-7` | the size, 1 being the largest |
| `is-size-small`, `is-size-normal`, `is-size-medium`, `is-size-large` | the same by name |
| `is-primary`, `is-link`, `is-info`, `is-success`, `is-warning`, `is-danger`, `is-white`, `is-black`, `is-light`, `is-dark` | the theme's palette |

The font's own classes work too - `fa-2x`, `fa-spin` and the rest for
FontAwesome - because they are just more classes on the same span. Prefer the
`is-` ones: they come from the theme, so they follow it when it changes.

## Which font

`FontIcon` does not care. It writes the classes it is given, and something else
has to have put the font's stylesheet on the page. Including one of the
`fontawesome*` modules does that automatically; a font of your own needs a
[header contributor](../../../look-and-feel/header-contributors/index.md) and an
enum of its own, which the [icon reference page](../icons/index.md) describes.
