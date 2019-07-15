import yaml
import requests
import re

from types import SimpleNamespace
from pykwalify.core import Core

GLOBAL_PARAMETER_PATTERN = re.compile('(\$\{([^\}]+)\})')
ARGUMENTS_PATTERN = re.compile('(\#\{([^\}]+)\})')
# schema is a dict object reading from yaml
def traverse_schema(schema, pattern, params={}):
  if isinstance(schema, dict):
    processed_schema = {}
    for key, value in schema.items():
      processed_schema[key] = traverse_schema(value, pattern, params)
    return SimpleNamespace(**processed_schema)

  elif isinstance(schema, list):
    return [ traverse_schema(v, pattern, params) for v in schema ]
  elif isinstance(schema, str):
    return process_parameters(schema, pattern, params)
  else:
    return schema

def process_parameters(template, compiled_pattern, params):
  found = compiled_pattern.search(template)
  if found:
    return replace_argument(template, found).format(**params)
  else:
    return template

def replace_argument(template, match):
  groups = match.groups()
  search = groups[0]
  if len(groups) > 1:
    replace = groups[1]
  else:
    replace = groups[0]
  return template.replace(search, "{{{0}}}".format(replace))

class LastApi:
  def __init__(self, api_name):
    api_definition_file = "{0}.yaml".format(api_name)
    api_parameters_file = "{0}-params.yaml".format(api_name)
    c = Core(source_file=api_definition_file, schema_files=["schemas/schema.yaml"])
    c.validate(raise_exception=True)
    with open(api_parameters_file, 'r') as fp:
      params = yaml.load(fp)
    with open(api_definition_file, 'r') as fp:
      self.schema = yaml.load(fp)
    self.headers = traverse_schema(self.schema['Headers'], GLOBAL_PARAMETER_PATTERN, params)

  def invoke(self, action_name, params):
    pass

"""
  curl -X PUT $CFAPI/zones/$1/dns_records/$2 \
    -H "X-Auth-Key: $CFKEY" \
    -H "X-Auth-Email: raynix@gmail.com" \
    -H "Content-type: application/json" \
    --data "{\"type\":\"$3\",\"name\":\"$4\",\"content\":\"$5\",\"ttl\":1,\"proxied\":true}"
"""
