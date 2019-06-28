import unittest
from lastapi.core import *

class TestApiCore(unittest.TestCase):
  def test_process_parameters(self):
    test_template = 'test${variable}'
    test_params = { 'variable': 'asdf' }
    self.assertEqual(process_parameters(test_template, test_params), 'testasdf')

  def test_traverse_schema(self):
    test_schema = {
      'key1': 'v1',
      'key2': { 'param1': 'test${variable}'},
      'key3': [ 'alpha', 'beta', '${theta}' ]
    }
    test_params = { 'variable': 'asdf', 'theta': 'theta' }
    assert_schema = {
      'key1': 'v1',
      'key2': { 'param1': 'testasdf'},
      'key3': [ 'alpha', 'beta', 'theta' ]
    }
    self.assertEqual(traverse_schema(test_schema, test_params), assert_schema)

if __name__ == '__main__':
  unittest.main()
