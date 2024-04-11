from dataclasses import dataclass, field
from typing import Callable, Optional, Protocol

from .ref import Ref

class MutationInfo(Protocol):
  name: str
  tags: set
  evaluation: ...

@dataclass
class Done:
  target: Ref
  mutation: Optional[MutationInfo] = None

@dataclass
class Change:
  target: Ref

  fn: Callable
  "mutation function"
  args: tuple
  "positional args of fn"
  kwargs: dict = field(default_factory=dict)
  "kwargs of fn"

  mutation = None

Event = Done | Change