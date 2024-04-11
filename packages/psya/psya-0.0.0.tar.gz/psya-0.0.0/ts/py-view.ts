import {AsyncDirective, directive, PartType, ChildPart, AttributePart, Part} from 'lit/async-directive.js'
import {html, noChange} from 'lit'

// py('mind').field('messages').map()

abstract class PyRef {
  parent: PyRef | undefined

  field(name: string) {
    return new NamedField(name, this)
  }

  get path() {
    const path = []
    let node: PyRef | undefined = this
    while (node) {
      path.unshift(node)
      node = node.parent
    }
    return path
  }
}

class Ptr extends PyRef {
  constructor(public readonly id: string) { super() }
}

class NamedField {
  constructor(public readonly name: string, public readonly parent: PyRef) {}

  toJSON() { return this.name }
}



class PyField extends AsyncDirective {
  override render(name: string): unknown {
    throw new Error('Method not implemented.')
  }

  static VALID_PART_TYPES = {
    // [PartType.ATTRIBUTE]: true,
    // [PartType.CHILD]: true,
    [PartType.PROPERTY]: true,
  }

  override update(part: Part, [name]: [string]) {
    if (!this.isConnected) return noChange
    if (part.type === PartType.CHILD) {
      let parents = ''
      let node: Node | null = part.parentNode
      while (node) {
        parents += ` - ${node} (${Object.keys(node)})\n`
        node = node.parentNode ?? (node as any).host
        if (node) (window as any).___pnode = node
      }
      return html`is child, name=${name}, parents: ${parents}`
    }
    return noChange
  }
}

export const field = directive(PyField)




// function guardPartType<P extends Part, T extends PartType>(part: P, validTypes: Record<T, any>): asserts part is P & {type: T} {
//   if (!(part.type in validTypes))
//     throw new Error(`Invalid location ${part.type}, must be ${Object.keys(validTypes).join(', ')}`)
// }


// import {LitElement, html} from 'lit'
// import {customElement, property} from 'lit/decorators'

// @customElement('py-view')
// class PyView extends LitElement {
//   @property({ type: String, attribute: true })
//   field: string | null = null

//   override connectedCallback(): void {
//     super.connectedCallback()    
//   }

//   override disconnectedCallback(): void {
//     super.disconnectedCallback()
//   }

//   get parentScopeElement(): PyView | null {
//     let node = this.parentElement
//     while (node) {
//       if (node instanceof PyView) return node
//     }
//     return null
//   }
// }

// export default PyView
