# -*- coding: utf-8 -*-
from unittest import TestCase

import zope.interface
import zope.interface.adapter
from ..managers import BaseRegistryManager
from ..interfaces import IRegistryManager
from ..dummy import (
    IDummyInterface,
    DummyImpl,
    )

class TestingRegistryFactory(object):
    """システムに共通で使用されるレジストリのファクトリ
    """
    _registry = zope.interface.adapter.AdapterRegistry()

    def __new__(cls):
        return cls._registry


@zope.interface.implementer(IRegistryManager)
class TestingRegistryManager(BaseRegistryManager):
    required = [IDummyInterface]
    provided = IDummyInterface
    registry_factory = TestingRegistryFactory


@zope.interface.implementer(IDummyInterface)
class ImplButBrokenInterface(object):
    pass


class NoImpl(object):
    pass


class BaseRegistryManagerTest(TestCase):
    def _make(self):
        return TestingRegistryManager()

    def setUp(self):
        manager = self._make()
        manager.register('test', DummyImpl, update=True)

    def test_verify_success(self):
        manager = self._make()
        manager.verify(DummyImpl)

    def test_verify_fail(self):
        from ..errors import InterfaceMismatchError
        manager = self._make()

        with self.assertRaises(InterfaceMismatchError):
            manager.verify(NoImpl)
        with self.assertRaises(InterfaceMismatchError):
            manager.verify(ImplButBrokenInterface)

    def test_names(self):
        manager = self._make()
        self.assertEqual(['test'], manager.names())

    def test_register(self):
        from ..errors import (
            AlreadyRegisterdNameError,
            InterfaceMismatchError,
            )
        manager = self._make()
        manager.register('test', DummyImpl, update=True)

        with self.assertRaises(AlreadyRegisterdNameError):
            manager.register('test', DummyImpl)

        with self.assertRaises(InterfaceMismatchError):
            manager.register('test', NoImpl)
        with self.assertRaises(InterfaceMismatchError):
            manager.register('test', ImplButBrokenInterface)

    def test_lookup(self):
        manager = self._make()
        self.assertEqual(DummyImpl, manager.lookup('test'))  # success
        self.assertEqual(None, manager.lookup('no registered'))  # error

    def test_create(self):
        manager = self._make()
        # success
        obj = manager.create('test')
        self.assertEqual(DummyImpl, type(obj))

        # error
        obj = manager.create('no registerd')
        self.assertEqual(None, obj)
