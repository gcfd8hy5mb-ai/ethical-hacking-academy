/* Branch-only V2 shell for separate assessment and practice HTML pages. */
(function(){
function init(){
  if(document.querySelector('.v2-standalone-nav')||!document.querySelector('main'))return;
  const main=document.querySelector('main');
  const title=(document.title||'Academy Workstation').split(/[|·]/)[0].trim();
  const nav=document.createElement('nav');nav.className='v2-standalone-nav';nav.setAttribute('aria-label','Academy workspace');
  nav.innerHTML='<div class="v2-logo"><span>⬡ ETHICAL<br>HACKING<br>ACADEMY</span><small>LEARN // PRACTICE // MASTER</small></div>'
   +'<a href="./index.html">⌂ dashboard();</a><a href="./index.html#courses">▤ courses();</a><a href="./index.html#lab">⌘ cyber_range();</a><a href="./index.html#progress">▥ progress();</a><div class="v2-mission">/* MISSION */<br>build_skills();<br>defend_systems();<br>practice_ethically();</div>';
  const hero=document.createElement('section');hero.className='v2-standalone-hero';
  const left=document.createElement('div'),prompt=document.createElement('span'),heading=document.createElement('h1'),p=document.createElement('p'),back=document.createElement('a');
  prompt.className='v2-prompt';prompt.textContent='>_ CYBER RANGE / PRACTICAL WORKSPACE';
  heading.textContent=title;p.textContent='/* Guided technical training // authorized practice only */';
  back.href='./index.html#lab';back.textContent='> return_to_cyber_range(); ↗';
  left.append(prompt,heading,p);hero.append(left,back);
  document.body.insertBefore(nav,document.body.firstChild);main.insertBefore(hero,main.firstChild);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
