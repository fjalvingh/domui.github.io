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
$link-color: #c00040;
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
$link-color: #2200cc !default;
```

`!default` means *this is the value unless the module was configured with
another*. `style.scss`, the theme's entry point, does exactly that configuring:

```scss
@use "custominit";
@use "variant-custominit";
@include meta.load-css("theme", $with: map.merge(meta.module-variables("custominit"), meta.module-variables("variant-custominit")));
@include meta.load-css("stylesheet");
```

It loads your `_custominit.scss` as a module - and `_variant-custominit.scss`, see
below - hands every variable they declare to the theme as its configuration, and
only then loads the stylesheet proper - so by the time any component partial reads
`$link-color`, the value is yours.

Two consequences of that are worth knowing:

- **A name the theme does not declare is an error.** The configuration may only
  set variables that exist with `!default` somewhere in the theme, so a
  misspelt `$lnk-color` fails the compile with *"$lnk-color was not declared
  with !default in the @used module"* rather than being silently ignored.
- `_custominit.scss` holds plain declarations. It cannot read a theme variable -
  the theme is not loaded yet when it runs - so a value *derived* from the theme
  belongs in `_userstyle.scss`, below. It may load
  [the parameters module](../sass-scss-support/index.md), which is how a
  request-time value becomes a theme variable:

  ```scss
  @use "parameters" as p;
  $link-color: if(p.$themeVariant == "dark", #ff80a0, #c00040);
  ```

  For more than a value or two, the next section is the better way.

## A value for one variant: `_variant-custominit.scss`

`_custominit.scss` applies to every [theme variant](../themes/index.md). A value
that should differ between light and dark goes in `_variant-custominit.scss`
instead, which exists once per variant:

```
src/main/webapp/themes/scss/winter/_variant-custominit.scss        the light variant
src/main/webapp/themes/scss/winter/dark/_variant-custominit.scss   the dark variant
```

```scss
// themes/scss/winter/dark/_variant-custominit.scss
$primary: #d9822b;
$link-color: #8ab4ff;
$header-bg: #3b4f63;
```

It is written like `_custominit.scss` - plain declarations of variables the theme
declares - and where both files set a variable, the variant's file wins. You only
write what you change: every colour you leave alone still comes from DomUI's own
palette for that variant, including the ones a later DomUI version adds.

The light file cannot leak into dark: DomUI ships an empty
`_variant-custominit.scss` in its own `dark/` directory, which is found before your
light one when the dark sheet is compiled. A variant directory of your own needs one
too, even an empty one, or it takes the light file.

## The second hook: `_userstyle.scss`

`_userstyle.scss` is loaded after the theme is configured and before any
component is styled. It is for what `_custominit` cannot do: rules of your own,
and values derived from what the theme computed. Reach the theme's variables and
functions with one line at the top:

```scss
@use "theme" as *;

// derived from a value the theme computed, not a raw override
$my-panel-bg: lighter($primary, 40%);

// or plain css of your own
.myapp-toolbar {
  background: $my-panel-bg;
  padding: $vertical-padding $horizontal-padding;
}
```

`theme` is a name the framework resolves to the theme's module, for the variant
the sheet is being compiled for - see
[SASS/SCSS support](../sass-scss-support/index.md). `as *` makes its members
available without a prefix, so a theme variable is written the way the theme
writes it.

Put the file in the same directory, next to `_custominit.scss`.

| Use | Where |
| --- | --- |
| change a theme variable | `_custominit.scss` |
| change it for one variant only | `_variant-custominit.scss`, in that variant's directory |
| use a theme variable, or add rules of your own | `_userstyle.scss` |
| a value that differs per request or per user | `_custominit.scss`, reading `parameters` - see [SASS/SCSS support](../sass-scss-support/index.md) |

!! Do not copy `_palette.scss`, `_component-colors.scss`, `_variables.scss` or
!! `_derived-variables.scss` into your webapp to edit them. A copy **shadows** the
!! framework's file completely, so every variable added to the theme afterwards is
!! missing from your build and the stylesheet fails to compile on an upgrade. The
!! override files exist so that you never have to.

## What you can override

Every `!default` variable in the theme. The colours are in two files under
`$themes/scss/winter` that exist once per variant - `_palette.scss`, the main set,
and `_component-colors.scss`, which names what each component paints, each
defaulting to a main-set value; the [themes](../themes/index.md) page explains how
they relate. What is not a colour - fonts, sizes, spacing - is in `_variables.scss`
and `_derived-variables.scss`, the same for every variant. The ones most
applications reach for, with their light defaults:

| Variable | Default | What it sets |
| --- | --- | --- |
| `$font-family` | a system font stack | the font for everything |
| `$font-size` | `14px` | base text size |
| `$fixed-font-family` | `Courier New, Courier, monospace` | code and other fixed-width text |
| `$body-bg` | `#ffffff` | page background |
| `$body-bg-img` | none | a background image for the body |
| `$horizontal-padding` | `10px` | the horizontal padding components inherit |
| `$vertical-padding` | `10px` | the vertical one |
| `$link-color` | `#2200cc` | links |
| `$primary` | `#f69231` | the accent: a default button, a selected row, a hovered menu entry |
| `$readonly-bg`, `$readonly-border` | transparent, `#EEEEEF` | how a readonly control shows |

The semantic colours - `$info`, `$success`, `$warning`, `$danger`, `$light`,
`$dark` - are in the derived tier and can be set directly when you want the
framework's warning colour to be yours. So can any single component's colour:
`$tlf-hdr-bg: #336;` restyles the LogTailer's header and nothing else.

## Checking what you changed

The stylesheet is compiled per request, so there is nothing to rebuild: save the
file and reload the page. If the SCSS does not compile, the request fails with a
`SassException` carrying the compiler's own error message rather than silently
serving the previous stylesheet. Anything the compiler merely warns about - a
`@warn` of yours, a deprecated construct - is logged; see
[SASS/SCSS support](../sass-scss-support/index.md).
