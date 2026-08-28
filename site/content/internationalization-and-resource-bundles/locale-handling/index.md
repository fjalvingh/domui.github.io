# Locale handling

TBD

<a id="determining-the-locale-for-a-request"></a>

## Determining the locale for a request

The NlsContext.getLocale() call returns the locale that should be used. But how is that value found?

By default DomUI looks at the HttpRequest and determines the locale from its getLocale() method. This method uses the browser's preferred language setting to determine the locale, so by default *DomUI uses the preferred locale as defined in the user's browser settings*.

There are two ways to override the locale settings:

- By passing the parameter \_\_locale=en\_US to the URL (or post values) you force the locale for this request to be en\_US.
- By overriding the method getRequestLocale in DomApplication you can define the locale for each request by yourself. For instance, to force all requests to use the Dutch locale add this to your Application class:
```
@Nonnull @Override public Locale getRequestLocale(HttpServletRequest request) {
   return DUTCH;
}
```

Currency locales
