export type Node = Element | string;

export class Element {
  name: string;
  children: Node[] = [];

  constructor(element: Element) {
    this.name = element.name;
    this.children = element.children;
  }

  static fromString(source: string) {
    const element = new Element({ 
      name: '',
      children: []
    });

    // TODO
    

    return element;
  }
}

export const add = (a: number, b: number) => a + b;
