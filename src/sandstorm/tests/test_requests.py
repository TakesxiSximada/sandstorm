# -*- coding: utf-8 -*-
from unittest import TestCase


class ArgumentsCleanerTest(TestCase):
    def _create(self):
        from ..requests import ArgumentsCleaner
        return ArgumentsCleaner()

    def _create_arguments(self):
        return {
            'string': 'string object',
            'number': 1,
            'integer': [3],
            'boolean': [False],
            'null': None,
            'array': [1, 2, 3, 4],
            'array2[]': [1, 2, 3, 4],
            'object': {
                'string': 'string object',
                'number': 1,
                'integer': [3],
                'boolean': [False],
                'null': None,
                'array': [1, 2, 3, 4],
                'array2[]': [1, 2, 3, 4],
                }
            }

    def _create_cleaned_arguments(self):
        return {
            'string': 'string object',
            'number': 1,
            'integer': [3],
            'boolean': [False],
            'null': None,
            'array': [1, 2, 3, 4],
            'array2': [1, 2, 3, 4],
            'object': {
                'string': 'string object',
                'number': 1,
                'integer': [3],
                'boolean': [False],
                'null': None,
                'array': [1, 2, 3, 4],
                'array2': [1, 2, 3, 4],
                }
            }

    def test_clean(self):
        cleaner = self._create()
        arguments = self._create_arguments()
        val = cleaner.clean(arguments)
        cleaned_arguments = self._create_cleaned_arguments()
        self.assertEqual(val, cleaned_arguments)


class ArgumentsNormalizerTest(TestCase):
    def _create(self):
        from ..requests import ArgumentsNormalizer
        return ArgumentsNormalizer()

    def _create_arguments(self):
        return {
            'string': 'string object',
            'number': 1,
            'integer': [3],
            'boolean': [False],
            'null': None,
            'array': [1, 2, 3, 4],
            'object': {
                'string': 'string object',
                'number': 1,
                'integer': [3],
                'boolean': [False],
                'null': None,
                'array': [1, 2, 3, 4],
                }
            }

    def _create_normalized_arguments(self):
        return {
            'string': 'string object',
            'number': 1,
            'integer': 3,
            'boolean': False,
            'null': None,
            'array': [1, 2, 3, 4],
            'object': {
                'string': 'string object',
                'number': 1,
                'integer': 3,
                'boolean': False,
                'null': None,
                'array': [1, 2, 3, 4],
                }
            }

    def _create_schema(self):
        return {
            'type': 'object',
            'properties': {
                'string': {'type': 'string'},
                'number': {'type': 'number'},
                'integer': {'type': 'integer'},
                'boolean': {'type': 'boolean'},
                'null': {'type': 'null'},
                'array': {'type': 'array'},
                'object': {
                    'type': 'object',
                    'properties': {
                        'string': {'type': 'string'},
                        'number': {'type': 'number'},
                        'integer': {'type': 'integer'},
                        'boolean': {'type': 'boolean'},
                        'null': {'type': 'null'},
                        'array': {'type': 'array'},
                        },
                    },
                },
            }

    def _create_schema_cannot_using_type(self):
        return {
            'type': 'cannot using type',
            'properties': {
                'string': {'type': 'string'},
                'number': {'type': 'number'},
                'integer': {'type': 'integer'},
                'boolean': {'type': 'boolean'},
                'null': {'type': 'null'},
                'array': {'type': 'array'},
                'object': {
                    'type': 'cannot using type',
                    'properties': {
                        'string': {'type': 'string'},
                        'number': {'type': 'number'},
                        'integer': {'type': 'integer'},
                        'boolean': {'type': 'boolean'},
                        'null': {'type': 'null'},
                        'array': {'type': 'array'},
                        },
                    },
                },
            }

    def test_normalize(self):
        arguments = self._create_arguments()
        normalized_arguments = self._create_normalized_arguments()
        schema = self._create_schema()
        normalizer = self._create()
        val = normalizer.normalize(arguments, schema)
        self.assertEqual(normalized_arguments, val)

    def test_normalize_cannot_using_type(self):
        arguments = self._create_arguments()
        schema = self._create_schema_cannot_using_type()
        normalizer = self._create()
        val = normalizer.normalize(arguments, schema)
        self.assertEqual(arguments, val)


