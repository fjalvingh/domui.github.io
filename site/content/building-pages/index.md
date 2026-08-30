---
menu:
  sort: "30"
---
# Building pages

A DomUI application is a set of pages, each of them a Java class. This section
describes the page model itself: what a page is, how its state and lifetime are
managed, how it is addressed in an URL, and how it is translated.

- [Building your first page](10-first-page/index.md) - what a page is, how its
  class name becomes an URL, and what `createContent()` does, in three small
  examples.
- [Using components](20-using-components/index.md) - what a component is, the
  state every input control has, how `getValue()` reports bad input and how a
  control reports a change.
- [Using databases](30-using-databases/index.md) - `QCriteria` as the question
  and `QDataContext` as the thing that runs it, restrictions and combinators,
  and querying over a relation.
- [Typed properties](40-typed-properties/index.md) - replacing the property
  strings in a query with generated, compile-time checked ones.
- [Data binding](50-data-binding/index.md) - letting a control and a model
  property follow each other, which way each kind of binding moves, and what
  `bindErrors()` is for.
- [Page navigation](60-page-navigation/index.md) - what a page keeps between
  requests, how `UIGoto` moves to another one, and the shelf of pages that the
  breadcrumb is made of.
- [Showing rows](70-showing-rows/index.md) - the model, the RowRenderer and the
  DataTable, a search screen built on a SearchPanel, and why a list re-queries
  when you come back to it.
- [Metadata](80-metadata/index.md) - saying once, on the class, what every
  screen showing it needs to know: labels, limits, presentation - and
  translating all of it through DomUI's own resource bundles.
- [Telling something to a user](90-telling-the-user/index.md) - the message box,
  the message that stays on the page, the exception dialog, and the error fence
  that decides where a message is shown.
- [Layout](100-layout/index.md) - the panel a page's content sits in, the bar its
  buttons sit on, tabs - and how to make a piece of screen of your own that
  several pages can use.
- [Writing a component](110-writing-a-component/index.md) - a component is a
  class implementing `IControl`; what `AbstractDivControl` already does, when a
  control decides its value changed, and why `bindValue` is not `value`.
- [The body document (UrlPage)](../70-implementation-details/urlpage/index.md) - the root of every page.
- [State management](../70-implementation-details/state-management/index.md) - pages, conversations and the
  lifetime of the data a page works with.
- [SubPages](../99-todo/subpages/index.md) - the 2.0 single-page-interface building block.
- [SPI pages and DomUI logins](../99-todo/spi-pages-and-logins/index.md) - single page
  interface applications and their login handling.
- [URL contexts](../99-todo/url-contexts/index.md) - how a page class becomes an URL.
