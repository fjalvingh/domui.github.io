---
menu:
  sort: "50"
---
# SASS/SCSS support

DomUI stylesheets are written in SCSS, and the framework's own theme - `winter` -
is a set of SCSS modules. Nothing compiles them ahead of time: a request for a
`.scss` or `.sass` file is compiled by the server on the spot and answered as
`text/css`, so a saved change is visible on the next reload.

[TOC]

## Parameters from outside the stylesheet

SASS has variables, and DomUI can hand a stylesheet some from the outside. They
arrive as a module called `parameters`, which does not exist as a file:

```scss
@use "parameters" as p;

.dm-banner {
  display: if(p.$themeVariant == "dark", none, block);
}
```

The module is generated per request and holds a `$name: value;` declaration for
each variable the framework has for this stylesheet. `$themeVariant` is always
there: the name of the theme variant the sheet is being compiled for, which is
how an application sheet branches on dark and light. The rest comes from two
sources.

### From the URL

Any parameter on the stylesheet's own URL becomes a variable:

| In the URL | In `parameters` |
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

`DomApplication.setThemeProperty(name, value)` sets a variable for every
stylesheet, which is the place for something an application decides once - a
house colour, a logo, a width. A value that starts with `$` is written as a
quoted string, with the dollar removed; that is the escape for a value that must
not be read as SASS.

For a variable that depends on the request rather than being fixed - the logged
in user's organisation, say - register an `IThemeVariablesCalculator` with
`setThemeVariablesCalculator()`. Its `calculate(parameters)` is called for each
compile, and what it returns is merged over the fixed properties.

A parameter is a value a sheet *reads*; it does not set a theme variable by
having the same name. To turn one into a theme variable, declare it in
`_custominit.scss` - see [overriding the theme](../overriding-the-theme/index.md):

```scss
@use "parameters" as p;
$link-color: p.$brand-color;
```

!! Compiled stylesheets are cached, and **the cache key is the full URL,
!! parameters and all**. Every distinct set of parameters is a separate compile
!! and a separate cache entry, so parameters must come from a small fixed set.
!! One parameter per user is a memory leak with extra steps.

## The theme as a module

The other name the framework resolves for you is `theme`: the theme's own
module - its variables, functions and mixins, nothing that emits css - for the
variant the sheet is being compiled for.

```scss
@use "theme" as *;

.myapp-toolbar {
  background: $surface-bg;
  border-bottom: 1px solid $line-color;
  padding: $vertical-padding $horizontal-padding;
}
```

It works from anywhere: a partial inside the theme, your `_userstyle.scss`, or a
sheet of your own under `css/`. `as *` puts the members in your file's own
namespace, so a theme variable is written the way the theme writes it.

## How it is compiled

`SassPartFactory` handles every request whose path ends in `.scss` or `.sass`.
It is a *buffered* part factory, which is where the caching comes from, and it
asks `SassCompilerFactory` for a compiler.

The compiler is **Dart Sass**, the reference implementation, run as a separate
process and spoken to over the Sass embedded protocol; the processes are pooled
and closed when the application stops. The `dart-sass` binary comes bundled for
every common platform, and the developer option or system property
`domui.sass.executable` points at one installed on the machine instead.
`SassCompilerFactory` keeps a list and takes the first compiler that reports
itself available, so an application can register an `ISassCompiler` of its own
and have it used instead.

File references inside a stylesheet do not reach the file system. An importer
maps them onto DomUI webapp resources - the same lookup that serves everything
else, so a module can live in a jar, and a file in your webapp shadows one of
the same name in the framework - and it is that importer which answers
`parameters` and `theme`. Both are matched on the name alone, from whatever
directory the loading sheet is in, which also means a file of your own called
`_parameters.scss` or `_theme.scss` can never be reached.

Whatever the compiler has to say about a sheet is logged under
`to.etc.domui.sass.DartSassCompiler`: a `@warn` and a deprecated construct at
warn level, a `@debug` at info level, each as Dart Sass formats it - the message,
the source line with the offending token underlined, and the sheet's url and
line number. With DomUI's default logging that is standard output. An error
fails the request instead, with the same text in the `SassException`.

## Two SASS things worth knowing

### Partials

A file whose name starts with an underscore is a **partial**: a file meant only
to be loaded by another, never compiled on its own. That convention exists for
the standalone SASS compilers, which watch a directory and compile everything in
it; the underscore tells them to skip the file.

DomUI compiles only what is asked for, so partials mean nothing to it. The
convention is kept anyway, because it keeps the option of compiling the same
sources statically with an ordinary SASS toolchain.

### A module is loaded once

`@use` loads a file as a **module**: once per compilation, however many files ask
for it, and each file sees only what it loaded itself. A variable, function or
mixin defined in a module is reached through the module's namespace - the file's
name unless `as` says otherwise, or no prefix at all with `as *` - and a file that
does not `@use` a module sees nothing of it.

`_file1.scss`:

```scss
$edge: 1px solid #ccc;
.dm-box { border: $edge; }
```

`file2.scss`:

```scss
@use "file1";
@use "file1";

.dm-other { border: file1.$edge; }
```

gives

```css
.dm-box { border: 1px solid #ccc; }
.dm-other { border: 1px solid #ccc; }
```

One `.dm-box`, not two, and `$edge` only as `file1.$edge`. That is the rule to
organise by: a file that *produces css* is `@use`d from the one place its rules
belong in the output, and a file that only *defines* things is `@use`d by every
file that reads from it - which costs nothing, because it is still loaded once.
`@use` rules go at the top of a file, before any rule.

A module's `!default` variables can be set from outside, once, by whoever loads
it first: `@use "file1" with ($edge: 2px solid red)`. That is what
[overriding the theme](../overriding-the-theme/index.md) is built on.
