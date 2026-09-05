---
menu:
  sort: "10"
---
# BreadCrumb2

The path that led to where the user is, as steps that can be clicked. Most of
the time that path is the page stack, and one call makes the whole thing:

```java
cp.add(BreadCrumb2.createPageCrumb("Home", true));
```

!demo(to.etc.domuidemo.pages.components.navigation.BreadCrumb2Page.ui, 100%, 900)

[TOC]

## The page stack as a crumb

`createPageCrumb()` reads the shelved page stack of the window session and makes
one step per page on it, with the application's root page in front:

| Call | What it gives |
| --- | --- |
| `createPageCrumb(String homeName)` | the stack, with a back arrow in front of it |
| `createPageCrumb(String homeName, boolean withBack)` | ...and a say in that arrow |
| `getPageStacktems(String homeName)` | the same steps as a list, to put in a crumb yourself |

`homeName` is the text next to the home icon; pass `null` for the icon alone. The
back arrow appears only when there *is* a page to go back to and that page is not
the root page - so on a screen opened straight from the menu there is nothing but
home.

The text of a step is the page's `getPageTitle()`, so a page that computes a
title of its own ("Artist: Led Zeppelin") says that in the crumb; a page with no
title at all falls back to its class name.

The last step is the page the user is on: it is drawn differently and clicking it
does nothing. Every other step moves to its page, and the home step to the
application's root page.

## A path of your own

The crumb does not care that the steps are pages. It is a list of `IItem`, and
each item says what it looks like and what happens when it is clicked:

```java
public interface IItem {
    NodeBase getIcon();                     // null for no icon
    String getName();                       // the text of the step
    String getTitle();                      // its tooltip
    void clicked(IItem item) throws Exception;
}
```

`BreadCrumb2.Item` is the ready-made implementation - icon, name, title and a
lambda - so a crumb over a genre tree, a folder or the steps of a wizard is a
list of those:

```java
List<IItem> path = new ArrayList<>();
path.add(new Item(Icon.faDatabase.createNode(), "Chinook", "The whole catalogue", it -> open(catalogue)));
path.add(new Item(null, "Rock", null, it -> open(genre)));
path.add(new Item(null, "Led Zeppelin", null, it -> open(artist)));
cp.add(new BreadCrumb2(path));
```

| Method | What it does |
| --- | --- |
| `new BreadCrumb2()` | an empty crumb, to be filled with `setValue()` |
| `new BreadCrumb2(List<IItem>)` | ...with its path |
| `setValue(List<IItem>)` / `getValue()` | replace the whole path; the crumb redraws |

## A crumb that follows its list

When the list handed to it is an `IObservableList`, the crumb listens to it: add
a step to the list or remove one, and the crumb rebuilds itself. Nothing needs to
tell it, and the page it is on is not rebuilt.

```java
private final ObservableList<IItem> m_path = new ObservableList<>();    // The state, in a field
...
cp.add(new BreadCrumb2(m_path));                                        // The component, local
...
button.setClicked(a -> m_path.add(new Item(null, "Level " + m_path.size(), null, null)));
```

That is the whole difference between the two lists: a plain `List` is a path the
code replaces with `setValue()`, an observable one is a path the code *changes*.

## What it looks like

The crumb writes a `ul` of arrow-shaped steps under `.ui-brcr2`, with the last
step marked `.ui-brcr2-a`. The colours are scss variables in `_breadcrumb2.scss`
(`$brcr2-bg`, `$brcr2-color`, `$brcr2-hover`, `$brcr2-sel-bg`,
`$brcr2-sel-color`), so an application restyles the crumb by overriding those in
its own `_variables.scss` rather than by writing css.
