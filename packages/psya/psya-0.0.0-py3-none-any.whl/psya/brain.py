from abc import abstractmethod
import asyncio as aio
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from functools import partial
from typing import Any, AsyncIterable, AsyncIterator, Callable, Protocol

from psya.the import the
from psya.dicts import BiDictionary
from psya.mut.bridge import Bridge
from psya.mut.evaluation import Evaluation
from psya.mut.ref import Ref
from psya.mut.observer import Receiver, Subscription
from psya.mut import Event
from psya.mut.dict import MutDict

class Emit(Protocol):
  def __call__(self, msg: ...): ...

ChanId = Any

@dataclass
class Msg:
  id: ChanId = field(default=None, kw_only=True)

@dataclass
class Data(Msg):
  data: ...

@dataclass
class Error(Msg):
  error: BaseException

@dataclass
class Cell:
  emit: Emit
  keep_alive: bool = field(default=False, kw_only=True)
  evaluation: Evaluation = None
  task: aio.Task = None

  def __hash__(self): return id(self)

  async def evaluate(self, globals) -> Evaluation:
    with Evaluation() as evaluation:
      self.evaluation = evaluation
      try:
        self.emit(Data(await self(globals)))
      except BaseException as ex:
        self.emit(Error(ex))
    return evaluation

  @abstractmethod
  async def __call__(self, globals) -> Any: ...

class Send(Protocol):
  def __call__(self, msg, **ext): ...

Recv = Callable[[], AsyncIterable[Any]]

@dataclass
class Brain(Receiver):
  globals: dict = field(default_factory=MutDict)

  deps: BiDictionary[Cell, Ref] = field(default_factory=BiDictionary)
  dirty: set[Cell] = field(default_factory=set)
  is_dirty: aio.Event = field(default_factory=aio.Event)
  activity: aio.Task = None

  async def run(self):
    with Subscription(self):
      while True:
        await self.is_dirty.wait()
        self.process()
        self.is_dirty.clear()

  def wake(self):
    activity = self.activity
    if activity and not activity.done():
      return
    self.start()
  
  def start(self):
    activity = self.activity
    if activity and not activity.done():
      activity.cancel()
    self.activity = aio.create_task(self.run())
  
  def process(self):
    while self.dirty:
      cell = self.dirty.pop()
      self.evaluate(cell)

  def evaluate(self, cell: Cell):
    if cell.task: cell.task.cancel()
    cell.task = aio.create_task(self.run_cell(cell))

  def kill(self, cell):
    if cell.task: cell.task.cancel()

  def remove(self, cell: Cell):
    del self.deps[cell]
    self.dirty.remove(cell)
    
  async def run_cell(self, cell: Cell):
    evaluation = await cell.run(self.globals, self.locals)
    if cell.keep_alive:
      self.deps[cell] = evaluation.deps
    else:
      del self.deps[cell]

  def _mut_notify_(self, event: Event):
    cells = self.deps.reverse.get(event.target, [])
    self.dirty.update(cells)
    if cells: self.is_dirty.set()

class Emit(Protocol):
  def __call__(self, msg, **extra): ...

@dataclass
class Portal:
  brain: Brain
  bridge: Bridge = field(default_factory=Bridge)
  cells: dict[ChanId, Cell] = field(default_factory=dict)

  def mount(self, *, id: ChanId, cell: Cell):
    cell.emit = partial(the[Emit], id=id)
    existing = self.cells.setdefault(id, cell)
    if existing != cell:
      self.brain.kill(existing)
      self.brain.remove(existing)
    self.cells[id] = cell
    self.brain.evaluate(cell)

  def unmount(self, *, id: ChanId):
    existing = self.cells.get(id, None)
    if existing:
      self.brain.kill(existing)
      self.brain.remove(existing)
    del self.cells[id]

  @abstractmethod
  def send(self, message, **extras):
    ...

  @abstractmethod
  def recv(self) -> AsyncIterator: ...

  async def run(self):
    with the(Emit, self.send):
      async for cmd in self.recv():
        id = getattr(cmd, 'id', None)
        with the(Emit, partial(self.send, id=id)):
          cmd(self)

  def __enter__(self): return self

  def __exit__(self, *_ex):
    brain = self.brain
    for cell in self.cells.values():
      brain.kill(cell)
      brain.remove(cell)