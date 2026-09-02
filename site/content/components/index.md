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
- [Component rules](rules/index.md) - the CSS and implementation rules every
  DomUI component follows, plus
  [vertical form builder details](rules/vertical-form-builder-details/index.md).
- [Forms and input](forms-and-input/index.md) - the form builder, buttons,
  checkboxes, file upload and the embedded editors.
- [Lookup and search](lookup-and-search/index.md) - LookupInput2, the
  SearchPanel and search-as-you-type.
- [Tables, trees and navigation](tables-trees-navigation/index.md) - DataTable,
  Tree2 and BreadCrumb2.

The page a component lives on is described separately, in
[The body document (UrlPage)](../70-implementation-details/urlpage/index.md).

<a id="still-to-be-written"></a>

## Still to be written

These subjects have no page yet:

- The metadata model: overview, metamodel annotations, metamodel initialization
- Embedding Hibernate
