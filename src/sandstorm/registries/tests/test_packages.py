# -*- coding: utf-8 -*-
from unittest import TestCase, mock


class IncludeTest(TestCase):
    def test_it(self):
        from .. import includeme
        config = mock.Mock()
        includeme(config)
