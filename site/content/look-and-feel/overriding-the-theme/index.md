---
menu:
  sort: "20"
---
# Overriding the theme

To give an application its own colours, put a file called `_custominit.scss` in
your webapp at the place the theme expects it:

```
src/main/webapp/themes/scss/winter/_custominit.scss
```

and declare the variables you want to change:

```scss
$link-text: #c00040;
$font-family: "Inter", sans-serif;
$font-size: 15px;
```

That is the whole mechanism. The framework's own `_custominit.scss` is empty but
for a comment, and yours replaces it, because
[a webapp file wins over a classpath resource](../themes/index.md).

[TOC]

## Why declaring a variable there works

Every variable in the theme is declared with SASS's `!default` flag:

```scss
$font-size: 14px !default;
$link-text: s.$link-text !default;			// a colour role, passed on from the scheme
```

`!default` means *this is the value unless the module was configured with
another*. `style.scss`, the theme's entry point, does exactly that configuring:

```scss
@use "theme-configuration" as c;
@include meta.load-css("theme", $with: c.$configuration);
@include meta.load-css("stylesheet");
```

`_theme-configuration.scss` loads your `_custominit.scss` as a module - and
`_variant-custominit.scss`, see below - and `style.scss` hands every variable they
declare to the theme as its configuration, and only then loads the stylesheet proper -
so by the time any component partial reads `$link-text`, the value is yours. (The same
configuration carries the theme's own [exceptions](../themes/index.md); yours outrank
them.)

Two consequences of that are worth knowing:

- **A name the theme does not declare is an error.** The configuration may only
  set variables that exist with `!default` somewhere in the theme, so a
  misspelt `$lnk-text` fails the compile with *"$lnk-text was not declared
  with !default in the @used module"* rather than being silently ignored.
- `_custominit.scss` holds plain declarations. It cannot read a theme variable -
  the theme is not loaded yet when it runs - so a value *derived* from the theme
  belongs in `_userstyle.scss`, below. It may load
  [the parameters module](../sass-scss-support/index.md), which is how a
  request-time value becomes a theme variable:

  ```scss
  @use "parameters" as p;
  $link-text: if(p.$themeNature == "dark", #ff80a0, #c00040);
  ```

  For more than a value or two, the next section is the better way.

## A value for light or dark: `_variant-custominit.scss`

`_custominit.scss` applies to every [colour scheme](../themes/index.md). A value
that should differ between light and dark goes in `_variant-custominit.scss`
instead, which exists once per nature - or once per scheme:

```
src/main/webapp/themes/scss/winter/light/_variant-custominit.scss       every light scheme
src/main/webapp/themes/scss/winter/dark/_variant-custominit.scss        every dark scheme
src/main/webapp/themes/scss/winter/dark/nord/_variant-custominit.scss   Nord only, instead of the one above
```

```scss
// themes/scss/winter/dark/_variant-custominit.scss
$primary-solid: #d9822b;
$link-text: #8ab4ff;
$chrome-solid: #3b4f63;
```

It is written like `_custominit.scss` - plain declarations of variables the theme
declares - and where both files set a variable, `_variant-custominit.scss` wins. You
only write what you change: every colour you leave alone still comes from the scheme,
including the ones a later DomUI version adds.

The light file cannot leak into dark, because each lives in its nature's directory and
the search path of a scheme only has its own nature in it. A copy in a scheme's own
directory is found before the nature's, so it replaces it for that scheme - it does not
add to it.

!! Before the colour schemes (October 2026) the light file was
!! `themes/scss/winter/_variant-custominit.scss`. That file is no longer read: move it to
!! `themes/scss/winter/light/`.

## The second hook: `_userstyle.scss`

`_userstyle.scss` is loaded after the theme is configured and before any
component is styled. It is for what `_custominit` cannot do: rules of your own,
and values derived from what the theme computed. Reach the theme's variables and
functions with one line at the top:

