import asyncio
import uvicorn
import sys

from .app import app

async def main():
  config = uvicorn.Config(app, port=0, log_level="info")
  server = uvicorn.Server(config)
  task = asyncio.create_task(server.serve())
  host, port = await get_sockname(server)
  print(f"http://{host}:{port}?ws=/__ws__")
  sys.stdout.flush()
  print("kernel: started")
  await task

async def get_sockname(server: uvicorn.Server) -> tuple[str, int]:
  while not server.started:
    await asyncio.sleep(0.1)
  for server in server.servers:
    for socket in server.sockets:
      host, port = socket.getsockname()
      return host, port

if __name__ == "__main__":
  asyncio.run(main())