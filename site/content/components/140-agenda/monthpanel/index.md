---
menu:
  sort: "20"
---
# MonthPanel

One month as a small calendar: a row per week, the week number in front of it,
and the days of the month before and after the one shown greyed out. It is what
you put next to something else to pick a day with.

```java
MonthPanel mp = new MonthPanel();
add(mp);
mp.setDate(new Date());
mp.setDayClicked((panel, date) -> {
    m_date = date;                       // The page keeps the date...
    forceRebuild();                      // ...and rebuilds with it
});
```

!demo(to.etc.domuidemo.pages.components.agenda.MonthPanelPage.ui, 100%, 420)

[TOC]

## Which month

`setDate()` takes any date in the month to show; the panel moves it to the first
day itself. Two panels next to each other, one with today and one with today plus
a month, is the usual way to show a period that can cross a month boundary.

`setFirstDay()` says which weekday a week starts on - `Calendar.MONDAY` by
default, `Calendar.SUNDAY` for an American calendar.

## Clicking a day

There is no click handler by default, and without one the panel is a calendar to
look at: the day cells get neither the pointer nor the hover.

`setDayClicked()` makes the days clickable. The handler is given the panel and
the date that was clicked:

```java
mp.setDayClicked((panel, date) -> agendaDate = date);
```

## Marking days

Marking is how an application shows which days have something on them - an
appointment, a deadline, a day that is fully booked:

| Call | What it does |
| --- | --- |
| `setMarked(date, css)` | adds the css class to that day's cell, if the day is on the panel |
| `setUnmarked(date, css)` | takes it off again |
| `unmarkAll(css)` | takes it off every cell of the panel |

Passing `null` as the class uses `MonthPanel.MARKED` (`ui-mp-mrk`), which the
theme draws as a highlighted day. Any other class is one of your own, so several
kinds of marking can be shown at once:

```java
mp.unmarkAll("app-busy");
for(Date d : fullyBookedDays)
    mp.setMarked(d, "app-busy");
```

A date that is not on the panel is ignored, so a caller can mark a whole month's
worth of dates on both panels without checking which one holds what.
