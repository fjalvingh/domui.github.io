---
menu:
  sort: "50"
---
# Databases and queries

Getting the model out of the database, in a way that is not tied to one
persistence framework.

- [The Hibernate/JPA POJO generator](pojo-generator/index.md) - generating data
  classes from an existing database schema.

Writing the queries themselves is part of the walkthrough:
[Using databases](../building-pages/30-using-databases/index.md) and
[Typed properties](../building-pages/40-typed-properties/index.md). What the query
layer is made of - executors, selections, subqueries - is in
[The generic query layer (QCriteria)](../70-implementation-details/qcriteria/index.md).
Moving that model into a screen and back is
[Data binding](../building-pages/50-data-binding/index.md), with
[Data binding details](../70-implementation-details/data-binding-details/index.md)
under it.