```scss
@use "theme" as *;

// derived from a value the theme computed, not a raw override
$my-panel-bg: lighter($primary-solid, 40%);

// or plain css of your own
.myapp-toolbar {
  background: $my-panel-bg;
  padding: $vertical-padding $horizontal-padding;
}
```

`theme` is a name the framework resolves to the theme's module, for the colour scheme
the sheet is being compiled for - see
[SASS/SCSS support](../sass-scss-support/index.md). `as *` makes its members
available without a prefix, so a theme variable is written the way the theme
writes it.

Put the file in the same directory, next to `_custominit.scss`.

| Use | Where |
| --- | --- |
| change a theme variable | `_custominit.scss` |
| change it for light or dark only, or for one scheme | `_variant-custominit.scss`, in the nature's or the scheme's directory |
| a colour scheme of your own | a `_scheme.scss` of your own - see [themes](../themes/index.md) |
| use a theme variable, or add rules of your own | `_userstyle.scss` |
| a value that differs per request or per user | `_custominit.scss`, reading `parameters` - see [SASS/SCSS support](../sass-scss-support/index.md) |

!! Do not copy a `_palette.scss`, `_component-colors.scss`, `_variables.scss` or
!! `_derived-variables.scss` into your webapp to edit them. A copy **shadows** the
!! framework's file completely, so every variable added to the theme afterwards is
!! missing from your build and the stylesheet fails to compile on an upgrade. The
!! override files exist so that you never have to.

## What you can override

Every `!default` variable in the theme. The colours come in two tiers, which the
[themes](../themes/index.md) page explains:

- the **colour roles**, which every scheme states in its `_scheme.scss` and the nature's
  `_palette.scss` passes on - `$surface-page`, `$text-subtle`, `$border-default`,
  `$primary-solid`, `$danger-wash`, `$chrome-tint` ... Set one, and everything that takes that
  role follows.
- the **component colours** in `_component-colors.scss`, one for each colour a component
  paints, each a role by default. `$tlf-hdr-bg: #336;` restyles the LogTailer's header and
  nothing else.

What is not a colour - fonts, sizes, spacing - is in `_variables.scss` and
`_derived-variables.scss`, the same for every scheme. The ones most applications reach for,
with their light defaults:

| Variable | Default | What it sets |
| --- | --- | --- |
| `$font-family` | a system font stack | the font for everything |
| `$font-size` | `14px` | base text size |
| `$fixed-font-family` | `Courier New, Courier, monospace` | code and other fixed-width text |
| `$surface-page` | `#ffffff` | page background |
| `$body-bg-img` | none | a background image for the body |
| `$horizontal-padding` | `10px` | the horizontal padding components inherit |
| `$vertical-padding` | `10px` | the vertical one |
| `$link-text` | `#2200cc` | links |
| `$primary-solid` | `#f69231` | the accent: a default button |
| `$control-solid` | `#2b6de8` | the colour of a control in use: a toggle that is on, the chosen item, a chip |
| `$field-surface-readonly` | `#f2f9fe` | how a read-only input shows |

A role you set in `_custominit.scss` holds for every scheme, dark ones included; set it in
the nature's or a scheme's `_variant-custominit.scss` to change it in those only. A role's
promise - the family's `-text` readable on its `-wash`, `-on-solid` on its `-solid` - is yours to
keep for the colours you choose.

!! The colours were renamed when the theme moved to colour roles (October 2026): `$link-color`
!! is `$link-text`, `$primary` is `$primary-solid`, `$body-bg` is `$surface-page`, and so on, and
!! the old names are gone. A `_custominit.scss` that still sets one fails to compile, naming it.
!! [Moving to modules](../moving-to-modules/index.md#after-the-colour-roles) has the table from
!! every old name to its new one.

## Checking what you changed

The stylesheet is compiled per request, so there is nothing to rebuild: save the
file and reload the page. If the SCSS does not compile, the request fails with a
`SassException` carrying the compiler's own error message rather than silently
serving the previous stylesheet. Anything the compiler merely warns about - a
`@warn` of yours, a deprecated construct - is logged; see
[SASS/SCSS support](../sass-scss-support/index.md).
