---
menu:
  sort: "40"
---
# The BreadCrumb2 component

This component shows a "breadcrumb" of items forming a path. It is normally used to show a path that lead to the current action or the current node in some tree. The component looks like this:

![](image2018-10-7_21-33-25.png)

(here on a black background).

Each of the parts of the breadcrumb is defined by an instance of BreadCrumb2.IItem, an interface which has getters for icon, name, title. The interface also has a clicked() method which will be called when the corresponding item is clicked. A basic implementation of IItem, BreadCrumb2.Item, has a constructor where you can add all of these values.

The breadcrumb2 component accepts a list of these as either a constructor parameter or set with setValue(). The list can be an IObservableList in which case the component will refresh itself automatically when the list contents changes.

A common use for this component is to be used to show the current page stack, as in the example above. For this you can call the static method BreadCrumb2.createPageCrumb() which will create the list of stack items and create a breadcrumb from it. The above example was created as follows in PageHeader.java:

```
add(BreadCrumb2.createPageCrumb("Home", true));
```

The CSS for the breadcrumb can be found in \_breadcrumb2.scss, it contains variables that can be overridden in the apps \_variables.scss file.
