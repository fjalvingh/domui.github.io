# Coding rules

TBD, will be filled in while I think of/encounter stuff

<a id="javadoc-rules"></a>

## Javadoc rules

- All **public** methods should have Javadoc, with the exception of setter methods. Rationale: public methods are interface and people should know what methods do. The exception for setter methods is because Java's idiocy with regard to the missing properties concept: getter and setter are exactly the same, and it is obvious that one does a get and the other a set. So a description of what the *property* does needs to be added only once, and it is done on the getter.
- Fields that are public with a getter and optionally a setter do not need Javadoc because that is part of the getter. If they have javadoc then make sure it does not contradict the getter's javadoc (they should be the same, and as we obviously do not copy information keep the text on the setter).
- Javadoc needs to be either meaningful or absent! Javadoc on the property "userName" that says "Returns the username" is utterly useless and should not exist. The same goes for methods: calculatePrice with "Calculates the price" - better not add it at all.
- Only use @param, @returns and @throws tags if there is really something to say about the parameters. For instance when you have a function abs(int value) it is enough to describe what the function does. It is beyond useless to say that value is the value it does it on. It is obvious and describing the obvious is dumb.
- Private and protected methods should have Javadoc if what they do is not obvious from the code. The preference is, however, to have the code so clear that looking at it tells the story. As a rule of thumb, any method that has > 10 lines of code usually needs javadoc.
