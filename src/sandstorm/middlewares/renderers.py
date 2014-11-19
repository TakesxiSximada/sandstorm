# -*- coding: utf-8 -*-
import json
from .core import Middleware


class RendererMiddleware(Middleware):
    keywords = {'renderer': 'json'}

    def teardown(self, handler):
        if self.renderer == 'json':
            self._response = json.dumps(self._response)
