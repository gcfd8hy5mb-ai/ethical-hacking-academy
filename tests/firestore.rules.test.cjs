const { test, before, after } = require('node:test');
const { readFileSync } = require('node:fs');
const { initializeTestEnvironment, assertFails, assertSucceeds } = require('@firebase/rules-unit-testing');
const { serverTimestamp, doc, getDoc, setDoc, deleteDoc } = require('firebase/firestore');
let env;
before(async()=>{env=await initializeTestEnvironment({projectId:'academy-rules-tests',firestore:{rules:readFileSync('firebase/firestore.rules','utf8')}})});
after(async()=>{if(env)await env.cleanup()});
const path=(uid,a='ethical-hacking')=>'users/'+uid+'/academies/'+a+'/snapshots/progress-v1';
const data=(a='ethical-hacking')=>({raw:'{}',academy:a,schemaVersion:1,updatedAt:serverTimestamp()});
const db=(uid,allowed,verified=true)=>env.authenticatedContext(uid,{academies:allowed,email_verified:verified}).firestore();
test('anonymous denied',async()=>{await assertFails(getDoc(doc(env.unauthenticatedContext().firestore(),path('alice'))))});
test('authorized student writes own record',async()=>{await assertSucceeds(setDoc(doc(db('alice',['ethical-hacking']),path('alice')),data()))});
test('cross-user access denied',async()=>{
 const x=db('bob',['ethical-hacking']);
 await assertFails(getDoc(doc(x,path('alice'))));
 await assertFails(setDoc(doc(x,path('alice')),data()));
});
test('hacking-only enrollment denied business and law',async()=>{
 const x=db('bob',['ethical-hacking']);
 for(const a of ['business','law']){
  await assertFails(getDoc(doc(x,path('bob',a))));
  await assertFails(setDoc(doc(x,path('bob',a)),data(a)));
 }
});
test('owner with claims can write all three',async()=>{
 const x=db('owner',['business','law','ethical-hacking']);
 for(const a of ['business','law','ethical-hacking'])await assertSucceeds(setDoc(doc(x,path('owner',a)),data(a)));
});
test('unverified and unenrolled users denied',async()=>{
 await assertFails(setDoc(doc(db('eve',['ethical-hacking'],false),path('eve')),data()));
 await assertFails(setDoc(doc(db('eve',[]),path('eve')),data()));
});
test('invalid record and deletion denied',async()=>{
 const x=db('alice',['ethical-hacking']);
 await assertFails(setDoc(doc(x,path('alice')),{...data(),updatedAt:'fake'}));
 await assertFails(deleteDoc(doc(x,path('alice'))));
});
