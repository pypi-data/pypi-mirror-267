import asyncio as aio
from dataclasses import dataclass, field
from typing import Hashable, Mapping
from weakref import ReferenceType, WeakKeyDictionary, WeakValueDictionary, ref

from .mut.observer import MutationObserver

from . import mut
from .view import View, Paint, walk
from .ht import Tag, h, hashable

@dataclass(slots=True, weakref_slot=True)
class Node:
  shell: 'Shell'
  subject: Hashable
  refs: tuple['Node', ...] = ()

  def __hash__(self):
    return hash(self.subject)

  def __del__(self):
    self.shell._drop(self)

class Shell:
  root: Node
  paint: Paint

  _observer: MutationObserver

  def __init__(self, subject: Hashable, paint: Paint = View):
    subj = hashable(subject)
    self.root = Node(self, hashable(subject))
    self.paint = paint
    self._nodes = WeakValueDictionary()
    self._nodes[subj] = self.root
    self._observer = MutationObserver(filter=lambda e: e.target in self._nodes)
  
  def open(self):
    self._observer.observe()
    yield from walk(self.root.subject, self.render)

  def render(self, data: Hashable) -> Tag | str:
    view = self.paint(data)
    if isinstance(view, Tag):
      self[data].refs = tuple(self[r] for r in view.refs)
    return view

  def connect(self, send, messages):
    self._output_task = aio.create_task(self._send_output(send))
    self._input_task = aio.create_task(self._read_input(messages))

  async def done(self):
    await aio.gather(self._input_task, self.output_task)

  def close(self):
    if self._output_task:
      self._output_task.cancel()
      self._output_task = None
    if self._input_task:
      self._input_task.cancel()
      self._input_task = None

  _output_task: aio.Task = None
  _output_sending: bool = False
  async def _send_output(self, send):
    async for events in self._observer:
      self._output_sending = True
      await send(events)
      self._output_sending = False

  async def flush(self):
    while self._output_sending or not self._observer.empty:
      await aio.sleep(0.1)

  _input_task: aio.Task = None
  async def _read_input(self, messages): ...
  
  _nodes: dict[Hashable, Node] = field(default_factory=WeakValueDictionary)
  def __getitem__(self, data: Hashable) -> Node:    
    if data not in self._nodes:
      node = Node(self, data)
      self._nodes[data] = node
    return self._nodes[data]
  
  def _drop(self, node: Node):
    if id(self._nodes.get(node.subject, None)) == node:
      del self._nodes[node.subject]

# def html_lines(data: ..., render=View, level=0):
#   rendered = render(data)
#   match rendered:
#     case Tag() as tag:
#       attrs = ''
#       if tag.attrs:
#         attrs = ' ' + ' '.join(f'{key}="{value}"' for key, value in tag.attrs.items())
#       if tag.tag_name:
#         yield level, f'<{tag.tag_name}{attrs}>'
#       if tag.children:
#         for child in tag.children:
#           yield from html_lines(child, render, level + 1)
#       if tag.tag_name:
#         yield level, f'</{tag.tag_name}>'
#     case _:
#       yield level, rendered

# def html(data: ..., render=View, indent='  ', join='\n'):
#   lines = html_lines(data, render)
#   indented_lines = (indent * level + text for level, text in lines)
#   return join.join(indented_lines)

# for level, line in html_lines(h('div') [
#     header ['hello', 'world', ['a list', 'could change']],
#     h('p') ['''
#       An example of some text.
#     '''],
#   ]):
#   print(level, line)

# @dataclass
# class Renderer:
#   cache: dict[Hashable, Tag]

  # def to_tag(item: Hashable) -> Tag: ...


# a_list = [1, 2, 3]
# shell = Shell(h('div')[{
#   'hello': 'world',
#   'value': a_list
# }])

# print(h('div')[
#   h('h1')[('Heading', ('x', 32))],
#   h('p')['Hello there, this is a paragraph.'],
# ])

# print(shell)
# print(shell.open())
# for watching in shell._nodes.keys():
#   print(f'{watching, shell[watching]=}')
# del a_list[1]
# shell.open()
# for watching in shell._nodes.keys():
#   print(f'{watching, shell[watching]=}')

