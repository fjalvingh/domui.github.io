---
menu:
  sort: "30"
---
# The winter theme

`winter` is the theme DomUI ships, and it lives in one directory:

```
to.etc.domui/src/main/resources/resources/themes/scss/winter/
```

117 SCSS files, of which `style.scss` is the only one the compiler is ever
handed. Everything else is a **partial** - a file whose name starts with an
underscore - and reaches the stylesheet because something `@use`s it.

[TOC]

## What `style.scss` does

Four lines:

```scss
@use "sass:meta";
@use "custominit";
@include meta.load-css("theme", $with: meta.module-variables("custominit"));
@include meta.load-css("stylesheet");
```

It loads the application's `_custominit.scss`, configures the theme with the
variables that file declares, and then loads the stylesheet proper. The order is
the theme's architecture: whatever the application says comes first, the
theme's own defaults yield to it, and every component partial reads the result.
The first two steps are described in
[overriding the theme](../overriding-the-theme/index.md); the rest is what this
page is about.

| File | What it is |
| --- | --- |
| `_index.scss` | the `theme` module: forwards `color`, `functions` and `bulmaish/core_defs`. Emits nothing |
| `_color.scss` | the variant's configuration of the variables: forwards `variables` and `derived-variables`. A variant directory holds its own |
| `_variables.scss` | the main set: palette, fonts, metrics |
| `_derived-variables.scss` | one variable per thing a component paints, each defaulting to a main-set value |
| `_functions.scss` | `ladder()`, `findColorInvert()`, `darker()`, `lighter()` and the rest |
| `bulmaish/_core_defs.scss` | the mixins every input control is built on |
| `_userstyle.scss` | the application's own rules |
| `_stylesheet.scss` | the list: 106 `@use` rules, one per file that emits css, in output order |

## The base layer

`bulmaish/` is a small set of definitions borrowed from the Bulma framework's
approach and kept deliberately thin: `_core_defs`, `_button_common`, `_icon`,
`_animations` and `_has_addons`. Buttons and icons across the theme build on
them, which is why a change there is felt widely and a change in a component
partial is not.

## Reset and core

There is no reset stylesheet in the usual sense - the theme does not strip the
default styling off every html tag. `_reset.scss` touches the few tags that need
it and stops there, because most of what DomUI renders is a `div` or a `span`
carrying a class, which has nothing to reset.

What `_core.scss` does set globally is the box model:

```scss
html {
  box-sizing: border-box;
}
*, *:before, *:after {
  box-sizing: inherit;
}
```

`border-box` makes an element's declared `width` and `height` the size it
actually occupies, with border and padding taken out of the inside rather than
added to the outside. A `width: 100%` element can then have a border without
overflowing its container, and a component can be given a fixed size without
every rule that adds a border having to subtract from it. The `inherit` on the
second rule means a local change to the box model percolates into the subtree
instead of being overridden by this one.

## One partial per component

Every component that has styles of its own has a partial named after it:
`_lookupInput.scss`, `_datatable.scss`, `_tree3.scss`, `_form5.scss`. Finding
where a component is styled is therefore a matter of guessing the file name,
and it is almost always right. Each starts the same way:

```scss
@use "theme" as *;
```

which is where its `$dt-border` and `@include ui-input-base` come from. A
partial declares no `!default` variables of its own: what it paints is named in
`_derived-variables.scss`, so that an application or a variant can set it.

The partials are grouped in `_stylesheet.scss` by what the component is - basic
components, complex components, input components, multicomponents, panels and
headers, navigation - which is close to, but not the same as, the grouping used
by [the component documentation](../../components/index.md).

Two names in that list carry a number for the same reason the components do:
`_tree3.scss`, `_caption2.scss`, `_datapager2.scss` style the current component,
and the unnumbered file next to them styles the older one that is still in the
framework. `_form5.scss` is the current form layout and `_form4.scss` is what
came before it.

!! Nothing finds a partial by itself. A new file has to be added to
!! `_stylesheet.scss` with a `@use` of its own, or it is simply never compiled -
!! and no error is reported, because as far as the compiler is concerned it does
!! not exist.
