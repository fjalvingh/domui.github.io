---
menu:
  sort: "50"
---
# GenericHeader

`GenericHeader` is a header line: a text in one of six styles, with optional
buttons at its right.

```java
cp.add(new GenericHeader(Type.HEADER_2, "Tracks"));

GenericHeader header = new GenericHeader(Type.HEADER_2, "Tracks");
header.addButton(Icon.faPencil, "Rename", a -> rename());
cp.add(header);
```

!demo(to.etc.domuidemo.pages.components.layout.HeadersPage.ui, 100%, 700)

| Type | What it is |
| --- | --- |
| `SIMPLE` | a bigger font, in black - the default |
| `BLUE` | the same in blue |
| `HEADER_1` … `HEADER_4` | the four generic header levels |

| Method | What it does |
| --- | --- |
| `new GenericHeader(String)` | a `SIMPLE` header |
| `new GenericHeader(Type, String)` | one of the six |
| `setText(String)` | change the text |
| `addButton(IIconRef, String hint, IClicked<NodeBase>)` | a small button at the right |
| `addButton(IIconRef, String hint, String onClickJs)` | the same, handled in the browser |

It renders as `ui-generichd ui-generichd-<type>`, with the buttons in a
`ui-generichd-btns` div.

## Not an HTag

`HTag(2, "Tracks")` is an `<h2>`: a heading in the document, which is what a
page's own title and its sections should be. `GenericHeader` is a styled div
that happens to look like one, and it exists for the buttons. Prefer `HTag`
where the header is only text.
