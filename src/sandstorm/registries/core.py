# -*- coding: utf-8 -*-
import zope.interface.adapter


class CommonRegistryFactory(object):
    """システムに共通で使用されるレジストリのファクトリ
    """
    _registry = zope.interface.adapter.AdapterRegistry()

    def __new__(cls):
        return cls._registry
