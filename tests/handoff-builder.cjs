const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../tools/ai-project-handoff/index.html'),'utf8');
const script=source.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
const context=vm.createContext({});
vm.runInContext(script.split('// UI binding.')[0],context);
const build=(data,instructions=true)=>context.makeHandoff(data,instructions);
test('missing notes remain explicit unknowns, never finished tasks',()=>{
 const text=build({});assert.match(text,/No completed work has been recorded/);assert.match(text,/Confirm what remains unfinished or unverified/);assert.match(text,/Choose the first concrete action/);
});
test('a published page does not close its untested download',()=>{
 const text=build({project:'Sample release',done:'Page published. Opened the live page.',open:'Download untested. Payment not verified.',next:'Download the live file.'});
 assert.match(text,/Download untested\. Payment not verified\./);assert.match(text,/Download the live file\./);assert.match(text,/builder has not verified/);
});
test('technical notes, Unicode and line breaks survive export',()=>{
 const text=build({project:'Café',context:'src/main.js\r\nKeep `local-only` mode.\n日本語'});assert.match(text,/Café/);assert.match(text,/src\/main.js\nKeep `local-only` mode\.\n日本語/);
});
test('assistant instructions can be omitted without losing project facts',()=>{
 const text=build({project:'One',next:'Review the saved file.'},false);assert.doesNotMatch(text,/## Instructions for the next assistant/);assert.match(text,/Review the saved file\./);assert.match(text,/## Verification note/);
});
test('download filenames cannot contain path traversal or control characters',()=>{
 assert.equal(context.fileName('../../Crème / site'),'creme-site-handoff.md');assert.equal(context.fileName('你好'),'handoff.md');assert.equal(context.fileName('One\nTwo'),'one-two-handoff.md');assert.ok(context.fileName('x'.repeat(160)).length<=81);
});
test('script-looking input is preserved as text with no HTML renderer',()=>{
 assert.match(build({done:'<img src=x onerror=alert(1)>'}),/<img src=x onerror=alert\(1\)>/);assert.doesNotMatch(script,/\.innerHTML\s*=/);assert.doesNotMatch(source,/<script[^>]+src=/);
});
