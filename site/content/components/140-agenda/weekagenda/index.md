---
menu:
  sort: "10"
---
# WeekAgendaComponent

A day, a work week or a full week of appointments, drawn on a raster of half
hours. It takes its appointments from a `ScheduleModel` and follows that model
while the user works.

```java
BasicScheduleModel<ScheduleItem> model = new BasicScheduleModel<>();
model.addWorkHour(monday0830, monday1730);
model.addItem(new BasicScheduleItem("1", start, end, "Release meeting", null, "meeting", null));

WeekAgendaComponent<ScheduleItem> agenda = new WeekAgendaComponent<>();
add(agenda);
agenda.setMode(ScheduleMode.WORKWEEK);
agenda.setDate(new Date());
agenda.setModel(model);
```

!demo(to.etc.domuidemo.pages.components.agenda.WeekAgendaPage.ui, 100%, 800)

[TOC]

## The period it shows

`setDate()` says which day, `setMode()` says how much around it:

| Mode | What is shown |
| --- | --- |
| `ScheduleMode.DAY` | that one day |
| `ScheduleMode.WORKWEEK` | the monday to friday of that week |
| `ScheduleMode.WEEK` | the sunday to saturday of that week |

The date is moved to the start of the period, so any day inside the week does.
Moving a week forward is therefore a matter of adding seven days to the date the
page keeps and rebuilding, which is what the buttons above the demo do.

## The hours it shows

The raster is not fixed: it runs from an hour before the earliest work hour the
model reports to an hour after the latest, rounded to whole hours. A model
without work hours gets 8:00 to 18:00.

That means the work hours do two things at once - they say when people work, and
they decide how much of the day is on the screen. A model that reports 08:30 to
17:30 produces a raster of 08:00 to 18:00.

## What an appointment looks like

`DefaultScheduleItemRenderer` draws the image, the type, the name, the time with
the duration behind it, and the details on the next line. To change that, set an
item renderer of your own - usually one that extends the default and adds
something:

```java
agenda.setItemRenderer(new DefaultScheduleItemRenderer<ScheduleItem>() {
    @Override public void render(WeekAgendaComponent<ScheduleItem> c, NodeContainer target, ScheduleItem item) throws Exception {
        super.render(c, target, item);
        if(item.getType() != null)
            target.addCssClass("app-" + item.getType());        // The colour comes from css
    }
});
```

The renderer fills the node; **where** the appointment lands and how wide it is
are decided in the browser from the start and end times, including the lanes that
overlapping appointments are put in.

## Making an appointment by dragging

Dragging over an empty piece of the raster asks for a new appointment there:

```java
agenda.setNewAppointmentListener((start, duration) -> askAndAdd(start, duration));
```

The listener gets the start date and the duration in milliseconds, and is
expected to do something about it - usually ask the user what the appointment is
and add it to the model. Adding it to the model is all it takes for the
appointment to appear: the component listens to the model.

```java
model.addItem(new BasicScheduleItem(id, start, new Date(start.getTime() + duration), what, null, "meeting", null));
```

Without a listener the raster does not react to dragging at all.

## Changing the appointments

Every change to the model reaches the component:

| On the model | On the screen |
| --- | --- |
| `addItem(item)` | the appointment is drawn |
| `deleteItem(item)` | it disappears |
| `changeItem(item)` | it is drawn again, at its new time |
| `addWorkHour(...)`, `addHoliday(...)` | the whole agenda is rebuilt: the raster can change |

An application whose model comes from a database calls `changeItem()` after it
saved, and the screen follows.
