// Workstation-specific regression tests — no server, browser or external requests.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const js=readFileSync(resolve(root,'app.js'),'utf8');
const start=js.indexOf("const workstationReportKey=");
const finish=js.indexOf("function go(dest){",start);
assert.ok(start>0&&finish>start,'Expected workstation helper definitions');
const values=new Map();
const elements=new Map();
const el=id=>{
 if(!elements.has(id))elements.set(id,{
  id,hidden:false,attrs:{},textContent:'',
  setAttribute(name,value){this.attrs[name]=value;}
 });
 return elements.get(id);
};
const state={
 screen:'lesson',courseIndex:0,lessonIndex:2,
 id:(c,l)=>c+'-'+l,
 safe:x=>String(x).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;'),
 document:{getElementById:el},
 localStorage:{getItem:k=>values.get(k)||null,setItem:(k,v)=>values.set(k,v)}
};
vm.createContext(state);
vm.runInContext(js.slice(start,finish),state,{filename:'workstation-helper.js'});
const key='ethical-hacking-workstation-reports-v1';
assert.equal(state.readWorkstationDraft(),'');
const draft='OBSERVED: <test> & checked; UNKNOWN: missing proof';
values.set(key,JSON.stringify({'0-2':draft}));
assert.equal(state.readWorkstationDraft(),draft);
const html=state.workstationPanelHTML();
assert.match(html,/Knowledge Check/);
assert.match(html,/Lab Report/);
assert.match(html,/not cloud-synced/i);
assert.match(html,/&lt;test&gt; &amp; checked/);
assert.ok(!html.includes('<test>'),'Draft must be escaped before insertion');
state.setWorkstationPanel('report');
assert.equal(el('academy-check-tab').attrs['aria-selected'],'false');
assert.equal(el('academy-report-tab').attrs['aria-selected'],'true');
assert.equal(el('academy-knowledge-check').hidden,true);
assert.equal(el('academy-lab-report').hidden,false);
state.setWorkstationPanel('check');
assert.equal(el('academy-knowledge-check').hidden,false);
assert.equal(el('academy-lab-report').hidden,true);
state.setWorkstationPanel('invalid');
assert.equal(el('academy-lab-report').hidden,true,'Unsupported tab should be ignored');
state.lessonIndex=3;
assert.equal(state.readWorkstationDraft(),'','Reports are scoped per lesson');
assert.match(js,/class="academy-workstation-split"/,'Lesson markup contains split workstation');
assert.match(js,/id="academy-embedded-practice"/,'Existing title matched practice area preserved');
assert.match(js,/id="complete"/,'Original completion control preserved');
assert.match(js,/id="grade"/,'Original grading control preserved');
assert.match(js,/localStorage\.setItem\(progressKey,JSON\.stringify\(progress\)\)/,'Existing progress persistence intact');
const desktop=readFileSync(resolve(root,'desktop.css'),'utf8');
const mobile=readFileSync(resolve(root,'style.css'),'utf8');
assert.match(desktop, /min-width:1180px/);
assert.match(desktop, /academy-workstation-split/);
assert.match(mobile, /academy-workstation-assessment/);
console.log('Learning workstation regression checks passed: tabs, hidden panels, local draft, escaping, course-scoped storage, split layout, original grading.');
