---
menu:
  sort: "40"
---
# SPI Pages and DomUI logins

The DomUI login process is quite complex because it has to work for both normal pages and SPI pages. The latter are a big problem because the actual target we want to go to is not present in the URL that is sent from the browser: it comes from the url fragment (the part after the # in an url), and this URL fragment is not sent by the browser.

<a id="basic-login-process"></a>

# Basic login process

The basic login process works as follows:

- A page is accessed through some URL (either normal or SPI), and requests (requires) the currently logged in user using UIContext.getLoggedInUser().
- The code detects that no one is logged in by checking all possible locations where a logged in user can hide (usually in the HttpSession).
- Because there is no logged in user the code throws NotLoggedInException. This exception is created with the full URL of the original page, including all parameters, as a string.
- The exception is caught by whatever process is running (full page build or delta build), which now knows we need to log in.
- The code asks for the registered ILoginDialogFactory, and asks for the login RURL. This call gets passed the original URL that came from the exception. The new URL should be the URL for the login page, and enough information should be provided for this login page so that it can find back the original target URL. The default example pages encode this original URL as the "target=" parameter for the new login page.
- The login page does whatever is needed to have the user login.
- If login is successful the login page uses the target= parameter to get back the original target, then redirects to there.
- Because the user is now logged in the original page will render.

This process is not too complex for "normal" pages, as all information is encoded in target URL: both the target page name and all parameters. But for a SPI page we are in trouble.

<a id="how-spi-pages-work"></a>

## How SPI pages work

<a id="url-fragment-processing"></a>

### Url fragment processing

When an URL for a SPI page is sent to/entered in the browser this always contains two parts:

- The SpiPage's URL or name. This is the actual "Page" that hosts all Spi fragments. This page consists of one or more SpiContainers, each with an unique name.
- The Spi fragment identifiers for each SpiContainer, encoded in the Url Fragment (the thing after the #).

Only the browser "sees" the entire URL entered. But it only sends the URL part, not the fragment, to the server. This means the server does not know the value of the #fragment at all- and so it cannot define what content must be present in the SpiContainers.

To get the content that is desired DomUI uses the only trick possible: as soon as an SpiPage is loaded a piece of Javascript in there will obtain the value of the #urlFragment (by getting window.location.hash). It will then send an asynchronous request back to the server with that hash, and this request (handled in PageRequestHandler.loadSpiFragments) will then decode that hash and load all of the SpiContainers in on the page with the content defined in that hash.

It is quite easy to "lose" the hash while processing, because it is not seen by the server. So there are some special adaptions for SPI pages in the DomUI code.

The first adaption is in the code that sends redirects. DomUI uses redirects to move to different pages, but also when an URL does not contain a $cid or if it contains an invalid $cid. For such a case DomUI generates a new and valid $cid, and then sends a redirect back to the exact same URL (both URL and query string) that it received before, but now with the $cid parameter added. The browser will then do a new request to this url - and this time we can build the page because the session is known.

But there is a problem here: when the redirect is sent we do not know the #urlFragment- so the new URL would be incorrect!

To fix this we use a trick. The redirect that is sent is not a normal HTTP redirect (304 or something), but instead we send a small HTML document containing Javascript. The javascript calls "location.replace()", passing in the new URL that we want to go to. And because this runs on the browser we can now use a trick: we send the following Javascript:

```
location.replace("https://xxxx/blabla.ui?parameters=xxxxxx&pp=yy" + location.hash)
```

This nicely appends the current #urlFragment to the new URL.

This first part means that the basic DomUI redirect for an initial page works properly: the redirect URL gets adjusted on the browser side to include the original hash.

<a id="rendering-spi-pages"></a>

### Rendering SPI pages

A SPI page registers one or more containers: places inside the page where content is to be shown, depending on the #urlFragment data. Each container has a (mandatory) name: a short name which is used in the urlFragment to target that container.

The urlFragment can have data for multiple containers; it should have a fragment rurl for every container in the SpiPage.

The UrlFragment has the following format:

```
urlFragment ::= '#' container-url { ';' container-url }*
container-url ::= { container-name ':' }? fragment-rurl
container-name ::= IDENTIFIER
fragment-rurl ::= urlencoded-string
```

When an URL (possibly containing an URL fragment) is entered in the browser only the real URL part is sent to the server, the #urlFragment remains. If the URL is indeed a SPI page then the page gets loaded as usual, and in the process the page registers all its SpiContainers. Each container also defines a "default content", but after registration all container parts remain completely empty (the default content is not loaded). This means that the initial page sent back to the browser is only the SpiPage, the containers are empty.

As part of that rendered page DomUI also sends a Javascript command that causes the browser to send back a call with the value for the #urlFragment known by the browser. This call is handled by PageRequestHandler.loadSpiFragment. If the hash passed is empty then this call loads all SpiContainers with the "default content" for each container. But if there is hash data it gets split into the different container-url parts, and for each container present in the fragment the appropriate fragment gets loaded.

<a id="logging-in-for-spi-pages"></a>

## Logging in for SPI pages

The login process for SPI pages also needs extra attention. When the originating SPI page throws an exception the server code might not yet have seen the asynchronous request with the hash. So we need some tricks to get to that url.

The page that requires the login throws the NotLoggedInException. This only contains the path for the spi page - no fragment, so for instance *http://www.test.nl/portal/?$cid=xxx*.

The exception handler now constructs the URL for the actual login page, and adds the "target=http://www.test.nl/portal?cid=xxx" as a parameter (in reality it is properly url encoded of course). It then sends a redirect to the login page - and it keeps the #urlFragment that was present on the original page in the redirected URL because it uses the same trick as above. So the login page has both the target= parameter AND the #urlFragment as a fragment in the browser.

The login handler, as usual, does the login and if successful redirects back to the originating page - with the same trick, so now the originating page sees its own fragments and can initialize as usual.
