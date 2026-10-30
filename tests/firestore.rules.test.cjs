const { test, before, after } = require('node:test');
const { readFileSync } = require('node:fs');
const { initializeTestEnvironment, assertFails, assertSucceeds } = require('@firebase/rules-unit-testing');
const { serverTimestamp } = require('firebase/firestore');
let env;
before(async () => {
  env = await initializeTestEnvironment({projectId:'academy-rules-tests',firestore:{rules:readFileSync('firebase/firestore.rules','utf8')}});
});
after(async()=>{ if(env) await env.cleanup(); });
const path=(user,academy='ethical-hacking')=>'users/'+user+'/academies/'+academy+'/snapshots/progress-v1';
const data=(academy='ethical-hacking')=>({raw:'{}',academy,schemaVersion:1,updatedAt:serverTimestamp()});
const signed=(user,academies,verified=true)=>env.authenticatedContext(user,{academies,email_verified:verified}).firestore();
test('anonymous denied', async()=>assertFails(env.unauthenticatedContext().firestore().doc(path('alice')).get()));
test('student can write own ethical hacking progress',async()=>assertSucceeds(signed('alice',['ethical-hacking']).doc(path('alice')).set(data())));
test('student cannot access another student',async()=>{
  const db=signed('bob',['ethical-hacking']);
  await assertFails(db.doc(path('alice')).get());
  await assertFails(db.doc(path('alice')).set(data()));
});
test('hacking-only student denied law and business',async()=>{
  const db=signed('bob',['ethical-hacking']);
  for(const academy of ['business','law']){
    await assertFails(db.doc(path('bob',academy)).get());
    await assertFails(db.doc(path('bob',academy)).set(data(academy)));
  }
});
test('owner enrolled in three academies can write each',async()=>{
  const db=signed('owner',['ethical-hacking','business','law']);
  for(const academy of ['business','law','ethical-hacking'])
    await assertSucceeds(db.doc(path('owner',academy)).set(data(academy)));
});
test('unverified and unenrolled students denied',async()=>{
  await assertFails(signed('eve',['ethical-hacking'],false).doc(path('eve')).set(data()));
  await assertFails(signed('eve',[]).doc(path('eve')).set(data()));
});
test('invalid record and deletion denied',async()=>{
  const db=signed('alice',['ethical-hacking']);
  await assertFails(db.doc(path('alice')).set({...data(),updatedAt:'not timestamp'}));
  await assertFails(db.doc(path('alice')).delete());
});
