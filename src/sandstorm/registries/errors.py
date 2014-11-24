# -*- coding: utf-8 -*-


class BaastRegistryError(Exception):
    pass


class NoProvidedInterfaceError(BaastRegistryError):
    pass


class AlreadyRegisterdNameError(BaastRegistryError):
    pass
