# compdescriptors

A library of tools that make it easy to favor composition over inheritance.

Avoiding inheritance can be helpful, because it makes classes more independent
from each other. A class which does not inherit has full control over its own
behavior, and changes in other classes do not force changes in that class's
interface. For more information, see [this
article](https://en.wikipedia.org/wiki/Composition_over_inheritance).

## Delegation

### class `compdescriptors.**Delegate**`(field)

A data descriptor that delegates its attribute to the instance attribute given
by *field*. All access, setting, and deletion of this attribute will apply to
the instance field, not the instance itself. It can be used like this:

```python
class Thing:

    def __init__(self):
        self.var = 'hello'

    def __len__(self):
        return 42

class C:
    var = Delegate('thing')
    __len__ = Delegate('thing')

    def __init__(self):
        self.thing = Thing()
```

## Validation

Due to the duck-typing nature of Python, the following tools are not strictly
necessary. They are provided to help enforce project requirements on classes.

### class `compdescriptors.**InheritanceError**`

Raised when a class attempts to inherit from a class that has been declared
`@final`.
