---
menu:
  sort: "30"
---
# The winter theme

`winter` is the theme DomUI ships, and it lives in one directory:

```
to.etc.domui/src/main/resources/resources/themes/scss/winter/
```

114 SCSS files, of which `style.scss` is the only one the compiler is ever
handed. Everything else is a **partial** - a file whose name starts with an
underscore - and reaches the stylesheet because `style.scss` imports it.

[TOC]

## What `style.scss` does

It is a list of imports in a deliberate order, and the order is the theme's
architecture:

| Block | Files | What it establishes |
| --- | --- | --- |
| Parameters | `parameters` | values passed in from the request |
| Application overrides | `_custominit` | your variable values, before any default |
| Variables | `color`, `variables`, `functions`, `derived-variables` | the palette, the metrics, the semantic colours |
| Application styles | `_userstyle` | your own rules |
| Base layer | `bulmaish/*` | shared button, icon, animation and add-on definitions |
| Reset and core | `reset`, `core`, `helperclasses` | the little that is reset, and the helper classes |
| Components | ~100 partials | one per component |

The first four blocks are described in
[overriding the theme](../overriding-the-theme/index.md); the rest is what this
page is about.

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
`_lookupinput2.scss`, `_datatable.scss`, `_tree3.scss`, `_form4.scss`. Finding
where a component is styled is therefore a matter of guessing the file name,
and it is almost always right.

The partials are grouped in `style.scss` by what the component is - basic
components, complex components, input components, multicomponents, panels and
headers, navigation - which is close to, but not the same as, the grouping used
by [the component documentation](../../components/index.md).

Two names in that list carry a number for the same reason the components do:
`_tree3.scss`, `_caption2.scss`, `_datapager2.scss` style the current component,
and the unnumbered file next to them styles the older one that is still in the
framework. `_form5.scss` is the current form layout and `_form4.scss` is what
came before it.

!! Nothing finds a partial by itself. A new file has to be added to `style.scss`
!! with an `@import` of its own, or it is simply never compiled - and no error
!! is reported, because as far as the compiler is concerned it does not exist.
