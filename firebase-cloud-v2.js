/* Ethical Hacking Academy cloud progress. Shares the existing Firebase Authentication app.
   Opt-in cloud linking and offline-first localStorage; never silently replace device work. */
import {getApps} from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js';
import {getAuth,onAuthStateChanged} from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js';
import {getFirestore,doc,getDoc,runTransaction,serverTimestamp} from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js';
const firebaseApp=getApps().find(a=>a.name==='ethical-hacking-academy');
if(!firebaseApp)throw Error('Existing academy sign-in must initialize first');
const auth=getAuth(firebaseApp),db=getFirestore(firebaseApp);
const prefix='ethical-hacking-',docName='progress-v1';
const panel=document.createElement('section');panel.id='ethical-cloud-panel';
panel.style.cssText='position:fixed;z-index:1000;right:10px;bottom:10px;width:min(330px,calc(100vw - 20px));max-height:50vh;overflow:auto;border-radius:12px;border:1px solid #b69c65;background:#222b30;color:#f3eee2;padding:10px;font:13px system-ui;box-shadow:0 8px 28px #0009';
document.body.append(panel);
let user=null,enabled=false,rev=0,last='',running=false,delay=null,activeRef=null,sessionGeneration=0;
const records=()=>{
 const out={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k.startsWith(prefix))out[k]=localStorage.getItem(k)}
 return out;
};
const snapshot=()=>JSON.stringify(records());
const valid=obj=>obj&&typeof obj==='object'&&!Array.isArray(obj)&&Object.entries(obj).every(([k,v])=>k.startsWith(prefix)&&typeof v==='string');
const el=(tag,txt)=>{const n=document.createElement(tag);n.textContent=txt;return n};
const btn=(txt,fn)=>{const b=el('button',txt);b.style.cssText='margin:4px;padding:8px;border-radius:7px;border:0;background:#e2c47f;color:#252525;font-weight:700';b.onclick=fn;return b};
const state=s=>{const e=panel.querySelector('[data-cloud-state]');if(e)e.textContent=s};
const backup=()=>{
 const a=document.createElement('a'),u=URL.createObjectURL(new Blob([JSON.stringify({exportedAt:new Date().toISOString(),records:records()},null,2)],{type:'application/json'}));
 a.href=u;a.download='ethical-hacking-progress-backup.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),10000);
};
function render(){
 panel.replaceChildren();
 panel.append(el('strong','Ethical Hacking · Cloud saving'));
 const info=el('p',!user?'Sign in to save coursework to your student account.':enabled?'Cloud saving linked · device copies retained':'Device progress preserved. Cloud connection not yet linked.');
 info.dataset.cloudState='';panel.append(info);
 if(!user||!user.emailVerified)return;
 if(!enabled){panel.append(btn('Check cloud progress',inspect),btn('Connect safely',connect))}
 else{panel.append(btn('Sync now',sync),btn('Back up progress',backup))}
}
const location=()=>doc(db,'users',user.uid,'academies','ethical-hacking','snapshots',docName);
const linkKey=uid=>'ethical-cloud-link-'+uid;
async function resume(u,generation){
 if(!u?.emailVerified||!localStorage.getItem(linkKey(u.uid)))return;
 try{
  const ref=doc(db,'users',u.uid,'academies','ethical-hacking','snapshots',docName),d=await getDoc(ref);
  if(generation!==sessionGeneration||auth.currentUser?.uid!==u.uid)return;
  if(!d.exists()){state('Cloud copy missing. Your device data remains intact.');return}
  let remote;try{remote=JSON.parse(d.data().raw)}catch{}
  if(!valid(remote)){state('Unrecognized cloud data. No local changes made.');return}
  if(JSON.stringify(remote)!==snapshot()){state('Device and cloud versions differ. Auto-sync paused; inspect Connect safely.');return}
  const cloudRevision=Number(d.data().revision);
  if(!Number.isSafeInteger(cloudRevision)||cloudRevision<1){state('Cloud revision invalid. No work was overwritten.');return}
  rev=cloudRevision;last=snapshot();activeRef=ref;enabled=true;render();state('Connected · cloud and device match');
 }catch(e){if(generation===sessionGeneration)state('Cloud reconnect error: '+(e.code||e.message))}
}

