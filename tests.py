#!/usr/bin/python3.6

import unittest

from composition import Delegate, Interface, final, InheritanceError


class DelegateTest(unittest.TestCase):
    """Test the delegation function."""

    def setUp(self):

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

        self.o = C()

    def test_delegate(self):
        self.assertEqual(self.o.var, 'hello')

    def test_delegate_set(self):
        self.o.var = 84
        self.assertEqual(self.o.thing.var, 84)

    def test_delegate_del(self):
        del self.o.var
        self.assertFalse(hasattr(self.o, 'var'))
        self.assertFalse(hasattr(self.o.thing, 'var'))

    def test_delegate_special(self):
        self.assertEqual(len(self.o), 42)


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

        self.implementors = ClassAttrs, InstanceAttrs, Getattr

    def _for_all_classes(f):
        """A decorator that runs the test for every class defined in setUp."""
        def test(self):
            for cls in self.implementors:
                with self.subTest(cls=cls):
                    f(self, cls)
        return test

    @_for_all_classes
    def test_required_defined(self, cls):
        """Get an attribute that is required by the interface and defined by the
        class.
        """
        self.assertIs(cls().foo, True)

    @_for_all_classes
    def test_defined(self, cls):
        """Get a defined, non-required attribute."""
        self.assertIs(cls().bar, True)

    @_for_all_classes
    def test_NotImplementedError(self, cls):
        """Raise an exception for a required, undefined attribute."""
        self.assertRaises(NotImplementedError, getattr, cls(), 'baz')

    @_for_all_classes
    def test_AttributeError(self, cls):
        """Raise an exception for an attribute that nobody defined."""
        self.assertRaises(AttributeError, getattr, cls(), 'yagami_raito')


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
