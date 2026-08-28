# CSS problems and solutions

A collection of tricks that were needed to create the new stylesheets

<a id="merging-the-borders-of-two-ajacent-divs-controls"></a>

## Merging the borders of two ajacent divs/controls

Two borders next to each other are ugly, and border-collapse does not work for divs. You can hide one border, but when the border changes on hover for instance that is fugly. See the [following fiddle for the trick to solve it](https://jsfiddle.net/fjalvingh/cht5wy6b/).

<a id="joining-controls-bulma-style"></a>

## Joining controls, Bulma style

See [this fiddle](https://jsfiddle.net/fjalvingh/tpjbdrq9/).

In DomUI I want something else: controls like Text2<> and DateInput2 have "internal" buttons. These must be inside the encapsulating div of the control so that the whole thing stays together. These buttons must join like has-addons. But the whole thing itself must *also* be joinable outside. See [this fiddle for the experiment with two levels of joining](https://jsfiddle.net/fjalvingh/Ljx34kan/) .

See also [this one which attempts to style all components using generic classes](https://jsfiddle.net/fjalvingh/m6hvvh8o/) and allowing for "joining" components together using "has-addons".

<a id="restyling-the-fugly-input-typefile-control"></a>

## Restyling the fugly input type="file" control

An example can be found [in this fiddle](https://jsfiddle.net/fjalvingh/b726k7Lb/). The core ideas are:

- Make a parent container position: relative
- Make the input itself position: absolute and make it fill its entire container (top, bottom, left, right: 0).
- Hide the fugly mother by setting opacity: 0
- In the parent container add whatever you want to show as button and selected filer UI

The button and selected UI overlays the input type=file, but clicking the whole rigmaroo will make the input type=file react as usual.

I tested the above fiddle on Chrome, Firefox and IE Edge 14, 15 and 16.
