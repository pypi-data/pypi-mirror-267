from abc import abstractmethod
import asyncio as aio
from dataclasses import dataclass, field
from functools import cached_property, partial
from os import stat_result
from pathlib import Path
from typing import Any, AsyncIterator, Callable, Generic, Iterable, Tuple, TypeVar, cast
from weakref import WeakValueDictionary

from psya.the import the
from psya.brain import Brain, Emit, Portal
from psya.wire import Json, Merge

from psya.mut.dict import MutDict
from psya.mut.ref import Ref, Ptr
from psya.mut import Event, mutation
import psya.mut
from psya.mut.observer import Receiver, Subscription
 
from starlette.websockets import WebSocket
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

BRAIN = Brain()
the(Brain, BRAIN).__enter__()

@dataclass
class WebSocketPortal(Portal):
  ws: WebSocket = field(kw_only=True)
  wire: Json = Json()
  queue: aio.Queue = field(default_factory=aio.Queue)

  async def recv(self):
    wire = self.wire
    async for message in self.ws.iter_text():
      yield wire.decode(message)

  async def send(self, msg, **extra):
    wire = self.wire
    if extra:
      encoded = wire.encode(Merge(msg, extra))
    else:
      encoded = wire.encode(msg)
    self.queue.put_nowait(encoded)

  async def run_send(self):
    queue = self.queue
    ws = self.ws
    while True:
      ws.send_text(await queue.get())

# app = Starlette(debug=True, routes=[
#   WebSocketRoute('/__ws__', connect, name='websocket'),
#   Mount('/', StaticFiles(packages=["psya"], html=True)),
# ])

from starlette.types import Scope, Receive, Send
import sys

async def portal(scope: Scope, receive: Receive, send: Send) -> None:
  ws: WebSocket = WebSocket(scope, receive, send)
  await ws.accept()
  brain = the[Brain]
  brain.wake()

  if not brain.activity:
    brain.start()
  with WebSocketPortal(brain, ws=ws) as portal:
    await portal.run()

class Stack(StaticFiles):
  # def lookup_path(self, path: str) -> Tuple[str, stat_result | None]:
  #   special, _, rest = path.partition('/')
  #   match special:
  #     case "__module__":
  #       ...
  #   return super().lookup_path(path)
  def __init__(self, packages, *, html=True, **kws):
    super().__init__(packages=packages, html=html, **kws)

  async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
    try:
      print(f"----- BEGIN {scope['type']} {Path(scope['path']).parts} ------ ", file=sys.stderr)
      print(scope, receive, send, file=sys.stderr)    
      if scope['type'] == 'websocket':
        return await portal(scope, receive, send)
      return await super().__call__(scope, receive, send)
    finally:
      print(f"----- END {scope['type']} {scope['path']} ------ ", file=sys.stderr)

app = Stack(packages=['psya'])
print(app.all_directories, file=sys.stderr)
