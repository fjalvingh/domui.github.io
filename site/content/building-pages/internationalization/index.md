---
menu:
  sort: "60"
---
# Internationalization and resource bundles

DomUI can be easily localized. But it needs some "extra's" to circumvent problems in the JDK.

<a id="determining-the-users-locale"></a>

# Determining the user's locale

It all starts with determining what the user's locale is. DomUI allows every request to the server to have it's own locale. This means that a single application can serve pages in multiple languages. The browser sends, with every request, a number of languages that it would like to have the requested pages rendered in. These are the "default languages", and they can be set by a user. Usually a Dutch language browser will have Dutch as it's primary preferred browser, and it can be configured so that English is the secondary browser (or vice versa).

In Firefox (3.x), these languages can be defined in Edit > Preferences > Content tab, then click the "Languages : Choose" button at the bottom.

<a id="localization-problems-in-the-jdk"></a>

## Localization problems in the JDK

Because every request has it's own locale(s), we cannot use much of the JDK's locale support - it is badly though out. The JDK supports localization, but like "select a locale at startup". It is ill-suited to serve multiple locales at the same time. In addition, lots of the locale support is very buggy. And it is hard to use.

<a id="domuis-locale-support"></a>

# DomUI's locale support

<a id="the-nlscontext-class"></a>

## The NlsContext class

DomUI uses the NlsContext class as the base for localization information. This class has one very important method:

```
/**
 * Gets the current locale in use by the request we're executing at this time - this is
 * the PROPER call to use from normal user code.
 * @return
 */
@NonNull static public Locale getLocale();
```

This method returns the locale of the current request that this thread is executing. It uses a ThreadLocal variable to allow every thread to store it's own information. The server code will set this locale just before it starts to execute DomUI code from the data present in the browser's request. For all Locale specific code you should use the result of this call to determine the user's locale properly.

All DomUI code uses this call to determine the locale to convert data to or from.

The default code to set the request locale from the incoming request just uses the request's locale as reported by the servlet request:

```
@NonNull
public Locale getRequestLocale(@NonNull HttpServletRequest request) {
 return request.getLocale();
}
```

This method in the DomApplication class can be overridden in your own Application class to implement your own logic for defining a request's locale, when needed.

<a id="resource-bundles"></a>

## Resource Bundles

DomUI uses resource bundles that are much like the JDK's resource bundles to contain translations for strings in several languages. The biggest difference is that JDK bundles determine the language at *load* time, while DomUI's bundles determine the correct language every time a string is looked up using the NlsContext as set by the current request. This means that a DomUI application returns the proper language string for each request.

A DomUI resource bundle is defined as a BundleRef, and a BundleRef defines all possible translations for a given set of keys, not one set of translations (in one language) as the JDK's ResourceBundle does.

A BundleRef can be created as follows:

```
public static final BundleRef BUNDLE = BundleRef.create(UserInfoPage.class, "messages");
```

This defines the class resources that are "next" to the class UserInfoPage and that start with the name "messages" as language resource files - so far exactly like the normal JDK's ResourceBundle mechanism. A BundleRef is usually defined as a constant (static final) because it only defines a location for messages; it does not define "a current language" or whatever. This makes it easy to pass BundleRef's around- you can do so without any regard for the current language. Again: a BundleRef is about all translations for a given key.

A reference to a single bundle exists only once in the system. So in the above example, if that BUNDLE variable is declared in multiple classes in the same package it creates only a single instance that is then shared between those classes (all of their BUNDLE constants point to the same instance). This prevents copies of bundles in memory, and makes efficient use of resources.

The resource files used by BundleRef are normal Java .properties file, again like the ResourceBundle mechanisms we know in Java. So the Dutch version for a resource file could have the name messages\_nl.properties, and contains something like:

```
# Control texts
ui.pagertext=Pagina {0} van {1}, {2} record(s)
ui.pagerover=Het aantal resultaten is afgekort naar {0}
ui.pagerempty=Geen resultaten
ui.dt.empty=Er zijn geen resultaten.
```

As is usual keys are mapped to strings in different languages. The BundleRef class itself has lots of methods to get strings by keys and to format a string using parameters in the messages using the regular MessageFormat class provided by the JDK. So a simple way to get a message would be:

```
String text = BUNDLE.getString("ui.dt.empty");
```

This usage returns the literal string from the bundle. To replace parameter placeholders use the following:

```
String message = BUNDLE.formatMessage("ui.pagertext", 12, 120, 1212);
```

Which would use the parameters to replace the {nn} placeholders in the message text, obeying the rules of the JDK's MessageFormat class. Internally, this call uses NlsContext.getLocale() to get the actual current request language, it will then locate the proper .properties file and load the message from there.

<a id="resource-bundle-keys-preventing-strings-as-keys-using-enums"></a>

## Resource bundle keys: preventing Strings as keys using enums

!i This is the preferred way to handle message bundles and their keys! Forget about Strings!!

The BundleRef uses a String as the key to a specific message. This makes the BundleRef flexible as String can be generated from anything. But using String constants to refer to a message sucks. Either the names need to be remembered or your code gets littered with String constants that are used to identify messages. Another problem is that a "message" is now always two things:

- The string constant used to identify the message
- The message bundle the message resides in

We can do that better. Enter IBundleCode and enums.

A Bundle enum is defined as a normal enum implementing IBundleCode. The enum values represent the constants for the messages in the bundle, and the bundle's name and location is derived from the enum class. So for example:

