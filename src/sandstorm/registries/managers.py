# -*- coding: utf-8 -*-
import zope.interface

from .core import CommonRegistryFactory
from .dummy import IDummyInterface
from .interfaces import IRegistryManager
from .errors import (
    NoProvidedInterfaceError,
    AlreadyRegisterdNameError,
    )


@zope.interface.implementer(IRegistryManager)
class BaseRegistryManager(object):
    required = []
    provided = IDummyInterface
    registry_factory = CommonRegistryFactory

    def __init__(self, required=None, provided=None, registry=None):
        self._required = required or self.required
        self._provided = provided or self.provided
        self._registry = registry or self.registry_factory()

    def implemented_by(self, impl):
        return self._provided.implementedBy(impl)

    def names(self):
        return self._registry.names(self._required, self._provided)

    def register(self, name, impl, update=False):
        if not self.implemented_by(impl):
            raise NoProvidedInterfaceError('{} -> {} {}'.format(
                self._provided, name, impl))
        if not update and name in self.names():
            raise AlreadyRegisterdNameError('Duplicate name error: {}'.format(name))
        self._registry.register(self._required, self._provided, name, impl)

    def lookup(self, name):
        return self._registry.lookup(
            self._required, self._provided, name)

    def create(self, name, *args, **kwds):
        klass = self.lookup(name)
        return klass(*args, **kwds) if klass else None