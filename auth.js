import {initializeApp} from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js';
import {getAuth,onAuthStateChanged,signInWithEmailAndPassword,createUserWithEmailAndPassword,sendEmailVerification,sendPasswordResetEmail,signOut} from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js';
const root=document.getElementById('academy-auth-root');
const config=window.ACADEMY_FIREBASE_CONFIG;
const app=initializeApp(config,'ethical-hacking-academy');
const auth=getAuth(app);
let mode='signin',busy=false;
document.body.classList.add('auth-locked');
const esc=x=>String(x||'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
function message(text,error=false){const m=document.getElementById('auth-message');if(m){m.textContent=text;m.style.color=error?'#ffc6ad':'#e7d09e';}}
function form(){
 root.hidden=false;root.innerHTML='<main class="auth-screen"><section class="auth-panel"><div class="auth-emblem">◇</div><p class="auth-kicker">ETHICAL HACKING ACADEMY · STUDENT PORTAL</p><h1>Learn to defend.<br><em>Think like a professional.</em></h1><p class="auth-intro">Your structured path from computer fundamentals to responsible cybersecurity practice.</p><form id="academy-auth-form"><label for="auth-email">Email address</label><input required id="auth-email" type="email" autocomplete="email" placeholder="you@example.com"><label for="auth-password">Password</label><input required id="auth-password" type="password" minlength="6" autocomplete="'+(mode==='register'?'new-password':'current-password')+'" placeholder="Your password"><button class="auth-primary" type="submit">'+(mode==='register'?'Create student account':'Sign in to Academy')+'</button></form><p id="auth-message" role="status" aria-live="polite"></p><div class="auth-actions"><button id="auth-switch" type="button">'+(mode==='register'?'Already have an account? Sign in':'Create an account')+'</button><button id="auth-reset" type="button">Forgot password?</button></div><p class="auth-foot">Use the same Firebase student account as Business Academy and Law Academy. Coursework stays on your device and can sync through Settings when your account is connected.</p></section></main>';
 document.getElementById('auth-switch').onclick=()=>{mode=mode==='register'?'signin':'register';form()};
 document.getElementById('auth-reset').onclick=async()=>{const email=document.getElementById('auth-email').value.trim();if(!email){message('Enter your email address first.',true);return;}try{await sendPasswordResetEmail(auth,email);message('If an account exists, password reset instructions have been sent.')}catch(e){message('Unable to send reset instructions. Please try again.',true)}};
 document.getElementById('academy-auth-form').onsubmit=async e=>{e.preventDefault();if(busy)return;busy=true;const email=document.getElementById('auth-email').value.trim(),password=document.getElementById('auth-password').value;message('Checking your account…');try{if(mode==='register'){const created=await createUserWithEmailAndPassword(auth,email,password);await sendEmailVerification(created.user);await signOut(auth);message('Account created. Check your email, verify your address, then sign in.');mode='signin';}else{const result=await signInWithEmailAndPassword(auth,email,password);await result.user.reload();if(!result.user.emailVerified){await sendEmailVerification(result.user);await signOut(auth);message('Please verify your email before entering. A verification email has been sent.');}}}catch(err){const code=err?.code||'';message(code==='auth/invalid-credential'?'Incorrect email or password.':code==='auth/email-already-in-use'?'This email already has an account. Sign in instead.':code==='auth/weak-password'?'Use a stronger password.':'Unable to complete sign-in. Check your details and try again.',true)}finally{busy=false}};
}
form();
onAuthStateChanged(auth,async user=>{
 if(!user){document.body.classList.add('auth-locked');form();return;}
 try{await user.reload()}catch{}
 if(!auth.currentUser||!auth.currentUser.emailVerified){document.body.classList.add('auth-locked');form();message('Verify your email address to continue.');return;}
 root.hidden=true;document.body.classList.remove('auth-locked');
 let panel=document.getElementById('academy-auth-account');
 if(!panel){panel=document.createElement('div');panel.id='academy-auth-account';}
 const attachAccount=()=>{const header=document.querySelector('#app header.top');if(header&&panel.parentElement!==header)header.append(panel);};
 if(!window.__academyAccountObserver){
   window.__academyAccountObserver=new MutationObserver(attachAccount);
   window.__academyAccountObserver.observe(document.getElementById('app'),{childList:true,subtree:true});
 }
 attachAccount();
 panel.replaceChildren();
 const label=document.createElement('span');label.textContent=user.email||'Student';
 const logout=document.createElement('button');logout.textContent='Sign out';logout.onclick=()=>signOut(auth);
 panel.append(label,logout);
});
