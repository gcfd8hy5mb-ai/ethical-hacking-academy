import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const app=readFileSync(new URL('../app.js',import.meta.url),'utf8');
const source=app.slice(app.indexOf('const rangeGroups='),app.indexOf('function nav(){'));
let category='all',query='';
const groups=['guided','workstations','investigations','assessments'].map(name=>({
 dataset:{rangeGroup:name},hidden:false,cards:[],
 querySelectorAll(){return this.cards;}
}));
const status={},empty={};
const root={querySelector:()=>({dataset:{rangeFilter:category}}),querySelectorAll:()=>groups};
const document={addEventListener(){},getElementById(id){return id==='academy-range-search'?{value:query}:id==='academy-range-count'?status:empty;}};
const context=vm.createContext({root,document,safe:t=>String(t).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;')});
vm.runInContext(source,context);
const entries=vm.runInContext('rangeActivities',context);
assert.equal(entries.length,39);
assert.equal(new Set(entries.map(e=>e.target)).size,39,'Every original destination appears once');
for(const e of entries){
 groups.find(g=>g.dataset.rangeGroup===e.group).cards.push({dataset:{rangeTitle:e.title.toLowerCase()},hidden:false});
 if(e.kind==='href')assert.ok(readFileSync(new URL('../'+e.target.replace('./',''),import.meta.url)).length,'Local destination exists');
}
const filter=()=>vm.runInContext('filterCyberRange()',context);
filter();assert.equal(status.textContent,'39 of 39 activities shown');assert.equal(empty.hidden,true);
query='LINUX';query=query.toLowerCase();filter();
assert.equal(groups.flatMap(g=>g.cards).filter(c=>!c.hidden).length,1);
assert.equal(groups.find(g=>g.dataset.rangeGroup==='workstations').hidden,false);
category='assessments';filter();assert.equal(empty.hidden,false);
query='';filter();assert.equal(status.textContent,'14 of 39 activities shown');
category='all';filter();assert.ok(groups.every(g=>!g.hidden));
const html=vm.runInContext('cyberRangeHTML()',context);
assert.match(html,/id="terminal"/);
for(const command of ['pwd','ls','whoami','uname -a','help'])assert.ok(html.includes('data-cmd="'+command+'"'));
assert.match(app,/\['#practice-lab','#lab'\]\.includes\(location.hash\)/);
console.log('Cyber Range: all 39 destinations, search/category combinations, empty state, reset, return aliases and command controls passed.');
