#!/usr/bin/python3.6

import unittest

from composition import Interface, final, InheritanceError


class InterfaceTest(unittest.TestCase):
    """This fixture tests getting attributes from different kinds of classes."""

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

        self.contexts = (
            (cls, self.subTest(cls=cls)) for cls
            in (ClassAttrs, InstanceAttrs, Getattr))

    def test_required_defined(self):
        """Get an attribute that is required by the interface and defined by the
        class.
        """
        for cls, context in self.contexts:
            with context:
                self.assertIs(cls().foo, True)

    def test_defined(self):
        """Get a defined, non-required attribute."""
        for cls, context in self.contexts:
            with context:
                self.assertIs(cls().bar, True)

    def test_NotImplementedError(self):
        """Raise an exception for a required, undefined attribute."""
        for cls, context in self.contexts:
            with context:
                self.assertRaises(NotImplementedError, getattr, cls(), 'baz')

    def test_AttributeError(self):
        """Raise an exception for an attribute that nobody defined."""
        for cls, context in self.contexts:
            with context:
                self.assertRaises(
                    AttributeError, getattr, cls(), 'yagami_raito')


class TestValidate(unittest.TestCase):

    def setUp(self):
        self.Fooer = Interface('foo')
        self.validate = self.Fooer.validate

    def test_true(self):
        """Return True for an object that implements the interface, even if it's
        not declared as such.
        """
        class C:
            foo = None
        self.assertTrue(self.validate(C()))

    def test_false(self):
        """Return False for an unregistered object which doesn't implement the
        interface.
        """
        class C:
            pass
        self.assertFalse(self.validate(C()))

    def test_NotImplementedError(self):
        """If implementor is registered, but fails to implement the interface,
        this is a bug in the implementor.
        """
        @self.Fooer
        class C:
            pass
        self.assertRaises(NotImplementedError, self.validate, C())


class FinalTest(unittest.TestCase):

    def test_final(self):
        """We can't inherit from a final class."""
        @final
        class Concrete:
            pass
        with self.assertRaises(InheritanceError):
            class Subclass(Concrete):
                pass


if __name__ == '__main__':
    unittest.main()
