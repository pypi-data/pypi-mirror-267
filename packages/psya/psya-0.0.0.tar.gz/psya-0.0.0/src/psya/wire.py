from dataclasses import fields, is_dataclass
from functools import cached_property, partial
import json
import inspect
import traceback as tb
import importlib

function = type(lambda: None)

class Json:
  def encode(self, obj) -> str:
    return self.encoder.encode(obj)
  
  def decode(self, string: str) -> ...:
    return self.decoder.decode(string)

  @cached_property
  def encoder(self):
    return json.JSONEncoder(separators=(',',':'), default=self.encode_default)
  
  @cached_property
  def decoder(self):
    return json.JSONDecoder(object_hook=self.decode_object)
  
  def encode_static(self, type):
    module = type.__module__
    qualname = type.__qualname__
    return f'{module}:{qualname}'

  def encode_default(self, obj):
    if isinstance(obj, Merge):      
      return {**self.encode_default(obj.obj), **obj.extra}
    data = {'__class__': self.encode_static(type(obj)) }
    if is_dataclass(obj):
      data.update({(f.name): getattr(obj, f.name) for f in fields(obj)})
      return data
    match obj:
      case BaseException():
        data['__traceback__'] = tb.format_tb(obj.__traceback__)
      case function():
        data['$static'] = self.encode_static(obj)
      case _:
        data['__str__'] = str(obj)
    return data

  def resolve_static(self, static: str):
    module_name, qual_name = static.split(':')
    node = importlib.import_module(module_name)    
    for part in qual_name.split('.'):
      if part: node = getattr(node, part)
    return node

  def decode_object(self, d: dict):
    static = d.get('$static')
    if static:
      object = self.resolve_static(static)
      if callable(object):
        args, kwargs = [], {}
        for key, value in d.items():
          if key in ('__class__', '$static'): continue
          try:
            _index = int(key)
            args.append(value)
          except ValueError:
            kwargs[key] = value
        if args or kwargs:
          return partial(object, *args, **kwargs)
      return object
    class_name = d.get('__class__')
    if not class_name: return d
    return sloppycall(self.decode_static(class_name), d)

class Merge:
  def __init__(self, obj, **extra):
    self.obj = obj
    self.extra = extra


KW_PARAMETER_TYPES = frozenset((inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY))
def sloppycall(fn, kws):
  # Get the signature of the function
  params = inspect.signature(fn).parameters
  
  # Exclude any items from kws which are not valid keyword parameters of fn
  valid_kws = {key: value for key, value in kws.items()
                if getattr(params.get(key, None), 'kind', None) in KW_PARAMETER_TYPES}
  
  # Call fn with valid_kws
  return fn(**valid_kws)
