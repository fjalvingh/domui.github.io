---
menu:
  sort: "10"
---
# Checking out DomUI and running the demo

To discover how DomUI works, to fix issues or to add new DomUI code you need to check out
the repository, build it and run the demo application that lives inside it.

The demo application also runs live on [${demo}](${demo}), so if all you want is to *see*
DomUI you do not need any of this.

## Checking out the repository from github

The branch that matters is **`skarp-master`**: it is the tip of development, the default
branch of the repository and the branch the releases are cut from. A plain clone gets it:

```bash
$ git clone https://github.com/fjalvingh/domui mydomuibranch
```

This makes a clone of the git repository in a new directory "mydomuibranch".

The only other branch of interest is `1.1`, the long-since released 1.1 version; it gets
no work. Everything else in the repository is a feature branch or a dependabot branch.

!w The above checkout does an anonymous checkout, meaning that pushing back is hard. If
!w you already have a github account you can of course also use the usual ssh url to
!w access the repository, i.e. `git@github.com:fjalvingh/domui`.

## Building the code

DomUI builds on **Java 21** and uses Maven as its build tool. You need **Maven 3.9 or
newer** ([which you can find here](https://maven.apache.org/download.cgi)), running on a
JDK 21: if the default `java` on your machine is a different version, point `JAVA_HOME` at
a JDK 21 before starting Maven. Linux users should download Maven rather than use the
version their distribution packages, as that is usually old.

To compile do the following:

```bash
$ cd mydomuibranch
$ mvn clean install -DskipTests -Dmaven.javadoc.skip=true
```

You might wonder why the above command line disables tests and Javadoc generation.
Javadoc generation is not usually interesting when building and it takes a lot of time,
so this speeds up the build.

The tests are disabled because a full test run needs more than a JDK. Next to the unit
tests there are Selenium integration tests (the `IT*` classes) which start Jetty and then
drive the demo application through a headless Chrome, so running them needs Chrome
installed. `-DskipTests` switches off the unit tests, the integration tests and the Jetty
run that serves them in one go. The chromedriver matching your Chrome is downloaded
automatically when the tests do run, so there is nothing to install by hand for that.

!i DomUI compiles with the **Eclipse batch compiler (ecj)** rather than javac, through the
!i `plexus-compiler-eclipse` plugin. That is what makes the `@NonNull`/`@Nullable`
!i annotations in the source into compile-time null checks. See
!i [Using the Eclipse Java compiler (ecj) in Maven builds](../../development-environment/ecj-in-maven/index.md)
!i for how that is configured.

## Running the demo web application

To run the demo application after the build change to the demo application's directory
(`to.etc.domui.demo`) and run the following:

```bash
$ cd to.etc.domui.demo
$ mvn jetty:run
```

This will start a web server on port 8088; you can reach the demo application at:
[http://localhost:8088/demo/](http://localhost:8088/demo/).

To stop the web server again press CTRL+C on the terminal running maven.

The demo needs no database setup: it uses an embedded HSQLDB database which is created
and filled with the Chinook example data on first use, in a temporary directory when
started from Maven and in `/tmp/demoDb` when started from an IDE.

## Working on DomUI with IntelliJ IDEA

IntelliJ IDEA has great support for Maven out of the box, and makes it very easy to work
on DomUI. To work with IntelliJ on the branch we just checked out do the following:

- Start IntelliJ and select "Open" from the welcome screen.
- Select the root directory of the repository you cloned. In the above example you would
  select the "mydomuibranch" directory.
- IntelliJ recognizes the Maven project and imports the whole reactor. Wait for that to
  finish before doing anything else.

Then check two things:

- Press F4 (or select File → Project Structure from the menu) and make sure that a **JDK
  21** is selected as the project SDK, and that the project language level is **21** as
  well. If no SDK is present, add one with the "Add SDK" button.
- The repository ships an `.idea/compiler.xml` which already selects the Eclipse compiler,
  so IntelliJ compiles the same way Maven does. If compilation gives errors that Maven
  does not give, check Settings → Build, Execution, Deployment → Compiler → Java Compiler
  and set "Use compiler" to **Eclipse**.

Always run `mvn clean install` from the command line at least once before building inside
IntelliJ. Parts of the source are generated during the Maven build - parser code and the
property annotation processor's output - and IntelliJ's Maven support does not generate
them on its own. Without that first Maven build you get compile errors about classes that
do not exist yet.

Once the build works you can start the demo application with the `demo` run configuration
that comes with the repository. It deploys the exploded war of `to.etc.domui.demo` on a
local **Tomcat 11** at [http://localhost:8088/demo/](http://localhost:8088/demo/), so you
need a Tomcat 11 installation registered in IntelliJ under Settings → Build, Execution,
Deployment → Application Servers. Run it with either the run or the debug button.

If the run configuration does not appear, or refuses to start, you most likely lack that
Tomcat installation; IntelliJ's own documentation on application servers explains how to
add one.
