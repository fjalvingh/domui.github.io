---
menu:
  sort: "70"
---
# Testing

A DomUI screen is tested by driving a browser: the test opens a page in Chrome,
types, clicks, and looks at what the browser shows. The framework for that -
`AbstractWebDriverTest`, the `WebDriverConnector` around Selenium, the page
object proxies and the generator that writes them - ships with DomUI and is
what your application uses too.

The pages those tests drive live **in the demo application**, next to the
tutorial and the component demos, and that is deliberate: they test the
framework, and they are at the same time the worked examples of how a page is
made testable. Every code fragment in this section comes from a page and a test
that are in the repository and that you can run.

- [Writing a UI test](10-writing-a-ui-test/index.md) - a test that opens a
  page, fills a form, clicks and asserts; testids and how components get one.
- [Running the tests](20-running-the-tests/index.md) - `IT` versus `Test`, the
  jetty that failsafe starts, the browser and driver you need, and the
  screenshot a failing test leaves behind.
- [Page objects](30-page-objects/index.md) - moving the selectors out of the
  test and into a class that describes the screen.
- [Generating page objects](40-generating-page-objects/index.md) - the page
  object generator: how to run it, the model it builds, and how to extend
  what it wrote.
- [The pages the tests drive](50-test-pages-in-the-demo/index.md) - the fixture
  pages in the demo application, what each group of them is for, and how to add
  one.
- [Testing what the DOM cannot tell you](60-rendering-tests/index.md) - reading
  the rendered pixels when the markup does not hold the answer.
- [Mockito pitfalls](70-mockito-pitfalls/index.md) - things that bite when
  mocking, in any Java test.
