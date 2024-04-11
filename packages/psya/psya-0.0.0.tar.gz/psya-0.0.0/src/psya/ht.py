from dataclasses import dataclass, field, replace
from typing import Any, Callable, Generic, Hashable, Iterable, Type, TypeVar
from weakref import WeakKeyDictionary

from psya.mut.ref import Ref

def hashable(x):
  if isinstance(x, Hashable):
    return x
  return Ref(x)

@dataclass(frozen=True, slots=True)
class Tag:
  tag_name: str = None
  classes: tuple[str, ...] = ()
  attrs: tuple[tuple[str, str], ...] = ()
  children: tuple[Hashable, ...] = ()
  events: tuple = ()
  refs: frozenset[Hashable] = frozenset()

  def __call__(self, *classes, **attrs):
    return replace(self,
                   classes=self.classes + classes,
                   attrs=self.attrs + tuple(attrs.items()))

  def __getitem__(self, children):
    if not isinstance(children, tuple):
      children = tuple((children,))
    return self.extend(children)

  def extend(self, children: Iterable):
    const_children, refs = constantize(children)
    return replace(self, children=self.children + tuple(const_children), refs=self.refs | refs)

def constantize(children: Iterable, children_out: list[Hashable]=None, refs_out=None):
  if children_out is None: children_out = []
  if refs_out is None: refs_out = set()
  for c in children:
    match c:
      case str():
        children_out.append(c)
      case Tag():
        children_out.append(c)
        refs_out.update(c.refs)
      case tuple():
        constantize(c, children_out, refs_out)
      case _:
        const = hashable(c)
        children_out.append(const)
        refs_out.add(const)
  return children_out, refs_out

def h(tag_name: str = None, *classes, **attrs):
  return Tag(tag_name, classes, tuple(attrs.items()))
