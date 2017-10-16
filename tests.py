#!/usr/bin/python3

# 2017 Luther Thompson
# This code is public domain under CC0. See the file COPYING for details.

import unittest

from compdescriptors import (
    Delegate, Abstract, Interface, final, InheritanceError)


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


class AbstractTest(unittest.TestCase):
    """Test the Abstract descriptor."""

    def setUp(self):
        class A:
            var = Abstract()
        self.A = A

    def test_same(self):
        """Works within a single class."""
        self.assertRaises(NotImplementedError, getattr, self.A(), 'var')

    def test_subclass(self):
        """Works with an inherited descriptor."""
        class B(self.A):
            pass
        self.assertRaises(NotImplementedError, getattr, B(), 'var')


class InterfaceTest(unittest.TestCase):
    """This fixture tests getting attributes from different kinds of classes."""

    def setUp(self):
        FooBazer = Interface.new('Foobazer', 'foo', 'baz')

        class ClassAttrs(FooBazer):
            foo = bar = True

        class InstanceAttrs(FooBazer):
            def __init__(self):
                self.foo = self.bar = True

        class Getattr(FooBazer):
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
        self.Fooer = Interface.new('Fooer', 'foo')

    def test_true(self):
        """Return True for an object that implements the interface, even if it's
        not declared as such.
        """
        class C:
            foo = None
        self.assertTrue(isinstance(C(), self.Fooer))

    def test_false(self):
        """Return False for an unregistered object which doesn't implement the
        interface.
        """
        class C:
            pass
        self.assertFalse(isinstance(C(), self.Fooer))

    def test_NotImplementedError(self):
        """If implementor is registered, but fails to implement the interface,
        this is a bug in the implementor.
        """
        class C(self.Fooer):
            pass
        self.assertRaises(NotImplementedError, isinstance, C(), self.Fooer)


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
