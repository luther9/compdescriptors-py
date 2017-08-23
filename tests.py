import unittest

from composition import Interface, final, InheritanceError


class InterfaceTest(unittest.TestCase):

    def setUp(self):
        FooBazer = Interface('foo', 'baz')

        @FooBazer
        class ClassAttrs:
            foo = bar = True

        @FooBazer
        class InstanceAttrs:
            def __init__(self):
                self.foo = self.bar = True

        @FooBazer
        class Getattr:
            def __getattr__(self, attr):
                if attr in ('foo', 'bar'):
                    return True
                raise AttributeError

        self.implementors = (ClassAttrs, InstanceAttrs, Getattr)

    def test_required_defined(self):
        """Get an attribute that is required by the interface and defined by the
        class.
        """
        for cls in self.implementors:
            with self.subTest(cls=cls):
                self.assertIs(cls().foo, True)

    def test_defined(self):
        """Get a defined, non-required attribute."""
        for cls in self.implementors:
            with self.subTest(cls=cls):
                self.assertIs(cls().bar, True)

    def test_NotImplementedError(self):
        """Raise an exception for a required, undefined attribute."""
        for cls in self.implementors:
            with self.subTest(cls=cls):
                self.assertRaises(NotImplementedError, getattr, cls(), 'baz')

    def test_AttributeError(self):
        """Raise an exception for an attribute that nobody defined."""
        for cls in self.implementors:
            with self.subTest(cls=cls):
                self.assertRaises(
                    AttributeError, getattr, cls(), 'yagami_raito')


class FinalTest(unittest.TestCase):

    def test_final(self):
        """We can't inherit from a final class."""
        @final
        class Concrete:
            pass
        with self.assertRaises(InheritanceError):
            class Subclass(Concrete):
                pass


if __name__ =='__main__':
    unittest.main()
