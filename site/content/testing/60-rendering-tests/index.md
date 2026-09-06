# Testing what the DOM cannot tell you

Most tests can be answered from the DOM: a class was added, a value changed, a
node appeared. Some cannot. When a component is drawn by javascript, or the
question is *what colour is it*, the only honest source is the picture the
browser drew.

[TOC]

## Reading the pixels

```java
ScreenInspector inspector = wd().screenInspector();
if(null == inspector)
	throw new IllegalStateException("This browser cannot take screenshots");

BufferedImage bi = inspector.elementScreenshot("t20");
Assert.assertTrue("The field should be red because it is in error", TestHelper.isReddish(bi));
```

`screenInspector()` takes a screenshot of the whole page and hands back an
object that can cut a single element out of it: Selenium knows the position and
the size of every element, so `elementScreenshot()` is a crop of the page
image. `ScreenInspector.getMostUsedColors()` then reduces that crop to the
colours it is mostly made of, which is how `isReddish()` in the demo's tests
decides that a field is showing its error state.

Checking the css class instead would prove less: a class can be there while a
stylesheet, a javascript or a more specific rule keeps the colour from
appearing.

## The case it was written for

The `HtmlEditor` is a `TextArea` that the editor's javascript **replaces** with
a set of elements, an `iframe` among them. When DomUI marks the control as
being in error it adds `ui-input-err` to the textarea - which is no longer
visible, so the user sees nothing. The fix was extra javascript that puts the
error mark on the elements the editor made; the test that keeps it working is
`ITTestHtmlEditorComponent`:

- open `HtmlEditorTestPage`, which has two mandatory editors, one of them
  empty, and a validate button that calls `bindErrors()`;
- click validate, find the editor's `iframe`, screenshot that element and
  assert that its dominant colour is reddish;
- refresh the page and assert it again, because the error state has to survive
  a full re-render.

## Screenshots of failures

Every UI test that fails leaves a screenshot in the module's
`target/failsafe-reports`, named after the test:

```
to.etc.domui.demo/target/failsafe-reports/ITOrderEntry_orderingSaysWhatWasOrdered.png
```

A test can also take one itself, at a moment it chooses:

```java
snapshot("after pressing order");
```

!! Chrome only screenshots the part of the page that is in the viewport. DomUI
!! carries its own screenshot helper for Chrome that stitches a full-page image
!! together, so element crops of things below the fold work - but it is worth
!! knowing that this is the one place where the browser being driven changes
!! what a test can see.
