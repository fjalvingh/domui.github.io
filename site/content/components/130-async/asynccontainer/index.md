---
menu:
  sort: "10"
---
# AsyncContainer

A box that stands where the answer will be: a spinner, how far the job got, and a
button to give up. When the job is done, the box replaces itself with the result.

```java
where.add(new AsyncContainer(p -> {
    p.setTotalWork(rows.size());
    ...
    Div result = new Div();
    result.add("Done: " + count + " rows");
    return result;                       // ...and this replaces the container
}));
```

!demo(to.etc.domuidemo.pages.components.async.AsyncContainerPage.ui, 100%, 620)

[TOC]

## Two ways to write the job

| Constructor | The job is |
| --- | --- |
| `AsyncContainer(IActivity)` | `Div run(Progress)` - it **builds the result itself** and the container is replaced by it |
| `AsyncContainer(IAsyncRunnable)` | `void run(Progress)` - it produces nothing, and a listener puts the result on the screen |
| `AsyncContainer(IAsyncRunnable, IAsyncCompletionListener)` | ...with that listener |

`IActivity` is the short way and is enough for most jobs. Its one catch is that
the `Div` is built **on the worker thread**, so it may hold only what the job
computed - no page components, nothing from the page at all.

Where that is awkward, [`AsyncDiv`](../asyncdiv/index.md) does the same job with
the result built afterwards, on the right thread.

## What it looks like while it runs

| Method | What it does |
| --- | --- |
| `setAbortable(boolean)` | whether there is a cancel button; there is by default |
| `setBusyMarkerSrc(String)` | the spinner image |
| `inline()` | make it an inline block, not abortable, with the small busy marker - for a spinner inside a line of text |
| `doCancel()` | cancel it from code |

The progress line is the percentage plus the text the job last reported, so
`p.setCompleted(i, "row " + i)` is what makes it say something useful.

!! Cancelling is a **request**, not a kill. It marks the progress as cancelled and
!! interrupts the thread; a job that never looks at `p.isCancelled()` and never
!! reacts to an interrupt keeps running to its end.

## When it ends

| How it ended | What the user sees |
| --- | --- |
| the job returned a `Div` | the container is replaced by it |
| the job returned null | "no results", or "cancelled" if it was |
| the job threw | a message box with the message and the stack trace |
| it was cancelled | a message saying so |

An exception is therefore never silently lost - which matters, because the job
ran on a thread nobody was watching.

## What the job may not touch

The rule the whole group shares, and the reason most mistakes here happen: while
the job runs, **the page is not active**. No components, no page fields, and not
the page's shared `QDataContext` - a job that queries makes an unmanaged context
of its own and closes it. See [the group page](../index.md).
