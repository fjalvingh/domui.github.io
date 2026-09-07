---
menu:
  sort: "70"
---
# Animations

`to.etc.domui.dom.Animations` runs a jQuery effect on a node. The node is a
DomUI node like any other; the effect happens in the browser, after the response
that carries the change has been rendered.

```java
Div newNode = new Div();
/* add content to the node here */
cp.add(newNode);

Animations.slideDown(newNode);
```

The node is added the ordinary way, and on the screen it appears to slide down
into place.

## What there is

| Method | What the browser does |
| --- | --- |
| `slideDown(node)` | slides the node open; the node ends up at its normal display |
| `slideUp(node)` | slides it closed; the node stays in the tree with `display: none` |
| `slideUp(node, jsCallback)` | the same, with a piece of javascript run when the slide finishes |
| `slideUpAndRemove(node)` | slides it closed and then removes it from the tree |
| `shake(node)`, `bounce(node)` | the jQuery UI effects of those names |
| `pulsate(node, times)` | pulsates; `0` means the effect's own default |
| `scrollIntoView(node)` | scrolls the node into view if it is not already |
| `animate(node, what)` | jQuery's `animate()`, with `what` as its options object |

The effect names are jQuery's, and its
[documentation](https://api.jquery.com/category/effects/) describes what each
one looks like.

## Hiding versus removing

`slideUp()` leaves the node in the DomUI tree with `display: none`, which is
what you want when the same node is to be shown again later - `slideDown()` on
it brings it back with its content intact.

More often a node that slides up is meant to be gone, and then leaving it
behind is a leak of screen state: it still holds its controls, its bindings and
its values. `slideUpAndRemove()` is the one to use there. It renders the node
one more time so the effect can run, and removes it from the tree afterwards -
the net effect of `remove()`, with the animation in front of it.

## How it works

An effect is not rendered as part of the node: it is a **javascript statement
appended to the response**, plus an after-render listener that repairs the
DomUI node afterwards.

The repair is the point. Most effects need the browser DOM to start in a state
that the server-side tree does not have - `slideDown()` needs the node to be
`display: none` before it can slide it open - so the node is rendered in that
odd state, and the listener sets the DomUI node back to the state it should
have once the effect has run. Without it the server's idea of the tree and the
browser's would drift apart, and the next delta would be computed against the
wrong one.