```
public enum FormulaError implements IBundleCode {
   attributeReferenceExpected
   , invalidRealNumber
   , invalidNumber
}
```

The bundle file that belongs to this is FormulaError.properties, and it must reside in the same package location as the enum. Because the bundle and the name of the message are now all related to that same enum a single label from this enum contains *both* the bundle *and* the message name. This is way easier than having BundleRef and key separate.

Any IBundleCode can get its message or the literal message string directly:

```
IBundleCode errorCode = FormulaError.invalidNumber;

String message = errorCode.format(...);
```

Because all members of a bundle enum implement IBundleCode it is peanuts to generalize error message handling.

<a id="the-message-file-resolution-mechanism"></a>

## The message file resolution mechanism

The BundleRef code uses a completely different mechanism than the JDK to find the proper language file for a given locale. It will start to find the "best match" by using language, country, variant, then only language and country, then only language and finally the default message bundle which is the name of the bundle without any localization info, like "messages.properties" in the example. So when a browser has the locale nl\_NL the following gets tried:

messages\_nl\_NL.properties

messages\_nl.properties

messages.properties

By definition every bundle must have a "default messages file" which is the one without any localization in the file name. All of these default message bundles must be in the same default language which will be used if the browser's language is unknown. For international applications this would mean that messages.properties would be in English and specific languages would add files including that language in the name (messages\_nl.properties, messages\_ru.properties etc).

Another change is that a key is looked up in all of the message files that match a locale, and the first file containing the key will define the translation. So in the above example, if messages\_nl\_NL.properties contains the key we look for the search ends immediately. But if it's not there it will be looked up in messages\_nl.properties and messages.properties too. This allows you to override only certain keys with different values. For instance if we support en\_US (American English) and en\_GB (Real ;-) English from Great Britain) we can have most keys in messages\_en.properties and only those that are spelled differently in US or GB in a separate file, for instance to use either "Color" or "Colour" as spelling.

<a id="component-bundles"></a>

## Component bundles

Any DomUI component (or page) can have a bundle associated with it, and the bundles for components "inherit" when components are subclassed.

A component message bundle can be one of two things:

- A specific message bundle set on the component using the setComponentBundle(IBundle) call. When this is used all messages obtained through the component's $() method (explained later) will always use this bundle. Use this sparingly, only for specific needs, for instance if a component set all use the same message bundle.
- A "Bundle Stack", comprised of message bundles for the component and all it's super components: components used as the base class for it.

The latter mechanism creates, for every component that actually uses it, a stack of BundleRef's. The stack is ordered, and starts with the bundles found for the actual class. Then it adds all bundles for the super classes for the component, also in order. For every class the code checks to see if a \[classname\] bundle exists in the class's package (i.e. a \[classname\].properties file is present), or if a \[messages\] bundle is present. These are added to the stack, and that goes on for every class up the hierarchy.

This means that a component message bundle looks like it consists of all message bundles of it's superclasses, and subclasses can "override" messages in superclasses by just defining the key with a different translation in the subclass' message bundle.

<a id="using-component-bundles"></a>

## Using component bundles

Every NodeBase derived class has the $(String code, Object... args) method. This method will use the component's bundle to translate the code into a message string, then calls the standard Java FormatMessage.format() method to apply all arguments to the message string found. This makes for short and easy to read code:

```
m_commentArea = new TwoLanguageTextArea($("edit.comment"));
```

<a id="the-dollar-function"></a>

### The dollar function $()

Within a page the $() function translates a resource key and optional parameters to a string. The usage is something like this:

```
MsgBox(this, $("recordNotFound", getName()));
```

The $ function locates the message string from one of the message bundles for the class it is in, uses NlsContext.getLocale() to find the current language, then uses MessageFormat() to format that text using the other parameters of the $ function. This is the quickest way to use message bundles for components and pages.

The $ function uses message bundle inheritance to build a message bundle *stack*: an ordered set of message bundles. The stack is formed as follows:

- Starting with the current class (as returned by getClass()), try to find a message bundle for this class as follows:
  - Use the class name in the class's package and add .properties. If this bundle is found add it to the bundle stack.
  - Use the class's package and look for a messages.properties. If that exists: add it to the stack
  - Move upward to the class package and check for messages.properties there; when found add them to the stack
- Now move to the superclass of the current class and do the exact same again.

This mechanism leads to a stack of bundles with message bundles for both the actual class but also for all base classes of that class in that stack, with the current class the 1st bundle.

Now when the $() function looks up a key it walks the stack and uses the string from the *first* bundle it finds.

In effect this does the following:

- Every class can have either a class message bundle (ClassName.properties) or a package level bundle (messages.properties) associated with it.
- All of a class' parent classes also can have bundles, and together they form a "search path" for keys.
- A new class X can both add its own keys to its own base class, but it can also *override* all of the keys that its parent classes use for texts by providing an alternate value in its class bundle!

Let's give an example.

We make a new page called CustomerListPage which extends AbstractListPage.

AbstractListPage has its own bundle (AbstractListPage\*.properties), and there is a piece of code that states:

```
lf.getButtonFactory().addButton($("newButton"), Theme.BTN_NEW, a -> addNew());
```

This adds a button with the button text coming from the "newButton" value inside the AbstractListPage.properties bundle.

If I do not like the text on the button I can create a new message bundle CustomerListPage.properties and add the newButton=xxxxx inside there to override the text.
