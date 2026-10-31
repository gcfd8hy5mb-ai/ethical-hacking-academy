/* Dependency-free desktop integration checks. Run: node --test tests/desktop-integration.test.cjs */
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const html=read('index.html');
const scripts=[...html.matchAll(/<script\b([^>]*)>/gi)].map(m=>m[1]).filter(a=>/\bsrc=/.test(a)).map(a=>{const q=a.match(/\bsrc=["']([^"']+)["']/);return q&&q[1]}).filter(Boolean).map(x=>x.split('?')[0].replace(/^\.\//,''));
const sheets=[...html.matchAll(/<link\b([^>]*)>/gi)].map(m=>m[1]).filter(a=>/stylesheet/.test(a)).map(a=>{const q=a.match(/\bhref=["']([^"']+)["']/);return q&&q[1]}).filter(Boolean).map(x=>x.split('?')[0].replace(/^\.\//,''));
test('Desktop styles are linked and source files exist',()=>{for(const f of ['desktop.css','desktop-workspace.css']){assert.ok(sheets.includes(f),f+' not linked');assert.ok(fs.existsSync(path.join(root,f)),f+' missing')}assert.match(read('desktop.css'),/@media\s*\(min-width:\s*900px\)/)});
test('Desktop workspace loaded after main app and script source exists',()=>{const pos=scripts.indexOf('desktop-workspace.js');assert.ok(pos>scripts.findIndex(s=>/(app\.js|app-v28\.js)/.test(s)));for(const s of scripts.filter(x=>x.startsWith('desktop-')))assert.ok(fs.existsSync(path.join(root,s)),s+' missing')});
test('Desktop script syntax is valid',()=>{for(const f of scripts.filter(s=>s.startsWith('desktop-')&&s.endsWith('.js')))assert.doesNotThrow(()=>new vm.Script(read(f),{filename:f}),f)});
test('Workspace does not execute shell commands or target external networks',()=>{const code=read('desktop-workspace.js');assert.match(code,/Unknown simulated command/);assert.doesNotMatch(code,/\beval\s*\(|\bfetch\s*\(|XMLHttpRequest|child_process/);});
test('Mobile first behavior and accessible close action',()=>{const css=read('desktop-workspace.css');assert.match(css,/@media\s*\(max-width:\s*750px\)/);const code=read('desktop-workspace.js');assert.match(code,/aria-modal/);assert.match(code,/Escape/);});
test('Optional modules are linked with valid scripts',()=>{for(const f of scripts.filter(x=>/desktop-(export|reliability|scenarios|report)\.js/.test(x))){assert.ok(fs.existsSync(path.join(root,f)));assert.doesNotThrow(()=>new vm.Script(read(f),{filename:f}))}});
