import yaml
import requests
import re

from types import SimpleNamespace

PARAMETER_PATTERN = re.compile('\$\{([^\}]+)\}')
def traverse_schema(schema, params):
  if isinstance(schema, dict):
    processed_schema = {}
    for key, value in schema.items():
      processed_schema[key] = traverse_schema(value, params)
    return SimpleNamespace(**processed_schema)

  elif isinstance(schema, list):
    return [ traverse_schema(v, params) for v in schema ]
  else:
    return process_parameters(schema, params)

def process_parameters(template, params):
  if re.search(PARAMETER_PATTERN, template):
    return template.replace('${', '{').format(**params)
  else:
    return template

class LastApi:
  def __init__(self, api_name):
    with open(api_name, 'r') as fp:
      self.schema = traverse_schema(yaml.load(fp), {})
