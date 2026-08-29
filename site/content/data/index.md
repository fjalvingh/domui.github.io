---
menu:
  sort: "50"
---
# Data binding and queries

Getting data into a page and back out of it again. Data binding connects
component properties to a model, and the query layer gets that model out of the
database in a way that is not tied to one persistence framework.

- [The Generic Query framework (QCriteria)](qcriteria/index.md) - writing
  database queries in a generic, typed way.
- [Data binding](data-binding/index.md) - what it is and how to use it, plus:
  - [how it works internally](data-binding/how-does-it-work/index.md)
  - [why property references exist](data-binding/property-references/index.md)
  - [generating typed properties](data-binding/typed-properties/index.md) and the
    [dotted path gotcha](data-binding/dotted-path-binding/index.md).
- [The Hibernate/JPA POJO generator](pojo-generator/index.md) - generating data
  classes from an existing database schema.
