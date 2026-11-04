(function(){
"use strict";
var enabled=new URLSearchParams(location.search).get("debug")==="1";
var marks=[],status="Starting",lastError="";
function short(s){return String(s||"").replace(/([a-z0-9._%+-]+)@([a-z0-9.-]+)/gi,"[email redacted]").replace(/AIza[\w-]+/g,"[key redacted]").slice(0,200)}
function write(kind,msg){var value=kind+": "+short(msg);marks.push(value);if(marks.length>14)marks.shift();if(kind==="ERROR")lastError=value;status=value;render()}
function render(){
 if(!enabled)return;
 var box=document.getElementById("academy-runtime-debug");if(!box)return;
 var app=document.getElementById("app"),auth=document.getElementById("academy-auth-root");
 var facts=["Visible view: "+(document.body.classList.contains("auth-locked")?"Sign-in locked":"Unlocked"),"App: "+(app?.querySelector(".hero")?"Home rendered":app?.querySelector(".loading")?"Loading placeholder":app?.textContent.trim().slice(0,55)||"No content"),"Sign-in: "+(auth?.hidden?"Hidden":auth?.querySelector("#academy-auth-form")?"Form shown":"Pending")];
 box.textContent=["ACADEMY STARTUP DIAGNOSTIC",...facts,"",...marks].join("\n")
}
function init(){
 if(!enabled)return;
 var el=document.createElement("pre");el.id="academy-runtime-debug";
 el.style.cssText="position:fixed!important;top:4px;left:4px;right:4px;max-height:55vh;overflow:auto;z-index:2147483647;background:#1b3038;color:#fbf3dc;border:2px solid #c3a46f;border-radius:10px;padding:10px;font:12px/1.45 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere;pointer-events:none;box-shadow:0 5px 15px #0006";
 document.body.append(el);
 write("INFO","Diagnostic activated; no student data inspected.");
 render();
}
window.__academyStage=function(label){write("STAGE",label)};
window.addEventListener("error",function(e){write("ERROR",e?.message||"Script or resource error")});
window.addEventListener("unhandledrejection",function(e){write("ERROR",e?.reason?.message||String(e?.reason||"Rejected promise"))});
document.addEventListener("DOMContentLoaded",init);
setInterval(render,1500);
})();