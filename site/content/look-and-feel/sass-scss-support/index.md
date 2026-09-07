---
menu:
  sort: "50"
---
# SASS/SCSS support

DomUI stylesheets are written in SCSS, and the framework's own theme - `winter` -
is a set of SCSS fragments. Nothing compiles them ahead of time: a request for a
`.scss` or `.sass` file is compiled by the server on the spot and answered as
`text/css`, so a saved change is visible on the next reload.

[TOC]

## Parameters from outside the stylesheet

SASS has variables, and DomUI can set them from the outside. A stylesheet that
wants them imports a file that does not exist:

```scss
@import "_parameters";
```

`_parameters.scss` is generated per request, and holds a `$name: value;` line
for each variable the framework has for this stylesheet. There are two sources
for them.

### From the URL

Any parameter on the stylesheet's own URL becomes a variable:

| In the URL | In `_parameters.scss` |
| --- | --- |
| `&xmas=true` | `$xmas: true;` |
| `&header$=bg1.png` | `$header: "bg1.png";` |

A name ending in `$` marks a **string**: the dollar is stripped from the name
and the value is quoted. Everything else is copied verbatim, which is what you
want for numbers, colours and booleans. An empty string value is skipped
entirely rather than written as `""`.

Names starting with `__` are skipped, and names starting with `$` never arrive -
those are DomUI's own request parameters, and the part factory drops them before
the stylesheet sees them.

Remember to url-encode when building the link: the dollar in `header$` has to be
written `%24`.

### From the application

```java
setThemeProperty("brand-color", "#c00040");
```

`DomApplication.setThemeProperty(name, value)` sets a variable for every theme
and every stylesheet, which is the place for something an application decides
once - a house colour, a logo, a width. A value that starts with `$` is written
as a quoted string, with the dollar removed; that is the escape for a value that
must not be read as SASS.

For a variable that depends on the request rather than being fixed - the logged
in user's organisation, say - register an `IThemeVariablesCalculator` with
`setThemeVariablesCalculator()`. Its `calculate(parameters)` is called for each
compile, and what it returns is merged over the fixed properties.

!! Compiled stylesheets are cached, and **the cache key is the full URL,
!! parameters and all**. Every distinct set of parameters is a separate compile
!! and a separate cache entry, so parameters must come from a small fixed set.
!! One parameter per user is a memory leak with extra steps.

## How it is compiled

`SassPartFactory` handles every request whose path ends in `.scss` or `.sass`.
It is a *buffered* part factory, which is where the caching comes from, and it
asks `SassCompilerFactory` for a compiler.

The compiler is **jsass**, a Java wrapper around the native libsass library. It
is the only one registered; `SassCompilerFactory` keeps a list and takes the
first that reports itself available, so an application can register an
`ISassCompiler` of its own and have it used instead.

File references inside a stylesheet do not reach the file system. A resolver
maps them onto DomUI webapp resources - the same lookup that serves everything
else, so a fragment can live in a jar - and it is that resolver which answers
`_parameters.scss` with the generated text.

## Two SASS things worth knowing

### Partials

A file whose name starts with an underscore is a **partial**: a file meant only
to be imported, never compiled on its own. That convention exists for the
standalone SASS compilers, which watch a directory and compile everything in it;
the underscore tells them to skip the file.

DomUI compiles only what is asked for, so partials mean nothing to it. The
convention is kept anyway, because it keeps the option of compiling the same
sources statically with an ordinary SASS toolchain.

### @import is include

`@import` is not what other languages call import - it is **include**. The
imported source is copied in at the point of the import, every time:

`_file1.scss`:

```scss
position: absolute;
```

`file2.scss`:

```scss
@import "file1";
@import "file1";
@import "file1";
```

gives

```css
position: absolute;
position: absolute;
position: absolute;
```

So a fragment that *produces css* must be imported once, while a fragment that
only *defines* things - variables, mixins, functions - must be imported by every
fragment that uses them, and costs nothing when it is. That is the rule to
organise by: put variables, mixins and functions in fragments of their own, and
import those wherever they are needed. Doing so also stops the IDE complaining
that a variable comes from a file that was never imported.
