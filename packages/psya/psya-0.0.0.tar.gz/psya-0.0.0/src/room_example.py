from psya.room import Room, Sub, Joined, Msg

async def echo(sub: Sub):
  yield f"hi, it's {sub.name}"
  async for messages in sub:
    for m in messages:
       match m:
          case Joined(): print(m)
          case Msg(sender, body):
             if sender != sub.name:
                yield body
  yield f"{sub.name}, signing off"

from aioconsole import ainput

async def shell_prompt(sub):
  async for messages in sub:
    for message in messages:
       print('msg:', message)
    print(sub.room.agents)
    yield await ainput('~> ')

async def amain():
  room = Room()
  e = room.join(echo)
  await asyncio.gather(e.done, room.join(shell_prompt).done)

import asyncio

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(amain())
finally:
    loop.close()



