---
menu:
  sort: "30"
---
# Building pages

A DomUI application is a set of pages, each of them a Java class. This section
describes the page model itself: what a page is, how its state and lifetime are
managed, how it is addressed in an URL, and how it is translated.

- [Building your first page](../building-pages/10-first-page/index.md) - what a page is, how its
  class name becomes an URL, and what `createContent()` does, in three small
  examples.
- [Using components](using-components/index.md) - what a component is, the
  state every input control has, how `getValue()` reports bad input and how a
  control reports a change.
- [The body document (UrlPage)](urlpage/index.md) - the root of every page.
- [State management](state-management/index.md) - pages, conversations and the
  lifetime of the data a page works with.
- [SubPages](subpages/index.md) - the 2.0 single-page-interface building block.
- [SPI pages and DomUI logins](spi-pages-and-logins/index.md) - single page
  interface applications and their login handling.
- [URL contexts](url-contexts/index.md) - how a page class becomes an URL.
- [Internationalization and resource bundles](internationalization/index.md) -
  translating an application, and [locale handling](internationalization/locale-handling/index.md)
  per request.
