# The pages the tests drive

A UI test needs a screen to drive. In DomUI those screens are not hidden in the
test sources: they are **pages of the demo application**, in
`to.etc.domui.demo`, reachable from its home page under "JUnit/Selenium Test
pages".

That is on purpose. The pages have two jobs, and they do both well:

- they put a component in the exact situation a test wants to check - a
  mandatory field that is empty, two bindings that depend on each other, a
  dialog inside a dialog;
- they are the worked examples of what a testable page looks like, next to the
  test that drives them. Every code fragment in this section comes from them.

[TOC]

## The groups

| Package under `pages/test` | What it holds | Tests |
| --- | --- | --- |
| `uitest` | the order entry page this documentation is written around | `ITOrderEntry`, `ITOrderEntryPageObject` |
| `proxies` | one page with every component that has a page object proxy | `ITTestProxiesPage1` |
| `binding` | pages where data binding has to do something exactly right | `ITTestBindingOrder`, `ITTestBuildOrder`, `ITBindValidationError`, `ITBindErrors1` |
| `componenterrors` | components in their error and layout states | `ITTestText2Layout`, `ITTestText2Behavior`, `ITTestForm4Layout`, `ITTestLookupInput2`, `ITTestHtmlEditorComponent` |
| `msgbox` | the message box in each of its shapes | `ITTestMsgBox` |

Two of them are worth reading before writing a test of your own.

**Build order.** DomUI builds nodes lazily: `createContent()` of a component
runs while the page is being rendered. If a binding were evaluated at the
moment its component is built, a binding reading a property of a component that
is *not yet built* would read a value that is about to change.
`BuildOrderPage` sets that situation up and `ITTestBuildOrder` asserts that
bindings run after every build is done.

**Binding order.** `TestBindingOrder1` has a country and a city combo that
depend on each other: changing the country must change the city, and the
binding that then runs for the city must not undo it. The test changes each of
them and checks that the other followed.

## The page the tests here are written against

`OrderEntryTestPage` in `pages/test/uitest`: a form of three controls, a basket
as a `DataTable` with a link button per row, and an answer that changes when
something is ordered.

!demo(to.etc.domuidemo.pages.test.uitest.OrderEntryTestPage.ui, 100%, 480)

```java
public class OrderEntryTestPage extends UrlPage {
	@Override
	public void createContent() throws Exception {
		ContentPanel cp = new ContentPanel();
		add(cp);
		cp.add(new HTag(1, "Order entry"));

		Div answer = new Div("dm-tut", NOTHING);
		answer.setTestID("answer");

		Text2<String> customer = new Text2<>(String.class);
		customer.setMandatory(true);
		ComboFixed2<Shipping> shipping = ComboFixed2.createEnumCombo(Shipping.class);
		shipping.setValue(Shipping.Standard);
		Text2<Integer> copies = new Text2<>(Integer.class);
		copies.setValue(1);

		FormBuilder fb = new FormBuilder(cp);
		fb.label("Customer").control(customer);
		fb.label("Shipping").control(shipping);
		fb.label("Copies").control(copies);

		...

		DataTable<BasketLine> table = new DataTable<>(new SimpleListModel<>(basket), rr);
		table.setTestID("basket");
		cp.add(table);
	}
}
```

Everything a test asserts on is fixed: three albums with fixed prices, a
shipping cost per option, one copy to start with. The page never queries the
database.

## Adding one

1. **Put it in the demo**, in the package of the group it belongs to, and link
   it from `JUnitTestMenuPage` so it can be reached by hand. A fixture nobody
   can open is a fixture nobody can debug.
2. **Make it deterministic.** Fixed data, no `new Date()`, no random order, no
   dependency on how many rows a query happens to return today. The demo
   database is there when a test needs one, but a page that can do without it
   is a test that cannot break on the data.
3. **Set a testid** on everything the test must find and that has no obvious
   calculated name - the containers especially, since a `Div` never gets one by
   itself.
4. **Keep it small and one-subject.** A page that shows one thing going wrong
   is worth more than a page that shows twelve things at once, because the
   screenshot of a failing test on it is readable.
5. **Follow the ordinary page rules**: content inside a `ContentPanel`,
   controls in local variables and not in fields, current components only. A
   fixture page is read as an example whether it was meant as one or not.
