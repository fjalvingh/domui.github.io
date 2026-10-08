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

## A colour scheme of your own

A colour scheme is one file of tokens, in a directory named for its nature and itself:

```
themes/scss/winter/dark/ocean/_scheme.scss
```

Start from a copy of one of DomUI's - `light/winter/_scheme.scss` for a light scheme,
`dark/midnight/_scheme.scss` for a dark one - and change the colours; the nature's
palette works every other colour out from them. The file must declare every token its
nature reads, which is also how an upgrade tells you that a nature reads a new one.
Then offer it:

```java
static private final IThemeVariant OCEAN = new SchemeVariant(ThemeNature.DARK, "ocean", "Ocean");

@Override
public List<IThemeVariant> getThemeVariants() {
	return List.of(SchemeVariant.WINTER, OCEAN, SchemeVariant.MIDNIGHT);
}
```

A component colour the scheme wants different from what its tokens give goes in a
`_scheme-exceptions.scss` next to it; a value you would rather set by name, in a
`_variant-custominit.scss` there - see [overriding the theme](../overriding-the-theme/index.md).

!! Before October 2026 a variant of your own was a directory with its own copies of
!! `_palette.scss` and `_component-colors.scss`, such as `themes/scss/winter/high-contrast/`.
!! Such a directory is no longer on any search path: make its colours a scheme.

## A copy of a framework partial

A webapp file that shadows one of the theme's partials - a copy of
`_datatable.scss` with an edit - has to be brought to the new form: the
`@use "theme" as *;` header, and no `!default` declarations, which the theme
keeps in `_component-colors.scss`. Better, now as before, is to not have the
copy: set the component's variables in `_custominit.scss`, or add your rules
in `_userstyle.scss`.

## After the dark theme work

The dark variant was reworked in October 2026 - before it became the colour schemes of
the section above: each variant got its own colour
files, and the components, images and variables that did not survive it went. What
an application may have to change:

- **Variables that are gone.** Setting one in `_custominit.scss` is a compile error.
  `$title-bg-img`, `$tab-img`, `$tab-close-img`, `$tab-close-hover-img`,
  `$tab-arrows-img`, `$tab-inactive-color`, `$tab-hover-inactive-color`,
  `$tab-active-color`, `$tab-btm-border-width`, `$stbp-border`,
  `$stbp-pager-border` (all of the old ScrollableTabPanel and title bar),
  `$ipa-border` (InfoPanel), `$expl-border` (the old Explanation),
  `$grey-ramp`, `$ladder-direction` and `$shades`. The function `ladder()` is gone
  too: a nested level is a variable of its own now (`$pmnu-sm1-bg`...).
- **Components that are gone.** `AppPageTitleBar`, its base `BasePageTitleBar` and
  `DomApplication.getDefaultPageTitleBar()`: applications write their own title bar.
  `InfoPanel`: use an `Explanation`, which has the same room for text and a
  severity. With them the css classes `.ui-atl*` and `.ui-ipa`, and `.ui-msgln2`,
  which nothing created.
- **Images that are gone.** An application that used one by its `THEME/` name gets
  a missing image, and can copy it from an earlier DomUI into its own webapp:
  `72x24_back`, `bg-expl`, `bg-horiz-separator`, `bg-new-ttl1`, `bg-new-ttl2`, `bg-ttl-domui`, `big-error`, `big-info`, `big-warning`, `blank`, `btnHeaderMenuActive`, `btn-hover-ClearMultipleLookup`, `btnMinus`, `bupl-cancel`, `defaultButton`, `exception-img-1`, `flare-important`, `hr-caption`, `iptLocation`, `iptSourceCode`, `lsel-delete`, `mbx-error`, `mbx-info`, `mbx-question`, `mbx-warning`, `pan-down`, `pan-left`, `pan-right`, `pan-up`, `paneh`, `panehc`, `panev`, `panevc`, `small-delete`, `sort-asc`, `sort-desc`, `sort-none`, `tab-all-domui`, `tab-blue-header-bg`, `tab-blue-header2-bg`, `tab-norm-left-sel`, `tab-norm-right-sel`, `tab-off-err-left`, `tab-off-err-right`, `tab-off-left`, `tab-off-right`, `tab-pnl-close`, `tab-pnl-close-hover`, `tab-scrl-icon`.
  The big severity icons (`Theme.ICON_MBX_*`, `ICON_BIG_*`) are css markers now
  rather than the `mbx-*` images.
- **Light colours that changed**, in case a screenshot test notices: the
  Explanation is a callout with a bar and a marker, MessageFlare has solid fills,
  the HamburgerMenu is larger and opens against what opened it, TabPanel's tab strip
  is a pale steel blue, and ScrollableTabPanel looks like TabPanel.

## After the colour schemes

In October 2026 every variant became a colour scheme of a nature, light or dark (see
[themes](../themes/index.md)). What an application may have to change:

- **Classes that are gone.** `DefaultThemeVariant.INSTANCE` is `SchemeVariant.WINTER`;
  `DarkThemeVariant.INSTANCE` is one of the dark schemes, `SchemeVariant.MIDNIGHT` (the
  new default for dark) or `SchemeVariant.DARCULA` (what the dark variant looked like,
  more or less). `IThemeVariant.of(name)` is gone - a name is looked up with
  `DomApplication.findThemeVariant(name)` - and so is `IThemeFactory.getDefaultVariant()`:
  the default is the first light scheme of `getThemeVariants()`.
  `new SassThemeFactory(style)` takes the list of the style's schemes as a second argument.
- **Names that are gone.** A session or cookie that still holds `default` or `dark` gets
  the default scheme, light; a URL `$THEME/dark/...` is served from it too. A sheet that
  branched on `p.$themeVariant == "dark"` should test `p.$themeNature` instead.
- **Files that moved.** `themes/scss/winter/_variant-custominit.scss` is now
  `themes/scss/winter/light/_variant-custominit.scss`; the dark one stays where it was.
- **Files that must go.** A `themes/scss/winter/_palette.scss`, or a
  `themes/scss/winter/dark/_palette.scss` or `dark/_component-colors.scss`, left in the
  webapp shadows DomUI's own and breaks the theme. The dark colours are now chosen per
  scheme, the light ones in `light/winter/_scheme.scss`.
- **Darcula changed** a little when it became a scheme: it has the light theme's orange
  accent and buttons, like every dark scheme, and a lighter red.

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
