# You cannot link a control property with a dotted path

Consider the following code:

```
public class DoNotBindControlDottedTestPage extends UrlPage {
   @Override public void createContent() throws Exception {
      MyLookup li = new MyLookup();
      add(li);

      li.bind("value.id").to(this, "id");
   }

   private Long m_id;

   /**
    * We need to extends LookupInput so that getValue() has an actual
    * type instead of type-erased Object. If we would not do this then
    * the screen would fail because Object has no id property.
    */
   public class MyLookup extends LookupInput<Customer> {
      public MyLookup() {
         super(QCriteria.create(Customer.class));
      }
   }

   public Long getId() {
      return m_id;
   }

   public void setId(Long id) {
      m_id = id;
   }
}
```

Here we bind the control's "value.id" property to some other "id" property in the model. This however is not allowed! The reason is this: when it is time to move the model values to the control (when the request leaves the server) then this binding would:

- call this.getId() to get the id value from the model
- call li.getValue().setId() with the id gotten above

This does not change the control's value, but it changes a *property* of that value! The net effect is that the control assumes that nothing changed.

To prevent this bug DomUI will throw an exception when this kind of binding is attempted.

See issue #2 on GitHub
