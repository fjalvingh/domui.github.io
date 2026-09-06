---
menu:
  sort: "10"
---
# What is DomUI

DomUI is an easy to use component-based framework to create AJAX rich web based user interfaces using only Java as the language and open sourced using the LGPL 2.1. It has a lot of predefined components, and allows you to easily define your own- usually without writing any Javascript. In addition it is an application framework which encapsulates many best practices, makes you DRY (Don't Repeat Yourself), and saves a developer's time. Its motto is:

> Make simple things simple, make complex things possible

## When should I use DomUI?

Use DomUI to create large web-based applications where there are lots of input and data screens. Using the (optional) metadata layer you can very quickly create all kinds of CRUD screens. The rich, generic and extensible metadata layer helps you by retrieving information in your (data) model classes, database etc. so that you do not have to define the same thing over and over again. One definition of "This string field is 30 characters long", for instance as a JPA/Hibernate annotation on a property, is all it takes to have all edit components reuse that value automatically. The stateful page handling makes handling data easy, and prevents serialization headaches. And data binding between business models and UI components allows for separation of business logic and UI without lots of work.

## When should I **not** use DomUI?

DomUI can be used for most applications, but is less suited for the following:

- DomUI can be styled at will, but if your goal is to create a *flashy piece of eye-candy of only 4 pages* then DomUI might not be the best for you.
- The statefulness of the UI means that developers are _extremely_ productive and can make lots of complicated forms in a short time. But "No pain, no gain": this means *UI's written in DomUI use more server resources*. The design goal for DomUI was to support 1,000-5,000 simultaneous users on a single piece of hardware. This does not mean that your app cannot grow beyond that! But you need more hardware (more machines) to support more users. If you're writing the next EBay or Google, and have to serve 50.000+ simultaneous users per server then DomUI might be less useful.

The design criteria for DomUI value developer productivity over hardware costs.

## Where can I get DomUI?

The code is [on Github](https://github.com/fjalvingh/domui) - the source, the branches, the releases and the bug tracker - under the **LGPL 2.1**, which allows commercial use without open-sourcing your own application. In return we ask only that fixes and additions to DomUI itself come back.

[Getting started](../../getting-started/index.md) is the fastest way in: the [skeleton application](../../getting-started/example-skeleton/index.md) is a working program with a database, a login and a build already in it. There is also [a plugin](../../getting-started/intellij-plugin/index.md) for Jetbrains' IntelliJ IDEA that helps with writing DomUI code.

Questions are welcome on the mailing lists:

- [domui-announce@googlegroups.com](mailto:domui-announce@googlegroups.com) for announcements
- [domui-users@googlegroups.com](mailto:domui-users@googlegroups.com) for using DomUI
- [domui-devel@googlegroups.com](mailto:domui-devel@googlegroups.com) for developing DomUI itself

Next page: [a developer list of facts about DomUI](../developer-view-of-domui/index.md)
