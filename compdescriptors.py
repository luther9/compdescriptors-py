# 2017 Luther Thompson
# This code is public domain under CC0. See the file COPYING for details.

__all__ = 'Delegate', 'Interface', 'final', 'InheritanceError'


class Delegate:
    """A data descriptor that delegates attribute access to a field in the
    instance.
    """

    def __init__(self, field):
        self.field = field

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return getattr(getattr(instance, self.field), self.name)

    def __set__(self, instance, value):
        setattr(getattr(instance, self.field), self.name, value)

    def __delete__(self, instance):
        delattr(getattr(instance, self.field), self.name)


class InheritanceError(Exception):
    """Raised when a new class attempts to inherit from an illegal base class.
    """


def final(cls):

    def _init_subclass(bad_class):
        raise InheritanceError(
            f'Class {cls.__name__} is concrete. It cannot be subclassed.')

    cls.__init_subclass__ = classmethod(_init_subclass)
    return cls


class _Descriptor:

    def __init__(self, attr):
        self.attr = attr

    def __get__(self, instance, owner):
        try:
            return instance.__getattr__(self.attr)
        except AttributeError:
            pass
        raise NotImplementedError(
            f'Class {owner.__name__} must define attribute {self.attr}.')


class Interface:
    """Arguments must be either strings or other Interface objects defining
    which attributes an implementing class must define. Return a class
    decorator.
    """

    def __init__(self, *attributes):
        attr_list = []
        for attr in attributes:
            if isinstance(attr, str):
                attr_list.append(attr)
            elif isinstance(attr, Interface):
                attr_list.extend(attr._attributes)
            else:
                raise TypeError('Expected str or Interface, got {attr}.')
        self._attributes = tuple(attr_list)

    def __call__(self, cls):
        for attr in self._attributes:
            if attr not in cls.__dict__:
                setattr(cls, attr, _Descriptor(attr))
        return cls

    def validate(self, o):
        """Check if object o has all the attributes of the Interface.

        If o's class was declared with this interface and it does not define all
        required attributes, consider this a bug in the class, and throw
        NotImplementedError.
        """
        return all(hasattr(o, attr) for attr in self._attributes)
