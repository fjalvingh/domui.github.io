---
menu:
  sort: "20"
---
# Why do we need first-class properties (actually: property REFERENCES)?

<a id="property-references-building-a-type-safe-framework-using-properties-and-failing-again-and-again-8"></a>

## Property references: building a type safe framework using properties - and failing again and again 8-(

In Java properties do not really exist: they are but a (pretty bad/sad) convention - a pair of getter and setter that have an agreed on name using a silly convention.

This means that any framework that needs to talk about properties has no other choice than to use a string for the property name: because Java has no properties as first-class objects there also are no ways that the compiler can refer to one. This leads to very bad problems in code that wants to talk about properties. For instance when we want to use data binding in a form we could make a framework that allows something like this:

```
FormBuilder fb = new FormBuilder(this); // add all things to edit to this screen
Invoice inv = ....; // The thing whose fields we want to edit
fb.property(inv, "amount").control(); // Add an input field for "amount" and use data binding to connect the control and the value of the amount prop in the invoice
fb.property(inv, "currency").control(); // Do the same for the currency
```

To make this work the Invoice class must have properties with the name "amount", implemented by getAmount() and setAmount() - hopefully of the same type, and the same for the currency property.

So far so good: the framework code can, at runtime, use the string for the property name and locate the getter and setter in the class. But of course we have sad problems with this because the code is very unsafe: as soon as we refactor the Invoice class and rename "amount" to "value" then the code still compiles fine - but it will die at runtime.

Another problem is that the above construct has no idea about the *type* of the value inside "amount", so any reference to a property can only see at runtime if the values passed to it will be correct. So for instance something silly like this:

```
fb.property(inv, "amount").control(new DateInput());
```

will compile just fine because there is no way in runtime to discover the type of "amount".

You can of course write tests for all this but that is a lot of work for something very common that *should* be done by the compiler! But it cannot because Java has no concept of a "property reference" - something that can be used as a typesafe reference to a property.

Having typesafe properties would help a lot, because not only would the compiler be able to report compilation errors for something like this:

```
fb.property(inv, Invoice::ammounts).control();
```

but IDE's like IntelliJ Idea and Eclipse can now flawlessly refactor properties so that nothing breaks. And of course - if you remove the property from the Invoice class you will get a compilation error too.

It is **this issue** that makes it important that Java would get first class properties **and property references**, not the replacement of getters and setters. But our Java "Architects" apparently do not get that.

<a id="possible-workarounds-in-java"></a>

## Possible workarounds in Java

<a id="method-references"></a>

### Method references?

Since Java 8 we apparently have Lambda's (we don't, but that is another subject). And this also brought the "method reference": for any method in a class we can get a reference to that method by using the Classname::MethodName syntax, i.e. Invoice::getAmount(). This seems like something usable: this does reference that method and it is typeful too: the returned thingy for that reference knows both the type of the class AND the type of the return value of the getter. So why can't we use that?

It turns out that method references like this are very badly implemented: the people that brought you lobotomized generics, Silly <> syntax and lambda's without functions also managed to make a mess of this, obviously. A method reference is nothing more than the compiler generating some sad code that makes an implementation of an interface on the fly. The interface implemented is one of the java.util.function, in this case an implementation of Function<Invoice, BigDecimal>. As this is a very bare bones type it knows nothing: not even the name of the function. So while this allows access to the getter we cannot use it to calculate how to reach the setter. Pretty dumb if you ask me.

![](over.jpg)

<a id="generating-something"></a>

### Generating something?

What appears to be too hard for Java's "architects" we can try to do ourselves, of course. We can make something that discovers the properties of a class and generates something to reference them. The simplest thing would be to generate String constants for each property inside the class that contains them, so Invoice would have something like:

```
public static final String pAMOUNT = "amount";
public static final String pCURRENCY = "currency";
```

This at least helps a bit: while coding you get code completion on the possible strings, and as long as you think about also refactoring the string constant when you refactor at least you can do that without breaking code. You can also see where properties are used (as long as everyone uses the constants - and of course what could *possibly* go wrong there). But these are still only Strings, and we can do better: we can create a Property class outselves and generate instances of that, something like:

```
public final class Property<C, V>....
```

and then use it inside the Invoice class like this:

```
public final Property<Invoice, BigDecimal> pAMOUNT = new Property<>(Invoice.class, BigDecimal.class, "amount");
```

As we would generate the thingy above the fact that is it a lot of typing does not need to concern us much - with Java's getter and setter jokefest what's another line, eh?

This is actually the approach taken by some reasonably well-known tools:

