---
menu:
  sort: "40"
---
# Animations

DomUI supports the most common JQuery animation effects for nodes. Descriptions for the animations can be found in [JQuery's documentation](http://api.jquery.com/category/effects/).

To animate a node use code like the following:

```
Div newNode = new Div();
/* add content to the node here */

Animations.slideDown(newNode);
```

In this example the node will be added, and on the screen it will appear to "slide down" from where it is added.

For animations that make nodes disappear there are usually two forms: a normal form (like Animations.slideUp) and a "destroy" form (like Animations.slideUpAndDestroy). The normal form will leave the node present in the DomUI DOM, but usually with display: none. This mode does allow showing the exact same node just by setting display back to block. But in DomUI nodes that are hidden by something like slideUp are meant to be removed from the DOM. For these cases we have the Destroy variant. This variant will first render the node back to the browser including the effect, and after the render it will remove the node from the DomUI DOM. The net effect is the same as if remove() was called.

<a id="how-it-works-internally"></a>

### How it works internally

The effects work by setting the required JQuery state in the node, and then adding the appropriate Javascript to the node to be executed at the render. Since many effects require an "odd" state of the DOM (like display: none to slide down) we want the DomUI node to be "fixed" after render so that it has the same state as the browser DOM. This is done by adding an after-render listener: this listener will "reset" the display state of the node back to what it should be in DomUI.

Since: DomUI 2.0
