/* Assessment notebook for simulated security scenarios. No network calls. */
(()=>{'use strict';
function init(){
 const host=document.querySelector('#academy-desktop-workspace');
 if(!host||document.getElementById('desk-security-report'))return;
 const section=document.createElement('section');section.id='desk-security-report';section.className='desk-panel';section.hidden=true;
 section.innerHTML='<h3>Security assessment report</h3><p>Document findings from the fictional training environment. This is separate from course grades.</p><label for="desk-report-scope">Assessment scope</label><textarea id="desk-report-scope" placeholder="Fictional training assets and permission boundaries"></textarea><label for="desk-report-finding">Finding and supporting evidence</label><textarea id="desk-report-finding"></textarea><label for="desk-report-risk">Potential business impact</label><textarea id="desk-report-risk"></textarea><label for="desk-report-fix">Recommended remediation</label><textarea id="desk-report-fix"></textarea><div class="desk-actions"><button id="desk-report-save" type="button">Save local report</button><button id="desk-report-export" type="button">Export report</button></div><p id="desk-report-status" role="status"></p>';
 host.querySelector('.desk-main')?.append(section);
 const toggle=document.createElement('button');toggle.type='button';toggle.textContent='Assessment Report';toggle.setAttribute('aria-expanded','false');host.querySelector('.desk-head')?.append(toggle);
 const ids=['scope','finding','risk','fix'];
 const key='academy-training-assessment-v1';
 const fields=ids.map(id=>section.querySelector('#desk-report-'+id));
 const status=section.querySelector('#desk-report-status');
 try{const saved=JSON.parse(localStorage.getItem(key)||'{}');ids.forEach((id,i)=>{if(typeof saved[id]==='string')fields[i].value=saved[id]})}catch{}
 function data(){return Object.fromEntries(ids.map((id,i)=>[id,fields[i].value]))}
 function save(){try{localStorage.setItem(key,JSON.stringify(data()));status.textContent='Saved locally on this device.'}catch{status.textContent='Storage unavailable. Export a report copy.'}}
 section.querySelector('#desk-report-save').addEventListener('click',save);
 section.querySelector('#desk-report-export').addEventListener('click',()=>{const d=data();const content='SIMULATED SECURITY ASSESSMENT\n\n'+ids.map((id,i)=>id.toUpperCase()+'\n'+(d[id]||'[not completed]')).join('\n\n')+'\n\nEducational scenario — not a real penetration test.';const u=URL.createObjectURL(new Blob([content],{type:'text/plain'}));const a=document.createElement('a');a.href=u;a.download='ethical-hacking-training-report.txt';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),3000);status.textContent='Report export requested.'});
 toggle.addEventListener('click',()=>{section.hidden=!section.hidden;toggle.setAttribute('aria-expanded',String(!section.hidden));if(!section.hidden)fields[0].focus()});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();