- [jooq](https://www.jooq.org/) uses the approach to allow a SQL like "language" to be expressed in Java, with the generated properties being used to create type-aware SQL.
- The JPA standard describes a "metamodel generator" which generates things like the above to be used by their Criteria API. Examples are [here](https://docs.jboss.org/hibernate/jpamodelgen/1.0/reference/en-US/html_single/) and [here](https://docs.oracle.com/javaee/6/tutorial/doc/gjiup.html).
- And of course DomUI has had an implementation since about 2013 too, gracefully donated by D Bekkering.

While currently the best idea to have at least something this too is fraught with problems. The biggest one is: *how do we get these properties generated*? It is important to have them be generated as automatically as possible because this will give the greatest benefit while refactoring: when we delete a property we would like to get the resulting issues as soon as possible.

A common idea is to use Java's annotation processor support for this and this would seem like a good plan: many IDE's profess support for annotation processing, and since it is part of the Java standard one can expect it to be portable. Sadly enough though for this solution there are quite some problems... While most IDE's support annotation processing they often do it wrong:

- Eclipse had a long period where annotation processing did not do anything. Whether it is currently fixed - no idea.
- IntelliJ has annotation processing support but it is hard to use and [it has a nasty bug](https://youtrack.jetbrains.com/issue/IDEA-168774): it first compiles all code (that is supposed to *use* the annotations) and only after that does it generate and compile the annotations. Sigh.
- Maven seems to have something but its utter braindead way of compiling code (by a load of badly maintained, badly described and buddy plugins) means that you are in trouble as soon as you try to do something as simple as wanting to use Eclipse's compiler - that plugin gracefully ignores any settings for annotation processing - without giving an error of course, because that would mean *less* time lost.

When using Maven you can of course create yet another (undoubdedly buggy) plugin that does this work - but I kind of dislike the several minute wait when compiling with this dungheap of a tool.

So while in theory at least reasonable (and I think the best that can be done) this method also has its trouble.

<a id="common-problems-in-do-it-yourself-options-like-the-above"></a>

### Common problems in "do it yourself" options like the above

One problem that both of the above have in common is- for which classes do we generate property references and for which classes not? Many frameworks have use for them, so you should not say "only for JPA entities". Data binding likes to have references to model classes. and so on. The alternative is to generate these for all classes having properties, or to use some signal annotation to mark a class as needing property refs. Sadly enough it's all manual work, and of course generating properties costs memory even when most of them are not used. This is something a compiler together with a runtime can easily fix as it KNOWS which references are used - but we cannot.

<a id="the-new-kid-on-the-block-kotlin"></a>

## The new kid on the block: Kotlin

Kotlin has fixed a lot of the badness in Java while still trying to be as compatible as possible with both Java and its ecosystem. This is a language that has Architects without quotes: they actually try to solve issues and not create new ones, and they are language quality first people.

Kotlin fixes a lot of Java issues:

- It has real lambda's because it has first-class function support - a requirement for lambda's
- It fixes at least some issues with generics, mostly the raw type jokes and the upper/lower bound bafflements (T extends and T super) - replacing them with the way clearer in and out. Sadly enough they did not fix the biggest fxxxup with generics: type erasure.. But let's hope and give them time...
- It does type inference so that silly jokes like: Map<String, List<Item>> result = calculatePerList(); can be replaced by var result = calculatePerList().. That is a lot less typing.
- It has null checking inside the type system so that you can define something to not be able to hold null (var s : String = "hello") or something that explicitly *can* be null (var s: String?) - meaning it needs to be checked before it is used. It also has things like the Elvis operator that seem to be too hard for Java to adopt - because the if(x != null) { if(x.getAuthor() != null) { if(x.getAuthor().getAddress() != null) { .... pyramid of doom is of course so much "clearer"...
- It does its best to fix the badly b0rked Collections API by explicitly having both immutable and mutable versions of collection types
- It does away with checked exceptions: one of the worst idea's EVER. It is understandable to try something and make a mistake. It is dumb to continue the mistake. It is insane to continue the mistake and then make an even bigger mess by not even properly supporting/using it YOURSELF, like lambda's in things like the stream() api not being able to throw anything... Or needing things like Unsafe to secretly throw stuff anyway.... That is beyond stupid and gets us in the realm of the utter incompetents...
- It has first-class property support AND it has property references!

Not all is well, of course:

- some of Kotlin's syntax is a bit arcane, and takes getting used to
- I do not care much for the fact that there is no real connection between a class and its source file like in Java - a .kt file can contain any class. I like this in Java because it makes files less big; I hate having to wade through 10.000 line files that contain 15 classes.
- It's a pity that public functions are the rule and private functions must be specified like that... The other way around is so much safer..

But: compared to Java it's a Godsent.

<a id="so-what-can-be-done-with-kotlins-property-references"></a>

### So: what can be done with Kotlin's property references?

A Kotlin property reference looks like Java's method references but it actually specifies the property:

```
Invoice::amount
```

The type of a property reference is:

```
val name2: KMutableProperty1<Invoice, BigDecimal> = Invoice::amount
```

This is typeful, and we can use it to properly restrict values to a method:

```
fun <T, V> eq(property: KMutableProperty1<T, V>, value: V) ....

eq(Invoice::amount, "Hello") // this will not compile because "hello" is not BigDecimal.
```

One thing to be aware of though: read-only properties (val) return a KProperty1 instead, and that one has an issue: its value parameter is defined as "out". Because of this using that type as a restriction does not really restrict:

```
fun <T, V> eq(property: KProperty1<T, V>, value: V)

eq(Invoice::amount, "Hello")  // This does compile, sadly enough 8-/
```

The KProperty1 type contains a method to return the property name - which is very useful when you want to use it to, for instance, generate a SQL query based on that name. It also contains get and set methods which will let you get the value and set the value of the property given an instance of Invoice. This is a pretty great implementation because it allows most of what we want:

- Kotlin properties are recognized by the compiler, so misspelling them will give a compile time error, not a runtime one
- Kotlin properties are known to the IDE, so it can refactor properties and help you with code completion
- Since we know a property's name we can discover other things about it, like what JPA Annotations are present on it so that we can generate SQL for criteria... Yay :wink:

!w While property references exist for Kotlin classes that have them, they do **not** exist for Java classes that have Java's "properties". This is a bit odd, because Kotlin *does* support accessing Java's properties using the name of the property. This does mean that using Kotlin's property references only works for Kotlin classes. Pity. See [https://youtrack.jetbrains.com/issue/KT-8575](https://youtrack.jetbrains.com/issue/KT-8575) for details of the issue and vote for it if you would like to fix it :wink:
