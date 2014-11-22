# -*- coding: utf-8 -*-
import tornado.web
import pyramid.httpexceptions
from .core import Middleware


class PyramidHTTPExceptionMiddleware(Middleware):
    def run(self, func, handler, middlewares):
        try:
            self.setup(handler)
            self._response = self.process(func, handler, middlewares)
        except pyramid.httpexceptions.HTTPException as pyramid_err:
            raise tornado.web.HTTPError(pyramid_err.code, pyramid_err.status)
        finally:
            self.teardown(handler)
        return self._response
