---
menu:
  sort: "30"
---
# Using the Eclipse Java compiler (ecj) in Maven builds

DomUI is compiled by the **Eclipse batch compiler (ecj)**, not by javac. It is
fast, it has far more warnings and errors that can be switched on per project,
and it can do [null analysis](https://help.eclipse.org/latest/topic/org.eclipse.jdt.doc.user/tasks/task-using_null_annotations.htm):
with `@NonNull` and `@Nullable` on your code, a null that cannot happen becomes
a compile error instead of an NPE in production.

To use it in Maven you need the `plexus-compiler-eclipse` compiler for
`maven-compiler-plugin`, and **nothing else**. This is the configuration DomUI's
own root pom uses:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.14.0</version>
    <configuration>
        <compilerId>eclipse</compilerId>
        <source>21</source>
        <target>21</target>

        <compilerArgs>
            <arg>-properties</arg>
            <arg>${project.basedir}/.settings/org.eclipse.jdt.core.prefs</arg>
            <arg>-enableJavadoc</arg>
            <arg>-nowarn</arg>
        </compilerArgs>

        <showWarnings>true</showWarnings>
        <showDeprecation>true</showDeprecation>
    </configuration>

    <dependencies>
        <dependency>
            <groupId>org.codehaus.plexus</groupId>
            <artifactId>plexus-compiler-eclipse</artifactId>
            <version>2.8.5</version>
        </dependency>

        <dependency>
            <groupId>org.eclipse.jdt</groupId>
            <artifactId>ecj</artifactId>
            <version>3.36.0</version>
        </dependency>
    </dependencies>
</plugin>
```

Put it in the `pluginManagement` or the `build` section of your parent pom;
Maven's configuration inherits, so a module only has to add what is specific to
it.

[TOC]

## The parts

**`<compilerId>eclipse</compilerId>`** is what switches the compiler; without it
the plugin uses javac and the two dependencies below do nothing.

**The two dependencies** are separate on purpose. `plexus-compiler-eclipse` is
the adapter that knows how to drive ecj from Maven; `org.eclipse.jdt:ecj` is the
compiler itself. **Always pin the ecj version.** If you leave it out, the
adapter picks a version, and the day it picks a different one is the day before
your release.

**`<compilerArgs>`** are passed to ecj as they stand. This is the tag to use;
the older `<compilerArguments>` is deprecated and mangles what it is given. The
four arguments above are:

| Argument | What it does |
| --- | --- |
| `-properties <file>` | read the warning/error configuration from that file |
| `-enableJavadoc` | check javadoc references, so a `@link` to something that no longer exists is reported |
| `-nowarn` | do not print the warnings; the properties file decides what is an *error*, and that is what should stop the build |

## The properties file

`-properties` points at a file in Eclipse's own format, and DomUI points it at
`${project.basedir}/.settings/org.eclipse.jdt.core.prefs` - which is exactly
where the Eclipse IDE writes its per-project compiler settings. So every module
carries its own file, and the build enforces what the IDE shows.

It is a flat list of `problem=error|warning|ignore` lines, 380 of them in
DomUI's case. The ones that matter most are the null-analysis block:

```properties
org.eclipse.jdt.core.compiler.annotation.nullanalysis=enabled
org.eclipse.jdt.core.compiler.annotation.nonnull=org.eclipse.jdt.annotation.NonNull
org.eclipse.jdt.core.compiler.annotation.nullable=org.eclipse.jdt.annotation.Nullable
org.eclipse.jdt.core.compiler.annotation.nonnullbydefault=org.eclipse.jdt.annotation.NonNullByDefault
org.eclipse.jdt.core.compiler.annotation.inheritNullAnnotations=enabled
```

They name the annotations to trust - DomUI uses the `org.eclipse.jdt.annotation`
ones - and switch the analysis on. `inheritNullAnnotations` makes an override
inherit the annotations of the method it overrides, so an interface annotated
once carries the contract to every implementation.

## Annotation processing

The adapter runs annotation processors, so the processor that generates DomUI's
[typed properties](../../70-implementation-details/typed-properties/index.md)
is configured on the same plugin:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>${maven-compiler-plugin.version}</version>
    <configuration>
        <annotationProcessors>
            <annotationProcessor>db.annotationprocessing.PropertyAnnotationProcessor</annotationProcessor>
        </annotationProcessors>
        <annotationProcessorPaths>
            <dependency>
                <groupId>to.etc.domui</groupId>
                <artifactId>property-annotations-processor</artifactId>
                <version>1.2-SNAPSHOT</version>
            </dependency>
        </annotationProcessorPaths>
    </configuration>

    <dependencies>
        <dependency>
            <groupId>to.etc.domui</groupId>
            <artifactId>property-annotations-processor</artifactId>
            <version>1.2-SNAPSHOT</version>
        </dependency>
    </dependencies>
</plugin>
```

There is no mention of `plexus-compiler-eclipse` here, and there does not need
to be: the parent pom above already said which compiler to use, and this module
only adds the processor to it.

!! Because part of the source is generated this way, a project has to be built
!! by Maven at least once before an IDE can build it - the generated sources do
!! not exist until the processor has run. For the same reason IntelliJ has to be
!! told to use the Eclipse compiler, or it will disagree with the build about
!! what compiles.
