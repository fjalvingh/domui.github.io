---
menu:
  sort: "60"
---
# Header contributors

A **header contributor** puts something in the `<head>` of the rendered page: a
stylesheet, a script, a piece of javascript. It exists because a component
cannot write into the head itself - the head is rendered before the body the
component lives in - and because fifteen components needing the same script
should still produce one `<script>` tag.

```java
//-- In an IApplicationInitializer, for every page of the application:
da.addHeaderContributor(HeaderContributor.loadStylesheet("css/font-awesome.min.css"), 10);

//-- In a component, for the page it is on:
getPage().addHeaderContributor(HeaderContributor.loadJavascript("$js/aceeditor-1.4.13/ace.js"), 10);
```

[TOC]

## The two places to add one

| Added to | Lives for | Added from |
| --- | --- | --- |
| `DomApplication.addHeaderContributor(hc, order)` | every page of the application | `DomApplication.initialize()`, or an `IApplicationInitializer` |
| `Page.addHeaderContributor(hc, order)` | that one page | a component, from `onAddedToPage()` or `createContent()` |

At render time the two lists are concatenated and sorted by `order`, lowest
first, and each contributor is asked to write itself. The framework's own scripts
sit at large negative orders - down to -990 - so a contribution of your own with
a positive order lands after them. Equal orders keep the order they were added
in.

A component adds its contribution every time it is added to a page, and that is
correct: contributors compare equal when they contribute the same thing - the
same path, the same script text - and an equal one is dropped. That is the whole
reason `HeaderContributor` demands `equals()` and `hashCode()` from its
subclasses.

## What can be contributed

| Factory | What it renders |
| --- | --- |
| `loadStylesheet(name, options...)` | a `<link rel="stylesheet">`; the options are attribute name/value pairs, for `integrity` and `crossorigin` |
| `loadJavascript(name)` | a `<script src="...">` |
| `loadJavaScriptlet(text)` | a `<script>` with that text as its body |
| `loadThemedJavasciptContributor(name)` | a script that is run through the theme first, so it can use theme variables |
| `loadGoogleAnalytics(uacode)` | the Google Analytics snippet for that account code |
| `loadGoogleCharts()` | the Google Charts loader |

The name of a stylesheet or a script is a resource path, resolved the way every
other resource is:

- one starting with `THEME/` is resolved against the theme that is current for
  this request, so a themed script or stylesheet follows the theme;
- one starting with `$` is served by the internal resource part, which looks
  first in the webapp's own files and then on the classpath under `/resources/`
  - that is how a component reaches a script that ships inside a jar, as in
  `$js/aceeditor-1.4.13/ace.js`. For the `$js/` and `$ts/` prefixes there is one
  extra step: **outside development mode a `-min` sibling of the file is used
  when one exists**, so `$js/mylib/mylib.js` serves `mylib-min.js` in production
  and the readable file while developing, from the same reference;
- anything else is taken as webapp-relative;
- a name starting with `http` is left exactly as it is, which is how a CDN is
  used.

## Writing one

```java
final public class MyContributor extends HeaderContributor {
	@Override public void contribute(IContributorRenderer r) throws Exception {
		r.renderLoadCSS("css/mine.css");
		r.renderLoadJavascript("js/mine.js", false, false);
	}

	@Override public boolean isOfflineCapable() {
		return true;
	}

	@Override public int hashCode() {
		return MyContributor.class.hashCode();
	}

	@Override public boolean equals(Object obj) {
		return obj instanceof MyContributor;
	}
}
```

`contribute()` is handed an `IContributorRenderer` rather than the output
stream, so the same contributor works for a full page render and for a delta.
`isOfflineCapable()` says whether what it contributes can be written into a
saved, self-contained copy of the page.

The **equality is not optional**: two contributors that contribute the same
thing must be equal, or the page gets the same script twice. The factories above
already take care of it - `loadJavascript()` and friends keep one instance per
name and hand out that same instance - so a contribution that is just a file
needs no class of its own.

## A font as a worked example

The `fontawesome*` integration modules do exactly this, from an
`IApplicationInitializer` registered through `META-INF/services`:

```java
final public class FontAwesome6FreeInitializer implements IApplicationInitializer {
	@Override public void onStartInitialization(DomApplication da) {
		da.addHeaderContributor(HeaderContributor.loadStylesheet("css/font-awesome.min.css"), 10);
		FaIcon.initializeIcons();
		da.iconPackInitialized();
	}
}
```

One line puts the font's stylesheet on every page of any application that has
the module on its classpath; the rest of the module is the icon enum. Adding a
font of your own is described with
[the icons](../../components/100-images-and-icons/icons/index.md).
