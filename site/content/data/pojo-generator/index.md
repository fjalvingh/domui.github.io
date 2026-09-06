---
menu:
  sort: "30"
---
# The Hibernate/JPA POJO generator

When the database already exists and you want JPA or Hibernate entities for it,
something has to write those classes with their annotations. DomUI ships a
generator for that in `utilities/hibernate-generator`.

What sets it apart from the usual reverse engineering tools is that it **updates
existing classes** instead of overwriting them: run it again after a schema
change and it adds the new columns, removes the dropped ones and leaves the code
you wrote alone.

[TOC]

## Running it

The generator's main class is `to.etc.domui.hibgen.HibernateGenerator`. The
module's jar has no `Main-Class` and does not carry its dependencies, so it is
run from the build rather than with `java -jar`:

```bash
$ mvn -q -pl utilities/hibernate-generator exec:java \
    -Dexec.mainClass=to.etc.domui.hibgen.HibernateGenerator \
    -Dexec.args="-dbtype postgres -db user:password@localhost/mydatabase \
                 -pkgroot org.mydomain.myprogram.database \
                 -source /home/me/myproject/src/main/java \
                 -s public -s auth"
```

Running it with no arguments prints the full option list.

This connects to a PostgreSQL database, reads the schemas `public` and `auth`,
and generates or updates the classes under
`/home/me/myproject/src/main/java/org/mydomain/myprogram/database`.

!w `-source` and `-pkgroot` are **separate**: the output directory is the source
!w root with the package path appended to it.

Only PostgreSQL and Oracle are supported, and PostgreSQL is the one that is
actually exercised. Adding a database type is not much work.

## What it generates

- a class per table in the schemas it was given;
- `@ManyToOne` parent references for every foreign key, and the matching
  `@OneToMany List<T>` in the parent;
- `XxxxId` classes for tables with a compound primary key (the relations above
  are not generated for those);
- a `[classname].properties` bundle per class, holding the property names, ready
  to be used as the class's [metadata labels](../../building-pages/80-metadata/index.md);
- a `HibernateConfigurator` class that registers every generated class with
  Hibernate.

It also uses any `@MappedSuperClass` it finds: when the columns of a table match
such a base class, the generated entity extends it instead of repeating the
properties.

## Updating instead of overwriting

Whenever the generator writes a file that already exists it first copies the old
one to `<name>.java.old`. On the next run it reads *that* file rather than the
one it wrote, so the input is always the code as it was before the generator
first touched it, however often it is re-run.

That is what makes the loop below work: run, look, adjust, run again. When the
result is right, delete the `.old` files. New files get a zero-length `.old` so
the generator can tell them from originals - keep that in mind if you ever
rename them back.

## Names, and overriding them

The generator derives class and property names from table and column names, and
how good they are depends entirely on how good those are. Two ways to change
them:

- **Rename in the IDE.** The next run reads the renamed source and keeps the new
  name, because it takes existing code as the truth.
- **Override in `genHib.xml`.** The generator writes and updates this file in the
  package directory it generates into, listing every table and column with an
  empty value meaning "decide it yourself". Fill one in to override it.

So the usual cycle is: generate, read the result, put what you dislike in
`genHib.xml`, generate again. Commit the xml file - it is the record of those
decisions.

## The options

Required: `-db`, `-source`, `-pkgroot`, and at least one `-s`.

| Option | What it does |
| --- | --- |
| `-db` | connection string, `username:password@hostname[:port]/databasename` |
| `-dbtype` | `postgres` (the default) or `oracle` |
| `-source` | root directory of the java sources, without the package path |
| `-pkgroot` | root java package for the generated classes |
| `-s`, `-schema` | a schema to read; repeat for more than one |
| `-i`, `-ignore` | a table to skip; repeatable |
| `-only` | regenerate only these tables; repeatable |
| `-schema-package` | add the schema name as the last package level |
| `-asc`, `-add-schema-classname` | add the schema name to the generated class name |
| `-append-schema-name`, `-as` | always write the schema name in `@Table`, not only when several schemas were read |
| `-no-remove-schema` | keep the schema name at the start of a table name instead of stripping it |
| `-field-prefix` | prefix for generated fields, `m_` by default; `none` for no prefix |
| `-ffr`, `-force-field-rename` | rename fields even in classes that already exist |
| `-fmr`, `-force-method-rename` | rename getters and setters in existing classes |
| `-pkname` | the name to force on the primary key property, `id` by default; `none` keeps the column's own name |
| `-keep-pktype` | keep a small numeric primary key as `Integer` instead of widening it to `Long` |
| `-no-deserial` | generate PostgreSQL `serial` columns as `GenerationType.IDENTITY` instead of finding the sequence and using `SEQUENCE` |
| `-no-onechar-boolean` | do not map a `char(1)`/`varchar(1)` column with at most two distinct values to `boolean` |
| `-enum-max-field-size`, `-emfs` | largest field size still scanned for enum values (20) |
| `-noi`, `-no-identifyable` | do not implement `IIdentifyable<T>` on the generated classes |
| `-no-baseclass` | do not look for `@MappedSuperClass` base classes |
| `-match-columns-only` | match those base classes on column names only, ignoring types |
| `-nb`, `-no-bundles` | skip the `.properties` bundles |
| `-bundles` | add a language for the bundles, e.g. `-bundles nl_NL`; repeatable |
| `-destroy-constructors` | remove all constructors from existing classes |
| `-verbose` | explain every decision it makes |
