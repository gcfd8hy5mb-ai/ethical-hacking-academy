const key='ethical-hacking-academy-lab-results-v1';
function escapeHTML(value){return String(value).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');}
function loadResults(){try{return JSON.parse(localStorage.getItem(key)||'{}')}catch{return {}}}
let dataPromise;
function getData(){return dataPromise??=fetch('./labs.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('Lab material unavailable');return r.json()})}
export async function mountLabs(container){
 if(!container)return;
 try{
  const data=await getData();if(!container.isConnected)return;
  let active=0,step=0,answers={},showResult=false;
  const prior=loadResults();
  const paint=()=>{
   const lab=data.labs[active],s=lab.steps[step],chosen=answers[step],correct=chosen===s[2],complete=step===lab.steps.length-1;
   container.innerHTML='<p class="muted">'+escapeHTML(data.disclaimer)+'</p>'+
     '<label for="academy-lab-select">Choose a guided lab</label><select id="academy-lab-select" style="display:block;width:100%;max-width:450px;padding:13px;margin:10px 0 20px;border:1px solid #b79969;border-radius:10px;background:#fffaf2;color:#252b2b">'+
     data.labs.map((x,i)=>'<option value="'+i+'" '+(active===i?'selected':'')+'>'+escapeHTML(x.title)+(prior[i]?' ✓':'')+'</option>').join('')+'</select>'+
     '<section class="sheet"><div class="kicker">'+escapeHTML(lab.course)+' · SCENARIO '+(step+1)+' OF '+lab.steps.length+'</div><h2>'+escapeHTML(lab.title)+'</h2><p>'+escapeHTML(lab.context)+'</p><div class="progress"><span style="width:'+((step+1)/lab.steps.length*100)+'%"></span></div><h3>'+escapeHTML(s[0])+'</h3><div class="answers">'+s[1].map((choice,i)=>'<button data-lab-answer="'+i+'" class="answer '+(chosen===i?'selected':'')+'">'+escapeHTML(choice)+'</button>').join('')+'</div>'+
     '<button class="button" id="lab-check" '+(chosen===undefined?'disabled':'')+'>Check response</button>'+
     (showResult?'<div class="feedback" role="status">'+(correct?'Correct. ':'Not quite. ')+escapeHTML(s[3])+'</div>':'')+
     (showResult&&correct?'<button class="button" style="margin-top:10px" id="lab-next">'+(complete?'Finish lab':'Continue to next step')+'</button>':'')+
     '<p class="muted">You can repeat these scenarios as often as needed. Completion is saved on this device.</p></section>';
  };
  container.addEventListener('click',event=>{
   const button=event.target.closest('button');if(!button)return;
   if(button.dataset.labAnswer!==undefined){answers[step]=Number(button.dataset.labAnswer);showResult=false;paint();}
   else if(button.id==='lab-check'){showResult=true;paint();}
   else if(button.id==='lab-next'){
    if(step+1<data.labs[active].steps.length){step++;showResult=false;paint();}
    else{prior[active]=true;localStorage.setItem(key,JSON.stringify(prior));step=0;showResult=false;answers={};paint();container.insertAdjacentHTML('afterbegin','<p class="feedback" role="status">Guided lab completed. Result saved on this device.</p>');}
   }
  });
  container.addEventListener('change',event=>{if(event.target.id==='academy-lab-select'){active=Number(event.target.value);step=0;answers={};showResult=false;paint();}});
  paint();
 }catch(error){container.textContent='Guided labs could not be loaded. Please reload this page.';console.error(error)}
}
