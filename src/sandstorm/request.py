# -*- coding: utf-8 -*-


class ArugmentsNormalizer(object):
    CAN_USE_TYPES = [
        'object',
        'number',
        'string',
        'array',
        'boolean',
        'integer',
        'null',
        ]

    def _is_str(self, obj):
        return hasattr(obj, 'encode') or hasattr(obj, 'decode')

    def _scalar(self, obj):
        return (obj[0] if
                not self._is_str(obj) and
                hasattr(obj, '__len__') and
                len(obj) == 1 else
                obj
                )

    def normalize(self, arguments, schema):
        typ = schema.get('type', None)
        if typ not in self.CAN_USE_TYPES:
            return arguments
        func = getattr(self, 'coerce_{}'.format(typ))
        return func(arguments, schema)

    def coerce_object(self, arguments, schema):
        if 'properties' not in schema:
            return arguments
        value = {}
        for name, subschema in schema['properties'].items():
            if name in arguments:
                subarg = arguments[name]
                value[name] = self.normalize(subarg, subschema)
        return value

    def coerce_array(self, arguments, schema):
        return arguments

    def coerce_string(self, arguments, schema):
        arguments = self._scalar(arguments)
        return arguments

    def coerce_number(self, arguments, schema):
        arguments = self._scalar(arguments)
        value = arguments
        try:
            value = float(arguments)
            value = int(arguments)
        except (TypeError, ValueError):
            pass
        return value

    def coerce_integer(self, arguments, schema):
        arguments = self._scalar(arguments)
        value = arguments
        try:
            value = int(arguments)
        except (TypeError, ValueError):
            pass
        return value

    def coerce_boolean(self, arguments, schema):
        arguments = self._scalar(arguments)
        return (arguments if
                hasattr(arguments, '__len__') else bool(arguments))

    def coerce_null(self, arguments, schema):
        arguments = self._scalar(arguments)
        return (arguments if
                hasattr(arguments, '__len__') else arguments)

import sys
import json
import argparse
import jsonschema
def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('schema')
    opts = parser.parse_args(argv)
    with open(opts.schema) as fp:
        schema = json.load(fp)
    req ={
        'second': [b'1'],
        'first': [b'1'],
        'third': [b'1'],
        }

    normalizer = ArugmentsNormalizer()
    import ipdb; ipdb.set_trace()
    res = normalizer.normalize(req, schema)
    print(res)


if __name__ == '__main__':
    main()
