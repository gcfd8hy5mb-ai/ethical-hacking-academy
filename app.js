






const root=document.querySelector('#app');
window.__academyStage?.('Main Academy script started');
let workedKeys=[],catalog,examCatalog=null,courseIndex=0,lessonIndex=0,screen='home',selected=-1,graded=false,learningPath=null,levelIndex=0;
const progressKey='ethical-hacking-academy-progress-v1';
function readProgress(){try{return JSON.parse(localStorage.getItem(progressKey)||'{}')}catch{return {}}}
let progress=readProgress();
const safe=t=>String(t).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const id=(c,l)=>c+'-'+l;
const isDone=(c,l)=>Boolean(progress[id(c,l)]);
const count=()=>catalog.courses.reduce((n,c,i)=>n+c.lessons.filter((_,j)=>isDone(i,j)).length,0);
const total=()=>catalog.courses.reduce((n,c)=>n+c.lessons.length,0);
function portfolioStatus(){try{const drafts=JSON.parse(localStorage.getItem('ethical-hacking-written-assignments-v1')||'{}');const reviews=JSON.parse(localStorage.getItem('ethical-hacking-assignment-reviews-v1')||'{}');return {drafts:Object.values(drafts).filter(v=>typeof v==='string'&&v.trim().length>0).length,reviewed:Object.values(reviews).filter(v=>v===true).length}}catch{return {drafts:0,reviewed:0}}}
function examEvidence(courseTitle){let scores={};try{scores=JSON.parse(localStorage.getItem('ethical-hacking-exam-results-v1')||'{}')}catch{}const exams=examCatalog?.exams||[];const related=exams.map((exam,index)=>({exam,index})).filter(item=>item.exam.courses.includes(courseTitle));return related.map(({exam,index})=>({title:exam.title,score:Number(scores[index]||0),passed:Number(scores[index]||0)>=(examCatalog?.passingPercent||80)}));}
function assessmentEvidence(){const get=(key)=>{try{return JSON.parse(localStorage.getItem(key)||'{}')}catch{return {}}};const exams=get('ethical-hacking-exam-results-v1'),investigations=get('ethical-hacking-investigation-results-v1'),simulations=get('ethical-hacking-multistage-simulations-v1');return {examPasses:Object.values(exams).filter(v=>Number(v)>=80).length,investigationPasses:Object.values(investigations).filter(v=>Number(v)>=80).length,simulationPerfect:Object.values(simulations).filter(v=>v&&Number(v.best)>=4).length};}
function technicalStudioEvidence(){let scores={};try{scores=JSON.parse(localStorage.getItem('ethical-hacking-technical-assessments-v1')||'{}')}catch{}const max=[10,10,10,12,12,12,12];return {attempted:Object.keys(scores).filter(k=>Number.isInteger(Number(k))&&Number(k)>=0&&Number(k)<7).length,passed:max.filter((m,i)=>Number(scores[i]||0)>=m*.8).length,total:max.length};}
const STUDIO_COURSES={'Enterprise Identity and Access Management':[0],'Cloud Infrastructure Security':[1,6],'Linux System Administration Lab Theory':[2],'Windows Administration and Security':[3],'Web Application Security Fundamentals':[4],'Security Operations and Incident Response':[5]};
function practicalEvidence(courseTitle){const indices=STUDIO_COURSES[courseTitle]||[];let scores={};try{scores=JSON.parse(localStorage.getItem('ethical-hacking-technical-assessments-v1')||'{}')}catch{}const maximum=[10,10,10,12,12,12,12];const passed=indices.filter(i=>Number(scores[i]||0)>=maximum[i]*.8);return {assigned:indices.length,passed:passed.length,ready:indices.length>0&&passed.length===indices.length,indices};}
function advancedQualificationEvidence(){let x={};try{x=JSON.parse(localStorage.getItem('ethical-hacking-qualification-exam-part2-v1')||'{}')}catch{}return {best:Math.min(30,Math.max(0,Number(x.best)||0)),passed:x.passed===true};}
function commandLabEvidence(){let x={};try{x=JSON.parse(localStorage.getItem('ethical-hacking-command-investigations-v1')||'{}')}catch{}const scores=[0,1,2].map(i=>Math.min(10,Math.max(0,Number(x[i])||0)));return {attempted:scores.filter(n=>n>0).length,passed:scores.filter(n=>n>=8).length};}
function randomizedEvidence(){let x={};try{x=JSON.parse(localStorage.getItem('ethical-hacking-randomized-enterprise-v1')||'{}')}catch{}return {attempted:Object.keys(x).length,mastered:Object.values(x).filter(v=>Number(v)===10).length};}
function multiFaultEvidence(){let scores={};try{scores=JSON.parse(localStorage.getItem('ethical-hacking-multifault-network-v1')||'{}')}catch{}return {attempted:Object.keys(scores).filter(k=>/^[0-3]$/.test(k)).length,mastered:Object.entries(scores).filter(([k,v])=>/^[0-3]$/.test(k)&&Number(v)>=10).length};}
function blindLabEvidence(){let x={};try{x=JSON.parse(localStorage.getItem('ethical-hacking-blind-network-lab-v1')||'{}')}catch{}return {attempted:Object.keys(x).length,mastered:Object.values(x).filter(v=>Number(v)===10).length};}
function networkLabEvidence(){let n=0;try{n=Number(localStorage.getItem('ethical-hacking-virtual-network-v1')||0)}catch{}return Math.min(10,Math.max(0,n));}
function windowsLabEvidence(){let best=0;try{best=Number(localStorage.getItem('ethical-hacking-virtual-windows-v1')||0)}catch{}return Math.min(10,Math.max(0,best));}
function virtualLabEvidence(){let best=0;try{best=Number(localStorage.getItem('ethical-hacking-virtual-workstation-v1')||0)}catch{}return Math.min(10,Math.max(0,best));}
function qualificationEvidence(){let x={};try{x=JSON.parse(localStorage.getItem('ethical-hacking-qualification-exam-v1')||'{}')}catch{}return {best:Math.min(40,Math.max(0,Number(x.best)||0)),pass:x.pass===true};}
function courseMastery(c,i){const complete=c.lessons.filter((_,j)=>isDone(i,j)).length;const exams=examEvidence(c.title);const allLessons=complete===c.lessons.length;const examsPassed=exams.length>0&&exams.every(e=>e.passed);return {complete,total:c.lessons.length,exams,allLessons,examsPassed,knowledgeReady:allLessons&&examsPassed,practical:practicalEvidence(c.title)};}
function courseMasteryPanel(c,i){const m=courseMastery(c,i);return '<section class="sheet"><h2>Course mastery requirements</h2><p>'+m.complete+' / '+m.total+' lessons completed '+(m.allLessons?'✓':'· continue coursework')+'</p>'+(m.exams.length?m.exams.map(e=>'<p>'+safe(e.title)+': '+(e.passed?'✓ '+e.score+'% passed':e.score?e.score+'% · 80% required':'Not attempted · 80% required')+'</p>').join(''):'<p>No dedicated exam currently assigned to this course.</p>')+'<p><strong>Knowledge checkpoint:</strong> '+(m.knowledgeReady?'Requirements met in locally saved lesson and exam records':m.exams.length?'Not yet met':'Pending a dedicated course examination')+'</p><p><strong>Simulated practical checkpoint:</strong> '+(m.practical.assigned?m.practical.passed+' / '+m.practical.assigned+' linked Technical Assessment Studio cases passed at 80% or higher'+(m.practical.ready?' ✓':' · pending'):'No linked studio case yet — not assessed')+'</p><p><strong>Combined simulation readiness:</strong> '+(m.knowledgeReady&&m.practical.ready?'Knowledge and linked simulation criteria met':'Pending knowledge or practical simulation requirements')+'</p><p class="muted">This is a separate evidence-based simulation checkpoint, not a graduation gate, real-system proficiency certificate or instructor-grade assessment. Written reasoning and physical skills are not independently verified.</p><p><a class="button" href="./technical-assessment-studio.html">Open technical assessments</a></p><div class="mastery-actions"><button class="button" data-screen="exams">Open examinations</button><button class="button" data-screen="assignments">Portfolio assignments</button></div></section>';}
function lessonReadingHTML(reading){return String(reading).split(/\n\s*\n/).filter(Boolean).map(block=>'<div class="lesson-section">'+block.split('\n').filter(Boolean).map(line=>{const m=line.match(/^([A-Z][A-Z0-9 ,\/()—–-]{3,85}):\s*(.*)$/);return m?'<p><strong>'+safe(m[1])+':</strong> '+safe(m[2])+'</p>':'<p>'+safe(line)+'</p>'}).join('')+'</div>').join('')}
// Supplemental practical instruction is lazy-loaded inside the existing lesson view.
// It never adds, removes, reorders or marks an original lesson complete.
const embeddedPracticeCatalogs=new Map();
let embeddedPracticeMapPromise=null;
const embeddedPracticeKey=t=>String(t||'').trim().toLowerCase().replace(/\\s+/g,' ');
// Thirty reviewed, read-only concept checkpoints. These never alter exam or progress records.
let practiceCheckpointCatalogPromise=null;
function checkpointUnitsAvailable(unitId){return /^core-practice-2026-(2|4|5|6)-[1-9][0-9]*$/.test(String(unitId));}
async function loadPracticeCheckpoint(unitId,expectedCourse,expectedLesson){
 const target=document.getElementById('academy-practice-checkpoint');
 if(!target||!checkpointUnitsAvailable(unitId))return;
 target.textContent='Loading the practice question…';
 try{
  if(!practiceCheckpointCatalogPromise){
   practiceCheckpointCatalogPromise=fetch('./practice-checkpoints-v1.json').then(r=>{
    if(!r.ok)throw Error('Checkpoint HTTP '+r.status);
    return r.json();
   }).catch(e=>{practiceCheckpointCatalogPromise=null;throw e;});
  }
  const data=await practiceCheckpointCatalogPromise;
  if(screen!=='lesson'||courseIndex!==expectedCourse||lessonIndex!==expectedLesson)return;
  const current=document.getElementById('academy-practice-checkpoint');
  if(!current||current.dataset.unit!==unitId)return;
  const entry=(data.entries||[]).find(x=>x.unitId===unitId);
  if(!entry||!Array.isArray(entry.options)||entry.options.length<2||!Number.isInteger(entry.answer)
     ||entry.answer<0||entry.answer>=entry.options.length){current.textContent='Checkpoint unavailable. Continue the written exercise.';return;}
  current.innerHTML='<div class="academy-checkpoint-heading">INTERACTIVE PRACTICE CHECK</div><p>'+safe(entry.question)+'</p><div class="academy-checkpoint-options">'
   +entry.options.map((o,i)=>'<button type="button" class="academy-checkpoint-answer" data-practice-choice="'+i+'">'+safe(o)+'</button>').join('')
   +'</div><div id="academy-checkpoint-feedback" class="academy-checkpoint-feedback" role="status" aria-live="polite">Select an answer to see the explanation.</div>'
   +'<p class="academy-checkpoint-scope">Training feedback only. This does not grade a lab, mark a lesson complete, or change your examination score.</p>';
 }catch(error){
  const current=document.getElementById('academy-practice-checkpoint');
  if(current&&current.dataset.unit===unitId&&screen==='lesson'&&courseIndex===expectedCourse&&lessonIndex===expectedLesson){
   current.textContent='Interactive question unavailable. Continue the written practice assignment.';
  }
 }
}
async function gradePracticeChoice(choice){
 const container=document.getElementById('academy-practice-checkpoint');
 if(!container)return;
 const unitId=container.dataset.unit;
 if(!checkpointUnitsAvailable(unitId)||!practiceCheckpointCatalogPromise)return;
 const data=await practiceCheckpointCatalogPromise.catch(()=>null);
 if(!data||screen!=='lesson'||document.getElementById('academy-practice-checkpoint')!==container)return;
 const entry=(data.entries||[]).find(x=>x.unitId===unitId);
 if(!entry||!Number.isInteger(choice)||choice<0||choice>=entry.options.length)return;
 container.querySelectorAll('[data-practice-choice]').forEach(b=>{
  const selected=Number(b.dataset.practiceChoice)===choice;
  b.setAttribute('aria-pressed',String(selected));
  b.classList.toggle('academy-choice-correct',Number(b.dataset.practiceChoice)===entry.answer);
  b.classList.toggle('academy-choice-incorrect',selected&&choice!==entry.answer);
 });
 const feedback=document.getElementById('academy-checkpoint-feedback');
 if(feedback)feedback.textContent=(choice===entry.answer?'Correct. ':'Not quite. ')+entry.explanation;
}
function embeddedPracticeSectionHTML(section,unit,lessonTitle){
 const block=(label,value,kind='note')=>'<div class="academy-practice-block academy-practice-'+kind+'"><h4>'+safe(label)+'</h4><p>'+safe(value)+'</p></div>';
 return '<section class="sheet body academy-practical-steps" aria-label="Practical lesson extension">'
 +'<div class="kicker">CURATED PRACTICAL EXTENSION</div>'
 +'<h2>'+safe(unit.title)+'</h2>'
 +'<p class="academy-practice-context">Mapped to '+safe(lessonTitle)+'. Complete this exercise using synthetic evidence or your own authorized training environment.</p>'
 +block('01 / Training scenario',unit.scenario,'scenario')
 +'<h3>'+safe(section.heading)+'</h3>'
 +block('02 / What you will do and why',section.instruction,'instruction')
 +'<div class="academy-practice-command"><div class="academy-practice-command-label"><span>03 / COMMAND OR METHOD</span><span class="academy-method-tag">REFERENCE</span></div><pre>'+safe(section.command)+'</pre></div>'
 +block('04 / How to interpret results',section.interpretation,'interpretation')
 +block('05 / Your assignment and evidence',section.task,'assignment')
 +(checkpointUnitsAvailable(unit.id)?'<div class="academy-checkpoint-launch"><button type="button" class="academy-checkpoint-start" data-practice-start="'+safe(unit.id)+'">Try an interactive knowledge check</button><div id="academy-practice-checkpoint" data-unit="'+safe(unit.id)+'" aria-live="polite"></div></div>':'')
 +'<details class="academy-practice-scope"><summary>Safety and authorized scope</summary><p>'+safe(section.safety)+'</p></details>'
 +'<a class="academy-practice-more" href="./coursework-practical-expansion.html">Explore the complete practical collection →</a>'
 +'</section>';
}
async function loadEmbeddedPracticeForLesson(expectedCourse,expectedLesson){
 const node=document.getElementById('academy-embedded-practice');
 if(!node)return;
 const course=catalog?.courses?.[expectedCourse],lesson=course?.lessons?.[expectedLesson];
 if(!lesson)return;
 const courseTitle=course.title,lessonTitle=lesson[0];
 try{
  if(!embeddedPracticeMapPromise)embeddedPracticeMapPromise=fetch('./lesson-practical-title-map-2026.json').then(r=>{if(!r.ok)throw Error('Mapping HTTP '+r.status);return r.json()}).catch(e=>{embeddedPracticeMapPromise=null;throw e});
  const map=await embeddedPracticeMapPromise;
  if(screen!=='lesson'||courseIndex!==expectedCourse||lessonIndex!==expectedLesson)return;
  const match=(map.mappings||[]).find(m=>embeddedPracticeKey(m.course)===embeddedPracticeKey(courseTitle)&&embeddedPracticeKey(m.lesson)===embeddedPracticeKey(lessonTitle));
  const current=document.getElementById('academy-embedded-practice');
  if(!current)return;
  if(!match){
   current.innerHTML='<section class="sheet body"><h2>Related practice library</h2><p class="muted">A lesson-specific practical exercise has not been reviewed for this exact lesson yet. Open the Academy practice library instead of showing an unrelated exercise.</p><p><a class="button" href="./coursework-practical-expansion.html">Browse practical coursework →</a></p></section>';
   return;
  }
  const allowedPracticeSources=new Set([
   'coursework-practical-expansion-2026.json',
   'coursework-specific-practice-2026.json',
   'core-lesson-guided-practice-2026.json',
   'core-guided-practice-batch2-2026.json',
   'core-guided-practice-batch3-2026.json'
  ]);
  const source=match.source||'coursework-practical-expansion-2026.json';
  if(!allowedPracticeSources.has(source))throw Error('Unrecognized practice source');
  if(!embeddedPracticeCatalogs.has(source)){
   const pending=fetch('./'+source).then(r=>{if(!r.ok)throw Error('Practice HTTP '+r.status);return r.json()}).catch(e=>{embeddedPracticeCatalogs.delete(source);throw e});
   embeddedPracticeCatalogs.set(source,pending);
  }
  const data=await embeddedPracticeCatalogs.get(source);
  if(screen!=='lesson'||courseIndex!==expectedCourse||lessonIndex!==expectedLesson)return;
  const latest=document.getElementById('academy-embedded-practice');
  if(!latest)return;
  const unit=(data.units||[]).find(u=>u.id===match.unitId),section=unit?.sections?.find(x=>x.id===match.sectionId);
  if(!section){latest.textContent='Assigned practice is unavailable. Continue the core lesson or open the practice library.';return;}
  latest.innerHTML=embeddedPracticeSectionHTML(section,unit,lessonTitle);
 }catch(error){
  const current=document.getElementById('academy-embedded-practice');
  if(current&&screen==='lesson'&&courseIndex===expectedCourse&&lessonIndex===expectedLesson){
   current.innerHTML='<p class="muted">Supplemental practice is temporarily unavailable. Your core lesson remains usable. <a href="./coursework-practical-expansion.html">Open the practice collection</a>.</p>';
  }
 }
}
function nav(){
 const items=[['home','⌂','dashboard()'],['courses','▱','courses()'],['lab','>_','cyber_range()'],['progress','▥','progress()'],['exams','◇','assessments()'],['settings','⚙','settings()']];
 return '<nav class="bottom academy-v2-nav" aria-label="Academy navigation"><div class="academy-v2-logo"><span class="academy-v2-logo-shield">⬡</span><strong>ETHICAL<br>HACKING<br>ACADEMY</strong><small>LEARN // PRACTICE // MASTER</small></div>'
 +items.map(x=>'<button type="button" data-screen="'+x[0]+'" class="'+(screen===x[0]?'active':'')+'"><span class="academy-v2-nav-icon">'+x[1]+'</span><span class="academy-v2-nav-label">&gt;_ '+x[2]+'</span></button>').join('')
 +'<div class="academy-v2-sidebar-mission"><span>/* MISSION */</span><p>build_skills();<br>defend_systems();<br>practice_ethically();</p></div></nav>';
}
function desktopContext(){
 if(screen!=='course'&&screen!=='lesson')return '';
 const course=catalog?.courses?.[courseIndex];
 if(!course)return '';
 const completed=course.lessons.filter((_,i)=>isDone(courseIndex,i)).length;
 const ratio=course.lessons.length?Math.round(completed*100/course.lessons.length):0;
 const info='<div class="desktop-context-label">YOUR STUDY SPACE</div><h2>'+safe(course.title)+'</h2><p>'+completed+' of '+course.lessons.length+' lessons complete</p><div class="desktop-context-track" role="progressbar" aria-label="Course lesson progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+ratio+'"><span style="width:'+ratio+'%"></span></div>';
 const links=screen==='lesson'
  ?'<div class="desktop-context-label desktop-section-label">IN THIS LESSON</div><a href="#academy-reading">Core reading</a><a href="#academy-embedded-practice">Practical exercise</a><a href="#academy-knowledge-check">Knowledge check</a>'
  :'<div class="desktop-context-label desktop-section-label">COURSE NAVIGATION</div><button data-screen="level">Level overview</button><button data-screen="courses">All learning levels</button>';
 return '<aside class="desktop-context" aria-label="Course study overview">'+info+links+'<div class="desktop-context-foot">Progress reflects existing lesson completion. Practical work is assessed separately.</div></aside>';
}
function shell(content){const labChild=new Set(['labs','investigations','simulations','diagnostics','terminal-challenges']).has(screen);const back=labChild?'<button class="back academy-practice-back" data-screen="lab" aria-label="Back to Practice Lab">← Back to Practice Lab</button>':'';root.innerHTML='<div class="wrap academy-v2-screen-'+safe(screen)+'"><header class="top"><div class="brand"><span class="seal">&gt;_</span> WORLD-CLASS CYBERSECURITY TRAINING</div><button data-screen="settings" class="chip" style="cursor:pointer;border:1px solid #b69c65;padding:9px 12px;border-radius:9px" aria-label="Open Academy settings">⚙ Settings</button></header>'+back+content+'</div>'+desktopContext()+nav();document.dispatchEvent(new Event('ethical-academy-rendered'))}
// Workstation report drafts are device-local and intentionally do not affect exams or mastery.
const workstationReportKey='ethical-hacking-workstation-reports-v1';
let workstationPanel='check';
function workstationDraftId(){return id(courseIndex,lessonIndex)}
function readWorkstationDraft(){
 try{
  const drafts=JSON.parse(localStorage.getItem(workstationReportKey)||'{}');
  return typeof drafts[workstationDraftId()]==='string'?drafts[workstationDraftId()]:'';
 }catch{return ''}
}
function workstationPanelHTML(){
 const report=readWorkstationDraft();
 return '<div class="academy-workstation-tabs" role="tablist" aria-label="Lesson assessment sections">'
 +'<button type="button" role="tab" data-workstation-tab="check" id="academy-check-tab" aria-controls="academy-knowledge-check" aria-selected="'+(workstationPanel==='check')+'">Knowledge Check</button>'
 +'<button type="button" role="tab" data-workstation-tab="report" id="academy-report-tab" aria-controls="academy-lab-report" aria-selected="'+(workstationPanel==='report')+'">Lab Report</button>'
 +'</div>'
 +'<section class="academy-lab-report" id="academy-lab-report" role="tabpanel" aria-labelledby="academy-report-tab" '+(workstationPanel!=='report'?'hidden':'')+'>'
 +'<div class="academy-eyebrow">EVIDENCE & REFLECTION</div><h2>Document your investigation</h2>'
 +'<p>Describe your steps, the output you observed, why it matters, and what you would verify next. Use only fictional or authorized training evidence.</p>'
 +'<label for="academy-report-notes" class="academy-report-label">Your lab report</label>'
 +'<textarea id="academy-report-notes" rows="9" maxlength="12000" placeholder="OBSERVED: What did you do and see?\\nINTERPRETATION: Why did it happen?\\nUNKNOWN: What is not yet verified?\\nNEXT STEP: What would you check?">'+safe(report)+'</textarea>'
 +'<div class="academy-report-actions"><button type="button" class="button" id="academy-save-report">Save draft on this device</button>'
 +'<span id="academy-report-status" class="muted" role="status" aria-live="polite">'+(report?'Previously saved local draft loaded.':'Not submitted or graded.')+'</span></div>'
 +'<p class="muted academy-report-disclaimer">Reports are stored in this browser only; they are not cloud-synced, independently graded, or required to mark a lesson complete.</p></section>';
}
function setWorkstationPanel(panel){
 if(screen!=='lesson'||(panel!=='check'&&panel!=='report'))return;
 workstationPanel=panel;
 for(const name of ['check','report']){
  const element=document.getElementById(name==='check'?'academy-knowledge-check':'academy-lab-report');
  const tab=document.getElementById(name==='check'?'academy-check-tab':'academy-report-tab');
  if(element)element.hidden=name!==panel;
  if(tab)tab.setAttribute('aria-selected',String(name===panel));
 }
}
function go(dest){screen=dest;selected=-1;graded=false;render();scrollTo(0,0)}
function openLesson(c,l){courseIndex=c;lessonIndex=l;workstationPanel='check';go('lesson')}
function pathwayLevels(){if(!learningPath?.levels?.length)return [];const used=new Set();const levels=learningPath.levels.map((level,i)=>({...level,index:i,courseIds:level.courses.map(name=>catalog.courses.findIndex((course,j)=>!used.has(j)&&course.title===name)).filter(j=>{if(j<0)return false;used.add(j);return true})}));const unmatched=catalog.courses.map((c,i)=>i).filter(i=>!used.has(i));if(unmatched.length)levels[3].courseIds.push(...unmatched);return levels;}
function levelStats(level){const lessons=level.courseIds.reduce((n,i)=>n+catalog.courses[i].lessons.length,0);const done=level.courseIds.reduce((n,i)=>n+catalog.courses[i].lessons.filter((_,j)=>isDone(i,j)).length,0);return {lessons,done,finished:lessons>0&&done===lessons};}
function nextLesson(level){for(const i of level.courseIds){const j=catalog.courses[i].lessons.findIndex((_,j)=>!isDone(i,j));if(j>=0)return {course:i,lesson:j};}return null;}
function allEarlierFinished(levels,target){for(let i=0;i<target;i++){if(!levelStats(levels[i]).finished)return false;}return true;}
const LEVEL_CHECKPOINTS={0:['fundamentals'],1:['hardware'],2:['linux','windows'],3:['monitoring'],4:['web'],5:['network'],6:['backup'],7:['fundamentals','hardware','linux','windows','monitoring','web','network','backup']};
const CHECKPOINT_LABELS={fundamentals:'Computer and network basics',hardware:'PC hardware and POST',linux:'Linux service outage',windows:'Windows domain discovery',monitoring:'Security alert investigation',web:'Web application access control',network:'Lab network isolation',backup:'Backup recovery readiness'};
function masteryReadiness(level){
 const lesson=levelStats(level);
 let examScores={};try{const v=JSON.parse(localStorage.getItem('ethical-hacking-exam-results-v1')||'{}');if(v&&typeof v==='object')examScores=v}catch{}
 const applicable=(examCatalog?.exams||[]).map((exam,index)=>({exam,index})).filter(item=>level.courseIds.some(i=>item.exam.courses.includes(catalog.courses[i].title)));
 const unique=[...new Map(applicable.map(x=>[x.index,x])).values()];
 const threshold=Number(examCatalog?.passingPercent)||80;
 const passed=unique.filter(x=>Number(examScores[x.index])>=threshold);
 let practical={};try{const v=JSON.parse(localStorage.getItem('ethical-hacking-practical-mastery-v1')||'{}');if(v&&typeof v==='object')practical=v}catch{}
 const required=LEVEL_CHECKPOINTS[level.index]||[];
 const checks=required.map(key=>{const saved=practical[key]||{};return {key,name:CHECKPOINT_LABELS[key],verified:saved.verified===true,reportDrafted:Boolean(saved.reasoning?.trim()&&saved.action?.trim()&&saved.evidence?.trim()),reviewComplete:saved.reviewComplete===true}});
 const written=checks.filter(x=>x.reportDrafted).length,verified=checks.filter(x=>x.verified).length,reviewed=checks.filter(x=>x.reviewComplete).length;
 // A completed browser test is only simulated evidence; real hands-on sign-off is independent.
 const lessonsReady=level.courseIds.length===0?true:lesson.finished;
 const capstone=level.index===7?{first:qualificationEvidence().pass,second:advancedQualificationEvidence().passed}:null;
 const examsReady=capstone?capstone.first&&capstone.second:unique.length>0&&passed.length===unique.length;
 const practicalReady=checks.length>0&&verified===checks.length&&written===checks.length;
 const reviewReady=lessonsReady&&examsReady&&practicalReady;
 return {lesson,examCount:unique.length,examsPassed:passed.length,threshold,examList:unique.map(x=>({title:x.exam.title,passed:Number(examScores[x.index])>=threshold,score:Number(examScores[x.index]||0)})),checks,verified,written,reviewed,capstone,reviewReady,lessonsReady,examsReady,practicalReady};
}
function masteryStatus(level){const x=masteryReadiness(level);if(x.reviewReady)return 'Simulation evidence ready for human review';if(!x.lessonsReady)return 'Lessons still in progress';if(!x.examsReady)return x.capstone?'Final qualification simulations outstanding':x.examCount?'Exam remediation or completion needed':'Level exam mapping pending';if(!x.practicalReady)return x.checks.length?'Practical checkpoint / written analysis pending':'Practical checkpoint not yet mapped';return 'Review outstanding';}
function masteryPanel(level){
 const x=masteryReadiness(level);
 const lessonLine=x.lesson.lessons?x.lesson.done+' / '+x.lesson.lessons+' lessons marked complete':'No distinct lesson IDs assigned';
 const examRows=x.examList.map(a=>'<p class="mastery-entry">'+(a.passed?'✓ ':'○ ')+safe(a.title)+' — '+(a.passed?a.score+'% passed':a.score?a.score+'% · '+x.threshold+'% required':'not passed or no score')+'</p>').join('');
 const checkRows=x.checks.map(a=>'<p class="mastery-entry">'+(a.verified?'✓ ':'○ ')+safe(a.name)+' — '+(a.verified?'simulated repair verified':'simulation not verified')+'; '+(a.reportDrafted?'written draft saved':'written evidence needed')+'; '+(a.reviewComplete?'self-review saved':'self-review optional / pending')+'</p>').join('');
 const lessonGuidance=x.lesson.lessons&&!x.lessonsReady?'<p><strong>Next:</strong> Finish the remaining lessons using Start / resume above.</p>':'';
 const capstoneGuidance=x.capstone&&!x.examsReady?'<p><a class="button" href="./practical-qualification-exam.html">Practical qualification simulation →</a> <a class="button" href="./advanced-qualification-exam.html">Advanced qualification Part II →</a></p>':'';
 const examGuidance=x.examCount&&!x.examsReady?'<p><button class="button" data-screen="exams">Review or retake level examinations →</button></p>':'';
 const practicalGuidance=x.checks.length&&!x.practicalReady?'<p><a class="button" href="./practical-mastery-checkpoint.html">Complete practical checkpoint & evidence notebook →</a></p>':'';
 const noExam=x.examCount===0&&!x.capstone?'<p class="muted">No exam is mapped to this level yet. Exam requirement cannot be verified.</p>':'';
 const noPractical=x.checks.length===0?'<p class="muted">Dedicated stateful practical evidence is not mapped yet; existing linked labs remain available for practice.</p>':'';
 return '<section class="sheet"><h2>Level readiness & remediation</h2><p><strong>'+safe(masteryStatus(level))+'</strong></p><p>Lesson progress: '+lessonLine+'</p><p>'+(x.capstone?'Final qualifications: '+(Number(x.capstone.first)+Number(x.capstone.second))+' / 2 simulated passes':'Relevant exams: '+x.examsPassed+' / '+x.examCount+' passed ('+x.threshold+'% minimum)')+'</p>'+examRows+noExam+'<p>Practical checkpoints: '+x.verified+' / '+x.checks.length+' simulation verifications · '+x.written+' / '+x.checks.length+' written drafts · '+x.reviewed+' / '+x.checks.length+' self-reviews</p>'+checkRows+noPractical+lessonGuidance+capstoneGuidance+examGuidance+practicalGuidance+'<p class="muted">Read-only summary from this browser. Standalone lab evidence is not yet synchronized to Firebase. This is not a level certificate, professional sign-off, or validation on physical systems.</p></section>';
}
function levelCard(level,levels){
 const stat=levelStats(level),prerequisite=allEarlierFinished(levels,level.index),percent=stat.lessons?Math.round(stat.done*100/stat.lessons):0;
 return '<button class="course academy-level-card" data-level="'+level.index+'"><span class="academy-level-top"><span class="academy-level-number">LEVEL '+String(level.index+1).padStart(2,'0')+'</span><span class="academy-level-status">'+(stat.finished?'LESSONS COMPLETE':stat.done?'IN PROGRESS':'AVAILABLE')+'</span></span><span class="academy-level-title">'+safe(level.title)+'</span><span class="academy-level-summary">'+safe(level.subtitle||'Guided coursework, simulations and skill assessment')+'</span><span class="academy-level-meter"><span style="width:'+percent+'%"></span></span><span class="academy-level-footer"><span>'+(stat.lessons?stat.done+' / '+stat.lessons+' lessons':'Practical assessment track')+'</span><span>EXPLORE ↗</span></span></button>';
}
function academyMissionStats(levels){
 const done=count(),all=total(),pct=all?Math.round(done*100/all):0,active=levels.find(l=>!levelStats(l).finished)||levels[levels.length-1];
 return '<section class="academy-dashboard-metrics" aria-label="Academy statistics"><div class="academy-metric"><span>LESSONS COMPLETED</span><strong>'+done+' <small>/ '+all+'</small></strong><p>Across all courses</p></div><div class="academy-metric"><span>LEARNING PROGRESS</span><strong>'+pct+'<small>%</small></strong><div class="academy-metric-bar"><span style="width:'+pct+'%"></span></div></div><div class="academy-metric"><span>COURSE MODULES</span><strong>'+catalog.courses.length+'</strong><p>Structured learning library</p></div><div class="academy-metric"><span>CURRENT TRACK</span><strong>0'+(active?active.index+1:1)+'</strong><p>'+safe(active?.title||'Start learning')+'</p></div></section>';
}
function academyOperations(){
 const ops=[['courses','▦','Learning pathways','Guided courses and instruction'],['lab','⌘','Cyber range','Controlled labs and simulation'],['exams','◇','Assessments','Knowledge checks and exams'],['progress','▥','Training record','Track your learning']];
 return '<div class="academy-dashboard-heading"><div><span class="academy-eyebrow">TRAINING OPERATIONS</span><h2>Your workspace</h2></div></div><section class="academy-operations">'+ops.map(o=>'<button class="academy-operation" data-screen="'+o[0]+'"><span class="academy-operation-icon">'+o[1]+'</span><span><strong>'+o[2]+'</strong><small>'+o[3]+'</small></span><span>↗</span></button>').join('')+'</section>';
}
function levelDisplay(level,levels){const stat=levelStats(level),recommended=allEarlierFinished(levels,level.index),next=nextLesson(level),courseLinks=level.courseIds.map(i=>{const c=catalog.courses[i],completed=c.lessons.filter((_,j)=>isDone(i,j)).length;return '<button class="course" data-course="'+i+'"><span class="course-index">'+String(i+1).padStart(2,'0')+'</span><span class="course-body"><strong>'+safe(c.title)+'</strong><small>'+completed+' / '+c.lessons.length+' lessons completed · original course ID preserved</small></span><span>›</span></button>';}).join('');const links=(level.labs||[]).filter(x=>Array.isArray(x)&&x.length===2).map(x=>x[1]==='index.html#lab'?'<button class="button" data-screen="lab">'+safe(x[0])+' →</button>':'<a class="button" href="./'+encodeURI(x[1])+'">'+safe(x[0])+' →</a>').join('');return '<button class="back" data-screen="courses">← All levels</button><p><a class="button" href="./practical-competency-standards.html">Practical competency standards & evidence rubric →</a></p><div class="kicker">LEVEL '+(level.index+1)+' OF 8 · '+safe(level.subtitle||'')+'</div><h1>'+safe(level.title)+'</h1><p>'+safe(level.goal||'')+'</p><p class="muted"><strong>Planning allocation:</strong> '+(level.plannedHoursBreakdown?'Guided study '+level.plannedHoursBreakdown.instruction+' hr · Practical work '+level.plannedHoursBreakdown.practical+' hr · Exams and reports '+level.plannedHoursBreakdown.assessment+' hr · Remediation '+level.plannedHoursBreakdown.remediation+' hr. ': 'Not yet allocated. ')+'These are planning estimates, not verified authored study hours.</p><p class="muted"><strong>Study budget: '+(Number.isFinite(level.targetHours)?level.targetHours+' planned hours':'not yet assigned')+'.</strong> Includes lessons, labs, exams and remediation; not logged study time or verified authored hours.</p><section class="sheet"><h2>Learning sequence</h2><p>'+ (stat.lessons?stat.done+' / '+stat.lessons+' existing lessons completed':'Final integrated practical assessments')+'</p><p class="muted">'+(recommended?'Prerequisites from earlier levels are completed or this is Level 1.':'Recommended prerequisite: complete earlier level lessons before advancing. Previously available courses remain accessible for review.')+'</p>'+(next?'<button class="button" data-start-course="'+next.course+'" data-start-lesson="'+next.lesson+'">Start / resume next lesson →</button>':stat.lessons?'<p>All lessons for this level are marked complete. Review associated exams and practical work before moving on.</p>':'<p>This level is assessed through the linked practical work rather than additional new lesson IDs.</p>')+'</section>'+masteryPanel(level)+ (courseLinks?'<div class="kicker">COURSES IN ORDER</div>'+courseLinks:'')+'<section class="sheet"><h2>Practice and assessment</h2><div class="action-list">'+links+'</div><p class="muted">Stand-alone lab results are tracked separately; links do not imply their results are included in this level completion count.</p></section>';}

