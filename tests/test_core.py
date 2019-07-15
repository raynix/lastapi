import unittest
from lastapi.core import *

class TestApiCore(unittest.TestCase):
  def test_process_parameters(self):
    test_template = 'test${variable}'
    test_params = { 'variable': 'asdf' }
    self.assertEqual(process_parameters(test_template,GLOBAL_PARAMETER_PATTERN, test_params), 'testasdf')

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
    sn = traverse_schema(test_schema, GLOBAL_PARAMETER_PATTERN, test_params)
    self.assertEqual(sn.key1, assert_schema['key1'])
    self.assertEqual(sn.key2.param1, assert_schema['key2']['param1'])
    self.assertEqual(sn.key3[2], assert_schema['key3'][2])

if __name__ == '__main__':
  unittest.main()
