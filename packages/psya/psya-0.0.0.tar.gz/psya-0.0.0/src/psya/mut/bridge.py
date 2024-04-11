from dataclasses import dataclass, field
from typing import Iterable
from typing import TypeVar

from psya.mut.ref import Ref, Ptr
from psya.dicts import RcDictionary

K = TypeVar('K')
@dataclass
class Bridge:
  "maintain a reversible Ptr mapping, given a set of id'd pin sets"
  references: RcDictionary[Ptr, Ref] = field(default_factory=RcDictionary)
  pins: dict[K, set[Ptr]] = field(default_factory=dict)

  def pin(self, key: K, pins: set[Ref]):
    for ref in pins:
      self.references[ref.ptr()] = ref
    if key in self.pins: self.drop(key)
    self.pins[key] = pins
  
  def drop(self, key: K):
    for ptr in self.pins[key]:
      del self.references[ptr]
    del self.pins[key]

  def deref(self, ptr: Ptr) -> Ref:
    return self.references[ptr]
  
  def __contains__(self, ptr: Ptr):
    return ptr in self.references
  
  def __getitem__(self, ptr: Ptr):
    return self.deref(ptr)


