# 2017 Luther Thompson
# This code is public domain under CC0. See the file COPYING for details.

__all__ = 'Delegate', 'Abstract', 'Interface', 'final', 'InheritanceError'


class Delegate:
    """A data descriptor that delegates attribute access to a field in the
    instance.
    """

    def __init__(self, field):
        self.field = field

    def __set_name__(self, _, name):
        self.name = name

    def __get__(self, instance, _):
        return getattr(getattr(instance, self.field), self.name)

    def __set__(self, instance, value):
        setattr(getattr(instance, self.field), self.name, value)

    def __delete__(self, instance):
        delattr(getattr(instance, self.field), self.name)


class InheritanceError(Exception):
    """Raised when a class attempts to inherit from a class that has been
    declared @final.
    """


def final(cls):
    """A class decorator that prevents other classes from inheriting from *cls*.
    """

    def _init_subclass(bad_class):
        raise InheritanceError(
            f'Class {cls.__name__} is concrete. It cannot be subclassed.')

    cls.__init_subclass__ = classmethod(_init_subclass)
    return cls


class Abstract:
    """Use this non-data descriptor to define an abstract attribute. If a class
    includes this descriptor, yet does not provide the attribute (whether by
    __init__, or __getattr__, or whatever), then instead of AttributeError,
    it will raise NotImplementedError with the message saying it's the class's
    fault.
    """

    def __set_name__(self, owner, name):
        self._owner = owner
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        name = self._name
        try:
            return instance.__getattr__(name)
        except AttributeError:
            pass
        base = self._owner
        owner_name = owner.__name__
        raise NotImplementedError(
            f"Type {owner_name} promises to define attribute '{name}', but doesn't."
            if owner is base
            else
            f"Class {base.__name__} requires type {owner_name} to define attribute '{name}'.")


class Interface(type):
    """A metaclass for inheritable interfaces.

    Interfaces should define __slots__=() to differentiate from concrete
    classes.
    """

    def __instancecheck__(self, instance):
        return all(
            hasattr(instance, f) for f in dir(self) if isinstance(getattr(
                self, f), Abstract))

    @classmethod
    def new(cls, name, *fields, bases=()):
        return cls(name, bases, dict(
            {'__slots__': ()}, **{f: Abstract() for f in fields}))
