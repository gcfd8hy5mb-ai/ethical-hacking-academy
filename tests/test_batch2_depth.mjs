// Regression guard for the November 2026 Batch 2 coursework expansion.
// Never treat these written self-checks as machine-graded examinations.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=path=>readFileSync(resolve(root,path),'utf8');
const sources=['core-lesson-guided-practice-2026.json','core-guided-practice-batch2-2026.json','core-guided-practice-batch3-2026.json'];
const units=sources.flatMap(path=>JSON.parse(read(path)).units);
assert.equal(units.length,198,'All 198 core practice units must remain available');
assert.equal(new Set(units.map(u=>u.id)).size,198,'Original practice identifiers must remain unique');
assert.equal(new Set(units.map(u=>u.course)).size,26,'All 26 authored core courses must have guided practice');
for(const unit of units){
 assert.ok(unit.course && unit.lesson && unit.scenario,'Each extension needs a specific lesson and scenario');
 assert.ok(unit.sections.length>=2,'Each unit needs foundational and verification exercises: '+unit.id);
 assert.equal(unit.sections[0].id,'s1','Preserve original section identifier: '+unit.id);
 const keys=new Set();
 for(const section of unit.sections){
  assert.ok(!keys.has(section.id),'Duplicate practice section ID: '+unit.id);
  keys.add(section.id);
  for(const field of ['heading','command','instruction','interpretation','task','safety'])
   assert.ok(typeof section[field]==='string'&&section[field].trim().length>15,unit.id+' missing '+field);
 }
 const verify=unit.sections.find(s=>s.id==='s2');
 assert.match(verify.task,/Self-check question:/,'Self-check question missing '+unit.id);
 assert.match(verify.task,/Model-answer criterion:/,'Model-answer criterion missing '+unit.id);
}
const js=read('app.js');
const start=js.indexOf('const embeddedPracticeCatalogs=new Map();');
const end=js.indexOf('function nav(){',start);
assert.ok(start>=0 && end>start);
const ctx={safe:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;')};
vm.createContext(ctx);vm.runInContext(js.slice(start,end),ctx,{filename:'embedded-practice.js'});
for(const unit of [units[0],units[50],units[128]]){
 const html=ctx.embeddedPracticeSectionHTML(unit.sections[0],unit,unit.lesson);
 assert.ok(html.includes(unit.sections[1].heading),'Follow-up section must render: '+unit.id);
 assert.ok(html.includes('Independent assessment question and evidence'));
}
assert.ok(!js.includes("localStorage.setItem('ethical-hacking-academy-progress-v1'") || js.includes("const progressKey='ethical-hacking-academy-progress-v1'"),'Legacy student progress key must remain');
console.log('Batch 2 verified: 198 units, 26 courses, section rendering, self-check questions, stable identifiers.');
