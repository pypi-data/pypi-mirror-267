from collections import Counter
from dataclasses import dataclass, field
from typing import Generic, TypeVar

K = TypeVar('K')
V = TypeVar('V')
@dataclass
class RcDictionary(Generic[K, V], dict[K, V]):
  """a ref-counted dictionary. 
  
  ```
  d = RcDictionary()
  d['meaning'] = 42
  d['meaning'] = 42
  d['meaning'] = 'money' # ValueError: 'money' != 42
  del d['meaning']
  'meaning' in d # -> True
  del d['meaning']
  'meaning' in d # -> False
  del d['meaning'] # -> KeyError: 'meaning'
  ```  
  """
  refcounts: Counter[K] = field(default_factory=Counter)

  def __setitem__(self, key: K, value: V):
    existing = super().setdefault(key, value)
    if existing != value:
      raise ValueError(f"{key} is already associated with {existing}, not {value}")
    self.refcounts[key] += 1

  def __delitem__(self, key: K):
    count = self.refcounts
    count[key] -= 1
    if count[key] <= 0:
      del count[key]
      super().__delitem__(key)
  
  def update(self, other):
    for key, value in other: self[key] = value
  
  def setdefault(self, key, default):
    if key not in self: self[key] = default
    return self[key]


@dataclass
class BiDictionary(Generic[K, V]):
  forward: dict[K, set[V]] = field(default_factory=dict)
  reverse: dict[V, set[K]] = field(default_factory=dict)

  def __setitem__(self, key: K, new_values: set[V] = None):
    if new_values is None: new_values = set()
    existing_values = self.forward.get(key, set())
    for existing in existing_values:
      if existing not in new_values:
        self._unlink_rev(key, existing)
    for new in new_values:
      if new not in existing_values:
        self._link_rev(key, new)
    if not new_values:
      del self.forward[key]
    else:
      self.forward[key] = new_values

  def __getitem__(self, key: K):
    return self.forward[key]

  def __delitem__(self, key: K):
    self[key] = None

  def __contains__(self, key: K):
    return key in self.forward

  def _link_rev(self, key: K, value: V):
    keys_for_value = self.reverse.setdefault(value, set())
    keys_for_value.add(key)

  def _link_fwd(self, key: K, value: V):
    values_for_key = self.forward.setdefault(key, set())
    values_for_key.add(value)    

  def unlink(self, key: K, value: V):
    self._unlink_rev(key, value)
    self._unlink_fwd(key, value)

  def _unlink_rev(self, key: K, value: V):
    keys_for_value = self.reverse[value]
    if keys_for_value:
      keys_for_value.remove(key)
    if not keys_for_value:
      del self.reverse[value]

  def _unlink_fwd(self, key: K, value: V):
    values_for_key = self.forward[key]
    if values_for_key:
      values_for_key.remove(value)
    if not values_for_key:
      del self.forward[key]
