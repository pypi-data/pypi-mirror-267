# standard imports
import copy
import unittest

# local imports
from potaahto.symbols import snake_and_camel
from potaahto.symbols import ensure_key
from potaahto.symbols import mimic_key


class TestFauna(unittest.TestCase):

    def test_snake_and_camel(self):
        k_stupid = {
            'fooBarBaz': 1,
            'barBazFoo': 2,
            'baz_foo_bar': 3,
            }
        
        k = snake_and_camel(k_stupid)

        self.assertEqual(k['fooBarBaz'], 1)
        self.assertEqual(k['barBazFoo'], 2)
        self.assertEqual(k['bazFooBar'], 3)

        self.assertEqual(k['foo_bar_baz'], 1)
        self.assertEqual(k['bar_baz_foo'], 2)
        self.assertEqual(k['baz_foo_bar'], 3)


    def test_ensure(self):
        k_stupid = {
            'fooBarBaz': 1,
            'barBazFoo': 2,
            }

        k = copy.copy(k_stupid)
        k = ensure_key(k, 'barBazFoo', 42)
        self.assertDictEqual(k_stupid, k)
        self.assertEqual(k['barBazFoo'], 2)

        k = copy.copy(k_stupid)
        ensure_key(k, 'barBazFoo', 42)
        self.assertEqual(k['barBazFoo'], 2)

        k = copy.copy(k_stupid)
        k = ensure_key(k, 'bazFooBar', 42)
        try:
            self.assertDictEqual(k_stupid, k)
        except AssertionError:
            self.assertEqual(k['bazFooBar'], 42)

        k = copy.copy(k_stupid)
        k = ensure_key(k, 'baz_foo_bar', 42)
        self.assertEqual(k['baz_foo_bar'], 42)

        k = copy.copy(k_stupid)
        k = ensure_key(k, 'foo_bar_baz', 42)
        self.assertEqual(k['fooBarBaz'], 1)

        k = copy.copy(k_stupid)
        ensure_key(k, 'baz_foo_bar', 42)
        self.assertEqual(k['baz_foo_bar'], 42)


    def test_mimic(self):
        k_stupid = {
            'fooBarBaz': 1,
            'barBazFoo': 2,
            }

        k = copy.copy(k_stupid)
        k = mimic_key(k, 'barBazFoo', 'xyzzy', 42)
        self.assertEqual(k['xyzzy'], 2)

        k = copy.copy(k_stupid)
        k = mimic_key(k, 'baz_baz_baz', 'inkyPinky')
        self.assertNotIn('baz_baz_baz', k.keys())
        self.assertNotIn('inkyPinky', k.keys())

        k = copy.copy(k_stupid)
        k = mimic_key(k, 'baz_baz_baz', 'inkyPinky', default_value=42)
        self.assertEqual(k['baz_baz_baz'], 42)
        self.assertEqual(k['inkyPinky'], 42)


if __name__ == '__main__':
    unittest.main()
