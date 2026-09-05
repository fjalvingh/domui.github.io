# Rich content editors

Three editors, for two different kinds of content. Two of them produce **html**
that a user formatted; the third edits **code**, with syntax colouring, and
produces plain text.

[TOC]

## The components

| Component | Edits | What it is |
| --- | --- | --- |
| [`HtmlEditor`](htmleditor/index.md) | html | a small wysiwyg editor that appears instantly |
| [`CKEditor`](ckeditor/index.md) | html | the full wysiwyg editor: styles, tables, colours, images |
| [`AceEditor`](aceeditor/index.md) | code | the Ace code editor, with completion and markers |

All three are `IControl<String>`, so `setValue()`, `getValue()`, `setReadOnly()`,
`setDisabled()`, `setMandatory()`, `setOnValueChanged()` and data binding work
the way they do on any other control. What differs is what the string *is*.

## Which of the two html editors

They produce the same thing - a string of html - and the choice is about weight:

| | `HtmlEditor` | `CKEditor` |
| --- | --- | --- |
| toolbar | one row: bold, italic, lists, alignment, a table, a rule | four toolbar sets, up to styles, fonts, colours, images and tables |
| appears | immediately | after a visible pause: a large third-party editor starting up |
| loaded | with the framework's own javascript | only on pages that ask for it |
| built on | a jQuery wysiwyg plugin over a `TextArea` | CKEditor 4 |

So a remark, a description, a note gets the small one; a screen whose *point* is
writing a document gets `CKEditor`.

!! `CKEditor` does not put its own javascript on the page. A page that uses one
!! must call `CKEditor.initialize(this)` in `createContent()` or **nothing
!! appears at all** - the framework deliberately stopped loading that script on
!! every page.

## Showing the result

None of these is for *displaying* what was written. The html an editor produced
is shown by [`DisplayHtml`](../50-display-only/displayhtml/index.md), which
sanitises it before it goes on the page; a piece of code is shown by
[`EmbeddedCode`](../50-display-only/embeddedcode/index.md).

!! What comes out of an html editor is html a **user** wrote, and it is never to
!! be trusted. `CKEditor` runs its value through the application's XSS checker on
!! the way in, because it has to allow image tags that the normal filter would
!! strip. Anything stored and shown again is filtered on the way out as well -
!! which is what `DisplayHtml` is for.
