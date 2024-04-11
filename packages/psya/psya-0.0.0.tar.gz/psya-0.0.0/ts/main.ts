import ws from "./socket"

console.log("socket:", ws)

import {LitElement, html} from "lit"
import {asyncReplace} from 'lit/directives/async-replace.js'
import {customElement, state} from "lit/decorators.js"

import {field} from './py-view'
import { DirectiveResult } from "lit/async-directive.js"

@customElement('kt-shell')
class KtShell extends LitElement {
  @state() ticker: AsyncGenerator | null = produce()

  stop() {
    this.ticker?.return(null)
    this.ticker = null
  }

  override render() {
    return html`
      <div>
        <pre>${field("hello")}</pre>
        <h1 @click=${this.stop}>${this.ticker ? asyncReplace(this.ticker) : null}</h1>
      </div>`
  }
}

export default KtShell

async function* produce() {
  try {
    let n = 0
    while (true) {
      yield n++
      await new Promise(r => setTimeout(r, 100))
    }
  } catch(x) {
    console.error(x)
  } finally {
    console.log('returning')
  }
}

async function consume() {
  for await (const i of produce()) {
    if (i === 10) break
    console.log(i)
  }
}

window.cons = consume