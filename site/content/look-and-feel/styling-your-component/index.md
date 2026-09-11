---
menu:
  sort: "40"
---
# Styling a component

A component gets its styles from a partial of its own, named after it, holding
classes that all start with the component's own prefix:

```scss
/* _myclearabletext.scss */
@use "theme" as *;

.ui-mct {
  display: inline-block;
}

.ui-mct-input {
  border: 1px solid $bevel-up;
  padding: 0 4px;
}

.ui-mct-clear {
  cursor: pointer;
  color: $link-color;
}
```

and the component puts that base name on its own root node:

```java
public class MyClearableText extends Div {
    @Override public void createContent() throws Exception {
        addCssClass("ui-mct");

        Text2<String> input = new Text2<>(String.class);
        input.addCssClass("ui-mct-input");
        add(input);

        Span clear = new Span("×");
        clear.addCssClass("ui-mct-clear");
        add(clear);
    }
}
```

[TOC]

## Where the partial goes

For a component in an application, put the file next to the two override files
in your webapp and pull it in from `_userstyle.scss`:

```
src/main/webapp/themes/scss/winter/_myclearabletext.scss
src/main/webapp/themes/scss/winter/_userstyle.scss
```

```scss
/* _userstyle.scss */
@use "myclearabletext";
```

The name is resolved relative to the file it appears in, so it finds your
partial in your webapp. The `@use "theme" as *;` at the top of the partial is
what gives it `$bevel-up` and `$link-color`: a module sees only what it loads
itself, and `theme` is the theme's variables, functions and mixins for the
variant being compiled - see [SASS/SCSS support](../sass-scss-support/index.md).

For a component in the framework itself the partial goes in the theme directory
and the `@use` goes in `_stylesheet.scss`, among the others of its kind. What it
paints is named in `_derived-variables.scss` - `$mct-border: $bevel-up !default;`
- rather than declared in the partial, so that an application or a variant can
set it.

!! Nothing finds a partial by itself. Without the `@use` the file is never
!! compiled, and no error says so.

## The CSS base name

Every component has one unique class, its **base name**: `ui-` followed by a
three to five letter abbreviation. `LookupInput2` uses `ui-lui`, `DataTable`
uses `ui-dt`.

Two rules follow from it, and they are absolute:

1. The component's **root node always carries the base name.** It may carry
   other classes as well, but the base name is always among them. That
   guarantees every component can be addressed by a class, including the ones
   that have no styles yet.
2. **Every class the component adds starts with the base name.** `ui-mct-input`,
   `ui-mct-clear`. This is what stops two components that both wanted to call
   something `input` from styling each other's insides.

## Address parts by class, never by tag

A component made of several tags - a table with a `tbody`, `tr`s and `td`s - is
tempting to style like this:

```scss
.ui-dt td { ... }
```

That finds the `td`s of the DataTable. It also finds every `td` of every table
an application put *inside* a DataTable cell, and styles those too.

So: **use only class names in selectors.** Give each part its own
`ui-dt-`-prefixed class and select that. It costs a class in the markup and
removes a whole category of bug.

## Sharing styles between components

A component must **never** use another component's classes. It looks like reuse
and it is a trap: the day the other component's styling changes, yours changes
with it, and nothing in either file says so.

What is allowed is a deliberately shared style, in a fragment of its own, with
no component base name on it. Keep those small - the more that is shared, the
harder each component is to change on its own.

## Browser differences

Stylesheets are written for current browsers, and hold nothing working around a
browser that is no longer around.

Where a tweak is unavoidable, use feature detection. The SCSS cannot do
anything else anyway: it is compiled once per theme and cached, not once per
request, so it does not know which browser will receive it.

## Using theme variables

Take sizes and colours from the theme rather than writing literals, so that an
application [overriding the theme](../overriding-the-theme/index.md) changes
your component along with everything else:

```scss
.ui-mct {
  padding: $vertical-padding $horizontal-padding;
  font-family: $font-family;
  font-size: $font-size;
}
```

The variables available are listed with the override mechanism, and the full
set is in `_variables.scss` and `_derived-variables.scss` in
[the winter theme](../the-winter-theme/index.md).

The rules about what a component may *do* - its node structure, its margins,
how it behaves inside a form - are in
[component rules](../../components/rules/index.md).
