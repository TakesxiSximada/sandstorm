# -*- coding: utf-8 -*-


class ArgumentsCleaner(object):
    def clean(self, arguments):
        if hasattr(arguments, 'items'):  # dict like?
            return dict((key.strip('[]'), self.clean(value)) for key, value in arguments.items())
        elif hasattr(arguments, 'pop'):  # iterator?
            return [self.clean(arg) for arg in arguments]
        else:
            return arguments


class ArgumentsNormalizer(object):
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
        _decode = lambda word: word.decode() if hasattr(word, 'decode') else word
        arguments = self._scalar(arguments)
        arguments = _decode(arguments)
        if not hasattr(arguments, 'encode'):  # list ?
            try:
                arguments = list(map(_decode, arguments))
            except Exception:  # cannot coerce -> ignore
                pass
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
        return self._scalar(arguments)
