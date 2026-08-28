---
menu:
  sort: "20"
---
# Use the "example" skeleton to create a new application

A quick way to create a DomUI application is to use the "skeleton" application inside the DomUI repository. This will give you a basic DomUI application that you can then alter and extend to your needs.

The skeleton application is a mostly empty DomUI web application but with most important parts wired:

- Config file management (to configure your application)
- Database configuration and upgrade (using Hibernate for persistence and Flyway for updating the database)
- Login and rights management

The skeleton app has three Maven subprojects to separate business code, UI code and web resources, and runs out of the box.

For details on how to use it, [go to the github page for the skeleton app](https://github.com/fjalvingh/domui-skeleton) which contains detailed instructions.
