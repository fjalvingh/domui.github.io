---
menu:
  sort: "70"
---
# EmbeddedCode

`EmbeddedCode` shows a piece of code as code.

```java
cp.add(new EmbeddedCode("SELECT * FROM Album WHERE title ilike '%rock%'"));
```

!demo(to.etc.domuidemo.pages.components.display.RulerPage.ui, 100%, 620)

The whole component is a div with the class `ui-embcd` and one span holding the
text, so what it looks like is entirely the theme's business. The text is added
as text: it is escaped, not interpreted, so code containing `<` and `&` shows as
written.

It does not highlight anything. For highlighted, editable code the component is
the [AceEditor](../../110-editors/aceeditor/index.md); for showing html *as
html* it is [`DisplayHtml`](../displayhtml/index.md).
