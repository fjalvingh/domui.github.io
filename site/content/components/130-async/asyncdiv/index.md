---
menu:
  sort: "20"
---
# AsyncDiv

The same delayed job as an [`AsyncContainer`](../asynccontainer/index.md), with
the work and the screen kept apart: the job only *collects*, and the component
builds the result afterwards - on the page's own thread, where it is allowed to.

```java
public class ReportDiv extends AsyncDiv<ReportJob> {
    public ReportDiv(ReportJob job) {
        super(job, "Building the report");
    }

    @Override
    public void createContent(ReportJob task) throws Exception {
        for(String line : task.getLines()) {          // Read what the job collected
            add(new Div().add(line));
        }
    }
}
```

!demo(to.etc.domuidemo.pages.components.async.AsyncDivPage.ui, 100%, 560)

[TOC]

## How it is used

It is **abstract** and generic over the job: `AsyncDiv<T extends IAsyncRunnable>`.
You write a subclass, implement `createContent(T task)`, and hand it the job.

| Constructor | What it gives |
| --- | --- |
| `AsyncDiv(T runnable)` | the job, and no heading |
| `AsyncDiv(T runnable, String what)` | ...with that heading over it while it runs |

While the job runs the component shows an `AsyncContainer` under that heading.
When it succeeds the component empties itself - heading and all - and calls
`createContent(task)` with the job object, so whatever the job put in its own
fields is what the screen is built from. When it fails the heading **stays**, with
the error under it, which is what tells the user which of several jobs went
wrong.

!! The job's fields are written on one thread and read on another. **Synchronise
!! them.** A list built without it is a race, and an intermittently empty report
!! is a miserable thing to debug.

## What it does with a failure

That is the other half of what the component buys you:

| How it ended | What happens |
| --- | --- |
| finished | `createContent(task)` builds the result |
| cancelled | a warning line saying so |
| threw a `MessageException` | an error line with its message - the exception meant for a user |
| threw anything else | an error line, plus a foldable panel with the stack trace |

`createError(task, exception, cancelled)` is `protected`, so a screen that wants
to say something of its own about a failure overrides that instead of catching in
the job.

## Which of the two

| | `AsyncContainer` | `AsyncDiv` |
| --- | --- | --- |
| who builds the result | the job, on the worker thread | the component, on the page's thread |
| errors | a message box with the stack trace | a message line, with the trace folded away |
| written as | a lambda or a small class | a subclass with `createContent(task)` |

For a short job whose answer is a sentence, `AsyncContainer` is less to write.
For a job whose result is a real screen, `AsyncDiv` is the one: building
components is what `createContent()` is for, and it runs where that is safe.
