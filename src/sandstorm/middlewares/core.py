# -*- coding: utf-8 -*-


class ViewConfig(object):
    def __init__(self, *middleware_classes):
        self.middleware_classes

    def __call__(self, *args, **kwds):
        middlewares = [klass(*args, **kwds) for klass in self.middleware_classes]

        def _deco(func):
            def _wrap(obj):
                for middleware in middlewares:
                    middleware.setup(obj)
                rc = func(obj)

                for middleware in middlewares:
                    middleware.teardown(obj, rc)

                return rc
            return _wrap
        return _deco


def view_config(middlewares, *args, **kwds):
    _middlewares = middlewares

    def _deco(func):
        def _wrap(self):
            middlewares = [
                middleware_class(*args, **kwds)
                for middleware_class in _middlewares
                ]
            for middleware in middlewares:
                middleware.setup(self)
            rc = func(self)
            for middleware in middlewares:
                middleware.teardown(self, rc)
            return rc


class Middleware(object):
    def __init__(self, *args, **kwds):
        pass

    def setup(self, handler):
        pass

    def teardown(self, handler, rc):
        pass
