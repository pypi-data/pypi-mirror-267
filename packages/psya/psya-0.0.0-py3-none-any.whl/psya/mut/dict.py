from typing import Mapping, Iterable
from dataclasses import dataclass, field

from psya.mut.events import Change
from psya.mut.ref import Ref
from psya.mut.observer import notify

class MutMapping:
  "a mixin for mappings which notifies on changes"
  def __setitem__(self, key, value):
    with DiffMap(self, (key,)):
      super().__setitem__(key, value)

  def __delitem__(self, key):
    with DiffMap(self, (key,)):
      super().__delitem__(key)

  def setdefault(self, key, default):
    with DiffMap(self, (key,)):
      super().setdefault(key, default)

  def update(self, other: Mapping):
    with DiffMap(self, other.keys()):
      super().update(other)

class MutDict(MutMapping, dict):
  "a dict which issues mutation events when changed"
  ...

@dataclass(frozen=True)
class NotFound: ...
NOT_FOUND = NotFound

@dataclass(frozen=True)
class DiffMap:
  target: Mapping
  keys: Iterable
  old_values: dict = field(init=False, default_factory=dict)

  def __enter__(self):
    old_values = self.old_values
    for key in self.keys:
      old_values[key] = self.target.get(key, NOT_FOUND)

  def __exit__(self, *_):
    target = self.target
    setitem = type(target).__setitem__
    delitem = type(target).__delitem__
    for key, old_value in self.old_values.items():
      new_value = target.get(key, NOT_FOUND)
      if new_value != old_value:
        if new_value is NOT_FOUND:
          notify(Change(Ref(target), delitem, (target, key)))
        else:
          notify(Change(Ref(target), setitem, (target, key, new_value)))
