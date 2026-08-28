---
menu:
  sort: "10"
---
# The body document (UrlPage)

All DomUI pages must extend UrlPage. This object forms the "body" element of the rendered page.

The UrlPage has a number of special attributes and methods compared with other nodes.

<a id="page-title-in-the-browser"></a>

### Page title in the browser

The page title in the browser (as sent by the <title> tag inside the <head> of the document) is defined by the title property of the UrlPage. This means that for UrlPage the title property is treated different than for other nodes, because on other nodes it forms the title *attribute*.

If no title is set on the UrlPage then it uses a generic term as defined by the method getDefaultPageTitle() inside DomApplication.
