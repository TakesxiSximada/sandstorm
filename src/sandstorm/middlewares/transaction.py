# -*- coding: utf-8 -*-
import transaction
from .core import Middleware


class TransactionMiddleware(Middleware):
    def teardown(self, handler, rc):
        transaction.commit()
