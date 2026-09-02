---
menu:
  sort: "60"
---
# PercentageCompleteRuler2

`PercentageCompleteRuler2` is a bar showing how far something got, with the
percentage written in it.

```java
PercentageCompleteRuler2 ruler = new PercentageCompleteRuler2();
ruler.setWidth(300);
ruler.setValue(35.0);
```

!demo(to.etc.domuidemo.pages.components.display.RulerPage.ui, 100%, 620)

[TOC]

## The API

| Method | What it does |
| --- | --- |
| `setValue(Double)` / `getValue()` | the percentage; **clipped** to 0..100 rather than refused, and `null` shows an empty bar |
| `setWidth(int pixels)` / `setHeight(int pixels)` | the size of the bar - the width is used to compute the filled part, so set it in pixels |
| `setShowPercentage(boolean)` | write the number in the bar; on by default |
| `setPercentageColor(String)` | the colour of that text |
| `setPercentageClass(String)` | a css class for it instead |
| `getBar()` | the filled `Div` itself, for a style binding |

The number is written as one decimal (`35.0 %`).

## What it renders

```html
<div class="ui-pct-rlr2" style="width:300px">
    <div class="ui-pct-rlr2-bar ui-rlr2-pct-35" style="width:105px"></div>
    <div class="ui-pct-rlr2-txt" style="width:300px">35.0 %</div>
</div>
```

The bar is a div whose width is the fraction of the total, with the text laid
over it. It also gets a css class naming its **rounded percentage**
(`ui-rlr2-pct-35`), which is how a theme can give particular values a look of
their own - the shipped theme only styles `ui-rlr2-pct-100`, so a finished bar
can be shown as finished.

`getBar()` exists for the other way of doing that: bind a style to the bar and
let the model decide its colour.
