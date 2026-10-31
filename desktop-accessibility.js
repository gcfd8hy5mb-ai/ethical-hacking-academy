/* Desktop workspace usability enhancements, independent from coursework. */
(()=>{'use strict';
function init(){
 const layer=document.getElementById('academy-desktop-workspace');
 const launch=document.getElementById('academy-desktop-toggle');
 if(!layer||!launch||layer.dataset.enhanced)return;
 layer.dataset.enhanced='true';
 const title=layer.querySelector('.desk-head h2');
 if(title){title.id='academy-workspace-heading';layer.setAttribute('aria-labelledby',title.id);}
 layer.removeAttribute('aria-label');
 const close=layer.querySelector('#desk-close');
 const content=layer.querySelector('.desk-main');
 const note=document.createElement('p');note.className='desk-keyboard-help';
 note.textContent='Keyboard: Escape closes workspace · Tab moves between controls.';
 content?.before(note);
 const report=document.createElement('div');report.className='desk-live-message';report.setAttribute('role','status');report.setAttribute('aria-live','polite');content?.before(report);
 launch.setAttribute('aria-controls',layer.id);
 launch.setAttribute('aria-expanded','false');
 const observer=new MutationObserver(()=>{
  const open=!layer.hidden;
  launch.setAttribute('aria-expanded',String(open));
  document.body.classList.toggle('academy-workspace-open',open);
  if(document.body.classList.contains('auth-locked')&&open)close?.click();
 });
 observer.observe(layer,{attributes:true,attributeFilter:['hidden']});
 // A signed-out user cannot retain the workspace over the authentication screen.
 const authObserver=new MutationObserver(()=>{if(document.body.classList.contains('auth-locked')&&!layer.hidden)close?.click()});
 authObserver.observe(document.body,{attributes:true,attributeFilter:['class']});
 window.addEventListener('pagehide',()=>{observer.disconnect();authObserver.disconnect()},{once:true});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();