async function inspect(){
 try{const d=await getDoc(location());state(d.exists()?'Cloud record exists. Connect to compare it with this device.':'No cloud coursework snapshot found for this account.')}catch(e){state('Firestore check failed: '+(e.code||e.message))}
}
async function connect(){
 if(!user?.emailVerified||running)return;running=true;
 try{
  activeRef=location();const d=await getDoc(activeRef);backup();
  if(d.exists()){
   let cloud;try{cloud=JSON.parse(d.data().raw)}catch{}
   if(!valid(cloud)){state('Cloud data format unrecognized. Device progress unchanged.');return}
   if(JSON.stringify(cloud)!==JSON.stringify(records())){
    if(!confirm('Existing Ethical Hacking cloud progress differs from this device. A backup was downloaded. OK replaces device records with cloud data and reloads. Cancel makes no changes.')){state('Two different copies found; no overwrite performed.');return}
    for(const [k,v] of Object.entries(cloud))localStorage.setItem(k,v);
    rev=Number(d.data().revision)||0;enabled=true;last=snapshot();window.location.reload();return;
   }
   rev=Number(d.data().revision)||0;
  }else{
   if(!confirm('Back up your progress before first upload. Continue saving Ethical Hacking coursework to this Firebase account?')){state('Cloud link canceled. Device progress preserved.');return}
   rev=0;
  }
  enabled=true;last=snapshot();
  const ok=await sync();
  if(!ok){enabled=false;activeRef=null;render();state('Upload failed. Device progress is intact; check Firebase rules and retry.');return}
  localStorage.setItem(linkKey(user.uid),String(rev));
  render();state('Saved to Firebase cloud');
 }catch(e){state('Unable to connect: '+(e.code||e.message))}
 finally{running=false}
}
async function sync(){
 if(!enabled||!user?.emailVerified||!activeRef)return false;
 const uid=user.uid,copy=snapshot(),previous=rev;
 try{
  state('Synchronizing progress…');
  const next=await runTransaction(db,async tx=>{
   const d=await tx.get(activeRef);
   const current=d.exists()?Number(d.data().revision)||0:0;
   if(current!==previous)throw Error('Cloud progress changed on another device. Save stopped to avoid overwriting it.');
   if(auth.currentUser?.uid!==uid)throw Error('Account changed during upload.');
   tx.set(activeRef,{academy:'ethical-hacking',schemaVersion:1,revision:current+1,raw:copy,updatedAt:serverTimestamp()});
   return current+1;
  });
  if(auth.currentUser?.uid!==uid)return false;
  rev=next;last=copy;localStorage.setItem(linkKey(uid),String(rev));state('Saved to Firebase cloud');return true;
 }catch(e){state('Saved only on this device: '+(e.message||e.code));return false}
}
onAuthStateChanged(auth,async u=>{sessionGeneration++;const generation=sessionGeneration;user=u;enabled=false;activeRef=null;rev=0;last=snapshot();clearTimeout(delay);render();if(u?.emailVerified){state('Checking existing cloud link…');await resume(u,generation);if(!enabled&&generation===sessionGeneration&&!localStorage.getItem(linkKey(u.uid)))state('Device progress preserved. Select Connect safely for the first cloud upload.')}});
setInterval(()=>{if(!enabled||running||!user?.emailVerified)return;const s=snapshot();if(s!==last){clearTimeout(delay);delay=setTimeout(async()=>{if(running)return;running=true;try{await sync()}finally{running=false}},1600)}},3500);
window.addEventListener('online',()=>{if(enabled)sync()});
