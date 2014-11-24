# -*- coding: utf-8 -*-


class BaastRegistryError(Exception):
    pass


class InterfaceMismatchError(BaastRegistryError):
    pass


class AlreadyRegisterdNameError(BaastRegistryError):
    pass
