---
menu:
  sort: "20"
---
# CKEditor

The full wysiwyg editor: styles, fonts, colours, tables, images and the rest,
wrapped as a DomUI control whose value is html.

```java
CKEditor.initialize(this);            // Without this, nothing appears at all

CKEditor editor = new CKEditor();
editor.setWidth("100%");
editor.setHeight("300px");
editor.setValue("<p>Some <b>text</b>.</p>");
cp.add(editor);
```

!demo(to.etc.domuidemo.pages.components.editors.CKEditorPage.ui, 100%, 900)

[TOC]

## It does not load itself

!! `CKEditor.initialize(UrlPage)` **must** be called by the page, in
!! `createContent()`, before the editor is used. The framework used to put the
!! editor's javascript on every page and stopped, deliberately: it is a large
!! script that most pages never need. A page that forgets the call renders a
!! blank space where the editor should be, and `CKEDITOR is not defined` in the
!! browser's console.

## The toolbar sets

`setToolbarSet(CKToolbarSet)` picks between four toolbars:

| Set | What is on it |
| --- | --- |
| `TXTONLY` | bold, italic, underline, strike, cut, copy, paste, undo, redo |
| `BASIC` | that, plus Styles, Format, Font and Size on a second row |
| `DOMUI` | three rows: the above plus alignment, lists, indent, links, table, rule, colours, and the framework's own image picker, special-characters button and smileys |
| `FULL` | the same toolbar as `DOMUI` |

`DOMUI` is the default, and `FULL` is identical to it today. Those two are also
the only ones that load the extra plugins, so choosing `BASIC` or `TXTONLY`
removes the image picker and the colours as well as the buttons.

!! Pick the set when the editor is made. Setting it on an editor that is already
!! on the screen changes the field but does not redraw the toolbar.

## The rest of the API

| Method | What it does |
| --- | --- |
| `setValue(String)` / `getValue()` | the html |
| `setReadOnly(boolean)` / `setDisabled(boolean)` / `setMandatory(boolean)` | as on any control |
| `setOnValueChanged(IValueChanged<?>)` | told when the user changed the text |
| `setToolbarStartExpanded(boolean)` | start with the toolbar folded away, and let the user open it |
| `setOnDomuiImageClicked(IClicked<NodeBase>)` | what the toolbar's image button opens |
| `setOnDomuiOddCharsClicked(IClicked<NodeBase>)` | the same for the special-characters button |
| `appendfixSizeJS()` | re-measure the editor after the layout around it changed |

Without an image handler the image button says so and closes; without a
special-characters handler the framework's own character picker is shown.

`setWidth()` and `setHeight()` size the `div` the editor sits in - they are not
passed to CKEditor's own width and height options.

## What it does with the value

The editor's content arrives at the server as **raw, unfiltered** request data on
purpose: an html editor must be allowed to produce `img` tags that the normal
input filter would strip. The component therefore does the filtering itself, by
running the value through the application's `XssChecker` with local image sources
allowed.

That makes the value safe to *store*. It does not make it safe to *show* -
that is [`DisplayHtml`](../../50-display-only/displayhtml/index.md)'s job.

## The version

The editor bundled with DomUI is **CKEditor 4.3**, served from the framework's
own resources under `$ckeditor`, with its toolbars and the DomUI-specific plugins
configured in `domuiconfig.js`.
