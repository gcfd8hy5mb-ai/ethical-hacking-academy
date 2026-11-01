const KEY='ethical-hacking-terminal-challenges-v3';
const esc=x=>String(x).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const norm=x=>x.trim().toLowerCase().replace(/\s+/g,' ');
export async function mountTerminalChallenges(root){
 try{
  const response=await fetch('./terminal-challenges.json',{cache:'no-store'});
  if(!response.ok)throw Error('Missing challenges');
  const data=await response.json();
  let current=0,used=new Set(),history=[],diagnosis='',action='',phase='investigate',fixed=false,verified=false;
  let best={};try{best=JSON.parse(localStorage.getItem(KEY)||'{}')}catch{}
  function reset(){used=new Set();history=[];diagnosis='';action='';phase='investigate';fixed=false;verified=false}
  function points(c){return c.required.filter(x=>used.has(x)).length+(Number(diagnosis)===c.correctDiagnosis?2:0)+(Number(action)===c.correctAction?2:0)+(verified?2:0)}
  function draw(){
   const c=data.cases[current],st=c.stateful,final=phase==='done';
   const commands=phase==='investigate'?Object.keys(c.commands):phase==='apply'?[st.fixCommand,st.checkCommand,st.verifyCommand]:[];
   const commandPanel=commands.length?'<p>Supported mock commands: <code>'+commands.map(esc).join(' · ')+'</code></p><form id="terminal-command-form" style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0"><input id="terminal-command-input" aria-label="Typed mock command" autocomplete="off" spellcheck="false" placeholder="Type a listed command" style="min-width:0;flex:1;padding:12px;border:1px solid #c6ad80;border-radius:8px"><button class="button" type="submit">Run mock command</button></form>':'';
   const choicePanel=phase==='decide'?'<h3>Root cause</h3><div class="answers">'+c.diagnoses.map((x,i)=>'<button class="answer '+(diagnosis===String(i)?'selected':'')+'" data-diagnosis="'+i+'">'+esc(x)+'</button>').join('')+'</div><h3>Corrective action</h3><div class="answers">'+c.actions.map((x,i)=>'<button class="answer '+(action===String(i)?'selected':'')+'" data-action="'+i+'">'+esc(x)+'</button>').join('')+'</div><button class="button" id="terminal-apply" '+(diagnosis===''||action===''?'disabled':'')+'>Continue to controlled fix</button>':'';
   const result=final?'<h3>Score: '+points(c)+'/9</h3><p><strong>Expected diagnosis:</strong> '+esc(c.answer)+'</p><p><strong>Remediation:</strong> '+esc(c.remediation)+'</p><p><strong>Validation goal:</strong> '+esc(c.verification)+'</p><p>Best v3 score: '+Math.max(Number(best[current]||0),points(c))+'/9</p><p class="muted">This is synthetic command-output reasoning, not real device or command proficiency.</p><button class="button" id="terminal-retry">Retry</button>':'';
   root.innerHTML='<label for="terminal-case">Practice scenario</label><select id="terminal-case" style="display:block;width:100%;padding:12px;margin:12px 0">'+data.cases.map((x,i)=>'<option value="'+i+'" '+(current===i?'selected':'')+'>'+esc(x.title)+'</option>').join('')+'</select><section class="sheet"><h2>'+esc(c.title)+'</h2><p>'+esc(c.brief)+'</p><p class="muted">Fictional simulator only. Stage: '+esc(phase)+'. Commands only match the listed mock commands; no access to your device or outside computers.</p><div class="terminal" aria-live="polite" style="white-space:pre-wrap;overflow-wrap:anywhere">'+(history.length?history.map(([cmd,out])=>'student@simulation $ '+esc(cmd)+'\n'+esc(out)).join('\n\n'):'student@simulation $')+'</div>'+commandPanel+(phase==='investigate'?'<p>Relevant evidence: '+c.required.filter(x=>used.has(x)).length+'/3</p><button class="button" id="terminal-next" '+(used.size<3?'disabled':'')+'>Continue to diagnosis</button>':'')+choicePanel+(phase==='apply'?'<p>Apply the simulation change, inspect the updated state, then run the dedicated verification command. The chosen corrective action must be safe and supported.</p><p>Applied: '+(fixed?'yes':'no')+' · Verified: '+(verified?'yes':'no')+'</p><button class="button" id="terminal-finish" '+(!verified?'disabled':'')+'>Finish and grade</button>':'')+result+'</section>';
  }
  root.addEventListener('change',e=>{if(e.target.id==='terminal-case'){current=Number(e.target.value);reset();draw()}});
  root.addEventListener('submit',e=>{
   if(e.target.id!=='terminal-command-form')return;e.preventDefault();
   const typed=root.querySelector('#terminal-command-input').value.trim(),c=data.cases[current],st=c.stateful;
   if(phase==='investigate'){
    const match=Object.keys(c.commands).find(x=>norm(x)===norm(typed));
    history.push([typed,match?c.commands[match]:'Unsupported mock command. No system command was executed.']);
    if(match)used.add(match);
   }else if(phase==='apply'){
    if(norm(typed)===norm(st.fixCommand)){
     fixed=Number(diagnosis)===c.correctDiagnosis&&Number(action)===c.correctAction;
     history.push([typed,fixed?st.fixOutput:'Fix not applied: the selected diagnosis or remediation does not support this change.']);
    }else if(norm(typed)===norm(st.checkCommand)){
     history.push([typed,fixed?st.checkOutput:c.commands[st.checkCommand]||'Original condition remains unchanged.']);
    }else if(norm(typed)===norm(st.verifyCommand)){
     verified=fixed;history.push([typed,verified?st.verifyOutput:'FAIL: corrective change has not been successfully applied.']);
    }else history.push([typed,'Unsupported mock command. No system command was executed.']);
   }
   draw();
  });
  root.addEventListener('click',e=>{
   const b=e.target.closest('button');if(!b)return;
   if(b.id==='terminal-next'&&phase==='investigate'&&used.size>=3)phase='decide';
   else if(b.dataset.diagnosis!==undefined&&phase==='decide')diagnosis=b.dataset.diagnosis;
   else if(b.dataset.action!==undefined&&phase==='decide')action=b.dataset.action;
   else if(b.id==='terminal-apply'&&phase==='decide'&&diagnosis!==''&&action!=='')phase='apply';
   else if(b.id==='terminal-finish'&&phase==='apply'&&verified){
    phase='done';best[current]=Math.max(Number(best[current]||0),points(data.cases[current]));
    try{localStorage.setItem(KEY,JSON.stringify(best))}catch{}
   }else if(b.id==='terminal-retry')reset();
   draw();
  });
  draw();
 }catch(error){root.textContent='Could not load terminal challenges. Refresh and retry.';console.error(error)}
}
