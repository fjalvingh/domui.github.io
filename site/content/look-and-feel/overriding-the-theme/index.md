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

and set the variables you want to change:

```scss
$link-color: #c00040;
$font-family: "Inter", sans-serif;
$font-size: 15px;
```

That is the whole mechanism. The framework's own `_custominit.scss` is empty and
carries one comment - *"meant to be used by clients to override default theme
settings. It should remain empty in DomUI itself"* - and yours replaces it,
because [a webapp file wins over a classpath resource](../themes/index.md).

[TOC]

## Why setting a variable there works

Every variable in the theme is declared with SASS's `!default` flag:

```scss
$font-size: 14px !default;
$link-color: #2200cc !default;
```

`!default` means *assign this only if the variable has no value yet*. So
whoever assigns first wins, and `style.scss` imports the files in an order
chosen to make that useful:

```scss
@import 'parameters';       // values from the request
@import "_custominit.scss"; // YOUR variables
@import 'color';            // the theme's colours    - all !default
@import 'variables';        // the theme's variables  - all !default
@import "functions";
@import "derived-variables";
@import "_userstyle";       // YOUR rules
                            // ... every component fragment follows
```

`_custominit` is imported **before** the definitions, so a value set there is
already present when the theme's `!default` assignments run and they do nothing.

## The second hook: `_userstyle.scss`

`_userstyle.scss` sits on the other side of the variable block, after everything
is defined but before any component is styled. It is for what `_custominit`
cannot do:

```scss
// derived from a value the theme computed, not a raw override
$my-panel-bg: lighten($primary, 40%);

// or plain css of your own
.myapp-toolbar {
  background: $my-panel-bg;
  padding: $vertical-padding $horizontal-padding;
}
```

Put it in the same directory, next to `_custominit.scss`.

| Use | Where |
| --- | --- |
| change a theme variable | `_custominit.scss` |
| use a theme variable, or add rules of your own | `_userstyle.scss` |
| a value that differs per request or per user | `setThemeProperty()`, see [SASS/SCSS support](../sass-scss-support/index.md) |

!! Do not copy `_variables.scss` or `_color.scss` into your webapp to edit them.
!! A copy **shadows** the framework's file completely, so every variable added to
!! the theme afterwards is missing from your build and the stylesheet fails to
!! compile on an upgrade. The two override files exist so that you never have to.

## What you can override

The variables worth knowing are in two files, both under
`$themes/scss/winter`. `_color.scss` holds the palette, and `_variables.scss`
the rest:

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
| `$readonly-bg`, `$readonly-border` | transparent, `#EEEEEF` | how a readonly control shows |

`_derived-variables.scss` then names the semantic colours - `$primary`,
`$info`, `$success`, `$warning`, `$danger`, `$light`, `$dark` - from the
palette. They are `!default` too, so `_custominit.scss` can set them directly
when you want the framework's warning colour to be yours.

## Checking what you changed

The stylesheet is compiled per request, so there is nothing to rebuild: save the
file and reload the page. If the SCSS does not compile, the request fails with a
`SassException` carrying the compiler's own error message rather than silently
serving the previous stylesheet.
