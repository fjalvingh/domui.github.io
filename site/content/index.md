# Welcome to DomUI

!i Work in progress (2026)

DomUI is a component-based Java framework for building AJAX web applications
without writing Javascript. If this is your first visit, read
[What is DomUI](introduction/what-is-domui/index.md) and then
[get started](getting-started/index.md).

## Current status

This is a newer version of the site, converted from Confluence to a static site generator. The
data is still very old, plan is to update the documentation step by step. The most recent version
is in branch skarp-master; this branch uses Java 21 and has upgraded to survive the javax -> jakarta 
absolute idiocy (I hope the idiots requiring that move lose as much money as this has cost 
the industry for absolutely nothing gained).

## The documentation

- [Introduction](introduction/index.md) - what DomUI is, and what a developer
  can expect from it.
- [Getting started](getting-started/index.md) - building DomUI and the demo, and
  creating an application of your own.
- [Building pages](building-pages/index.md) - the page model: UrlPage, state and
  conversations, SubPages, URL contexts and internationalization.
- [Components](components/index.md) - the component library, and the rules for
  writing your own.
- [Data binding and queries](data/index.md) - binding components to a model, and
  getting that model out of the database.
- [Look and feel](look-and-feel/index.md) - stylesheets, icons and animation.
- [Testing](testing/index.md) - JUnit testing DomUI applications and DomUI
  itself.
- [Development environment](development-environment/index.md) - the build, the
  tooling and the coding rules.
- [Release notes](release-notes/index.md) - what changed in DomUI 2.0.
- [FAQs and issues](faqs-and-issues/index.md) - the gotchas that keep biting.

## Demo application

There is a demo app from which we will show pages in this manual, embedded in
an IFRAME:

!demo(/)

