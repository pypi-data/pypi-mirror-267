const args = new URLSearchParams(location.search)
const socketPath = args.get('ws')!
const ws = getSocket(socketPath)

export default ws

ws.onopen = onOpen
ws.onmessage = onMessage

let nextMessageId = 0
const listeners = new Map()

function pyEval(expr: string, kind: 'Eval' | 'Mutate' = 'Eval'): Promise<any> {
  const id = `eval_${nextMessageId++}`
  ws.send(JSON.stringify({$t: kind, id, expr}))
  let resolve: (value: unknown) => void
  let reject: (reason?: any) => void
  const promise = new Promise((res, rej) => {
    resolve = res; reject = rej
  })
  listeners.set(id, msg => {
    switch (msg.$t) {
      case 'SetData':
        resolve(msg.data)
        break
      case 'SetError':
        reject(msg.error)
        break
    }
    listeners.delete(id)
  })
  return promise
}

function pyWatch(path: string[], onData, onError = (_) => {}) {
  const id = `watch_${nextMessageId++}`
  ws.send(JSON.stringify({$t: 'Watch', id, path}))
  listeners.set(id, msg => {
    switch (msg.$t) {
      case 'SetData':
        onData(msg.data)
        break
      case 'SetError':
        onError(msg.error)
        break
    }
  })
  return () => listeners.delete(id)
}

;(window as any).python = {
  watch: pyWatch,
  eval: pyEval
}

function onOpen(this: WebSocket) {
  console.log("socket open :: ", this)
  // this.send(JSON.stringify({$t: 'Watch', id: "watch_0", path: ["hello", "world"]}))
}

function onMessage(this: WebSocket, ev: MessageEvent<any>) {
  const msg = JSON.parse(ev.data)
  switch(msg.$t) {
    case 'Trace':
      console.log(
        '%ctrace', 'color:lightblue;',
        ...msg.message,
        msg.metadata
      )
      break
    default:
      console.log(msg)    
  }
}

function getSocket(path: string) {
  // Get the current protocol and hostname of the page
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const hostname = window.location.hostname
  const port = window.location.port ? ':' + window.location.port : ''

  // Construct the WebSocket URL
  const url = `${protocol}//${hostname}${port}${path}`

  // Create a new WebSocket object
  return new WebSocket(url)
}

