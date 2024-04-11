from dataclasses import dataclass

"""A hashable identity reference to any object."""
@dataclass(frozen=True)
class Ref:
  target: ...
  def ptr(self):
    return Ptr(id(self.target))
  def __hash__(self): return id(self.target)
  def __eq__(self, other: object) -> bool:
    match other:
      case Ref(target): return target == self.target
      case Ptr(addr): return addr == id(self.target)
    return False

"""A bare pointer to an IdRef"""
@dataclass(frozen=True)
class Ptr:
  id: int
  def __hash__(self): return self.id
  def __eq__(self, other: object) -> bool:
    match other:
      case Ref(target): return id(target) == self.id
      case Ptr(addr): return addr == self.id
    return False
