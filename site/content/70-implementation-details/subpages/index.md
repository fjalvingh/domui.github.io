# SubPages

A **SubPage** is a page inside a page: a fragment with a conversation and a
database connection of its own. It exists for the application that loads one
`UrlPage` and then changes only parts of it, never navigating again - where
everything would otherwise share the single conversation and the single
`QDataContext` of that one page.

```java
public class AlbumEditFragment extends SubPage {
	@UIReinject
	private Album m_album;

	public AlbumEditFragment(Album album) {
		m_album = album;
	}

	@Override public void createContent() throws Exception {
		//-- built like any other page
	}
}

cp.add(new AlbumEditFragment(album));
```

[TOC]

## What it is

`SubPage` extends `AbstractPage`, which is a `Div`, so a SubPage is a node: it is
added with `add()` wherever a node can go, and it builds itself in
`createContent()` like a `UrlPage` does. A `UrlPage` can hold several of them,
and a SubPage can hold SubPages of its own.

What it adds to a plain fragment is the two things below - its own conversation,
and its own database context - which is why it is a class of its own and not
just a `Div` with a `createContent()`.

## Its own conversation

Every SubPage has a `SubConversationContext`. It is created with the SubPage and
attached to the `UrlPage`'s conversation the moment the SubPage is added to a
page, so it follows that conversation's lifecycle: when the main conversation is
detached, so is the sub-conversation, and the resources hanging off it are
managed with it.

Removing the SubPage from the page destroys its conversation - but not
immediately. Removed SubPages are collected and discarded at the *end* of the
request, so a SubPage can be taken out and put back somewhere else within one
request without losing its state. Only when the request ends without it having
been re-added is the sub-conversation destroyed.

## Its own database context

`getSharedContext()` on any node inside a SubPage returns the context of the
**nearest enclosing SubPage**, not the page's - `SubPage` overrides
`getSharedContextFactory()` to allocate from its own conversation.

So a SubPage has its own database connection and its own Hibernate session, and
acts as a fence: what is loaded, changed or flushed inside it is separate from
the rest of the page. The connection is released when the sub-conversation
detaches, like any other.

## Entities passed into it

That fence is also a trap, and it is the reason `@UIReinject` exists.

A SubPage is normally constructed with the objects it is to work on, and those
objects come from *outside* - they were loaded in the enclosing page's context.
Using them as they are would mean the SubPage changes objects belonging to
another session, in another transaction, which is exactly what the fence was
meant to prevent.

So when a SubPage is added to a page, DomUI walks its fields and **re-injects**
them: for every field holding an entity, the same record is loaded again through
*this* SubPage's context, and the new instance is put back into the field. The
SubPage then works on its own copy throughout.

Fields that hold an entity must say so:

```java
public abstract class CdbFormPage<T extends AbstractBaseEntity> extends SubPage {
	@UIReinject
	private T m_model;
```

The annotation goes on a field or a getter, and the rules around it are enforced
rather than assumed:

- a field whose **type** is a persistent class and which is *not* annotated is a
  `ProgrammerErrorException` when the SubPage is first added - in every mode;
- an annotated field may not be `final`, for the obvious reason that the
  injector has to write to it;
- `@UIReinject(false)` says "leave this one alone" - the way to keep a reference
  into the enclosing page's context deliberately.

A field whose declared type says nothing - `Object`, or a generic parameter -
cannot be judged from the type alone. In **development mode** those get a
checking injector that looks at the value at runtime and throws a
`SubPageInjectorException` when it turns out to hold an entity that nobody
annotated. In production that check is not made, so a mistake there is a bug
that only development mode will show you.

## Adding injections of your own

`SubPageInjector` holds a list of `ISubPageInjectorFactory`. Each factory is
asked, once per SubPage class, which fields need doing something to, and returns
`ISubPageInjector`s that are then run on every instance. The default factory is
the entity one described above; `DomApplication.getSubPageInjector()` is where
another is registered, for a kind of field that needs the same treatment.
