from ast import arguments
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, AsyncIterator, Protocol
import itertools

class Agent(Protocol):
  @property
  def __name__(self) -> str: ...
  async def __call__(self, subscription: 'Sub') -> AsyncIterator[Any]: ...

@dataclass
class Room:
  history: list = field(default_factory=list)
  agents: dict[str, 'Sub'] = field(default_factory=dict)

  def push(self, message):
    self.history.append(message)
    for agent in self.agents.values():
      agent.notify()

  @property
  def now(self):
    return len(self.history)

  def join(self, agent) -> 'Sub':
    name = agent.__name__
    for i in itertools.count(1):
      if name not in self.agents: break
      name = f'{agent.__name__}_{i}'
    sub = Sub(self, agent, name, self.now)
    self.agents[name] = sub
    self.push(Joined(name, agent))
    return sub
  
  def is_current(self, index: int):
    return index >= len(self.history)
  
  def __getitem__(self, index):
    return self.history[index]

@dataclass
class Joined:
  name: str
  agent: Agent

from typing import Generic, TypeVar
T = TypeVar('T')

@dataclass
class Msg(Generic[T]):
  sender: str
  body: T

from asyncio import sleep, gather, Task, Event, create_task

class Sub:
  room: Room
  agent: Agent
  name: str
  at: int | slice

  _task: Task = None
  _dirty: Event = None

  def __init__(self, room: Room, agent: Agent, name: str, at: int):
    self.room = room
    self.agent = agent
    self.name = name
    self.at = at

    self._task = create_task(self.send(agent(self)))
    self._dirty = Event()

  def __hash__(self): return id(self)

  def notify(self): self._dirty.set()

  @property
  async def done(self): await self._task

  def __aiter__(self): return self

  async def __anext__(self) -> list:
    match self.at:
      case slice(): self.at = self.at.stop
    while self.at >= self.room.now:
      await self._dirty.wait()
    self._dirty.clear()
    self.at = slice(self.at, self.room.now)
    messages = self.room[self.at]
    return messages
  
  async def send(self, stream):
    async for message in aiterable(stream):
      self.room.push(Msg(self.name, message))

@dataclass
class aiterable:
  iter: ...
  def __aiter__(self): return aiter(self.iter)
