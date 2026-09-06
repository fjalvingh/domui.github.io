---
menu:
  sort: "10"
---
# DomUI component rules

These are the rules a DomUI component follows - the ones the framework's own components are held to, and the ones a component of your own should obey.

Some component names carry a number: LookupInput2, ComboFixed2, Tree3. Where they do, **the highest number is the component to use**; the ones below it are still in the framework because applications use them, and are not documented here. A name without a number is simply the only version there is.

Styles come from the **SCSS theme**, and the theme is `winter`: standard SCSS, one fragment per component, compiled by the framework at runtime. The `.frag.css` themes next to it in `resources/themes` are what the framework used before SCSS; nothing is maintained in them, and a component that only styles itself in `winter` is the normal case.

<a id="stylesheet-rules"></a>

## Stylesheet rules

<a id="no-reset-stylesheet"></a>

### No reset stylesheet

The stylesheets do not clear the default styling off all html tags first. A reset sheet is hard to do well, its effects percolate through everything styled on top of it, and it breaks the one thing an application does a lot: *showing* html that came from somewhere else, which then renders as flat text until every style the reset removed has been put back by hand.

Instead a component styles itself through its own classes (see below) and resets a tag only where it has to. Most of what DomUI renders is a `div` or a `span` - which have nothing to reset - with a class on it.

<a id="the-box-model-used-is-border-box"></a>

### The box model used is border-box.

The default (original) box model used by browsers leaves a lot to be desired. When you specify something like:

```
height: 100px;
width: 200px;
padding: 10px;
border: 2px solid black;
```

the *actual width of the element* is padding + border + width. The same applies to height: padding + border + height. This makes defining the actual size of element very hard because adding a border means decreasing the size if the element's size needs to be constant. It also causes huge problems with things like "width: 100%" because those cannot have border nor padding: it would make the element exceed the 100% width causing those annoying scroll bars.

There is a better box model that is currently well supported by all major browsers (and IE up to version 8): the *border-box model*. This model uses the defined width and height of an element as the actual rendered size, and subtracts from that size the sizes of borders and padding to get the content area's size. In effect this means that the above definition would *always* result in an element of *exactly* 200x100 pixels wide. The content area (inside the element) would be exactly 176x76 pixels big: 200 - 2\*2 - 2\*2 for width and the similar calculation for height.

The script used for this is in \_core.scss, and applies the following:

```
html {
  box-sizing: border-box;
}
*, *:before, *:after {
  box-sizing: inherit;
}
```

This sets all tags to use border-box sizing by default, and makes it inherit so that changes made locally (should) percolate through.

See the following links for more information:

