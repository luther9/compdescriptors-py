__all__ = 'Interface', 'final', 'InheritanceError'


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
        """Check if object o has all the attributes of the Interface."""
        for attr in self._attributes:
            try:
                getattr(o, attr)
            except (AttributeError, NotImplementedError):
                return False
        return True
