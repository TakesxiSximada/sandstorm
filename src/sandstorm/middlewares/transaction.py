# -*- coding: utf-8 -*-
import transaction
from .core import Middleware


class TransactionMiddleware(Middleware):
    def setup(self, handler):
        pass

    def run(self, func, handler, middlewares):
        try:
            self.setup(handler)
            self._response = self.process(func, handler, middlewares)
        except Exception:
            transaction.abort()
        else:
            transaction.commit()
        finally:
            self.teardown(handler)
        return self._response

    def teardown(self, handler):
        pass
