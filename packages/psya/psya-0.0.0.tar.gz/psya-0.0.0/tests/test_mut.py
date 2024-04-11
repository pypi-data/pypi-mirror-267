from psya.mut import mutation, mut, Ref, Done, Change
from psya.mut.observer import watch
import pytest

import asyncio as aio

@pytest.mark.asyncio
async def test_basic_mutation():
  x = []
  async def append_to(l):
    with mutation("add list items"):
      mut(l.append, 'hello')
      await aio.sleep(0.2)
      # print(get_mut(l))
      mut(l.append, 'world')
  events = []
  watcher = aio.create_task(observe(x, events))
  changer = aio.create_task(append_to(x))
  await changer
  assert x == ['hello', 'world']
  await watcher
  match events:
    case [
      [Change(Ref(x0), list.append, (x1, 'hello',), _)],
      # sleep should cause the mutations to arrive
      # in two batches
      [
        Change(Ref(x2), list.append, (x3, 'world',), _),
        Done(Ref(x4))
      ]
    ]: assert x0 == x1 == x2 == x3 == x4
    case _:
      assert events is not events

async def observe(target: ..., events_out: list):
  # print("observing", target)
  # print("\n\n\n")
  async for events in watch(target):
    events_out.append(events)
    # print(f"observe awoke with {events=}")
    # for event in events:
    #   print(event)

