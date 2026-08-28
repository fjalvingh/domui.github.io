---
menu:
  sort: "10"
---
# What is DomUI

DomUI is an easy to use component-based framework to create AJAX rich web based user interfaces using only Java as the language and open sourced using the LGPL 2.1. It has a lot of predefined components, and allows you to easily define your own- usually without writing any Javascript. In addition it is an application framework which encapsulates many best practices, makes you DRY (Don't Repeat Yourself), and saves a developer's time by making simple things simple (while allowing for complex things).

## When should I use DomUI?

Use DomUI to create large web-based applications where there are lots of input and data screens. Using the (optional) metadata layer you can very quickly create all kinds of CRUD screens. The rich, generic and extensible metadata layer helps you by retrieving information in your (data) model classes, database etc. so that you do not have to define the same thing over and over again. One definition of "This string field is 30 characters long", for instance as a JPA/Hibernate annotation on a property, is all it takes to have all edit components reuse that value automatically. The stateful page handling makes handling data easy, and prevents serialization headaches. And data binding between business models and UI components allows for separation of business logic and UI without lots of work.

## When should I **not** use DomUI?

DomUI can be used for most applications, but is less suited for the following:

- DomUI can be styled at will, but if your goal is to create a *flashy piece of eye-candy of only 4 pages* then DomUI might not be the best for you.
- The statefulness of the UI means that developers are _extremely_ productive and can make lots of complicated forms in a short time. But "No pain, no gain": this means *UI's written in DomUI use more server resources*. The design goal for DomUI was to support 1,000-5,000 simultaneous users on a single piece of hardware. This does not mean that your app cannot grow beyond that! But you need more hardware (more machines) to support more users. If you're writing the next ebay or Google, and have to serve 10.000+ simultaneous users per server then DomUI might be less useful.

The design criteria for DomUI value developer productivity over hardware costs.

## Where can I get DomUI?

- The code was released on January 28, 2011 using the LGPL 2.1 license. This allows commercial use without having to open-source your application too. In return we ask only that you return fixes and additions to the DomUI code itself.
- I am still busy adding documentation and tutorials. In the meantime: ask questions if you have them by becoming a member of one of the mailing lists:
  - [domui-announce@googlegroups.com](mailto:domui-announce@googlegroups.com) for announcements
  - [domui-users@googlegroups.com](mailto:domui-users@googlegroups.com) for users of DomUI
  - [domui-devel@googlegroups.com](mailto:domui-devel@googlegroups.com) when you're developing for DomUI itself
- The project is maintained [on Github](https://github.com/fjalvingh/domui). Here you find the code, branches, binary releases and the bug tracker. 
- [There is a plugin](../../getting-started/intellij-plugin/index.md) for Jetbrains' IntelliJ Idea IDE that helps with developing DomUI applications.

This site contains the documentation for the code, tutorials to help you with learning and a FAQ for those questions that are frequently asked.

Next page: [a developer list of facts about DomUI](../developer-view-of-domui/index.md)
