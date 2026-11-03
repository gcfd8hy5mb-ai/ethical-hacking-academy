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
panel.style.cssText='position:relative;width:100%;max-width:100%;max-height:none;overflow:visible;border-radius:14px;border:1px solid #b69c65;background:#222b30;color:#f3eee2;padding:16px;font:15px system-ui;box-shadow:none;box-sizing:border-box';
function mountInSettings(){
 const slot=document.getElementById('ethical-cloud-settings-slot');
 if(slot){if(panel.parentElement!==slot)slot.appendChild(panel)}
 else if(panel.parentElement)panel.remove();
}
document.addEventListener('ethical-academy-rendered',mountInSettings);
mountInSettings();
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
 if(!enabled){panel.append(btn('Compare cloud and iPhone',connect),btn('Back up iPhone',backup))}
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
function downloadBundle(name,obj){
 const url=URL.createObjectURL(new Blob([JSON.stringify({exportedAt:new Date().toISOString(),academy:'ethical-hacking',...obj},null,2)],{type:'application/json'}));
 const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),15000);
}
function displayDifferences(device,cloud){
 const box=document.createElement('div');box.style.cssText='max-height:25vh;overflow:auto;border-top:1px solid #b69c65;padding-top:8px;margin-top:8px';
 const keys=[...new Set([...Object.keys(device),...Object.keys(cloud)])].sort();
 let changes=0;
 for(const k of keys){
  if(device[k]===cloud[k])continue;changes++;
  const section=document.createElement('details');section.style.cssText='border-bottom:1px solid #68727a;padding:6px 0';
  const summary=document.createElement('summary');summary.textContent=k+' · Different';section.append(summary);
  const p=document.createElement('p');
  const desc=v=>{if(v===undefined)return 'Missing';try{const x=JSON.parse(v);if(Array.isArray(x))return x.length+' items';if(x&&typeof x==='object')return Object.keys(x).length+' entries';return 'Saved value'}catch{return v.length+' characters'}};
  p.textContent='iPhone: '+desc(device[k])+' · Firebase: '+desc(cloud[k]);section.append(p);
  try{const x=JSON.parse(device[k]),y=JSON.parse(cloud[k]);if(x&&y&&typeof x==='object'&&typeof y==='object'&&!Array.isArray(x)&&!Array.isArray(y)){const changed=[...new Set([...Object.keys(x),...Object.keys(y)])].filter(key=>JSON.stringify(x[key])!==JSON.stringify(y[key]));const d=document.createElement('p');d.textContent='Different entries: '+changed.slice(0,25).join(', ')+(changed.length>25?'…':'');section.append(d)}}catch{}
  box.append(section);
 }
 state(changes+' saved record(s) differ. No local or cloud data has been changed.');
 panel.append(box);
}
async function connect(){
 if(!user?.emailVerified||running)return;running=true;const uid=user.uid,generation=sessionGeneration;
 try{
  const ref=location(),d=await getDoc(ref);
  if(uid!==auth.currentUser?.uid||generation!==sessionGeneration)return;
  const device=records();
  if(d.exists()){
   let cloud;try{cloud=JSON.parse(d.data().raw)}catch{}
   const remoteRevision=Number(d.data().revision);
   if(!valid(cloud)||!Number.isSafeInteger(remoteRevision)||remoteRevision<1){state('Cloud data is unrecognized. Nothing changed.');return}
   if(JSON.stringify(cloud)===JSON.stringify(device)){
    activeRef=ref;rev=remoteRevision;last=snapshot();enabled=true;localStorage.setItem(linkKey(uid),String(rev));render();state('Cloud connected · device progress matches Firebase');return;
   }
   render();displayDifferences(device,cloud);
   panel.append(btn('Download both backups',()=>{downloadBundle('ethical-hacking-both-versions.json',{iphone:device,cloud,cloudRevision:remoteRevision});state('Backup requested. Save it to Files and verify it before selecting a version.')}));
   panel.append(btn('Keep iPhone version in Firebase',async()=>{
    if(!confirm('Only continue after verifying the backup is saved to Files. Replace the FIREBASE copy with this iPhone copy?'))return;
    if(!confirm('Confirm again: overwrite existing Firebase progress with this iPhone copy?'))return;
    try{
     const data=records(),copy=JSON.stringify(data);
     const next=await runTransaction(db,async tx=>{
      const current=await tx.get(ref);
      if(!current.exists()||Number(current.data().revision)!==remoteRevision)throw Error('Firebase changed. Compare again.');
      if(auth.currentUser?.uid!==uid)throw Error('Account changed');
      tx.set(ref,{academy:'ethical-hacking',schemaVersion:1,revision:remoteRevision+1,raw:copy,updatedAt:serverTimestamp()});
      return remoteRevision+1;
     });
     if(auth.currentUser?.uid!==uid||generation!==sessionGeneration)return;
     activeRef=ref;rev=next;last=copy;enabled=true;localStorage.setItem(linkKey(uid),String(rev));render();state('Saved iPhone version to Firebase cloud');
    }catch(e){state('No overwrite completed: '+(e.code||e.message))}
   }));
   return;
  }
  render();state('No Firebase cloud record found. Device progress retained.');
  panel.append(btn('Download iPhone backup',backup));
  panel.append(btn('Enable first cloud save',async()=>{
   if(!confirm('First save: verify your iPhone backup is saved to Files. Create a new Firebase record without replacing other progress?'))return;
   try{
    const copy=snapshot();
    const next=await runTransaction(db,async tx=>{
     const existing=await tx.get(ref);
     if(existing.exists())throw Error('Cloud record appeared. Compare before connecting.');
     if(auth.currentUser?.uid!==uid)throw Error('Account changed');
     tx.set(ref,{academy:'ethical-hacking',schemaVersion:1,revision:1,raw:copy,updatedAt:serverTimestamp()});return 1;
    });
    if(auth.currentUser?.uid!==uid||generation!==sessionGeneration)return;
    activeRef=ref;rev=next;last=copy;enabled=true;localStorage.setItem(linkKey(uid),String(rev));render();state('Saved first Ethical Hacking copy to Firebase cloud');
   }catch(e){state('First cloud save failed without replacing progress: '+(e.code||e.message))}
  }));
 }catch(e){state('Cloud comparison unavailable: '+(e.code||e.message))}
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
