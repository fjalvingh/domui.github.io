---
menu:
  sort: "80"
---
# Tree3

`Tree3<T>` shows a tree: records that contain records. It asks a model for the
children of a node, and only when that node is opened - so a tree over a large
structure costs one query per opened branch rather than one for the whole thing.

```java
Tree3<DemoNode> tree = new Tree3<>(model);
cp.add(tree);
tree.setContentRenderer((node, value) -> {
    node.add(value.getIcon().createNode());
    node.add(value.getText());
});
```

!demo(to.etc.domuidemo.pages.components.tables.Tree3Page.ui, 100%, 760)

[TOC]

## The model

`ITreeModel<T>` is what the tree asks, and it is four questions:

```java
T getRoot() throws Exception;
int getChildCount(T item) throws Exception;
T getChild(T parent, int index) throws Exception;
T getParent(T child) throws Exception;
```

plus `hasChildren(item)`, which defaults to `getChildCount(item) != 0` and is
worth overriding when knowing *whether* there are children is cheaper than
counting them - that is the call that decides whether a node gets an expand
button.

A model that changes tells the tree through `ITreeModelChangedListener`:
`onNodeAdded`, `onNodeUpdated` and `onNodeRemoved` update just that part of the
screen.

## The tree

| Method | What it does |
| --- | --- |
| `new Tree3<>(ITreeModel<T>)` | the model; `setModel()` replaces it |
| `setContentRenderer(IRenderInto<T>)` | what a node's label looks like - everything else is the tree's own |
| `setShowRoot(boolean)` | whether the root itself is a node on screen |
| `expandNode(T)` / `collapseNode(T)` / `toggleNode(T)` | open and close from code |
| `collapseAll()` | close everything |
| `isExpanded(T)` | is this node open |
| `getTreePath(T)` | the nodes from the root down to this one |

## Selecting and clicking

| Method | What it does |
| --- | --- |
| `setCellClicked2(ICellClicked2<T>)` | called when a node is clicked, with the click info |
| `setSelectedValue(T)` / `getSelectedValue()` | the selected node |
| `setNodeSelectablePredicate(INodePredicate<T>)` | which nodes may be selected at all |
| `setEnableDoubleclickExpand(boolean)` | double-clicking a node opens it; on by default |

A node the predicate refuses gets the css class `ui-tree3-unselectable` and
cannot become the selected value, which is the usual way to let a user pick a
leaf but not a branch.

## What it renders

Nested `ul`/`li`, which is what a tree is:

```html
<div class="ui-tree3">
  <ul class="ui-tree3-list ui-tree3-rootlist">
    <li class="ui-tree3-item ui-tree3-closed ui-tree3-branch">
      <div class="ui-tree3-fbtn ui-tree3-closed"></div>
      <span class="ui-tree3-label">…your content…</span>
    </li>
  </ul>
</div>
```

Three things are worth knowing about that structure, because the css depends on
them:

- the **fold button** is a div with `ui-tree3-opened` or `ui-tree3-closed`, sized
  in `em` and pulled left with a negative margin, so it sits over the branch
  line rather than beside it;
- the **branch lines** are not elements: they are a `:before` on the `li`,
  absolutely positioned from top to bottom with a `border-left`, so a line is
  automatically as long as the item it belongs to - short for a closed node,
  long for an open one;
- the **label** is a span containing whatever the content renderer added, and
  nothing else; the tree owns everything around it.

An item is marked `ui-tree3-branch` or `ui-tree3-leaf`, and `ui-tree3-opened` or
`ui-tree3-closed`, so a theme can style all four states without the component
knowing about any of them.
