import asyncio as aio
from typing import Callable, TypeVar
from weakref import WeakKeyDictionary

from psya.mut.evaluation import Evaluation
from psya.the import TheContext, the

from .events import Change, Done, MutationInfo
from .ref import Ref

from dataclasses import dataclass, field

@dataclass
class Mutation(TheContext, MutationInfo):
  """An ongoing or scheduled mutation."""
  name: str = None
  tags: set = field(default_factory=set)
  done: aio.Event = aio.Event()
  targets: set[Ref] = field(default_factory=set)
  evaluation: Evaluation = None

  def touch(self, ref):
    self.targets.add(ref)

  def lock(self, target):
    """Synchronously lock a target.
    
    Raises LockedError if the target is already locked by another mutation."""
    ref = Ref(target)
    mutation = MUTATOR.setdefault(ref, self)
    if mutation is not self:
      raise LockedError(target, mutation, self)
    self.touch(ref)

  async def alock(self, target):
    """Asynchronously lock a target.
    
    If the target is currently being mutated, waits until the current mutation
    completes."""
    ref = Ref(target)
    while True:
      mutation = MUTATOR.setdefault(ref, self)
      if mutation is self: break
      await mutation.done.wait()
    self.touch(ref)

  def close(self):
    """Unlock all targets held by this mutation"""
    for ref in self.targets:
      notify(Done(ref))
      if MUTATOR[ref] is self:
        del MUTATOR[ref]
    self.done.set()

  def __enter__(self):
    self.evaluation = the.get(Evaluation, None)
    super().__enter__()

  def __exit__(self, *args):
    super().__exit__()
    self.close()

def mutation(name_or_func: str | Callable, *tags):
  name = getattr(name_or_func, '__name__', name_or_func)
  if not isinstance(name, str):
    name = None
  return Mutation(name, tags)

@dataclass
class LockedError(RuntimeError):
  """Attempted to mutate an object which is already locked for mutation."""
  target: ...
  current_mutation: Mutation
  failed_mutation: Mutation

MUTATION = the.var(Mutation)
MUTATOR = WeakKeyDictionary[Ref, Mutation]()

T = TypeVar('T')
def touch(target: T) -> T:
  MUTATION.get().lock(target)

def lock(target: T) -> T:
  """Synchronously lock an object for mutation.
  
  Raises LockedError if the target is already locked by another mutation.  
  Raises AttributeError if there is no current mutation."""
  MUTATION.get().lock(target)
  return target

async def alock(target: T) -> T:
  """Asynchronously lock an object for mutation.
  
  If the target is currently being mutated, waits until the current mutation
  completes.
  
  Raises AttributeError if there is no current mutation."""
  await MUTATION.get().alock(target)
  return target

def is_mut(target):
  """True if the target is being mutated, False otherwise"""
  return Ref(target) in MUTATOR

def get_mut(target):
  """Get the mutation currently modifying target"""
  return MUTATOR[Ref(target)]

def mut(bound_method: Callable, /, *args, **kwargs):
  """Mutate an object.
  
  Raises LockedError if the object is already being mutated elsewhere."""
  (method, args) = normalize_call(bound_method, args)
  self = args[0]
  touch(self)
  notify(Change(Ref(self), method, args, kwargs))
  return method(*args, **kwargs)

def normalize_call(maybe_bound: Callable, args):
  if hasattr(maybe_bound, '__self__'):
    method, self = unbind(maybe_bound)
    return (method, (self, *args))
  return (maybe_bound, args)

def unbind(bound_fn):
  bound_self = bound_fn.__self__
  method_name = bound_fn.__name__
  unbound_fn = getattr(type(bound_self), method_name)
  return unbound_fn, bound_self

from .observer import notify