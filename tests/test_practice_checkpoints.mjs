// Run thirty practical checkpoint checks without browser, network access, or student storage.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=name=>readFileSync(resolve(root,name),'utf8');
const data=JSON.parse(read('practice-checkpoints-v1.json'));
const core=JSON.parse(read('core-lesson-guided-practice-2026.json'));
const known=new Set(core.units.map(u=>u.id));
assert.equal(data.entries.length,30,'First interactive batch contains 30 reviewed questions');
const keys=new Set();
for(const item of data.entries){
 assert.ok(known.has(item.unitId),'Checkpoint must target an authored practice unit');
 assert.ok(!keys.has(item.unitId),'No repeated checkpoint IDs');
 keys.add(item.unitId);
 assert.ok(typeof item.question==='string'&&item.question.length>=30);
 assert.ok(Array.isArray(item.options)&&item.options.length===3);
 assert.ok(item.options.every(x=>typeof x==='string'&&x.length>=3));
 assert.ok(Number.isInteger(item.answer)&&item.answer>=0&&item.answer<item.options.length);
 assert.ok(typeof item.explanation==='string'&&item.explanation.length>=60);
}
const js=read('app.js');
const start=js.indexOf('const embeddedPracticeCatalogs=new Map();');
const end=js.indexOf('function nav(){',start);
assert.ok(start>0&&end>start);
const markupElements=new Map();
function element(id){
 if(!markupElements.has(id))markupElements.set(id,{
  dataset:{unit:data.entries[0].unitId},textContent:'',innerHTML:'',
  buttons:[],
  querySelectorAll(){return this.buttons}
 });
 return markupElements.get(id);
}
let requests=0;
const ctx={
 screen:'lesson',courseIndex:0,lessonIndex:0,
 catalog:{courses:[]},safe:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;'),
 document:{getElementById:element},
 fetch:async url=>{
  assert.equal(url,'./practice-checkpoints-v1.json');
  requests++;
  return {ok:true,json:async()=>data};
 }
};
vm.createContext(ctx);
vm.runInContext(js.slice(start,end),ctx,{filename:'academy-practice-checkpoint.js'});
const first=data.entries[0];
assert.equal(ctx.checkpointUnitsAvailable(first.unitId),true);
assert.equal(ctx.checkpointUnitsAvailable('unsupported-practice-id'),false);
const unit=core.units.find(u=>u.id===first.unitId);
const practiceMarkup=ctx.embeddedPracticeSectionHTML(unit.sections[0],unit,unit.lesson);
assert.match(practiceMarkup,/data-practice-start=/);
assert.match(practiceMarkup,/academy-checkpoint-launch/);
const other=core.units.find(u=>u.id==='core-practice-2026-1-1');
assert.ok(!ctx.embeddedPracticeSectionHTML(other.sections[0],other,other.lesson).includes('data-practice-start='));
await ctx.loadPracticeCheckpoint(first.unitId,0,0);
const target=element('academy-practice-checkpoint');
assert.match(target.innerHTML,/INTERACTIVE PRACTICE CHECK/);
assert.match(target.innerHTML,/aria-live="polite"/);
assert.ok(target.innerHTML.includes(first.question));
assert.equal(requests,1);
const answerButtons=first.options.map((_,i)=>({
 dataset:{practiceChoice:String(i)},attrs:{},classes:new Set(),
 setAttribute(k,v){this.attrs[k]=v;},
 classList:{toggle(k,v){this.owner.classes[v?'add':'delete'](k);}}
}));
for(const b of answerButtons)b.classList.owner=b;
target.buttons=answerButtons;
const wrong=(first.answer+1)%3;
await ctx.gradePracticeChoice(wrong);
assert.match(element('academy-checkpoint-feedback').textContent,/Not quite/);
assert.equal(answerButtons[wrong].attrs['aria-pressed'],'true');
await ctx.gradePracticeChoice(first.answer);
assert.match(element('academy-checkpoint-feedback').textContent,/Correct/);
assert.equal(answerButtons[first.answer].attrs['aria-pressed'],'true');
assert.equal(answerButtons[wrong].attrs['aria-pressed'],'false');
await ctx.loadPracticeCheckpoint(first.unitId,0,0);
assert.equal(requests,1,'Catalog should load only once');
target.innerHTML='New lesson visible';ctx.lessonIndex=1;
await ctx.loadPracticeCheckpoint(first.unitId,0,0);
assert.equal(target.innerHTML,'New lesson visible','Stale navigation must never modify a different lesson');
assert.ok(!js.slice(start,end).includes('localStorage'),'Checkpoint feedback must never change student progress');
assert.ok(!js.slice(start,end).includes('eval('),'No arbitrary command/code evaluation in interactive checks');
console.log('Practice checkpoint tests passed: 30 mappings, schema, feedback, caching, escaping, no scoring mutations, stale navigation.');
