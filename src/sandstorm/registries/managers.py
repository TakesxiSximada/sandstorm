# -*- coding: utf-8 -*-
import zope.interface
import zope.interface.verify
from zope.interface.exceptions import (
    DoesNotImplement,
    BrokenImplementation,
    )
from .core import CommonRegistryFactory
from .dummy import IDummyInterface
from .interfaces import IRegistryManager
from .errors import (
    InterfaceMismatchError,
    AlreadyRegisterdNameError,
    )


@zope.interface.implementer(IRegistryManager)
class BaseRegistryManager(object):
    required = []
    provided = IRegistryManager
    registry_factory = CommonRegistryFactory

    def __init__(self, required=None, provided=None, registry=None):
        self._required = required or self.required
        self._provided = provided or self.provided
        self._registry = registry or self.registry_factory()

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_val, exec_tb):
        pass

    def verify(self, impl):
        """
        raise zope.interface.exceptions.BrokenImplementation
        """
        try:
            return zope.interface.verify.verifyClass(self._provided, impl)
        except (BrokenImplementation, DoesNotImplement) as err:
            raise InterfaceMismatchError(err)

    def implemented_by(self, impl):
        try:
            return self.verify(impl)
        except InterfaceMismatchError:
            return None

    def names(self):
        return self._registry.names(self._required, self._provided)

    def register(self, name, impl, update=False):
        if not self.verify(impl):
            raise zope.interface.exceptions.BrokenImplementation()
        if not update and name in self.names():
            raise AlreadyRegisterdNameError('Duplicate name error: {}'.format(name))
        self._registry.register(self._required, self._provided, name, impl)

    def lookup(self, name):
        return self._registry.lookup(
            self._required, self._provided, name)

    def create(self, name, *args, **kwds):
        klass = self.lookup(name)
        return klass(*args, **kwds) if klass else None


@zope.interface.implementer(IRegistryManager)
class DummyRegistryManager(object):
    required = []
    provided = IDummyInterface
    registry_factory = CommonRegistryFactory
