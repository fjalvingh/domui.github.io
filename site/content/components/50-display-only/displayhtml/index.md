---
menu:
  sort: "50"
---
# DisplayHtml

`DisplayHtml` shows a piece of html as html: a review, a description, whatever a
[`CKEditor`](../../forms-and-input/index.md) produced. What it is given goes
through a sanitizer first.

```java
DisplayHtml review = new DisplayHtml(album.getReview());
review.setWidth("400px");
```

!demo(to.etc.domuidemo.pages.components.display.DisplayHtmlPage.ui, 100%, 620)

[TOC]

## The API

| Method | What it does |
| --- | --- |
| `new DisplayHtml()` / `new DisplayHtml(String)` | empty, or with html |
| `setValue(String)` / `getValue()` | the html; **setting it runs the sanitizer**, and `getValue()` returns what came out |
| `setMode(Mode)` | `BLOCK` (the default), `INLINE` or `INLINEBLOCK` |
| `setUnchecked(boolean)` | skip the sanitizer entirely |

The three modes decide the box, not the content: `BLOCK` is a block of its own
(`ui-dhtml-blk`), `INLINE` flows with the text around it (`ui-dhtml-inl`), and
`INLINEBLOCK` is a block that sits in a line (`ui-dhtml-ibl`).

The value is rendered as an `XmlTextNode`, which is what lets the html through
to the browser instead of escaping it.

## What the sanitizer does

`HtmlUtil.removeUnsafe()` works with allow-lists, and checks both what an
element *is* and what its attributes *say*.

**Elements.** Only `b`, `i`, `u`, `p`, `br`, `a`, `ol`, `ul`, `li`, `code`,
`div`, `strike`, `strong`, `blockquote`, `sup`, `sub` and `hr` survive. For most
rejected elements only the tags go and the text between them is kept - a table
loses its markup but not its cell texts. For the elements whose content is
*not* text to show - `script`, `style`, `iframe`, `object`, `embed`, `applet`,
`noscript`, `svg`, `math`, `template`, `title`, `head`, `frame`, `frameset`,
`base`, `link`, `meta` - the element is removed **with everything inside it**.
An unclosed one of those takes everything after it, because that is what a
browser would treat as its content too.

**Attributes.** Only `id`, `class`, `href`, `target`, `title`, `color`, `face`,
`size` and `style` survive, and three of them have their *value* checked:

| Attribute | What is refused |
| --- | --- |
| `href` (and the other url attributes) | any scheme that is not `http`, `https`, `mailto`, `ftp`, `ftps` or `tel`. A url with no scheme is relative and always allowed |
| `style` | values containing `url(`, `expression`, `behavior`, `binding`, `@import`, a backslash escape or a script scheme - ordinary colour and font styling is unaffected |
| `id` | a value starting with `_`, which could collide with a DomUI node id in the browser |

A refused *value* costs the attribute, not the element: a link with a script
scheme keeps its text and loses its `href`. Characters a browser ignores while
working out a scheme - spaces, tabs, newlines, control characters - are removed
before that check, and entities are decoded before it, so neither can be used to
hide one. A link that carries a `target` gets `rel="noopener noreferrer"` added.

!! `setUnchecked(true)` **skips all of that**. It is for html the application
!! produced itself, and for nothing else.
