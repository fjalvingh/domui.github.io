# Implementation details

This section collects in-depth descriptions of how DomUI works underneath: the mechanisms
the rest of the documentation uses without explaining them. It is a collection, not a
course - the pages are in no particular order, and each can be read on its own once you
know what it is about from the chapter that uses it.

- [The body document (UrlPage)](urlpage/index.md) - what makes UrlPage different from
  every other node.
- [DomUI State management](state-management/index.md) - how pages, conversations and
  their database resources are kept and cleaned up.
- [Data binding details](data-binding-details/index.md) - soft binding, where a binding
  lives, in what order bindings run, and when a value counts as changed.
- [Typed properties: the annotation processor](typed-properties/index.md) - the classes
  the processor generates, and how it decides which properties get one.
