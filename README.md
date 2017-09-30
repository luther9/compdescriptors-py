# compdescriptors

A library of tools that make it easy to favor composition over inheritance.

Avoiding inheritance can be helpful, because it makes classes more independent
from each other. A class which does not inherit has full control over its own
behavior, and changes in other classes do not force changes in that class's
interface. For more information, see [this
article](https://en.wikipedia.org/wiki/Composition_over_inheritance).

## Delegation

### class `Delegate`(field)

A data descriptor that delegates its attribute to the instance attribute given
by *field*. All access, setting, and deletion of this attribute will apply to
the instance field, not the instance itself. It can be used like this:

```python
from compdescriptors import Delegate

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

### `final`(cls)

A class decorator that prevents other classes from inheriting from *cls*.

### class `Abstract`

Use this non-data descriptor to define an abstract attribute. If a class
includes this descriptor, yet does not provide the attribute (whether by
`__init__`, or `__getattr__`, or whatever), then instead of AttributeError, it
will raise NotImplementedError with the message saying it's the class's fault.

Using this, `NotImplementedError` indicates a mistake in the class, while
`AttributeError` is more likely to indicate a mistake in the client code. It can
also be used to define abstract classes. For example, this is how you could
define an interface with class syntax. All concrete subclasses would be required
to define `foo` and `bar`:

```python
from compdescriptors import Abstract

class FooBarer:
    __slots__ = ()
    foo = Abstract()
    bar = Abstract()
```

### class `Interface`(*attributes)

Return a class decorator that adds Abstract descriptors for the given attribute
names. The arguments may be strings and/or other Interface objects. Example:

```python
from compdescriptors import Interface

@Interface('foo', 'bar')
class A:
    foo = 'hello'

    def __init__(self):
        self.bar = 'bye'
```

**Why not use the `abc` module?** The standard library `abc` module can only
  validate a concrete class at the time of its creation. It cannot check
  `__getattr__`, nor can it check instance attributes unless the class defines
  properties, which means defining extra methods just to satisfy the ABC. With
  the Abstract attributes described here, we need only add the decorator to the
  class declaration. Nothing special needs to be done to satisfy the Interface
  object's requirements.

Interface objects have a method:

#### `validate`(obj)

Return True if *obj* has all of the attributes that would be required by this
Interface, otherwise False. This lets you check undecorated classes. Note that
if *obj*'s class was decorated with this Interface and does not fully implement
it, this is a bug in the class. In that case, `validate` will raise NotImplementedError.

## Exceptions

### class `InheritanceError`

Raised when a class attempts to inherit from a class that has been declared
`@final`.
