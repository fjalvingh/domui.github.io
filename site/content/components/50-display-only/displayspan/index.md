---
menu:
  sort: "10"
---
# DisplaySpan

`DisplaySpan<T>` shows a value of any type as a span. It works out how to render
the value itself, which is what makes it the display counterpart of a
[`Text2`](../../10-text-and-value-input/text2/index.md).

```java
DisplaySpan<BigDecimal> price = new DisplaySpan<>(BigDecimal.class);
price.setConverter(ConverterRegistry.getConverterInstance(MoneyBigDecimalFullConverter.class));
price.setValue(new BigDecimal("14.95"));

FormBuilder fb = new FormBuilder(cp);
fb.label("Price").control(price);
```

!demo(to.etc.domuidemo.pages.components.display.DisplaySpanPage.ui, 100%, 700)

[TOC]

## How it decides what to show

`createContent()` tries, in this order, and stops at the first that works:

1. the **converter**, when one is set - it *must* convert the value;
2. the **renderer**, when one is set - it may put anything at all inside the
   span, and is asked even for a `null` value;
3. the **empty string** when the value is `null`;
4. the **default converter** for the value's own class, from the
   `ConverterRegistry`;
5. the **domain label** when the value has domain values - an enum or a boolean
   gets its metadata label;
6. failing all that, the class's default renderer, which ends at `toString()`.

That order is why a `DisplaySpan<Date>` shows a properly formatted date without
being told anything, and why an enum shows its label rather than its constant
name.

| Method | What it does |
| --- | --- |
| `setValue(T)` / `getValue()` | the value; setting it rebuilds the span |
| `setConverter(IConverter<T>)` | convert the value to text yourself |
| `setRenderer(IRenderInto<T>)` | build the content yourself |
| `setEmptyString(String)` | what to show for a `null` value - nothing at all by default |
| `defineFrom(PropertyMetaModel)` | take the hint and, for a number, the numeric converter from a property |

!! A converter and a renderer cannot both be set: `setRenderer()` on a span that
!! already has a converter throws. Clear the converter first.

## Constructors

| Constructor | Use it for |
| --- | --- |
| `new DisplaySpan<>(Class<T>)` | the usual case: the type, no value yet |
| `new DisplaySpan<>(Class<T>, T)` | the type and its first value |
| `new DisplaySpan<>(PropertyMetaModel<T>)` | configured from a property, through `defineFrom()` |
| `new DisplaySpan<>(T literal)` | a value whose class speaks for itself |

## What it renders

A `<span>` with the text in it, and nothing else - no wrapper, no control class.
That is what makes it right inside running text, inside a table cell, or next to
another value. When it has to line up with the input controls in a form, use
[`DisplayControl`](../displaycontrol/index.md) instead.
