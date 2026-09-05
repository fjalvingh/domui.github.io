---
menu:
  sort: "10"
---
# JUnit testing DomUI

Non-visual code can be JUnit tested as usual. But as a visual UI framework testing DomUI itself brings some challenges. While still a work in progress this is what is currently done to help with testing the visual and browser based aspects of DomUI.

<a id="selenium-based-testing"></a>

## Selenium based testing

The visual tests all use Selenium WebDriver to run tests. To run these we actually need two parts operational:

- A web server which runs the several DomUI pages under tests. Components are tested by creating special pages for them that exhibit the behavior we want to test. These pages are all present in the DomUI DEMO application (to.etc.domui.demo).
- A JUnit test runner which then runs a test. The test controls a browser using Selenium WebDriver, and uses Selenium tests written in Java to exercise the pages running on the web server.

The Maven build runs these tests as *Integration Tests*. These can be found automatically (by Maven) because the class names all start with **IT**, like ITHtmlEditorComponentTest. Them being Integration Tests means that they run only after all "normal" tests have run, and after the whole web application has been constructed. This works as follows:

- Maven does the normal build cycles until after *package*. This is the normal compile, and as part of it the per-module JUnit tests are executed as usual.
- After the package phase Maven starts a Jetty server with the to.etc.domui.demo web application deployed on it on port 8088.
- Now Maven locates all Integration Tests and runs them. These tests use localhost:8088 as the base URL and so connect to the Jetty server started by Maven.
- Once done Maven stops the Jetty server and reports the test results.

The browser to use is set with `webdriver.hub`, in `~/.test.properties` or as a `-D` property on the JVM; without it the tests run headless Chrome. That means Chrome and a matching chromedriver have to be present on the machine DomUI is built on:

- Install Chrome as usual.
- Install the chromedriver for that Chrome version - the [Chrome for Testing downloads](https://googlechromelabs.github.io/chrome-for-testing/) have both.
- Put the `chromedriver` binary in `/usr/local/bin`, `/usr/bin`, `~/bin` or `~`, which are the places the tests look, or name it with the `webdriver.chrome.driver` property.

<a id="using-headless-chrome"></a>

## Using Headless Chrome

The tests run in headless Chrome. `webdriver.hub` picks another browser: `chrome-desktop` for a Chrome you can watch, `firefox` for Firefox.

There are some issues with using chrome. The most important issue is that ChromeDriver/Chrome does not properly take screenshots. Unlike the other drivers chrome takes only partial screenshots of the page, and that breaks some tests and makes bugs harder to find.

To circumvent this issue the DomUI wrapper around WebDriver has a special implementation of the code that creates a screenshot for Chrome. [The code is described on Stackoverflow](https://stackoverflow.com/questions/45199076/take-full-page-screen-shot-in-chrome-with-selenium/46025126).

<a id="test-helper-base-classes"></a>

## Test helper base classes

The DomUI code wraps Selenium in a few helper classes that help with easier testing of DomUI code. See the provided JUnit tests for details. These classes are thin wrappers around WebDriver itself so missing functionality is easily added.

The base class to write Selenium tests is called AbstractWebDriverTest, and it handles everything to access a webdriver wrapper: just call wd() inside any test to get the proper WebDriver wrapper.

<a id="rendering-tests"></a>

## Rendering tests

A lot of tests can be written by just querying the DOM state as delivered by DomUI and its javascript during a test. These tests are all quite simple: just click on buttons, enter texts, then check the resulting DOM in the browser.

But there are tests that we cannot do with this. A good example is [the test for the HtmlEditor.](the-htmleditor-junit-tests/index.md) This component contains a lot of Javascript, and the actual DomUI node (a TextArea) actually gets replaced by an IFRAME by the editor's Javascript. Other tests require that a layout is fully correct, and that is also difficult to do with just DOM matching.

For this we can use Selenium's ability to take screenshots. Using screenshots of a rendered page we can load the screenshot, then use Selenium's knowledge of the *position* and *size* of a web page element to extract from the screenshot the *actual rendering of the component* as a bitmap. This bitmap can then be further analyzed.

<a id="failed-test-screenshots"></a>

## Failed test screenshots

The UI tests make a screenshot of every test that fails. They are written to \[module\]/target/failsafe-reports as classname\_testname.png, for instance:

```
display ./to.etc.domui.demo/target/failsafe-reports/ITTestLookupInput_testInitialLayout.png
```
