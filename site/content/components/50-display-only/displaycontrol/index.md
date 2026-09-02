---
menu:
  sort: "20"
---
# DisplayControl

`DisplayControl<T>` is [`DisplaySpan`](../displayspan/index.md) as a div: the
same value handling, wrapped so that it lines up with the input controls around
it in a form.

```java
DisplayControl<String> title = new DisplayControl<>(String.class);
title.setValue("Rubber Soul");

FormBuilder fb = new FormBuilder(cp);
fb.label("Album title").control(title);
```

!demo(to.etc.domuidemo.pages.components.display.DisplaySpanPage.ui, 100%, 700)

[TOC]

## The difference

Everything on the [`DisplaySpan`](../displayspan/index.md) page applies here:
the same six-step rendering order, the same `setConverter()`, `setRenderer()`,
`setEmptyString()` and `defineFrom()`, the same
`IDisplayControl<T>` contract.

What differs is the element and the css:

| | `DisplaySpan` | `DisplayControl` |
| --- | --- | --- |
| renders | a `<span>` | a `<div class="ui-dspctl">` with a span inside it |
| flows | with the text around it | as a block of its own |
| in a form | sits where the text sits | lines up with the input boxes |

Use `DisplayControl` in a form where some fields are editable and others are
not, so the read-only ones share the baseline and the left edge of the inputs
beside them. Use `DisplaySpan` anywhere the value is part of something else.
