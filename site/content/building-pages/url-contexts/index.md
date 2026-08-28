---
menu:
  sort: "50"
---
# URL Contexts

A DomUI page in an URL is referred to by its fully qualified class name, followed by the page extension (usually .ui). This page name is usually just added to the web application's root URL. So for a web application with the base URL

> [https://etc.to/master/](https://etc.to/master/)

a typical page URL would look like

> [https://etc.to/master/to.etc.portal.definitions.DefinitionListPage.ui](https://etc.to/master/to.etc.portal.definitions.DefinitionListPage.ui)

The full class name here is of course to.etc.portal.definitions.DefinitionListPage.

Since 2.0 it is also possible to refer to a page using a "directory structure" before the class name, so the above could also be:

> [https://etc.to/master/microsoft/legal/to.etc.portal.definitions.DefinitionsListPage.ui](https://etc.to/master/microsoft/legal/to.etc.portal.definitions.DefinitionsListPage.ui)

The part of the URL before the page name and after the webapp root is called the **URL Context String** or **URL Context.**

If the class name is present in the "root" URL of the application we say that the page is in the "root URL context"; the context string is the empty string. For the second example the context URL string is "microsoft/legal/"; the context URL ALWAYS ends in a slash except when the page is in the webapp root. This makes it easy to reconstruct URLs.

Pages *can* use the URL context if wanted. The URL context usually has no effect on the page unless the page uses the context to change its behavior (see below). There is one thing to watch out for though: if you have written components yourself and those components use relative paths to web resources then those components need to be changed to render those paths as absolute paths so that the resources can be found regardless of where the page is started from.

<a id="using-an-url-context"></a>

## Using an URL Context

There are two ways to use an URL context:

- By retrieving it from the request with a call to UIContext.getRequestContext().getUrlContextString(). The nonnull return can then be used to somehow change what you do inside the page. This is very simple, and by using base classes for pages you can share the actions taken for the context.
- By defining an IUrlContextDecoder and registering it in DomApplication (setUrlContextDecoder).

The IUrlContextDecoder interface has the following method:

```
Map<String, Object> getContextValues(@NonNull String urlContextString);
```

It is supposed to "decode" the URL string and put the different parts in the map as name, value pairs. These name, value pairs will then be automatically *injected* into pages that have properties that are annotated with @UIUrlContext.

Say for instance that we define that the URLContextString has two parts:

- An organisation name
- A department

We can write an URL decoder that decodes this into Java types:

```
public class MyUrlContextDecoder implements IUrlContextDecoder {
  Map<String, Object> getContextValues(@NonNull String urlContextString) {
    String[] values = urlContextString.split("/");
    if(values.length != 2)
      return null;    // null means: no values available
  }
  Organisation org = findOrganisationByName(values[0]);
  if(null == org)
    throw new IllegalStateException("Organisation not found");
  Department dep = findDepartmentByName(org, values[1]);
  Map<String, Object) map = new HashMap<>();
  map.put("organisation", org);
  map.put("department", dep);
  return map;
}
```
