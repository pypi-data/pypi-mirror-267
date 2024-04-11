from abc import abstractmethod
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from typing import TypeVar

from psya.the import the, TheContext
from .ref import Ref, Ptr
from .events import Event

@dataclass
class Evaluation(TheContext):
  """tracks the set of deps and pins across some set of code

  deps are references whose state the code depends on. if they
  are mutated, the code's output may be stale

  pins are references the code outputs but doesn't necessarily
  hold onto itself. i.e. they are pointers we have sent to
  the client which we would like to remain dereferenceable
  for as long as the evaluation is valid
  """
  deps: set[Ref] = field(default_factory=set)
  pins: set[Ref] = field(default_factory=set)
  _token: Token = None

  def match(self, evt: Event):
    if evt.mutation.evaluation is self:
      # prevent loopback
      # (make this configurable later)
      return False
    return evt.target in self.deps

  def read(self, value):
    self.deps.add(Ref(value))
    return value
  
  def pin(self, ref: Ref) -> Ptr:
    self.pins.add(ref)
    return ref.ptr()

T = TypeVar('T')
def read(value: T) -> T:
  return the[Evaluation].read(value)

def pin(ref: Ref) -> Ptr:
  return the[Evaluation].pin(ref)
