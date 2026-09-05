---
menu:
  sort: "10"
---
# HtmlEditor

The small wysiwyg editor: a toolbar with the everyday buttons over an editing
area, and the value is the html the user made.

```java
HtmlEditor editor = new HtmlEditor();
editor.setWidth("600px");
editor.setValue("<p>Some <b>text</b>.</p>");
cp.add(editor);
```

!demo(to.etc.domuidemo.pages.components.editors.HtmlEditorPage.ui, 100%, 560)

[TOC]

## Making one

| Constructor | What it gives |
| --- | --- |
| `HtmlEditor()` | the editor at its default size |
| `HtmlEditor(int cols, int rows)` | ...sized as a textarea would be |

It **extends `TextArea`**, which is more than a detail: the wysiwyg is a jQuery
plugin drawn over a textarea, and everything a textarea can be told - the size,
`setReadOnly()`, `setDisabled()`, `setMandatory()`, `setOnValueChanged()`, data
binding - works unchanged. `setWidth()` and `setHeight()` size it in css.

| Method | What it does |
| --- | --- |
| `setValue(String)` / `getValue()` | the html; null empties the editor |
| `setStyleSheet(String)` | the stylesheet the *content* is rendered with, inside the editor |

## The buttons it has

The set is fixed - it is not configurable from Java - and it is deliberately
short: **bold, italic, strikethrough, underline, highlight**, the four
alignments, indent and outdent, subscript and superscript, undo and redo, a
numbered and a bulleted list, a horizontal rule, a table, a "code" view and
remove-formatting.

What it deliberately does **not** have: links, images and headings. Those are
switched off in the component.

## Why it exists

It shows itself immediately. The [`CKEditor`](../ckeditor/index.md) next to it
can do far more, and takes a visible moment to start - long enough to notice on a
screen where the editor is one field among many.

So the rule of thumb is the size of the job: a remark, a description, a note gets
this one; a screen whose whole purpose is writing a document gets the big one.

## What comes out

A string of html, written by a user - so it is filtered on the way out, not
trusted. [`DisplayHtml`](../../50-display-only/displayhtml/index.md) is the
component that shows it again and sanitises it while doing so.
