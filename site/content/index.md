# Welcome to DomUI

!i This documentation is being updated and is woefully incomplete 8-/ It's hard to do everything by yourself :wink:

<a id="current-status"></a>

# Current status

I'm currently working on DomUI 2.0. This will be a big change where a lot of problematic things will be rewritten. As a consequence the master branch's code is unstable and a work in progress. This also has its effect on [the demo application](https://etc.to/demo/) as that is also updated, changed, and uses the unstable 2.0 master.

Progress on the work is [tracked on github](https://github.com/fjalvingh/domui/projects/1), and the [github issue list](https://github.com/fjalvingh/domui/issues) and planboard should be updated with things to do/done.

<a id="getting-started"></a>

# Getting started

- [What is DomUI](what-is-domui/index.md)
- [Quick DomUI facts for a developer](developer-view-of-domui/index.md)
- [Checking out DomUI itself and running the demo application in Maven and IntelliJ](getting-started/index.md)
- [Using the skeleton app as the basis for a new application](use-the-example-skeleton-to-create-a-new-application/index.md) (encouraged)
- [Using a Maven artefact to create a bare bones application](getting-started/creating-a-new-domui-application-from-scratch-using-a-maven-archetype/index.md) (discouraged)
- [Installing the IntelliJ Idea plugin for DomUI](using-the-domui-intellij-plugin/index.md)

<a id="technical-reference-documentations-wip"></a>

## Technical reference documentations (WIP)

- [Generating and using typed properties](using-typed-properties-the-property-annotations-processor/index.md)
- [Component Overview](domui-component-overview/index.md)
- Application initialization
  - [Header Contributors](header-contributors/index.md)
- Data Binding
  - [DomUI Data binding](data-binding/index.md)
  - [Data binding technical description](data-binding-how-does-it-work/index.md)
  - Data binding FAQ
    - You cannot bind a control property with a dotted path
- [Internationalization](internationalization-and-resource-bundles/index.md)
  - [The locale for a request](internationalization-and-resource-bundles/locale-handling/index.md)
- Using the database
  - [The QCriteria query API](the-generic-query-framework-qcriteria/index.md)
- Styling
  - [Sass and SCSS support](sass-scss-support/index.md)
  - [Using Icons in DomUI applications](icons/index.md)
  - [Playing with flexbox and grid layout](playing-with-flexbox-layout/index.md)
  - [CSS tips and tricks](css-problems-and-solutions/index.md)
- Writing DomUI components
  - [Component CSS rules and implementation details](domui-component-rules/index.md)
  - [LookupInput/LookupInput2 layout and behavior details](domui-20-changes/lookupinput-lookupinput2-behavior-and-layout-rules/index.md)
  - Text2 layout and behavior details
- DomUI Internals
  - [DomUI page state management: Pages and Conversations](domui-state-management/index.md)
  - [SubPages](subpages/index.md) (2.0)
  - [URL Contexts](url-contexts/index.md)
- DomUI JUnit tests
  - [Writing DomUI Junit tests](junit-testing-domui/index.md)
  - [Using Mockito: pitfalls to be aware of](mockito-pitfalls/index.md)
  - [The HtmlEditor tests](junit-testing-domui/the-htmleditor-junit-tests/index.md)
  - [Data binding tests](tests-data-binding/index.md)

<a id="domui-tools"></a>

## DomUI tools

- [The Hibernate/JPA POJO generator](the-hibernate-jpa-pojo-generator/index.md)
- The dbpool database pool manager

<a id="participating-in-development"></a>

## Participating in development

We can always hope, can't we?

- [What's new / what's changing](domui-20-changes/index.md)
- [Github / TravisCI / DeployHQ details](domui-github-environment/index.md)
- [FAQs and issues](faqs-and-issues/index.md)

<a id="reference-and-todos"></a>

## Reference and todo's

- [Installing Oracle Database 12c R2 on Ubuntu 18.04](https://domui.atlassian.net/wiki/spaces/~admjal/pages/20086805/Install+Oracle+Database+12c+r2+on+Ubuntu+18.04.)
- Sass and Scss
  - [The SassMeister website to quickly test Sass fragments](https://www.sassmeister.com/) is a Godsend.
- Maven
  - [Using the Eclipse compiler inside Maven builds](using-the-eclipse-java-compiler-ecj-in-maven-builds/index.md)
- CSS Styling frameworks
  - [Bulma looks quite promising](https://bulma.io/) (Thanks Yoeri). It also has a [theme site](https://jenil.github.io/bulmaswatch/).
    - [Reports about experimenting with Bulma](playing-with-bulma/index.md)
  - [Materializecss](http://materializecss.com/color.html) which shows a way to style the upload button
  - [Semantic UI](https://semantic-ui.com/)
  - Juiced
    - [Has some nice alternative to checkbox: switches](http://juicedcss.com/bower_components/juiced/docs/components.html#buttons)
  - Spectre
    - Has a very interesting "loading" modifier to classes - [see the css in the examples](https://picturepan2.github.io/spectre/elements.html#forms)
  - Bootstrap does not seem to be a good plan: it changes versions quickly once one is there, but the last one is a complete rewrite and has taken > 2 years already. It also seems big and bloated.
- Form designs worth looking at
  - [https://codepen.io/nikhil8krishnan/pen/gaybLK](https://codepen.io/nikhil8krishnan/pen/gaybLK) and [https://codepen.io/lukeandrewreid/pen/OVPGXN](https://codepen.io/lukeandrewreid/pen/OVPGXN)
- [Very good Antlr4 walkthrough](https://tomassetti.me/antlr-mega-tutorial/)
- Graphs
  - [http://fperucic.github.io/treant-js/](http://fperucic.github.io/treant-js/)

