# -*- coding: utf-8 -*-
from zope.interface import (
    Interface,
    Attribute,
    implementer,
    )


class IDummyInterface(Interface):
    attribute = Attribute(u'')  # cannot verify

    def func(arg1, arg2):
        pass


@implementer(IDummyInterface)
class DummyImpl(object):

    def func(self, arg1, arg2):
        pass
