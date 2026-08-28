---
menu:
  sort: "10"
---
# The FormBuilder (form4 version)

DomUI does not have a specific "form" component. Instead forms are built either by hand by adding components, or forms are being built by a *Form Builder*. A form builder is not a component by itself (so it is not added to a page), but it is a utility that helps building a form by creating the appropriate layout and input nodes.

DomUI contains many FormBuilders, most of them are attempts to "get it right". This describes one of them: FormBuilder in package form4.

TBD

<a id="binding-to-controls"></a>

## Binding to controls

By default the value for controls will be bound to the instance and property passed to the form builder:

```
fb.property(d, Definition.pNAME).control();
```

This will cause the "value" property of the automatically created control to be bound to the "name" property of the thing that is in "d".

While value binding is the most common kinds of binding we have others that can be done too.

<a id="readonly-binding"></a>

### ReadOnly binding

The readOnly property of a control can be directly set in the builder by adding readOnly() or readOnly(boolean) to the build pattern. But it's more useful to bind the readOnly property to some business logic property that specifies whether the data is editable or not. This can be done by the following methods:

- readOnly(Object instance, String property) binds the next component to the specified (boolean) property on instance. As soon as this property changes value then the control's readOnly property will change too.
- readOnlyAll(Object instance, String property) bind **all next components** to the specified property, until readOnlyAll() (without parameters) gets called.

The readOnly property will be set by the first method above that defines some readOnly value or binding. This means that for instance a readOnly() call "wins" over an earlier readOnlyAll(xxx) call.

<a id="disabled-binding"></a>

### Disabled binding

Similar to the readOnly binding we have the same methods to set the disabled property:

- setDisabled(boolean)
- setDisabled(Object instance, String propertyName);
- setDisabledAll(Object instance, String propertyName);

In addition we also have setDisabledBecause() forms of the above to both disable a control and to also set a reason for why it is disabled. These can be bound as above too.
