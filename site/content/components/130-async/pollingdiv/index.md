---
menu:
  sort: "30"
---
# PollingDiv

A piece of the screen that keeps itself up to date. Nothing on the page does the
updating: the browser asks the server every couple of seconds whether anything
changed, and this component gets asked the same question.

```java
public class QueueLength extends PollingDiv {
    private Span m_count;

    @Override public void createContent() throws Exception {
        m_count = new Span();
        add(m_count);
    }

    @Override public void checkForChanges() throws Exception {
        m_count.setText(queue.size() + " waiting");
    }
}
```

!demo(to.etc.domuidemo.pages.components.async.PollingDivPage.ui, 100%, 520)

[TOC]

## The one method

`checkForChanges()` is called on every poll - by default every two and a half
seconds - and whatever it changes goes to the browser as an ordinary delta.

The default implementation **rebuilds the whole component**. That is the simplest
thing that works and the wrong thing for anything but the smallest div: it throws
the built tree away, so the delta is large, the screen flickers and anything the
user was doing inside it is lost.

!! Override `checkForChanges()` and change **only what changed**. Keep the nodes
!! that have to be updated in fields of the component - that is the one place the
!! rule against holding components in fields does not apply, because a polling
!! div that rebuilds itself is exactly what you are avoiding.

## Registering

There is nothing to register and nothing to clean up: the component adds itself
to the conversation's pollers when it is added to a page and removes itself when
it is taken off. Put it on the screen and it polls; remove it and the polling
stops, along with the requests.

## What it costs

A request every couple of seconds, per browser, for as long as the page is open.
That is cheap for one user and not cheap for a thousand, so it is worth being
deliberate:

- a value that changes on its own - a queue length, a job's state, a temperature
  - is what this is for;
- a value that changes because the *user* did something does not need it; the
  click that changed it is already a request;
- a long job with an end is an [`AsyncContainer`](../asynccontainer/index.md),
  which stops polling when it finishes.
