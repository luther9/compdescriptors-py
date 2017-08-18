__all__ = 'final', 'InheritanceError'


class InheritanceError(Exception):
    pass


def final(cls):

    def init_subclass(cls):
        raise InheritanceError(
            f'{cls.__name__} is concrete. It cannot be subclassed.')

    cls.__init_subclass__ = init_subclass
    return cls
