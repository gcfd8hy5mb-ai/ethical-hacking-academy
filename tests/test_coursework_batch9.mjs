// PR #4 coursework regression: links, HTML structure and simulated interaction.
// Run: node tests/test_coursework_batch9.mjs
import assert from 'node:assert/strict';
import {readFileSync, existsSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {Script,createContext} from 'node:vm';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>readFileSync(resolve(root,p),'utf8');
const pages=[
'advanced-authorized-redteam-field-guide.html',
'authorized-redteam-purpleteam-field-labs.html',
'cross-system-defensive-operations-labs.html',
'diagnostic-evidence-simulator.html',
'independent-local-investigation-workbench.html',
'independent-systems-incident-fieldbook.html',
'integrated-multistage-investigation-studio.html',
'real-system-readonly-lab-manual.html',
'repeatable-local-vm-practice.html',
'security-operations-purple-team-fieldbook.html'
];
const pathway=JSON.parse(read('learning-pathway.json'));
assert.equal(pathway.levels.length,8,'Eight academy levels must remain present');
let linked=0;
for(const level of pathway.levels){
  for(const lab of level.labs||[]){
    if(!Array.isArray(lab)||lab.length!==2)continue;
    if(!pages.includes(lab[1]))continue;
    assert.ok(lab[0].trim(),'New curriculum link must have a name');
    assert.ok(existsSync(resolve(root,lab[1])), 'Missing linked file: '+lab[1]);
    linked++;
  }
}
assert.ok(linked>=52,'Expected at least 52 new resource references');
const pageData=new Map();
for(const page of pages){
  const html=read(page);
  assert.match(html,/^<!doctype html>/i,page+' missing doctype');
  assert.match(html,/<title>[^<]+<\/title>/i,page+' title missing');
  const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
  assert.equal(ids.length,new Set(ids).size,page+' duplicate DOM ID');
  for(const anchor of html.matchAll(/href="#([^"]+)"/g)){
    assert.ok(ids.includes(anchor[1]),page+' unresolved #'+anchor[1]);
  }
  for(const link of html.matchAll(/href=["']\.\/([^"'#]+)(?:#[^"']*)?["']/g)){
    assert.ok(existsSync(resolve(root,link[1])),page+' missing local link '+link[1]);
  }
  const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(x=>x[1]);
  for(const js of scripts)new Script(js,{filename:page});
  pageData.set(page,{html,ids,scripts});
}
function node(){
  return {textContent:'',hidden:false,disabled:false,children:[],attributes:{},events:{},
    appendChild(n){this.children.push(n);return n;},
    setAttribute(k,v){this.attributes[k]=v;},
    addEventListener(k,callback){this.events[k]=callback;},
    querySelectorAll(q){assert.equal(q,'button');return this.children;},
    click(){assert.ok(!this.disabled,'Attempted click on disabled control');assert.ok(this.events.click);this.events.click();}};
}
const interactive=[
{page:'diagnostic-evidence-simulator.html',container:'case-tabs',panel:'answer',change:'case-title',expected:10,type:'selection'},
{page:'independent-local-investigation-workbench.html',container:'selector',panel:'teaching',change:'stageNumber',expected:4,type:'stage'},
{page:'integrated-multistage-investigation-studio.html',container:'cases',panel:'interpretation',change:'stageLabel',expected:7,type:'stage'}
];
for(const test of interactive){
  const {ids,scripts}=pageData.get(test.page);
  assert.equal(scripts.length,1,test.page+' script count');
  const elements=new Map(ids.map(id=>[id,node()]));
  const document={getElementById(id){assert.ok(elements.has(id),'Unknown DOM element '+id);return elements.get(id);},
    createElement(){return node();},
    querySelectorAll(selector){assert.equal(selector,'#case-tabs button');return elements.get('case-tabs').children;}};
  new Script(scripts[0],{filename:test.page}).runInContext(createContext({document}));
  const buttons=elements.get(test.container).children;
  assert.equal(buttons.length,test.expected,test.page+' scenario count');
  const reveal=elements.get('reveal'),panel=elements.get(test.panel);
  assert.equal(reveal.attributes['aria-expanded'],'false');
  assert.equal(panel.hidden,true);
  reveal.click();
  assert.equal(reveal.attributes['aria-expanded'],'true');
  assert.equal(panel.hidden,false);
  reveal.click();
  assert.equal(reveal.attributes['aria-expanded'],'false');
  assert.equal(panel.hidden,true);
  const before=elements.get(test.change).textContent;
  if(test.type==='stage')elements.get('next').click();
  else buttons[1].click();
  assert.notEqual(elements.get(test.change).textContent,before,test.page+' did not navigate');
}
const app=read('app.js');
assert.match(app,/learning-pathway\.json/,'Academy must still load pathway');
assert.match(app,/level\.labs\|\|\[\]/,'Academy must still render lab links');
console.log('Batch 9 PASS: '+pages.length+' pages, '+linked+' pathway references, 3 functional DOM interactions. Browser/device acceptance remains separate.');
