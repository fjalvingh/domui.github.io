---
menu:
  sort: "10"
---
# DomUI component rules

These are the rules a DomUI component follows - the ones the framework's own
components are held to, and the ones a component of your own should obey.

Some component names carry a number: `LookupInput2`, `ComboFixed2`, `Tree3`.
Where they do, **the highest number is the component to use**; the ones below it
are still in the framework because applications use them, and are not documented
here. A name without a number is simply the only version there is.

[TOC]

## Two kinds of component

Every component is one of two shapes, and which one it is decides the rules it
has to follow:

- **Inline** components take the width they need and sit next to each other:
  `Text2`, `LookupInput2`, `Checkbox`, `ComboLookup2`.
- **Panel** components are blocks that usually contain other components:
  `DataTable`, `Tree3`, `ContentPanel`, the headers.

The rules below are the inline ones. They are stricter than the rest, and they
cost something - a page sometimes needs an extra layout component to look right.
What they buy is fewer odd layout cases, and simpler CSS everywhere else.

## An inline component is one node

All of an inline component lives inside a single node:

```html
<div class='ui-myc'>
  <input type='email' size='12'>
  <button class='ui-myc-btn'><span class='fa-icon'></span></button>
</div>
```

and not:

```html
<div class='ui-myc'>
  <input type='email' size='12'>
</div>
<button class='ui-myc-btn'><span class='fa-icon'></span></button>
```

The second one cannot be addressed relative to a container at all, so aligning
it with anything next to it becomes a fight. One containing node means the parts
can be positioned relative to it, and the whole component can be positioned as
one thing.

Inline components behave as `inline-block` by default, which is what lets them
be placed one after another.

## An inline component brings no padding

By default an inline component has **no padding or margin around it**. Two of
them placed next to each other touch. Spacing between components is the
*container's* job, not the component's.

The reason is that components are built out of other components. A control with
a small button attached to it is a common thing to build, and it wants the
button against the control, touching it. If every component carried its own
padding, the new component would have to undo the padding of each part before
adding its own - and getting that wrong is both easy and invisible until
someone looks closely.

The price is that components dropped onto a page with no container to space them
look bad. That is intended: it is a container's job, and the page should use one.

## Forms

Input components are normally used inside forms, and a form is not a component:
it is what the `FormBuilder` builds out of the controls it is handed. A
component therefore has to look right inside a form's label/control pair, which
mostly means it must not bring margins of its own - the form supplies the space
between its rows.

What the builder does, and what it leaves on the page, is described in
[forms](../15-forms/index.md).

## Styling

A component's styles live in a partial of its own, and every class it uses
starts with the component's own `ui-` base name. How to write one, where the
file goes, and the selector rules that go with it are in
[styling a component](../../look-and-feel/styling-your-component/index.md).
