---
menu:
  sort: "55"
---
# Moving an application to the module system

The theme is a set of Sass **modules**: every file loads what it needs with
`@use`, and sees nothing it did not load. An application whose stylesheets were
written for the earlier model - one global scope, filled by `@import` in the
order `style.scss` chose - has a handful of things to change. This page lists
them, file by file. Each is small; what changes is where a variable comes from.

[TOC]

## What does not change

- Where files go. `_custominit.scss` and `_userstyle.scss` still live in
  `src/main/webapp/themes/scss/winter/`, a webapp file still shadows a
  framework file of the same name, and a variant is still a directory holding
  the files it replaces.
- The variables. Every theme variable keeps its name and its meaning, and
  `_custominit.scss` sets them the same way.
- How a sheet reaches the page: `HeaderContributor.loadStylesheet()` and the
  `$THEME/` links are as they were.
- The compiler is Dart Sass either way; the same sheets compiled under it
  before this. What is new is that nothing it warns about is silenced any more.

## `_custominit.scss`

Plain `$name: value;` declarations, one per theme variable, as before:

```scss
$link-color: #c00040;
$font-size: 15px;
```

Two things to check:

- **Every name must be one the theme declares.** The file's variables are handed
  to the theme as its configuration, and a name the theme has no `!default` for
  is an error: *"$lnk-color was not declared with !default in the @used
  module"*. A line that was silently doing nothing - a typo, or a variable of an
  earlier theme version - now stops the compile. Remove it, or fix the name.
- **Nothing but declarations.** An `@import` here has no place to go, and a
  `!default` on a value is pointless. A value may be computed from a request
  parameter, by loading that module first:

  ```scss
  @use "parameters" as p;
  $link-color: p.$brand-color;
  ```

## `_userstyle.scss`

Add one line at the top, and change `@import` to `@use`:

```scss
@use "theme" as *;

@use "myclearabletext";
@use "reports";

.myapp-toolbar {
  background: $surface-bg;
  padding: $vertical-padding $horizontal-padding;
}
```

`theme` is the theme's module - its variables, functions and mixins for the
variant being compiled - and `as *` puts them in this file's namespace, so a
rule written before reads the same. Without that line every theme variable is
*undefined variable*.

The old `@import` came with the theme's functions in scope too. Of those,
`darken()`, `lighten()` and `saturate()` are Sass's own and are deprecated;
their replacements in `sass:color` do not clamp, so the theme provides
`darker()`, `lighter()` and `moreSaturated()`, which do and come with `theme`:

```scss
$my-panel-bg: lighter($primary, 40%);
```

## Partials of your own

Every partial that reads a theme variable or uses a theme mixin needs the same
first line:

```scss
@use "theme" as *;

.ui-mct-input {
  @include ui-input-base;
  border: 1px solid $bevel-up;
}
```

There is no global scope to inherit from any more: a partial that relied on
`_userstyle.scss` having imported `variables` before it, or on its own
`@import "derived-variables"`, has to load `theme` itself. Replace every
`@import` of a theme file with that one line, and every `@import` of a file of
your own with `@use`.

Two consequences of *loaded once*:

- A partial that produced css and was imported from two places produced its
  rules twice. Under `@use` it produces them once, where it is first loaded.
  If you relied on the second copy to win a cascade, order the `@use` rules so
  the first copy sits where you need it.
- A variable declared in one partial is not visible in another. Put shared
  values in a partial of their own and `@use` it from both.

## Sheets loaded with `HeaderContributor`

A sheet under `css/` that branches on the theme variant read `$themeVariant`
from `@import 'parameters'`. Now it loads the module and reads through its
namespace:

```scss
@use "parameters" as p;

@if p.$themeVariant == "dark" {
  .dm-banner { display: none; }
}
```

Each file that reads a parameter loads the module itself - a partial does not
see what the sheet that loaded it loaded. `!global` on a variable assigned
inside an `@if` is not needed: Dart Sass assigns to the file-level variable.

The same sheet can read the theme's variables, which it could not before:
`@use "theme" as *;` works from anywhere, and resolves to the variant the sheet
is being compiled for.

## `setThemeProperty()`, the calculator and URL parameters

These are a sheet's **parameters**: values it reads as `p.$name`. They no longer
set a theme variable by having the same name. An application that used
`setThemeProperty("link-color", ...)` to recolour the theme makes the
connection in `_custominit.scss` instead:

```scss
@use "parameters" as p;
$link-color: p.$link-color;
```

which is one line per variable, and makes the file say which parameters drive
the theme.

## A variant of your own

A variant directory used to hold a `_color.scss` of plain `!default`
declarations that won by being loaded first. It now *configures* the two
variable modules, which is `@forward ... with`:

```scss
// themes/scss/winter/high-contrast/_color.scss
@forward "variables" with (
	$black:      #000 !default,
	$white:      #fff !default,
	$line-color: #000 !default,
	$link-color: #0000ee !default,
);
@use "variables" as v;
@forward "derived-variables" with (
	$dt-hdr-bg: v.$black !default,
	$pmnu-bg:   v.$white !default,
);
```

Each variable goes in the clause of the file that declares it - `_variables.scss`
or `_derived-variables.scss`; the compiler tells you when one is in the wrong
clause - and keeps its `!default`, so that `_custominit.scss` still wins over
the variant. A value in the second clause that needs one from the first reads
it as `v.$name`. Trailing commas are fine. The shipped `dark/_color.scss` is a
complete example.

## A copy of a framework partial

A webapp file that shadows one of the theme's partials - a copy of
`_datatable.scss` with an edit - has to be brought to the new form: the
`@use "theme" as *;` header, and no `!default` declarations, which the theme
keeps in `_derived-variables.scss`. Better, now as before, is to not have the
copy: set the component's variables in `_custominit.scss`, or add your rules
in `_userstyle.scss`.

## Finding what is left

Reload the page. A sheet that does not compile fails the request with the
compiler's message, which names the file, the line and the construct; the
first error hides the ones after it, so go round until the sheet compiles.
Then look at the log: every deprecated construct that still compiles - an
`@import`, a `darken()`, a `/` used as division, `map-get()` and the other
global functions - is logged at warn level under
`to.etc.domui.sass.DartSassCompiler`, with the same file and line. Sass's
[migrator](https://sass-lang.com/documentation/cli/migrator/) does the
mechanical part of the last group.