function render(){const courses=catalog.courses;
if(screen==='home'){
 const levels=pathwayLevels(),first=levels.find(l=>!levelStats(l).finished)||levels[0],next=first&&nextLesson(first);
 const done=count(),all=total(),percent=all?Math.round(done*100/all):0;
 const courses=catalog.courses.slice(0,6).map((c,i)=>{
  const complete=c.lessons.filter((_,j)=>isDone(i,j)).length,pct=c.lessons.length?Math.round(complete*100/c.lessons.length):0;
  const icons=['>_','⌘','{ }','⬡','◇','▣'];
  return '<button class="academy-v2-course-card" data-course="'+i+'"><span class="academy-v2-card-art"><span>'+icons[i]+'</span><small>MODULE_'+String(i+1).padStart(2,'0')+'</small></span><span class="academy-v2-card-body"><strong>'+safe(c.title)+'</strong><span class="academy-v2-card-progress">'+complete+' / '+c.lessons.length+' lessons · '+pct+'%</span><span class="academy-v2-course-meter"><span style="width:'+pct+'%"></span></span><span class="academy-v2-card-action">&gt; '+(complete===0?'start_course();':'continue();')+' ↗</span></span></button>';
 }).join('');
 shell('<section class="hero academy-v2-hero"><div class="academy-v2-hero-copy"><span class="academy-v2-prompt">&gt;_ learning_environment.init();</span><h1>ethical_hacking_<br><em>academy();</em></h1><p>/* Learn computer systems, defend networks, and develop practical security skills with guided coursework and authorized labs. */</p><div class="academy-v2-hero-actions">'+(next?'<button class="button" data-start-course="'+next.course+'" data-start-lesson="'+next.lesson+'">&gt; continue_learning(); ↗</button>':'<button class="button" data-screen="courses">&gt; explore_courses(); ↗</button>')+'</div></div><div class="academy-v2-hero-map" aria-hidden="true"></div><div class="academy-v2-progress-ring" role="progressbar" aria-label="Core lesson completion" aria-valuenow="'+percent+'" aria-valuemin="0" aria-valuemax="100" style="--academy-progress:'+percent+'"><strong>'+percent+'%</strong><span>overall_progress();</span></div></section>'
 +'<section class="academy-v2-stats" aria-label="Student progress"><div><span class="academy-v2-stat-icon">▤</span><strong>'+done+' <small>/ '+all+'</small></strong><span>lessons_completed();</span></div><div><span class="academy-v2-stat-icon">◷</span><strong>'+catalog.courses.length+'</strong><span>course_modules();</span></div><div><span class="academy-v2-stat-icon">▱</span><strong>'+levels.length+'</strong><span>training_levels();</span></div><div><span class="academy-v2-stat-icon">◇</span><strong>0'+(first?first.index+1:1)+'</strong><span>current_level();</span></div></section>'
 +'<div class="academy-v2-dashboard-layout"><section class="academy-v2-learning"><div class="academy-v2-section-head"><h2>&gt;_ your_learning_path();</h2><button data-screen="courses">view_all_courses(); ↗</button></div><div class="academy-v2-course-grid">'+courses+'</div></section>'
 +'<aside class="academy-v2-side"><section class="academy-v2-cyber-card"><h2>&gt;_ cyber_range();</h2><span class="academy-v2-live-indicator">● SIMULATED LABS</span><p>Explore guided command practice, investigations, and safe browser simulations.</p><button data-screen="lab">&gt; enter_lab(); ↗</button></section><section class="academy-v2-activity"><div class="academy-v2-section-head"><h2>&gt;_ training_status();</h2></div><p>'+done+' verified lesson completions saved in your current Academy progress.</p><div class="academy-v2-status-row"><span>▣</span><span>Lessons completed</span><strong>'+done+'</strong></div><div class="academy-v2-status-row"><span>◇</span><span>Remaining core lessons</span><strong>'+Math.max(0,all-done)+'</strong></div><button data-screen="progress">view_progress(); ↗</button></section></aside></div>'
 +'<section class="academy-v2-next"><div><strong>&gt;_ ready_for_the_next_challenge();</strong><p>Read the concept. Practice safely. Verify your understanding.</p></div><button data-screen="courses">explore_learning_levels(); ↗</button></section>'
 +'<p class="muted academy-v2-ethics">Training activities use authorized environments. Browser simulations are not real operating-system shells; practical competence requires separate verification.</p>');
}
else if(screen==='courses'){
 const levels=pathwayLevels();
 shell('<div class="academy-page-intro"><span class="academy-eyebrow">CURRICULUM / 8 TRAINING LEVELS</span><h1>Learning pathways</h1><p class="muted">Work through systems, networks, security and authorized practical assessment. Your original course and lesson completion records remain unchanged.</p></div><div class="academy-level-grid academy-pathway-grid">'+levels.map(level=>levelCard(level,levels)).join('')+'</div>');
}
else if(screen==='settings'){shell('<div class="kicker">STUDENT SETTINGS</div><h1>Settings</h1><p class="muted">Manage cloud saving, review connection status, compare progress, and download your own backup. This panel is no longer displayed over coursework.</p><section class="sheet"><h2>Cloud saving & backups</h2><div id="ethical-cloud-settings-slot"><p class="muted">Loading cloud connection…</p></div></section><p class="muted">Your existing Firebase cloud save, conflict comparison, and backup functions are unchanged. If devices disagree, compare both copies before selecting a version.</p>');}
else if(screen==='level'){const levels=pathwayLevels();const level=levels[levelIndex];if(!level){go('courses');return;}shell(levelDisplay(level,levels));}
else if(screen==='course'){const c=courses[courseIndex];shell('<button class="back" data-screen="level">← Level overview</button><div class="kicker">COURSE '+(courseIndex+1)+'</div><h1>'+safe(c.title)+'</h1><p class="muted">Study each lesson, answer the knowledge check, and review the rationale before marking it complete.</p><div class="academy-module-grid">'+c.lessons.map((l,j)=>'<button class="lesson-row academy-lesson-tile" data-lesson="'+j+'"><span>'+(j+1)+'. '+safe(l[0])+'</span><small>'+(isDone(courseIndex,j)?'✓ Complete':'Open →')+'</small></button>').join('')+'</div>'+courseMasteryPanel(c,courseIndex));}
else if(screen==='lesson'){
 const lesson=courses[courseIndex].lessons[lessonIndex],options=lesson[3];
 const header='<button class="back" data-backcourse="1">← Course overview</button><div class="academy-workstation-jumps" role="navigation" aria-label="Lesson quick navigation"><button type="button" data-workstation-jump="academy-reading">01 Learn</button><button type="button" data-workstation-jump="academy-practice-panel">02 Practice</button><button type="button" data-workstation-jump="academy-knowledge-check">03 Knowledge check</button><button type="button" data-workstation-jump="academy-lab-report">04 Lab report</button></div><div class="academy-workstation-title"><div class="kicker">TECHNICAL LEARNING WORKSTATION · '+safe(courses[courseIndex].title)+' · LESSON '+(lessonIndex+1)+'</div><h1>'+safe(lesson[0])+'</h1><p class="muted">Read the method, investigate the practice evidence, and demonstrate your understanding.</p></div>';
 const reading='<section class="sheet body academy-reading-panel" id="academy-reading" aria-label="Core lesson reading"><div class="academy-workstation-section-head"><span class="academy-eyebrow">01 / STUDY THE CONCEPT</span><h2>Learn</h2></div>'+lessonReadingHTML(lesson[1])+'<h2>Apply the concept</h2><p>'+safe(lesson[2])+'</p>'+(workedKeys.some(k=>k.course===courses[courseIndex].title&&k.lesson===lesson[0])?'<p><a class="button" href="./worked-answer-review.html?course='+courseIndex+'&lesson='+lessonIndex+'">Review a worked solution →</a></p>':'')+'</section>';
 const practice='<section class="academy-practice-panel" id="academy-practice-panel" aria-label="Guided practical lesson"><div class="academy-workstation-section-head"><span class="academy-eyebrow">02 / USE THE METHOD</span><h2>Practice</h2><button class="academy-expand-practice" type="button" id="academy-expand-practice" aria-pressed="false">Expand practice</button></div><p class="academy-simulation-disclaimer">Guided instructions and example commands, not a live operating-system terminal. Use your own authorized lab for actual execution.</p><div id="academy-embedded-practice" aria-live="polite"><p class="muted">Loading the relevant guided practice…</p></div></section>';
 const check='<section class="assessment academy-check-panel" id="academy-knowledge-check" role="tabpanel" aria-labelledby="academy-check-tab" '+(workstationPanel!=='check'?'hidden':'')+'><span class="academy-eyebrow">03 / TEST YOUR UNDERSTANDING</span><h2>Knowledge check</h2><p class="muted">Select the best response. Feedback explains why it is right.</p><div class="answers">'+options.map((o,j)=>'<button class="answer '+(selected===j?'selected':'')+'" data-answer="'+j+'">'+safe(o)+'</button>').join('')+'</div><button class="button" id="grade" '+(selected<0?'disabled':'')+'>Check my answer</button><div id="result" aria-live="polite">'+(graded?'<div class="feedback">'+(selected===lesson[4]?'Correct. ':'Review this answer. ')+safe(lesson[5])+'</div>':'')+'</div>'+(graded&&selected===lesson[4]?'<button class="button" id="complete">Mark lesson complete ✓</button>':'')+'</section>';
 shell(header+'<div class="academy-workstation-split" id="academy-workstation-split">'+reading+practice+'</div><div class="academy-workstation-assessment">'+workstationPanelHTML()+check+'</div>');
 loadEmbeddedPracticeForLesson(courseIndex,lessonIndex);
}
else if(screen==='lab'){shell("<div class=\"kicker\">SAFE PRACTICE ENVIRONMENT</div><h1>Practice Lab</h1><p>Explore safe command practice, investigations and assessments. All browser workstations are simulations, not real operating-system sessions.</p><section class=\"lab\"><div class=\"chip\">ISOLATED BROWSER SIMULATION</div><h2>Linux command familiarization</h2><div class=\"terminal\" id=\"terminal\">student@academy:~$</div><div class=\"cmds\"><button data-cmd=\"pwd\">pwd</button><button data-cmd=\"ls\">ls</button><button data-cmd=\"whoami\">whoami</button><button data-cmd=\"uname -a\">uname -a</button><button data-cmd=\"help\">help</button></div><p>Objective: identify your working directory, list sample files, and check the simulated identity.</p></section><section class=\"practice-section\"><h2>Practical qualification guidance</h2><p>Review the task evidence and safety criteria for each of the eight learning levels.</p><p><a class=\"button\" href=\"./practical-competency-standards.html\">Open practical competency standards →</a></p></section><section class=\"practice-section\"><h2>Interactive practice</h2><div class=\"practice-links\"><button class=\"button\" data-screen=\"labs\">Guided scenario labs →</button><button class=\"button\" data-screen=\"investigations\">Evidence investigations →</button><button class=\"button\" data-screen=\"simulations\">Multi-stage simulations →</button><button class=\"button\" data-screen=\"diagnostics\">Interactive diagnostic labs →</button><button class=\"button\" data-screen=\"terminal-challenges\">Terminal challenges →</button></div></section><section class=\"practice-section\"><h2>Workstations and assessments</h2><div class=\"practice-links\"><a class=\"button\" href=\"./pc-building-practice-studio.html\">PC Building Practice Studio →</a><a class=\"button\" href=\"./pc-hardware-diagnostics.html\">Hardware Engineering & Diagnostics →</a><a class=\"button\" href=\"./virtual-pc-build-simulator.html\">Virtual PC Build Simulator →</a><a class=\"button\" href=\"./red-team-server-lab-builder.html\">Red Team Server Lab Builder →</a><a class=\"button\" href=\"./virtual-corporate-redteam-network.html\">Virtual Corporate Red Team Network →</a><a class=\"button\" href=\"./red-team-practical-assessment.html\">Evidence-Based Red Team Assessment →</a><a class=\"button\" href=\"./independent-redteam-engagements.html\">Independent Red Team Engagements →</a><a class=\"button\" href=\"./enterprise-case-portfolio.html\">Enterprise Case Portfolio →</a><a class=\"button\" href=\"./real-system-lab-field-guide.html\">Real-System Lab Field Guide →</a><a class=\"button\" href=\"./independent-diagnostic-challenge.html\">Independent Diagnostic Challenge →</a><a class=\"button\" href=\"./hands-on-competency-review.html\">Hands-on Competency Review →</a><a class=\"button\" href=\"./competency-evidence-review.html\">Competency Evidence Review →</a><a class=\"button\" href=\"./practice-evidence-transfer.html\">Practice Evidence Transfer →</a><a class=\"button\" href=\"./advanced-reasoning-diagnostic.html\">Advanced Reasoning Diagnostic →</a><a class=\"button\" href=\"./redteam-infrastructure-capstone.html\">Integrated Red Team Infrastructure Capstone →</a><a class=\"button\" href=\"./command-troubleshooting-field-lab.html\">Command & Troubleshooting Field Lab →</a><a class=\"button\" href=\"./stateful-troubleshooting-workstation.html\">Stateful Troubleshooting Workstation →</a><a class=\"button\" href=\"./practical-mastery-checkpoint.html\">Practical Mastery Checkpoint →</a><a class=\"button\" href=\"./practical-command-fieldbook.html\">Practical command fieldbook →</a><a class=\"button\" href=\"./technical-assessment-studio.html\">Technical assessment studio →</a><a class=\"button\" href=\"./practical-qualification-exam.html\">Practical qualification exam →</a><a class=\"button\" href=\"./advanced-qualification-exam.html\">Advanced qualification — Part II →</a><a class=\"button\" href=\"./command-investigation-lab.html\">Typed command investigation lab →</a><a class=\"button\" href=\"./investigation-terminal-v2.html\">Investigation Terminal II →</a><a class=\"button\" href=\"./virtual-linux-workstation.html\">Virtual Linux workstation →</a><a class=\"button\" href=\"./virtual-windows-workstation.html\">Virtual Windows workstation →</a><a class=\"button\" href=\"./virtual-network-workstation.html\">Virtual network workstation →</a><a class=\"button\" href=\"./blind-troubleshooting-lab.html\">Blind troubleshooting lab →</a><a class=\"button\" href=\"./multi-fault-troubleshooting-lab.html\">Multi-fault troubleshooting lab →</a><a class=\"button\" href=\"./randomized-enterprise-lab.html\">Randomized enterprise lab →</a><a class=\"button\" href=\"./curriculum-quality-review.html\">Curriculum quality review →</a><a class=\"button\" href=\"./worked-answer-review.html\">Worked answer review →</a><a class=\"button\" href=\"./independent-competency-assessment.html\">Independent competency assessment →</a></div></section>");}
else if(screen==='terminal-challenges'){shell('<div class="kicker">SIMULATED COMMAND-LINE PRACTICE</div><h1>Terminal investigation challenges</h1><div id="terminal-challenge-root">Loading terminal challenges…</div>');void import('./terminal-challenges-ui.js').then(m=>m.mountTerminalChallenges(document.querySelector('#terminal-challenge-root'))).catch(err=>{console.error('Optional module mountTerminalChallenges unavailable',err);const slot=document.querySelector("#terminal-challenge-root");if(slot)slot.textContent='This optional module could not load. Check your connection and reopen the section.'});}
else if(screen==='diagnostics'){shell('<div class="kicker">INTERACTIVE TECHNICAL PRACTICE</div><h1>Diagnostic labs</h1><div id="diagnostic-labs-root">Loading diagnostics…</div>');void import('./diagnostic-labs-ui.js').then(m=>m.mountDiagnosticLabs(document.querySelector('#diagnostic-labs-root'))).catch(err=>{console.error('Optional module mountDiagnosticLabs unavailable',err);const slot=document.querySelector("#diagnostic-labs-root");if(slot)slot.textContent='This optional module could not load. Check your connection and reopen the section.'});}
else if(screen==='labs'){shell('<div class="kicker">GUIDED PRACTICAL ASSESSMENTS</div><h1>Scenario labs</h1><div id="guided-labs">Loading guided labs…</div>');void import('./labs-ui.js').then(m=>m.mountLabs(document.querySelector('#guided-labs'))).catch(err=>{console.error('Optional module mountLabs unavailable',err);const slot=document.querySelector("#guided-labs");if(slot)slot.textContent='This optional module could not load. Check your connection and reopen the section.'});}
else if(screen==='exams'){shell('<div class="kicker">ACADEMIC ASSESSMENTS</div><h1>Mastery examinations</h1><div id="academy-exams">Loading examinations…</div>');void import('./exams-ui.js?v=revised-assessment-v5-20261103').then(m=>m.mountExams(document.querySelector('#academy-exams'))).catch(err=>{console.error('Optional module mountExams unavailable',err);const slot=document.querySelector("#academy-exams");if(slot)slot.textContent='This optional module could not load. Check your connection and reopen the section.'});}
else if(screen==='assignments'){shell('<div class="kicker">PROFESSIONAL PORTFOLIO</div><h1>Written assignments</h1><div id="academy-assignments">Loading portfolio assignments…</div>');void import('./assignments-ui.js').then(m=>m.mountAssignments(document.querySelector('#academy-assignments'))).catch(err=>{console.error('Optional module mountAssignments unavailable',err);const slot=document.querySelector("#academy-assignments");if(slot)slot.textContent='This optional module could not load. Check your connection and reopen the section.'});}
else if(screen==='investigations'){shell('<div class="kicker">EVIDENCE-BASED SECURITY PRACTICE</div><h1>Investigations</h1><div id="academy-investigations">Loading investigations…</div>');void import('./investigations-ui.js').then(m=>m.mountInvestigations(document.querySelector('#academy-investigations'))).catch(err=>{console.error('Optional module mountInvestigations unavailable',err);const slot=document.querySelector("#academy-investigations");if(slot)slot.textContent='This optional module could not load. Check your connection and reopen the section.'});}
else if(screen==='simulations'){shell('<div class="kicker">ADVANCED GUIDED PRACTICE</div><h1>Multi-stage simulations</h1><div id="simulations-root">Loading simulations…</div>');void import('./simulations-ui.js').then(m=>m.mountSimulations(document.querySelector('#simulations-root'))).catch(err=>{console.error('Optional module mountSimulations unavailable',err);const slot=document.querySelector("#simulations-root");if(slot)slot.textContent='This optional module could not load. Check your connection and reopen the section.'});}
else if(screen==='progress'){const done=count();const ae=assessmentEvidence();const studio=technicalStudioEvidence();const qualification=qualificationEvidence();const advanced=advancedQualificationEvidence();const commandLab=commandLabEvidence();const virtualScore=virtualLabEvidence();const windowsScore=windowsLabEvidence();const networkScore=networkLabEvidence();const blind=blindLabEvidence();const multifault=multiFaultEvidence();const randomized=randomizedEvidence();shell('<div class="kicker">STUDENT RECORD</div><h1>Learning progress</h1><section class="sheet"><h2>Eight-level learning pathway</h2>'+pathwayLevels().map(l=>{const st=levelStats(l);return '<p>Level '+(l.index+1)+' · '+safe(l.title)+': '+(st.lessons?st.done+' / '+st.lessons+' lessons':'Practical assessments')+'</p>';}).join('')+'<p class="muted">These counts reflect recorded lesson completion. Exam and practical readiness are listed below; real-world competency is not verified.</p></section><section class="sheet"><h2>Readiness by level</h2>'+pathwayLevels().map(l=>'<p><strong>Level '+(l.index+1)+'</strong> — '+safe(masteryStatus(l))+'</p>').join('')+'<p class="muted">The readiness summary reads local exam and practical results without changing them. These records do not all sync to Firebase.</p></section><div class="sheet"><h2>'+done+' of '+total()+' lessons completed</h2><div class="progress"><span style="width:'+(done/total()*100)+'%"></span></div><p class="muted">Lesson progress is saved locally and can sync through the configured Firebase account in Settings. Practical checkpoint records are separate; confirm their storage status before changing devices.</p>'+courses.map((c,i)=>'<p>'+safe(c.title)+': '+c.lessons.filter((_,j)=>isDone(i,j)).length+' / '+c.lessons.length+'</p>').join('')+'</div>' + '<section class="sheet"><h2>Graded assessment evidence</h2><p>Passed mastery exams (80%+): '+ae.examPasses+' · Passed investigations (80%+): '+ae.investigationPasses+' · Perfect-score simulations: '+ae.simulationPerfect+'</p><p class="muted">These results are automated multiple-choice assessments, not independently validated hands-on proficiency. Course-specific exam evidence appears below.</p>'+courses.map(c=>{const evidence=examEvidence(c.title);return evidence.length?'<p><strong>'+safe(c.title)+'</strong>: '+evidence.map(e=>safe(e.title)+' — '+(e.score?e.score+'%'+(e.passed?' ✓ passed':' · review needed'):'not attempted')).join('; ')+'</p>':''}).join('')+'</section>' + '<section class="sheet"><h2>Technical Assessment Studio</h2><p>Attempts with a best score: '+studio.attempted+' / '+studio.total+' · Objective scores at or above 80%: '+studio.passed+' / '+studio.total+'</p><p class="muted">These are scored synthetic multiple-choice and evidence-selection exercises. Written reasoning quality and actual computer proficiency have not been independently assessed.</p><a class="button" href="./technical-assessment-studio.html">Open technical assessment studio</a></section>' + '<section class="sheet"><h2>Practical qualification simulation</h2><p>Best objective score: '+qualification.best+' / 40 · '+(qualification.pass?'Simulation pass recorded':'Not yet passed')+'</p><p class="muted">Four fictional investigations; 80% overall plus 6/10 each required. This is not real-system certification.</p><p>Advanced Part II: '+advanced.best+' / 30 · '+(advanced.passed?'Simulation pass recorded':'Not yet passed')+'</p><p>Typed command investigations: '+commandLab.attempted+' / 3 attempted · '+commandLab.passed+' scoring 8/10 or higher</p><p>Virtual Linux Workstation: best objective lab score '+virtualScore+' / 10</p><p>Virtual Windows Workstation: best objective lab score '+windowsScore+' / 10</p><p>Virtual Network Workstation: best objective lab score '+networkScore+' / 10</p><p>Blind troubleshooting: '+blind.attempted+' / 4 scenarios attempted · '+blind.mastered+' focused resolutions mastered</p><p>Multi-fault troubleshooting: '+multifault.attempted+' / 4 scenarios attempted · '+multifault.mastered+' mastered</p><p>Randomized enterprise troubleshooting: '+randomized.attempted+' / 10 fault pairs attempted · '+randomized.mastered+' mastered</p><div class="action-list"><a class="button" href="./randomized-enterprise-lab.html">Open Randomized enterprise lab →</a><a class="button" href="./multi-fault-troubleshooting-lab.html">Open Multi-fault investigations →</a><a class="button" href="./blind-troubleshooting-lab.html">Open Blind troubleshooting →</a><a class="button" href="./virtual-network-workstation.html">Open Network simulation →</a><a class="button" href="./virtual-windows-workstation.html">Open Windows simulation →</a><a class="button" href="./virtual-linux-workstation.html">Open Stateful Linux lab →</a><a class="button" href="./command-investigation-lab.html">Open Command investigations →</a><a class="button" href="./practical-qualification-exam.html">Open Qualification exam →</a><a class="button" href="./advanced-qualification-exam.html">Open Advanced Qualification — Part II →</a></div></section>' + '<section class="sheet"><h2>Portfolio progress</h2><p>Drafts with content: '+portfolioStatus().drafts+' · Self-reviewed: '+portfolioStatus().reviewed+'</p><p class="muted">Self-reviews are not graded exams or proof of hands-on proficiency. All portfolio progress is stored on this device.</p><button class="button" data-screen="assignments">Open written assignments</button></section>');}}
document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
 if(b.dataset.practiceStart){
  if(screen==='lesson')loadPracticeCheckpoint(b.dataset.practiceStart,courseIndex,lessonIndex);
  return;
 }
 if(b.dataset.practiceChoice!==undefined){
  if(screen==='lesson')gradePracticeChoice(Number(b.dataset.practiceChoice));
  return;
 }

 if(b.dataset.workstationJump){
  const target=b.dataset.workstationJump;
  if(target==='academy-knowledge-check')setWorkstationPanel('check');
  if(target==='academy-lab-report')setWorkstationPanel('report');
  document.getElementById(target)?.scrollIntoView({behavior:window.matchMedia?.('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});
  return;
 }

 if(b.dataset.workstationTab){setWorkstationPanel(b.dataset.workstationTab);return}
 if(b.id==='academy-expand-practice'){
  const split=document.getElementById('academy-workstation-split');
  const focused=split?.classList.toggle('academy-practice-expanded')||false;
  b.setAttribute('aria-pressed',String(focused));
  b.textContent=focused?'Restore split view':'Expand practice';
  return;
 }
 if(b.id==='academy-save-report'&&screen==='lesson'){
  const note=document.getElementById('academy-report-notes');
  const status=document.getElementById('academy-report-status');
  try{
   const store=JSON.parse(localStorage.getItem(workstationReportKey)||'{}');
   const saved=store&&typeof store==='object'&&!Array.isArray(store)?store:{};
   saved[workstationDraftId()]=note?.value?.slice(0,12000)||'';
   localStorage.setItem(workstationReportKey,JSON.stringify(saved));
   if(status)status.textContent='Draft saved on this device. Not cloud-synced or graded.';
  }catch(error){
   if(status)status.textContent='Could not save draft. Your browser storage may be unavailable.';
  }
  return;
 }
if(b.dataset.screen){go(b.dataset.screen);return}if(b.dataset.level!==undefined){levelIndex=Number(b.dataset.level);go('level');return}if(b.dataset.startCourse!==undefined){openLesson(Number(b.dataset.startCourse),Number(b.dataset.startLesson));return}if(b.dataset.course!==undefined){courseIndex=Number(b.dataset.course);go('course');return}if(b.dataset.lesson!==undefined){openLesson(courseIndex,Number(b.dataset.lesson));return}if(b.dataset.backcourse){go('course');return}if(b.dataset.answer!==undefined){selected=Number(b.dataset.answer);graded=false;render();return}if(b.id==='grade'){graded=true;render();return}if(b.id==='complete'){progress[id(courseIndex,lessonIndex)]=true;localStorage.setItem(progressKey,JSON.stringify(progress));if(lessonIndex+1<catalog.courses[courseIndex].lessons.length)openLesson(courseIndex,lessonIndex+1);else go('course');return}if(b.dataset.cmd){const outputs={'pwd':'/home/student','ls':'documents  practice-notes.txt  samples','whoami':'student','uname -a':'Linux academy-simulator 1.0 educational','help':'Available: pwd, ls, whoami, uname -a, help'};const terminal=document.querySelector('#terminal');terminal.textContent+=' '+b.dataset.cmd+'\n'+outputs[b.dataset.cmd]+'\nstudent@academy:~$';}});
const startupPaths=["./pc-building-track.json","./coursework-foundations-expansion-v1.json","./coursework-systems-redteam-v1.json","./coursework-applied-security-v1.json","./learning-pathway.json","./exams.json","./worked-answer-keys.json","./worked-answer-supplement-v8.json","./worked-answer-supplement-v9a.json","./worked-answer-supplement-v9b.json","./worked-answer-supplement-v9c.json"];
const startupRequests=new Map();
function loadResource(path,options){
 if(!startupRequests.has(path)){
  const controller=new AbortController();
  const kill=setTimeout(()=>controller.abort(),15000);
  const request=fetch(path,{...options,signal:controller.signal}).finally(()=>clearTimeout(kill)).catch(()=>null);
  startupRequests.set(path,request);
 }
 return startupRequests.get(path);
}
// Load the primary curriculum first; avoid saturating mobile networking with optional downloads.
const loadingMessage=(message)=>{const n=root?.querySelector('.loading');if(n)n.textContent=message};
loadingMessage('Loading core lessons and course catalog…');
window.__academyStage?.('Fetching primary curriculum');
try{const response=await loadResource('./curriculum.json',{cache:'no-store'});if(!response)throw Error('Primary course catalog could not be downloaded. Check network access and retry.');if(!response.ok)throw Error('Curriculum could not load');catalog=await response.json();window.__academyStage?.('Primary curriculum parsed: '+catalog.courses.length+' courses');for(const path of startupPaths)loadResource(path,{cache:'no-store'});try{const pcResponse=await loadResource('./pc-building-track.json',{cache:'no-store'});if(pcResponse.ok){const pcTrack=await pcResponse.json();if(Array.isArray(pcTrack.courses)){catalog.courses.push(...pcTrack.courses.filter(c=>typeof c.title==='string'&&Array.isArray(c.lessons)));}}else{console.warn('PC Building track could not load:',pcResponse.status)}}catch(pcError){console.warn('PC Building track unavailable:',pcError)}
try{
 const expansionResponse=await loadResource('./coursework-foundations-expansion-v1.json',{cache:'no-store'});
 if(expansionResponse.ok){
  const expansion=await expansionResponse.json();
  if(Array.isArray(expansion.courses)){
   for(const section of expansion.courses){
    const course=catalog.courses.find(c=>c.title===section.course);
    if(!course||!Array.isArray(section.lessons))continue;
    const existing=new Set(course.lessons.map(l=>l[0]));
    for(const lesson of section.lessons){
     if(Array.isArray(lesson)&&lesson.length>=6&&typeof lesson[0]==='string'&&!existing.has(lesson[0])){
      course.lessons.push(lesson);
      existing.add(lesson[0]);
     }
    }
   }
  }
 }else console.warn('Foundation coursework supplement unavailable:',expansionResponse.status);
 }catch(expansionError){console.warn('Foundation coursework supplement failed:',expansionError)}
try{
 const res=await loadResource('./coursework-systems-redteam-v1.json',{cache:'no-store'});
 if(res.ok){
  const supplement=await res.json();
  if(Array.isArray(supplement.courses)){
   for(const section of supplement.courses){
    const course=catalog.courses.find(c=>c.title===section.course);
    if(!course||!Array.isArray(section.lessons))continue;
    const titles=new Set(course.lessons.map(l=>l[0]));
    for(const lesson of section.lessons){
     if(Array.isArray(lesson)&&lesson.length>=6&&typeof lesson[0]==='string'&&!titles.has(lesson[0])){
      course.lessons.push(lesson);titles.add(lesson[0]);
     }
    }
   }
  }
 }else console.warn('Systems/Red Team supplement unavailable:',res.status);
}catch(error){console.warn('Systems/Red Team supplement failed:',error)}
try{
 const response=await loadResource('./coursework-applied-security-v1.json',{cache:'no-store'});
 if(response.ok){
  const addition=await response.json();
  if(Array.isArray(addition.courses)){
   for(const section of addition.courses){
    const course=catalog.courses.find(c=>c.title===section.course);
    if(!course||!Array.isArray(section.lessons))continue;
    const existing=new Set(course.lessons.map(l=>l[0]));
    for(const lesson of section.lessons){
     if(Array.isArray(lesson)&&lesson.length===6&&typeof lesson[0]==='string'&&!existing.has(lesson[0])){
      course.lessons.push(lesson);existing.add(lesson[0]);
     }
    }
   }
  }
 }else console.warn('Applied security curriculum unavailable:',response.status);
}catch(error){console.warn('Applied security curriculum failed:',error)}
try{const pathRes=await loadResource('./learning-pathway.json',{cache:'no-store'});if(pathRes.ok)learningPath=await pathRes.json();else console.warn('Learning path unavailable:',pathRes.status)}catch(pathErr){console.warn('Learning path could not load:',pathErr)}try{const examsResponse=await loadResource('./exams.json',{cache:'no-store'});if(examsResponse.ok)examCatalog=await examsResponse.json()}catch{}try{const workedResponse=await loadResource('./worked-answer-keys.json',{cache:'no-store'});if(workedResponse.ok){const data=await workedResponse.json();workedKeys=Array.isArray(data.items)?data.items:[];try{const supplementResponse=await loadResource('./worked-answer-supplement-v8.json',{cache:'no-store'});if(supplementResponse.ok){const supplement=await supplementResponse.json();if(Array.isArray(supplement.items))workedKeys=workedKeys.concat(supplement.items);for(const path of ['./worked-answer-supplement-v9a.json','./worked-answer-supplement-v9b.json','./worked-answer-supplement-v9c.json']){try{const res=await loadResource(path,{cache:'no-store'});if(res.ok){const json=await res.json();if(Array.isArray(json.items))workedKeys=workedKeys.concat(json.items)}}catch{}}}}catch{}}}catch{}if(location.hash==='#practice-lab')screen='lab';window.__academyStage?.('Coursework ready: '+catalog.courses.length+' courses');render();window.__academyStage?.('Academy home or selected screen rendered')}catch(error){window.__academyStage?.('Coursework startup failed: '+String(error?.message||error));console.error('Academy startup failed:',error);root.innerHTML='<div class="wrap"><section class="sheet" style="max-width:550px;margin:28px auto;padding:20px"><h2>Coursework could not open</h2><p>The main catalog could not be loaded on this device. Your previously saved progress has not been reset.</p><p>Check your internet connection and try again. If the Home Screen app remains stuck, open the Academy in Safari.</p><button class="button" id="academy-coursework-retry" onclick="window.location.reload()">Retry loading coursework</button></section></div>'}
