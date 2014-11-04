# -*- coding: utf-8 -*-
import os
import transaction
from tornado.web import (
    StaticFileHandler,
    RequestHandler,
    )


class SandstormHandler(RequestHandler):
    schemas = {}

    def parse_params(self):
        method = self.request.method.lower()
        schema = self.schemas[method]
        params = {}
        for key, (type_, count) in schema.items():
            values = self.request.arguments[key]
            values = map(lambda x: x.decode(), values)
            values = list(map(type_, values))
            params[key] = values[0] \
              if count == 1 else values[:count]
        return params

    def on_finish(self):
        transaction.commit()


class YAStaticFileHandler(StaticFileHandler):
    def parse_url_path(self, path):
        if not path:
            path = ''

        for target in ('index.html', 'index.htm', ''):
            target = os.path.join(path, target)
            if target.endswith('/'):
                target = target[:-1]
            abspath = os.path.join(self.root, target)
            if os.path.isfile(abspath):
                return target
        return None
