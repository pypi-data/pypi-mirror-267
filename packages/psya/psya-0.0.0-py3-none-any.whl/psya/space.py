from contextvars import ContextVar
from typing import Generic, Protocol, TypeVar
from weakref import WeakKeyDictionary
from psya import the
from psya.mut.ref import Ref, Ptr

class Space(Protocol):
  def pin(self, ref: Ref) -> Ptr: ...
  def unpin(self, ptr: Ptr): ...
  def deref(self, ptr: Ptr) -> Ref: ...

def pin(self, ref: Ref) -> Ptr:
  return the[Space].pin(ref)

def unpin(self, ptr: Ptr):
  return the[Space].unpin(ptr)

def deref(self, ptr: Ptr) -> Ref:
  return the[Space].deref(ptr)