class ArgumentsNormalizerObjectTest(ArgumentsNormalizerTest):
    def _create_harf_normalized_arguments(self):
        return {
            'string': 'string object',
            'number': 1,
            'integer': 3,
            'boolean': False,
            'null': None,
            'array': [1, 2, 3, 4],
            'object': {
                'string': 'string object',
                'number': 1,
                'integer': [3],
                'boolean': [False],
                'null': None,
                'array': [1, 2, 3, 4],
                }
            }

    def _create_schema_no_property(self):
        return {
            'type': 'object',
            'property-aaa': {  # typo
                'string': {'type': 'string'},
                'number': {'type': 'number'},
                'integer': {'type': 'integer'},
                'boolean': {'type': 'boolean'},
                'null': {'type': 'null'},
                'array': {'type': 'array'},
                'object': {
                    'type': 'object',
                    'properties': {
                        'string': {'type': 'string'},
                        'number': {'type': 'number'},
                        'integer': {'type': 'integer'},
                        'boolean': {'type': 'boolean'},
                        'null': {'type': 'null'},
                        'array': {'type': 'array'},
                        },
                    },
                },
            }

    def test_coerce_object(self):
        arguments = self._create_arguments()
        normalized_arguments = self._create_normalized_arguments()
        schema = self._create_schema()
        normalizer = self._create()
        val = normalizer.coerce_object(arguments, schema)
        self.assertEqual(normalized_arguments, val)

    def test_coerce_object_cannot_using_type(self):
        arguments = self._create_arguments()
        normalized_arguments = self._create_harf_normalized_arguments()
        schema = self._create_schema_cannot_using_type()
        normalizer = self._create()
        val = normalizer.coerce_object(arguments, schema)
        self.assertEqual(normalized_arguments, val)

    def test_coerce_object_no_property_schema(self):
        arguments = self._create_arguments()
        schema = self._create_schema_no_property()
        normalizer = self._create()
        val = normalizer.coerce_object(arguments, schema)
        self.assertEqual(arguments, val)


class ArgumentsNormalizerArrayTest(ArgumentsNormalizerTest):
    def test_coerce_array_scalar(self):
        value = 'array object'
        arguments = value
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_array(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_array_single_element_list(self):
        value = 'array object'
        arguments = [value]
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_array(arguments, schema)
        self.assertEqual(arguments, val)

    def test_coerce_array_multi_element_list(self):
        value = 'array object'
        arguments = [value, 1, 'A']
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_array(arguments, schema)
        self.assertEqual(arguments, val)

    def test_coerce_array_no_array(self):
        value = -100
        arguments = [value]
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_array(arguments, schema)
        self.assertEqual(arguments, val)


class ArgumentsNormalizerStringTest(ArgumentsNormalizerTest):
    def test_coerce_string_scalar_string(self):
        value = 'string object'
        arguments = value
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_string(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_string_scalar_unicode(self):
        value = u'unicode object'
        arguments = value
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_string(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_string_scalar_binary(self):
        value = b'binary object'
        arguments = value
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_string(arguments, schema)
        self.assertEqual(value.decode(), val)

    def test_coerce_string_single_element_list(self):
        value = 'string object'
        arguments = [value]
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_string(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_string_multi_element_list(self):
        value = 'string object'
        arguments = [value, 1, 'A']
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_string(arguments, schema)
        self.assertEqual(arguments, val)

    def test_coerce_string_no_string(self):
        value = -100
        arguments = [value]
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_string(arguments, schema)
        self.assertEqual(value, val)


class ArgumentsNormalizerNumberTest(ArgumentsNormalizerTest):
    def test_coerce_number_scalar_true(self):
        value = 0
        arguments = value
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_number(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_number_single_element_list(self):
        value = 1
        arguments = [value]
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_number(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_number_multi_element_list(self):
        value = 100
        arguments = [value, 1, 'A']
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_number(arguments, schema)
        self.assertEqual(arguments, val)

    def test_coerce_number_negative_number(self):
        value = -100
        arguments = value
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_number(arguments, schema)
        self.assertEqual(value, val)


class ArgumentsNormalizerIntegerTest(ArgumentsNormalizerTest):
    def test_coerce_integer_scalar_true(self):
        value = 0
        arguments = value
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_integer(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_integer_single_element_list(self):
        value = 1
        arguments = [value]
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_integer(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_integer_multi_element_list(self):
        value = 100
        arguments = [value, 1, 'A']
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_integer(arguments, schema)
        self.assertEqual(arguments, val)

    def test_coerce_integer_negative_number(self):
        value = -100
        arguments = value
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_integer(arguments, schema)
        self.assertEqual(value, val)


class ArgumentsNormalizerBooleanTest(ArgumentsNormalizerTest):
    def test_coerce_boolean_scalar_true(self):
        value = True
        arguments = value
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_boolean(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_boolean_single_element_list(self):
        value = True
        arguments = [value]
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_boolean(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_boolean_multi_element_list(self):
        value = False
        arguments = [value, 1, 'A']
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_boolean(arguments, schema)
        self.assertEqual(arguments, val)


class ArgumentsNormalizerNullTest(ArgumentsNormalizerTest):
    def test_coerce_null_scalar(self):
        value = None
        arguments = value
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_null(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_null_single_element_list(self):
        value = None
        arguments = [value]
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_null(arguments, schema)
        self.assertEqual(value, val)

    def test_coerce_null_multi_element_list(self):
        value = None
        arguments = [value, 1, 'A']
        schema = {}
        normalizer = self._create()
        val = normalizer.coerce_null(arguments, schema)
        self.assertEqual(arguments, val)
