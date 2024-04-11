
import asyncio as aio
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import AsyncIterable, AsyncIterator, Callable, Protocol, TypeVar

from .mutation import MUTATION
from .events import Done, Event
from .ref import Ref

T = TypeVar('T')

class Receiver(Protocol):
  def _mut_notify_(self, event: Event): ...

def everything(e: Event):
  return True

@dataclass
class MutationObserver(Receiver, AsyncIterator[Event], AsyncIterable[Event]):
  filter: Callable[[Event], bool] = everything
  _mut_queue: aio.Queue = field(default_factory=aio.Queue, kw_only=True)
  _sub: 'Subscription' = field(default=None, kw_only=True)

  def observe(self):
    if not self._sub:
      self._sub = Subscription(self)
    self._sub.__enter__()

  @property
  def empty(self):
    return self._mut_queue.empty()
  
  def disconnect(self):
    if self._sub:
      self._sub.__exit__()
      if not self._sub.active:
        self._sub = None

  def __enter__(self):
    self.observe()

  def __exit__(self, *args):
    self.disconnect()    

  def __hash__(self): return id(self)

  def _mut_notify_(self, event: Event):
    if self.filter(event):
      self._mut_queue.put_nowait(event)

  def __aiter__(self): return self

  async def __anext__(self):
    sync = sync_batch(self._mut_queue)
    if sync: return sync      
    if not self._sub:
      raise StopAsyncIteration()
    return await batch(self._mut_queue)

async def batch(queue: aio.Queue[T]) -> list[T]:
  return [await queue.get(), *sync_batch(queue)]

def sync_batch(queue: aio.Queue[T]) -> list[T]:
  msgs = []
  try:
    while True:
      msgs.append(queue.get_nowait())
  finally:
    return msgs

OBSERVERS = ContextVar[set[Receiver]]('observers', default=set())

def notify(event):
  if not event.mutation:
    event.mutation = MUTATION.get(None)
  for obs in OBSERVERS.get():
    obs._mut_notify_(event)

@dataclass
class Subscription:
  receiver: Receiver
  receiver_set: set[Receiver] = None

  @property
  def active(self):
    return self.receiver_set is not None

  def __enter__(self):
    self.receiver_set = OBSERVERS.get()
    self.receiver_set.add(self.receiver)
  
  def __exit__(self, *args):
    self.receiver_set.remove(self.receiver)
    self.receiver_set = None

async def watch(target, until_done=True):
  watching: set[Ref] = set((Ref(target),))
  obs = MutationObserver(lambda e: e.target in watching)
  with obs:
    async for events in obs:
      yield events
      for event in events:
        match event:
          case Done(target as t) if t == target:
            if until_done: return