- [Box sizing layout secrets](http://blog.teamtreehouse.com/box-sizing-secret-simple-css-layouts)

<a id="browser-support-and-tweaks"></a>

### Browser support and tweaks

Stylesheets are written for current browsers. There is nothing in them working around a browser that is no longer around.

If a tweak is needed, use feature detection rather than browser identification. The SCSS sheets cannot do the latter anyway: they are compiled once, not per request, and know nothing about the browser they will be sent to.

<a id="one-fragment-per-component"></a>

### One fragment per component

Each component must have its own stylesheet fragment which contains most of the scss needed to render the component. For a component like LookupInput2 there is a fragment called \_lookupinput2.scss, in the theme directory `resources/themes/scss/winter`.

A new fragment has to be added to that theme's `style.scss` with an `@import` of its own; nothing finds fragments by itself.

<a id="styling-a-component"></a>

### Styling a component

Each component must have an unique CSS class "base name". These names usually start with "ui-" followed by a 3 to 5 letter abbreviation for the component's name. For example: the LookupInput component uses *ui-lui* as its base name. All classes added to html nodes should always starts with this css base name. Using the base name prevents name clashes when different components define the same class name, leading to oddities in rendering.

The root node for the component *must* define itself to have as its class the CSS base name. This ensures that all components can always be addressed by a CSS class - even when there is no apparent need, yet. The root node may have multiple classes, as long as:

1. They all start with the CSS base name (or ARE the CSS base name)
2. The CSS base name is ALWAYS present.

An example css structure for a simple DomUI button component could look like this:

```
<button class='ui-gbtn'>
  <span class='ui-gbtn-icon'></span>
  <span class='ui-gbtn-label'>He<span class='ui-gbtn-accel'>l</span>lo</span>
</button
```

All of the styles for a component *must* be assigned using CSS. Components should never contain code that hard sets the css attributes for the component. The only exception to this rule is when there is no other way to effect what is needed. Adding CSS related code inside the Java code makes the UI very hard to maintain.

<a id="sharing-styles"></a>

### Sharing styles

Components should **never** use classes from other components to handle their styling!! That would lead to very hard to maintain code: changing the style for one component now suddenly has an effect on some other component, and the styles were not designed for that in the first place!

You can define shared styles, but these should be clearly marked as such and be present in a separate stylesheet fragment. Shared styles have no CSS base name suffix.

Shared styles should normally only be used for small things, because sharing too much means that it becomes hard to change components using that style.

<a id="using-css-selectors-for-the-parts-of-a-component"></a>

### Using CSS selectors for the "parts" of a component

More complex components can consists of multiple html tags. For instance the DataTable component contains a table, a tbody, tr's, td's and more. The "root" of the component, as said, **must** have the CSS base class name which for DataTable is "ui-dt".

A common mistake is to now address the parts in the DataTable with selectors like:

```
.ui-dt td {...
```

This finds the td's in the DataTable allright. But the problem is: *it also finds all td's of tables that are INSIDE a DataTable cell!*

So a style that is supposed to work for a cell of the DataTable only now also applies for something *inside* such a cell. That is a bad idea.

So the rule is: **use only class names in selectors, do not use tags**.

<a id="layout-rules"></a>

# Layout rules

Layout has stricter rules than the rest. They cost something: a page sometimes needs more css, or an extra "layout" component, to look right. What they buy is fewer odd layout cases and simpler css everywhere else.

<a id="two-basic-types-of-components"></a>

## Two basic types of components

For the purpose of the discussion we divide the components in two big "groups" related to their layout:

- The "inline" component group. These components use limited width, and often occur together with other components in some "inline" way. Good examples of inline components are Text<T>, LookupInput, CheckBox, ComboLookup and all.
- The "panel" component group. These usually contain other components and show as a block. They can either be complex components like DataTable and Tree, or they can be Panels or Headers.

<a id="inline-component-rules"></a>

## Inline component rules

<a id="component-structure"></a>

### Component structure

Inline components should, by default, all behave as an inline-block. So by default it should be possible to place inline components one after another.

All inline components must have a single Node that contains all of the component. This is important because it allows the parts of the component to be addressed relative to its container, so that alignment rules can be applied. So a proper component would be:

```
<div class='ui-myc'>
  <input type='email' size='12'>
  <button class='ui-myc-btn'><span class='fa-icon' /></button>
</div>
```

while a bad, bad one (hello DateInput) would be:

```
<div class='ui-myc'>
  <input type='email' size='12'>
</div>
<button class='ui-myc-btn'><span class='fa-icon' /></button>
```

The latter cannot be addressed relative to a container at all, which makes aligning it with anything a fight.

<a id="inline-component-layout"></a>

### Inline component layout

By default an inline component should **not** have any padding around it. So adding two inline components after each other should show with those components touching each other! It is the responsibility of the *container* to place components in such a way that groups of components "look nice".

The reason for this rule is that having paddings around the components makes it hard to construct *other* components from existing ones.

Take the following example:

Say that the SmallButton itself came with 5px padding all around it. The Text<T> component also has this. But a common "supercomponent" is to combine a Text with one or more small buttons, and for that it is customary to have the buttons touching the Text control and each other:

\[IMAGE HERE\]

To get this done the new component now has to "undo" the styles of the components, then add its own. That is error prone.

This rule also means that adding "naked" components together, without help, will look like shit. This btw has always been the case, but it was just a different kind of the smelly stuff.

<a id="forms"></a>

### Forms

Input components are normally used inside forms, and a form is not a component: it is what the `FormBuilder` builds out of the controls it is handed. A component therefore has to look right inside a form's label/control pair, which mostly means it must not bring margins of its own - the form supplies the space between its rows.

What the builder does, and what it leaves on the page, is described in [forms](../15-forms/index.md).
