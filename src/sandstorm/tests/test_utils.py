# -*- coding: utf-8 -*-
from unittest import TestCase


class GetCallerModuleTest(TestCase):
    def test_it(self):
        from ..utils import get_caller_module

        get_caller_module()
