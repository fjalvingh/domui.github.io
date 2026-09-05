---
menu:
  sort: "30"
---
# AceEditor

The [Ace](https://ace.c9.io/) code editor as a DomUI control: syntax colouring,
themes, code completion and markers, over a value that is plain text.

```java
AceEditor editor = new AceEditor();
editor.setMode("ace/mode/javascript");        // The language
editor.setTheme("iplastic");                  // The colour scheme
editor.setWidth("100%");
editor.setHeight("300px");                    // Without a size it does not show
cp.add(editor);
```

!demo(to.etc.domuidemo.pages.components.editors.AceEditorPage.ui, 100%, 800)

[TOC]

## Size, mode and theme

!! **Set a width and a height.** The editor draws itself into a `div` and cannot
!! work out how big that should be; without a size there is nothing to see.

| Method | What it takes |
| --- | --- |
| `setMode(String)` | the **full** path of the language: `"ace/mode/javascript"`, `"ace/mode/pgsql"`, `"ace/mode/java"` |
| `setTheme(String)` | the **bare name** of the theme: `"iplastic"`, `"monokai"`, `"eclipse"` |
| `setTabSize(int)` | how wide a tab is; 4 by default |
| `setWrapMode(AceWrapMode)` | `None`, `Wrap` or `IndentedWrap` |

!! The two are not written the same way, which is easy to get wrong: the mode is
!! given whole and the theme gets `ace/theme/` put in front of it. `"monokai"` is
!! the theme when none is set, `"ace/mode/javascript"` the mode.

## The value, and the selection

It is an `IControl<String>` whose value is the text being edited. On top of that:

| Method | What it does |
| --- | --- |
| `getSelectedText()` | what the user has selected - it arrives with every value change |
| `gotoLine(int)` / `gotoLine(int, int)` | move the caret to a 1-based line, and column |
| `select(line1, col1, line2, col2)` | select that range |
| `insertAtCursor(String)` | put text in where the caret is |
| `insertAt(String, row, column)` | ...or at a given position |

Changes are not sent on every keystroke: the editor waits half a second after
typing stops before telling the server, so `onValueChanged` fires per pause
rather than per character.

## Code completion

Set a handler and the editor asks it for possibilities when the user presses
**CTRL+SPACE**:

```java
editor.setCompletionHandler((text, row, col, prefix) -> complete(text, prefix));
```

The handler is given the whole text, the caret's row and column, and the word
typed so far, and returns a list of `AceEditor.Completion` - a name, the value to
insert, a "meta" label shown next to it, and a score that orders the list.

The prefix Ace works out contains identifier characters only, so it stops at a
dot: in `day.num` the prefix is `num`. Two ways round that:

| Call | What it does |
| --- | --- |
| `setPrefixAllowDotted()` | treat `.` as part of the prefix |
| `setPrefixPredicate(Predicate<Character>)` | say for yourself which characters belong to it |
| `getDottedPrefix(row, col, predicate)` | work the prefix out from the text yourself |

## Markers

A marker underlines a range of the text and hangs a message on it - what a
compiler's errors and warnings look like in an editor:

```java
editor.markerAdd(MsgType.WARNING, line, col, endLine, endCol, "Use 'let' instead of 'var'");
```

| Method | What it does |
| --- | --- |
| `markerAdd(MsgType, line, col, endLine, endCol, message)` | a marker over that range; returns its id |
| `markerAdd(MsgType, line, col, endLine, endCol, message, css)` | ...with a css class of your own |
| `markerAdd(MsgType, startPosition, endPosition, message)` | the same by character offset |
| `markerRemove(int id)` | one marker |
| `markerClear()` | all of them |

`PositionCalculator` is the helper that turns a character offset in the text into
the line and column the line-based calls want - which is what a parser that
reports offsets needs.

## Where the javascript comes from

Ace is served from the framework's own resources
(`$js/aceeditor-<version>/ace.js` and `ext-language_tools.js`), not from a
content delivery network. The editor registers those itself when it is built, so
a page that has one on it needs no setup; a page that adds an editor *later* -
into a tab that was not open, say - calls `AceEditor.initialize(this)` in
`createContent()` so the scripts are on the page before the editor arrives.
