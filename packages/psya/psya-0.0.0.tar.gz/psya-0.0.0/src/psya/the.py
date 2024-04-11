from contextvars import ContextVar
from typing import Generic, Protocol, TypeVar
from weakref import WeakKeyDictionary

from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass
class DefiniteArticle:
  name: str
  vars: WeakKeyDictionary[type[T], ContextVar[T]] = field(default_factory=WeakKeyDictionary)

  def __getitem__(self, type):
    return self.vars[type].get()
  
  def get(self, type, default):
    if type not in self.vars: return default
    return self.vars.get(type).get(default)
  
  def var(self, type):
    var = self.vars.get(type, None)
    if not var:
      var = ContextVar[type](f'{self.name}[{type}]')
      self.vars[type] = var
    return var
  
  def __call__(self, type, value):    
    return Definition[type](self.var(type), value)

@dataclass
class Definition(Generic[T]):
  var: ContextVar[T]
  value: T
  _token: ... = None

  def __enter__(self):
    self._token = self.var.set(self.value)
  
  def __exit__(self, *_):
    self.var.reset(self._token)

the = DefiniteArticle('the')

@dataclass
class TheContext:
  _def: ... = field(kw_only=True, default=None)

  def __enter__(self):
    definition = the(type(self), self)
    self._def = definition
    definition.__enter__()
    return self

  def __exit__(self, *ex):
    self._def.__exit__(self, *ex)
