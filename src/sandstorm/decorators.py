# -*- coding: utf-8 -*-
import os
import copy
import json
import inspect
import jsonschema
from .request import ArgumentsNormalizer


def validate(schema, *args, **kwds):
    frame = inspect.currentframe()
    prev_frame = frame.f_back
    parent_name = prev_frame.f_globals['__name__']
    try:
        module = __import__(
            parent_name, globals={}, locals={}, fromlist=True)
        module_path = module.__file__
    except ImportError:
        raise
    else:
        module_dir = os.path.dirname(module_path)
        try:
            schema = os.path.join(module_dir, schema)
        except AttributeError:  # schema is not string
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

    def _deco(func):
        def _wrap(self):
            setattr(self, 'validation_error', None)
            setattr(self, 'normalized_arguments', {})

            arguments = copy.deepcopy(self.request.arguments)
            normalizer = ArgumentsNormalizer()
            arguments = normalizer.normalize(arguments, schema)
            self.normalized_arguments = arguments

            try:
                jsonschema.validate(
                    self.normalized_arguments, schema)
            except jsonschema.exceptions.ValidationError as err:
                self.validation_error = err
            return func(self)
        return _wrap
    return _deco
