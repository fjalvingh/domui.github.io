---
menu:
  sort: "40"
---
# Components

DomUI applications are built from components: Java objects that render
themselves as HTML and handle their own events. This section documents the
components DomUI provides, and the rules for writing your own.

The components are grouped by what they are for. Each group page describes the
group and its members; each member has a page of its own with its properties and
methods, and a demo page showing it working.

- [Text and value input](10-text-and-value-input/index.md) - `Text2`,
  `TextArea`, `DateInput2` and the colour pickers.
- [Choice input](20-choice-input/index.md) - `Checkbox`, `RadioGroup`,
  `ComboFixed2`, `ComboLookup2` and `EnumSetInput`.
- [Lookup and search](30-lookup-and-search/index.md) - `LookupInput2`,
  `SearchInput2`, `SearchAsYouType` and the `SearchPanel`.
- [Buttons and actions](40-buttons/index.md) - `DefaultButton`, `LinkButton`,
  `SmallImgButton`, `HoverButton`, the two toggle buttons, `IUIAction` and
  `ButtonBar2`.
- [Display-only components](50-display-only/index.md) - `DisplaySpan`,
  `DisplayControl`, the boolean displays, `DisplayHtml` and the ruler.
- [Tables, lists and trees](60-tables-and-trees/index.md) - `DataTable`, the
  row renderer, the table models, the other table shapes and `Tree3`.
- [Layout and page structure](70-layout/index.md) - the panels, the headers,
  the tab panels, the splitter and `ChildFragment`.
- [Windows, dialogs and messages](80-windows-and-dialogs/index.md) - `Window`,
  `Dialog`, `InputDialog`, `MsgBox2`, `ExceptionDialog` and the components that
  show a message on the page.
- [Navigation and menus](90-navigation/index.md) - `BreadCrumb2`,
  `AppPageTitleBar`, `ALink` and the two menus.
- [Images, icons and file upload](100-images-and-icons/index.md) - `IIconRef`
  and the three kinds of icon, `Img`, the two image controls and the two upload
  controls.
- [Component rules](rules/index.md) - the CSS and implementation rules every
  DomUI component follows, plus
  [vertical form builder details](rules/vertical-form-builder-details/index.md).
- [Forms and input](forms-and-input/index.md) - the form builder, file upload
  and the embedded editors.

The page a component lives on is described separately, in
[The body document (UrlPage)](../70-implementation-details/urlpage/index.md).

<a id="still-to-be-written"></a>

## Still to be written

These subjects have no page yet:

- The metadata model: overview, metamodel annotations, metamodel initialization
- Embedding Hibernate
