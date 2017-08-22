__all__ = 'Interface', 'final', 'InheritanceError'


class InheritanceError(Exception):
    pass


def _init_subclass(cls):
    raise InheritanceError(
        f'{cls.__name__} is concrete. It cannot be subclassed.')


def final(cls):
    cls.__init_subclass__ = _init_subclass
    return cls


def _new_property(cls, attr):

    def get(self):
        try:
            return self.__getattr__(attr)
        except AttributeError:
            raise NotImplementedError(
                f"{cls.__name__} must define attribute {attr}.")

    return property(get)


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
            cls.__dict__.setdefault(_new_property(cls, attr))

    def validate(self, o):
        """Check if object o has all the attributes of the Interface."""
        for attr in self._attributes:
            try:
                getattr(o, attr)
            except (AttributeError, NotImplementedError):
                return False
        return True
