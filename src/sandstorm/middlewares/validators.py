# -*- coding: utf-8 -*-
import os
import json
import jsonschema
from .core import Middleware
from ..utils import get_caller_module
from ..requests import (
    ArgumentsCleaner,
    ArgumentsNormalizer,
    )


class ValidationMiddleware(Middleware):
    keywords = {
        'schema': None,
        'ignore_error': False,
        }

    @classmethod
    def coerce_kwds(cls, kwds):
        schema = kwds.get('schema')
        if schema:
            dotted, module, path, module_dir = get_caller_module(depth=1)
            try:
                schema = os.path.join(module_dir, schema)
            except AttributeError:  # schema is not string, dict?
                pass
            else:
                if os.path.exists(schema):
                    with open(schema, 'r') as fp:
                        schema = fp.read()
            try:
                schema = json.loads(schema)
            except ValueError:
                raise
            except TypeError:  # may be dict like object?
                pass

            # check json like object
            json.dumps(schema)
            kwds['schema'] = schema
        return kwds

    def setup(self, handler):
        arguments = handler.request.arguments
        setattr(handler, 'validation_error', None)
        setattr(handler, 'normalized_arguments', arguments)

        cleaner = ArgumentsCleaner()
        normalizer = ArgumentsNormalizer()
        arguments = cleaner.clean(arguments)
        if self.schema:
            arguments = normalizer.normalize(arguments, self.schema)
            handler.normalized_arguments = arguments

        try:
            jsonschema.validate(arguments, self.schema)
        except jsonschema.exceptions.ValidationError as err:
            handler.validation_error = err
            if not self.ignore_error:
                raise
