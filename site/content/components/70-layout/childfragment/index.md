---
menu:
  sort: "110"
---
# ChildFragment

`ChildFragment<P, C>` shows the children of a record: give it the parent and the
property holding its children, and it works out the rest.

```java
ChildFragment<Artist, Album> albums = new ChildFragment<>(artist, Artist_.albumList());
cp.add(albums);
albums.column(Album_.title()).label("Album").width(50);
albums.onClick(album -> UIGoto.moveSub(AlbumEditPage.class, "id", album.getId()));
```

!demo(to.etc.domuidemo.pages.components.layout.ChildFragmentPage.ui, 100%, 700)

[TOC]

## What it does for you

From the parent and the `QField` alone it:

- checks that the property really is a **downward relation to a collection**, and
  says so plainly if it is not;
- works out the child type from the collection's generic type;
- **binds itself to the relation**, so it shows whatever the parent's collection
  holds at any moment;
- puts the children in a [`DataTable`](../../60-tables-and-trees/datatable/index.md),
  using the list *as an observable list* when it is one - which a Hibernate
  relation is. Adding a child to the parent's collection then adds a row,
  with the fragment told nothing.

| Method | What it does |
| --- | --- |
| `column(QField<C,V>)` / `column()` | a column, exactly as on a [`RowRenderer`](../../60-tables-and-trees/rowrenderer/index.md) |
| `setRenderer(RowRenderer<C>)` | replace the whole row renderer |
| `onClick(ConsumerEx<C>)` | what clicking a child does |
| `setOnNew(ConsumerEx<C>)` | show an **Add** button, and be called with a new child that already has its parent set |
| `setPageSize(int)` | rows per page; ten by default |
| `getValue()` / `setValue(List<C>)` | the children, as the binding sees them |

## Why it is worth having

The master/detail screen - a record with its lines under it - is the one screen
every application writes many times. Written by hand it is a query, a model, a
table, a renderer and the code that keeps them in step with the record on
screen. This is four lines, and the part that usually goes wrong - the table
still showing the previous record's children - cannot happen, because the
fragment is bound to the relation rather than filled from it.

!! The property must be the collection side of a relation (`@OneToMany`), and
!! the fragment must be **added to the page**: like any control, its binding only
!! works once it is part of the tree.
