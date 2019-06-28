import yaml
import requests
import re

PARAMETER_PATTERN = re.compile('\$\{([^\}]+)\}')
def traverse_schema(schema, params):
  processed_schema = {}
  if isinstance(schema, dict):
    for key, value in schema.items():
      processed_schema[key] = traverse_schema(value, params)

  elif isinstance(schema, list):
    return [ traverse_schema(v, params) for v in schema ]
  else:
    return process_parameters(schema, params)
  return processed_schema

def process_parameters(template, params):
  if re.search(PARAMETER_PATTERN, template):
    return template.replace('${', '{').format(**params)
  else:
    return template
