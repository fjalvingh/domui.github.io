---
menu:
  sort: "30"
---
# DateInput2

`DateInput2` is a box for a `java.util.Date`, with a calendar to pick from and a
button that fills in today.

```java
DateInput2 released = new DateInput2();          // a date
DateInput2 ordered = new DateInput2(true);       // a date and a time

FormBuilder fb = new FormBuilder(cp);
fb.label("Released").control(released);
fb.label("Ordered at").control(ordered);
```

!demo(to.etc.domuidemo.pages.components.input.DateInput2Page.ui, 100%, 860)

[TOC]

## It is a Text2

`DateInput2 extends Text2<Date>`, so everything on the
[`Text2` page](../text2/index.md) applies: `setMandatory()`, `addValidator()`,
`setReadOnly()`, `setDisabledBecause()`, `getValue()` reporting on the control
and throwing, `hasError()`, the change handler.

The two buttons are the ordinary `Text2` add-on buttons: a calendar button whose
click is handled in the browser, and a today button that sets the value on the
server, marks the control modified and calls the change handler. Both are
hidden when the control is read only and greyed out when it is disabled.

## Date, or date and time

| Method | What it does |
| --- | --- |
| `new DateInput2()` | a date only |
| `new DateInput2(true)` | a date and a time |
| `setWithTime(boolean)` | the same afterwards; it swaps the converter and resizes the box |
| `setWithSeconds(boolean)` | seconds as well as hours and minutes |
| `setHideTodayButton(boolean)` | leave the today button off |

`setWithTime()` does three things at once: it chooses `DateTimeConverter`
instead of `DateConverter`, sets the maximum input length (10 characters for a
date, 16 with a time, 19 with seconds) and sizes the box to match. Call it
before adding a validator that depends on the converter.

The value is always a `java.util.Date`. A date-only control still hands back a
`Date` - one whose time part is midnight.

## The format follows the locale

!! **What may be typed depends on the locale of the request**, because the
!! conversion does. `DateConverter` has three branches: Dutch, English, and
!! everything else.

| Locale | Format | How it is read |
| --- | --- | --- |
| `nl` | `dd-MM-yyyy` | leniently: the short forms below are all accepted |
| `en` | `yyyy-MM-dd` | strictly - anything else is *Invalid date* |
| anything else | the JDK's SHORT format for that locale | strictly |

In a Dutch locale `13/3/2012`, `13-3-13`, `13/3` (this year) and `13032012` all
arrive as the same date - `/`, `.` and `-` are interchangeable, a two-digit year
is 19yy above 29 and 20yy otherwise, and a missing year is the current one. The
browser rewrites what was typed into the full format as soon as the field is
left.

!! That rewriting is **not locale-aware**: it assumes the day-month-year shape
!! whatever the request's locale is. In an English locale, typing `13-3-13` into
!! a `DateInput2` leaves `2013-03-13` in the box while the value the server took
!! from it is the year **13**, and typing `13/3/2012` opens a browser alert
!! saying *Invalid date* rather than reporting the error the way every other
!! control does.

Where the locale of a request comes from, and how to change it, is described
under [metadata and internationalization](../../../building-pages/80-metadata/index.md).

## Making one from a property

```java
DateInput2 di = DateInput2.createDateInput(Invoice.class, "invoiceDate", true);
```

`createDateInput(clz, property, editable)` and its `PropertyMetaModel` variants
build a control configured from the property: the time part is switched on when
the property's temporal presentation is `DATETIME`, and the property's
validators are added.

A form builder does the same by itself - `ControlCreatorDate` claims every
`java.util.Date` property - so `fb.property(invoice, Invoice_.invoiceDate())`
already yields a `DateInput2`.
