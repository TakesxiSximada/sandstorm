# -*- coding: utf-8 -*-
from .managers import BaseRegistryManager


def includeme(config):
    manager = BaseRegistryManager()
    manager.register('', BaseRegistryManager)
