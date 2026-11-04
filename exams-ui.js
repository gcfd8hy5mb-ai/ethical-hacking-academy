const escapeHTML=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const LEGACY_KEY='ethical-hacking-exam-results-v1';
const REVISED_KEY='ethical-hacking-exam-results-revised-v2';
const REVISED_V3_KEY='ethical-hacking-exam-results-revised-v3';
const REVISED_V4_KEY='ethical-hacking-exam-results-revised-v4';
function saved(key){try{const v=JSON.parse(localStorage.getItem(key)||'{}');return v&&typeof v==='object'&&!Array.isArray(v)?v:{}}catch{return {}}}
const shuffled=n=>{const indexes=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[indexes[i],indexes[j]]=[indexes[j],indexes[i]]}return indexes};
export async function mountExams(root){
 try{
  const response=await fetch('./exams.json',{cache:'no-store'});
  if(!response.ok)throw Error('Legacy exam catalog unavailable');
  const original=await response.json();
  if(!root.isConnected)return;
  let revised=null;
  try{
   const response=await fetch('./exams-revised-v2.json',{cache:'no-store'});
   if(response.ok){const candidate=await response.json();if(candidate.version===2&&Array.isArray(candidate.exams)&&candidate.exams.length===8)revised=candidate}
  }catch(e){console.warn('Revised exams unavailable; original exams remain accessible',e)}
  let v3=null;
  try{
   const response=await fetch('./exams-revised-v3.json',{cache:'no-store'});
   if(response.ok){const candidate=await response.json();if(candidate.version===3&&Array.isArray(candidate.exams)&&candidate.exams.length===9)v3=candidate}
  }catch(e){console.warn('Revised V3 exams unavailable; original and V2 exams remain accessible',e)}
  let v4=null;
  try{
   const response=await fetch('./exams-revised-v4.json',{cache:'no-store'});
   if(response.ok){const candidate=await response.json();if(candidate.version===4&&Array.isArray(candidate.exams)&&candidate.exams.length===7)v4=candidate}
  }catch(e){console.warn('Revised V4 exams unavailable; previous exams remain accessible',e)}
  const revisedCount=revised?.exams.length||0;
  const revisedV3Count=v3?.exams.length||0;
  const revisedV4Count=v4?.exams.length||0;
  const catalog=[...(revised?.exams||[]),...(v3?.exams||[]),...(v4?.exams||[]),...original.exams];
  let selectedExam=0,answers={},submitted=false,orders=catalog[0].questions.map(q=>shuffled(q[1].length));
  const currentHistory=()=>{
   if(selectedExam<revisedCount)return {modern:true,key:REVISED_KEY,index:selectedExam,version:'V2'};
   if(selectedExam<revisedCount+revisedV3Count)return {modern:true,key:REVISED_V3_KEY,index:selectedExam-revisedCount,version:'V3'};
   if(selectedExam<revisedCount+revisedV3Count+revisedV4Count)return {modern:true,key:REVISED_V4_KEY,index:selectedExam-revisedCount-revisedV3Count,version:'V4'};
   return {modern:false,key:LEGACY_KEY,index:selectedExam-revisedCount-revisedV3Count-revisedV4Count,version:'legacy'};
  };
  const isAnswered=()=>Object.keys(answers).length===catalog[selectedExam].questions.length;
  function paint(){
   if(!root.isConnected)return;
   const exam=catalog[selectedExam],ref=currentHistory(),history=saved(ref.key),score=exam.questions.reduce((n,q,i)=>n+(answers[i]===q[2]?1:0),0),percent=Math.round(score/exam.questions.length*100),pass=percent>=original.passingPercent;
   root.innerHTML='<label for="exam-selector">Choose examination</label><select id="exam-selector" style="display:block;width:100%;padding:12px;border-radius:8px;margin:10px 0 20px">'+catalog.map((x,i)=>'<option value="'+i+'" '+(i===selectedExam?'selected':'')+'>'+escapeHTML(i<revisedCount?'UPDATED V2 · '+x.title:i<revisedCount+revisedV3Count?'UPDATED V3 · '+x.title:i<revisedCount+revisedV3Count+revisedV4Count?'UPDATED V4 · '+x.title:'LEGACY · '+x.title)+'</option>').join('')+'</select>'+
   '<p class="muted">Pass mark: '+original.passingPercent+'%. The revised V2, V3 and V4 examinations are optional, separately scored assessments. They do not replace historical grades or Academy mastery status. All 24 legacy examinations remain accessible.</p>'+
   exam.questions.map((q,i)=>'<section class="sheet" style="margin:14px 0"><div class="kicker">QUESTION '+(i+1)+' OF '+exam.questions.length+'</div><h3>'+escapeHTML(q[0])+'</h3><div class="answers">'+orders[i].map(j=>'<button class="answer '+(answers[i]===j?'selected':'')+'" data-exam-answer="'+i+':'+j+'" '+(submitted?'disabled':'')+'>'+escapeHTML(q[1][j])+'</button>').join('')+'</div>'+(submitted?'<p class="feedback">'+(answers[i]===q[2]?'Correct. ':'Incorrect. ')+escapeHTML(q[3])+'</p>':'')+'</section>').join('')+
   (submitted?'<section class="sheet"><h2>Score: '+score+'/'+exam.questions.length+' ('+percent+'%)</h2><p>'+(pass?(ref.modern?'Revised diagnostic pass threshold met.':'Mastery achieved.'):'Below pass threshold. Review explanations and retry.')+'</p><p class="muted">Best score for this exam version: '+Math.max(Number(history[ref.index]||0),percent)+'%'+(ref.modern?' · Separate from original mastery records':'')+'</p><button id="exam-retry" class="button">Retake examination</button></section>':'<button id="exam-submit" class="button" '+(!isAnswered()?'disabled':'')+'>Grade examination</button>');
  }
  const fresh=()=>{answers={};submitted=false;orders=catalog[selectedExam].questions.map(q=>shuffled(q[1].length));paint()};
  root.addEventListener('change',event=>{if(event.target.id==='exam-selector'){selectedExam=Number(event.target.value);fresh()}});
  root.addEventListener('click',event=>{
   const b=event.target.closest('button');if(!b)return;
   if(b.dataset.examAnswer&&!submitted){const [i,j]=b.dataset.examAnswer.split(':').map(Number);answers[i]=j;paint()}
   else if(b.id==='exam-submit'&&!submitted&&isAnswered()){
    submitted=true;const exam=catalog[selectedExam],percentage=Math.round(100*exam.questions.reduce((n,q,i)=>n+(answers[i]===q[2]?1:0),0)/exam.questions.length),ref=currentHistory(),history=saved(ref.key);
    history[ref.index]=Math.max(Number(history[ref.index])||0,percentage);
    try{localStorage.setItem(ref.key,JSON.stringify(history))}catch(e){console.warn('Exam result could not be saved locally',e)}
    paint();
   }else if(b.id==='exam-retry')fresh();
  });
  paint();
 }catch(error){root.textContent='Unable to load examinations. Reload the page and try again.';console.error(error)}
}
