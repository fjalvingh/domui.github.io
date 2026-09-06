# URL contexts

A DomUI page is addressed by its fully qualified class name plus the page
extension, usually `.ui`, appended to the application's root URL:

> https://example.com/master/to.etc.portal.definitions.DefinitionListPage.ui

Anything **between the application root and the class name** is the
**URL context string**:

> https://example.com/master/microsoft/legal/to.etc.portal.definitions.DefinitionListPage.ui

Here it is `microsoft/legal/`. The page is the same page; the context is extra
information the URL carries into it.

[TOC]

## How it is split off

The framework takes the request path and looks for the last dot and the last
slash. What follows the slash and precedes the dot is the page name; what
precedes the slash is the context string. A page in the application root has the
empty string as its context, and a context string **always ends in a slash**
when there is one - which is what makes putting URLs back together easy.

A URL that is matched by the application's own URL mapping is not split this way
at all: the mapping decides what the page and its parameters are, and the
context string is empty.

The context normally does nothing. A page has to ask for it, in one of the two
ways below, before it changes anything.

!! A component that builds a *relative* path to a web resource breaks under a
!! context: the browser resolves it against the context, not against the
!! application root. Components must render absolute paths, so that they work
!! wherever the page is started from.

## Reading it directly

```java
String context = UIContext.getRequestContext().getPageParameters().getUrlContextString();
```

Never null - it is the empty string when there is no context - and a base class
for your pages is the natural place to act on it.

## Decoding it into typed values

The other way is to have the framework decode the context once and inject the
result into the pages that want it.

An `IUrlContextDecoder` turns the context string into named values:

```java
public class MyUrlContextDecoder implements IUrlContextDecoder {
	@Override public Map<String, Object> getContextValues(String urlContextString) {
		String[] values = urlContextString.split("/");
		if(values.length != 2)
			return null;                    // null: this context has no values

		Organisation org = findOrganisationByName(values[0]);
		if(null == org)
			throw new IllegalStateException("Organisation not found: " + values[0]);
		Department dep = findDepartmentByName(org, values[1]);

		Map<String, Object> map = new HashMap<>();
		map.put("organisation", org);
		map.put("department", dep);
		return map;
	}
}
```

It is registered on the application:

```java
setUrlContextDecoder(new MyUrlContextDecoder());
```

A page then declares what it wants with `@UIUrlContext` on a **setter**:

```java
@UIUrlContext
public void setOrganisation(Organisation org) {
	m_organisation = org;
}
```

The injector calls the decoder once per request, and gives each annotated setter
the first value from the map whose **type fits** that setter's parameter. The
names in the map are not matched against property names - the type is what
decides - so two setters wanting the same type is not something this can
express.

What is missing is an error:

- a page with a `@UIUrlContext` setter reached through a URL that has no context
  string throws `UrlContextUnknownException`;
- so does a setter for which the decoder returned no value of that type.

`@UIUrlContext(optional = true)` turns both of those into "leave the property
alone", for a page that works with and without a context.

The default decoder returns `null` for everything, so nothing is injected until
an application registers one of its own.
