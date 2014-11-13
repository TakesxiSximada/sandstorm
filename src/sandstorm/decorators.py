# -*- coding: utf-8 -*-
import os
import copy
import json
import jsonschema
from .utils import get_caller_module
from .request import ArgumentsNormalizer


def validate(schema, *args, **kwds):
    dotted, module, path, module_dir = get_caller_module()

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
