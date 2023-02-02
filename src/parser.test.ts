import { describe, it, expect, test } from 'vitest';
import { add, Element } from './parser';
import fs from 'fs-extra';
import { XMLParser } from 'fast-xml-parser';
import path from 'path';

test('add', () => {
  expect(add(1, 2)).toBe(3);
});

describe.skip('Element from string', () => {
  it('should parse simple xml', () => {
    const source = `
      <foo>
        <bar></bar>
        <answer>42</answer>
      </foo>
    `;
    const parser = Element.fromString(source);
    expect(parser).toEqual<Element>({
      name: 'foo',
      children: [
        { name: 'bar', children: [] },
        { name: 'answer', children: ['42'] }
      ]
    });
  });
});

interface PubMedArticleBody{
  PubMedArticleSet:PubMedArticleSet;
}

interface PubMedArticleSet {
  PubmedArticle: PubMedArticle[];
}

interface PubMedArticle {
  MedlineCitation: MedlineCitation;
  PubmedData:PubmedData;
}

interface MedlineCitation {
  PubmedArticleSet: any;
  DateCreated:Date;
  DateCompleted:Date;
}

interface PubmedData {
  PubmedArticleSet: any;
  DateCreated:Date;
  DateCompleted:Date;
}

interface Date {
  Year: Number;
  Month: Number;
  Day: Number;
}

test('xml test', async () => {
  const filename = path.resolve(__dirname, './4020a1-datasets.xml')
  const source = await fs.readFile(filename, 'utf-8');
  const parser = new XMLParser();
  const tree: PubMedArticleBody = parser.parse(source);
  console.log(JSON.stringify(tree, null, 2));
  expect(tree).instanceOf(Object);
  debugger
});


