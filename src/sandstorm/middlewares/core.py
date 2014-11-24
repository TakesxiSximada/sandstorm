# -*- coding: utf-8 -*-
from .errors import (
    DuplicateKeywordError,
    IlligalViewConfigArgumentError,
    )


class Middleware(object):
    keywords = {
        }

    @classmethod
    def coerce_kwds(cls, kwds):
        return kwds

    def __init__(self, **kwds):
        self._response = None  # _response cannot use kwds
        for key, value in self.keywords.items():
            val = kwds.get(key, value)
            setattr(self, key, val)

    def _process_childen(self, func, handler, middlewares):
        return middlewares[0].run(func, handler, middlewares[1:])

    def process(self, func, handler, middlewares):
        middleware = middlewares[0] if len(middlewares) > 0 else None
        self._response = (middleware.run(func, handler, middlewares[1:])
                          if middleware else func(handler))
        return self._response

    def setup(self, handler):
        pass

    def run(self, func, handler, middlewares):
        try:
            self.setup(handler)
            self.process(func, handler, middlewares)
        finally:
            self.teardown(handler)
        return self._response

    def teardown(self, handler):
        pass


class TeadownOptionalMiddleware(Middleware):

    def run(self, func, handler, middlewares):
        self.setup(handler)
        self.process(func, handler, middlewares)
        self.teardown(handler)
        return self._response


class DummyMiddleware(Middleware):
    pass


class ViewConfig(object):
    """view_config factory
    """
    def __init__(self, *args):
        self.keywords = []
        self.middleware_classes = []
        self.install(*args)

    def install(self, *middleware_classes):
        for middleware_class in middleware_classes:
            for keyword in middleware_class.keywords:
                if keyword in self.keywords:
                    raise DuplicateKeywordError(keyword)
                self.keywords.append(keyword)
            self.middleware_classes.append(middleware_class)

    def create_middlewares(self, **kwds):
        return [klass(**kwds) for klass in self.middleware_classes]

    def get_next_middleware_classes(self):
        return self.middleware_classes[1:]

    def __call__(self, **kwds):
        """view_config function
        """
        for key in kwds.keys():
            if key not in self.keywords:
                raise IlligalViewConfigArgumentError(key)

        for klass in self.middleware_classes:
            kwds = klass.coerce_kwds(kwds)

        def _deco(func):
            def _wrap(handler):
                middlewares = self.create_middlewares(**kwds)
                middleware = DummyMiddleware(**kwds)
                return middleware.run(func, handler, middlewares)
            return _wrap
        return _deco
