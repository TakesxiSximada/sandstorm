# -*- coding: utf-8 -*-
from .managers import BaseRegistryManager
from .dummy import DummyImpl


def includeme(config):
    manager = BaseRegistryManager()
    manager.register('', DummyImpl)
