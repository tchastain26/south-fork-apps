/* Run with Node 20+: node tests/dog-poop-tracker-browser.cjs
   Starts an isolated loopback server and disposable browser contexts. No real GPS. */
const {chromium,webkit}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const http=require('node:http');
const path=require('node:path');
const root=path.resolve('tools/dog-poop-tracker');
const out=path.resolve('artifacts/dog-poop-tracker');fs.mkdirSync(out,{recursive:true});
let swGeneration=0,failAsset=false,legacyWorker=false;
// Reproduce the first v2.1 worker so its waiting-update recovery stays covered.
const legacySW=`const CACHE='poop-tracker-v3-2026.10.02-review2';
const scope=new URL('./',self.location.href),shellURL=new URL('./index.html',scope).href;
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll([scope.href,shellURL]))));
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{if(e.request.mode==='navigate')e.respondWith(caches.open(CACHE).then(c=>c.match(shellURL)))});`;
const server=http.createServer((req,res)=>{
 const pathname=new URL(req.url,'http://localhost').pathname;
 // Match Cloudflare Pages' canonical redirect, absent from a plain file server.
 if(pathname.endsWith('/index.html')){res.writeHead(308,{Location:pathname.slice(0,-10)});return res.end();}
 const name=pathname.endsWith('/')?'index.html':path.basename(pathname);
 if(legacyWorker && name==='sw.js'){res.writeHead(200,{'Content-Type':'application/javascript','Cache-Control':'no-store'});return res.end(legacySW);}
 if(failAsset && name==='favicon.svg'){res.writeHead(503);return res.end('simulated outage');}
 const types={html:'text/html',js:'application/javascript',webmanifest:'application/manifest+json',svg:'image/svg+xml',png:'image/png'};
 try{let body=fs.readFileSync(path.join(root,name));if(name==='sw.js')body=Buffer.from(body.toString().replace("const CACHE = 'poop-tracker-v3-2026.10.02-release1'",`const CACHE = 'poop-tracker-v3-2026.10.02-release1-test-${swGeneration}'`));
 res.writeHead(200,{'Content-Type':types[name.split('.').at(-1)]||'application/octet-stream','Cache-Control':'no-store'});res.end(body);
 }catch{res.writeHead(404);res.end();}
});
const results=[];
const corners=[{lat:36.00025,lng:-82},{lat:36.00025,lng:-81.9997},{lat:36,lng:-81.9997},{lat:36,lng:-82}].map(c=>({...c,acc:3,samples:8,capturedAt:1000,legacy:false}));
const empty=()=>({version:3,corners:[null,null,null,null],markers:[],settings:{snapGrid:false,manualYard:false}});
const seeded=()=>({...empty(),corners});
let base,browser;
async function run(name,fn){await fn();results.push(name);console.log('PASS',name);}
async function context(seed,options={}){
 const ctx=await browser.newContext({viewport:{width:390,height:844},serviceWorkers:'block',...options});
 await ctx.addInitScript(({seed})=>{
  if(seed && !sessionStorage.getItem('seeded')){for(const [k,v]of Object.entries(seed))localStorage.setItem(k,typeof v==='string'?v:JSON.stringify(v));sessionStorage.setItem('seeded','yes');}
  window.__geo={ok:null,error:null};
  Object.defineProperty(navigator,'geolocation',{value:{watchPosition(ok,error){window.__geo.ok=ok;window.__geo.error=error;return 1},clearWatch(){}}});
 },{seed});
 const p=await ctx.newPage();p.errors=[];p.on('pageerror',e=>p.errors.push(e.message));
 await p.goto(base);return {ctx,p};
}
async function state(p){return p.evaluate(()=>JSON.parse(JSON.stringify(window.PT.getState())))}
async function samples(p,lat=36.00012,lng=-81.99985,acc=3,age=0){await p.evaluate(({lat,lng,acc,age})=>{window.PT.clearSamples();for(let i=0;i<4;i++)window.PT.injectSample(lat,lng,acc,Date.now()-age-i*600)},{lat,lng,acc,age})}
async function point(p,u,v){return p.locator('#yard-svg').evaluate((el,{u,v})=>{const pt=el.createSVGPoint();pt.x=22+u*296;pt.y=22+v*376;const q=pt.matrixTransform(el.getScreenCTM());return {x:q.x,y:q.y}},{u,v})}
async function clickPoint(p,u,v){const q=await point(p,u,v);await p.mouse.click(q.x,q.y)}
async function importData(p,data){if(!await p.locator('#data-panel').isVisible())await p.locator('#btn-data').click();await p.locator('#import-file').setInputFiles({name:'backup.json',mimeType:'application/json',buffer:Buffer.from(typeof data==='string'?data:JSON.stringify(data))});}
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));base=`http://127.0.0.1:${server.address().port}/tools/dog-poop-tracker/`;
 browser=await chromium.launch({headless:true});
 await run('first use without GPS: setup, manual placement, correction, cleanup, undo and persistence',async()=>{
  const {ctx,p}=await context();assert.equal(await p.evaluate(()=>window.__geo.ok),null);
  await p.screenshot({path:path.join(out,'after-first-use-phone.png')});
  await p.locator('#simple-map-btn').click();await clickPoint(p,.3,.3);await p.locator('#tap-add').click();
  assert.equal((await state(p)).markers.length,1);assert.ok(Math.abs((await state(p)).markers[0].u-.3)<.01);
  await p.locator('#ma-right').click();assert.ok((await state(p)).markers[0].u>.31);
  // Repeated selection must not accidentally clean the spot.
  await clickPoint(p,.32,.3);assert.equal((await state(p)).markers[0].cleaned,false);
  // Drag selected marker; physical screen conversion also tests SVG letterboxing.
  const start=await point(p,.32,.3),end=await point(p,.6,.45);await p.mouse.move(start.x,start.y);await p.mouse.down();await p.mouse.move(end.x,end.y,{steps:8});await p.mouse.up();
  assert.ok(Math.abs((await state(p)).markers[0].u-.6)<.02);
  await p.locator('#ma-clean').click();assert.equal((await state(p)).markers[0].cleaned,true);
  await p.locator('#undo-btn').click();assert.equal((await state(p)).markers[0].cleaned,false);
  await p.reload();assert.equal((await state(p)).markers.length,1);assert.ok(Math.abs((await state(p)).markers[0].u-.6)<.02);
  await p.locator('#manual-btn').click();await p.locator('#yard-svg').press('ArrowLeft');await p.locator('#yard-svg').press('Enter');assert.equal((await state(p)).markers.length,2);
  assert.deepEqual(p.errors,[]);await ctx.close();
 });
 await run('GPS denied, weak, stale and outside yard use manual fallback; fresh fix marks',async()=>{
  const {ctx,p}=await context({poop_tracker_v3:seeded()});
  await samples(p);assert.match(await p.locator('#mark-sub').innerText(),/Use GPS estimate/);
  await p.evaluate(()=>window.__geo.error({code:1}));assert.match(await p.locator('#gps-value').innerText(),/blocked/);
  await p.locator('#mark-btn').click();assert.equal((await state(p)).markers.length,0);assert.equal(await p.locator('#tap-confirm').isVisible(),true);await p.locator('#tap-cancel').click();
  await samples(p,36.00012,-81.99985,25);assert.match(await p.locator('#mark-sub').innerText(),/Choose/);
  await samples(p,36.00012,-81.99985,3,8000);assert.match(await p.locator('#mark-sub').innerText(),/Choose/);
  await samples(p,36.002,-82.002);assert.equal(await p.locator('#yard-badge').isVisible(),true);await p.locator('#mark-btn').click();assert.equal((await state(p)).markers.length,0);await p.locator('#tap-cancel').click();
  await samples(p);await p.locator('#mark-btn').click();assert.equal((await state(p)).markers[0].source,'gps');
  await p.locator('#ma-done').click();await samples(p);await p.evaluate(()=>window.PT.injectSample(36.00012,-81.99985,100));assert.match(await p.locator('#mark-sub').innerText(),/Choose/);
  assert.deepEqual(p.errors,[]);await ctx.close();
 });
 await run('four hold-still captures, weak-corner decision and redo preserve markers',async()=>{
  const {ctx,p}=await context();await p.clock.install();await p.locator('#placeholder-cal-btn').click();
  for(let i=0;i<4;i++){
   await samples(p,corners[i].lat,corners[i].lng,3);await p.locator('#cap-btn').click();
   for(let j=0;j<10;j++){await p.clock.runFor(650);await p.evaluate(c=>window.PT.injectSample(c.lat,c.lng,3),corners[i]);}
   assert.ok((await state(p)).corners[i]);
  }
  assert.equal(await p.locator('#cal-success').isVisible(),true);await p.locator('#cal-done-btn').click();
  await p.locator('#manual-btn').click();await p.locator('#tap-add').click();await p.locator('#ma-done').click();
  await p.locator('#btn-calibrate').click();await p.locator('#cal-c0').click();await samples(p,corners[0].lat,corners[0].lng,20);await p.locator('#cap-btn').click();
  for(let j=0;j<16;j++){await p.clock.runFor(650);await p.evaluate(c=>window.PT.injectSample(c.lat,c.lng,20),corners[0]);}
  assert.equal(await p.locator('#cap-save-anyway').isVisible(),true);await p.locator('#cap-save-anyway').click();assert.ok((await state(p)).corners[0].acc>=19);assert.equal((await state(p)).markers.length,1);
  assert.deepEqual(p.errors,[]);await ctx.close();
 });
 await run('strict imports, cancellation, round-trip export, recovery and settings',async()=>{
  const initial=seeded();initial.markers=[{id:'keep',lat:36.0001,lng:-81.9999,u:.5,v:.5,acc:3,cleaned:false,source:'gps',adjusted:false,createdAt:1000,updatedAt:1000}];
  const {ctx,p}=await context({poop_tracker_v3:initial});const before=await p.evaluate(()=>localStorage.getItem('poop_tracker_v3'));
  for(const bad of ['{',{}, {...initial,version:99}, {...initial,markers:[{...initial.markers[0],lat:999}]}]){await importData(p,bad);await p.waitForFunction(()=>document.getElementById('data-status').textContent.includes('Import failed'));assert.equal(await p.evaluate(()=>localStorage.getItem('poop_tracker_v3')),before);}
  const incoming=seeded();incoming.settings.snapGrid=true;
  p.once('dialog',d=>d.dismiss());await importData(p,incoming);await p.waitForTimeout(100);assert.equal(await p.evaluate(()=>localStorage.getItem('poop_tracker_v3')),before);
  p.once('dialog',d=>d.accept());await importData(p,incoming);await p.waitForFunction(()=>document.getElementById('data-status').textContent.includes('Import complete'));
  assert.equal(await p.locator('#snap-toggle').isChecked(),true);assert.equal(await p.evaluate(()=>localStorage.getItem('poop_tracker_v3_before_import')),before);
  const downloadPromise=p.waitForEvent('download');await p.locator('#export-btn').click();const download=await downloadPromise;const exported=JSON.parse(fs.readFileSync(await download.path(),'utf8'));assert.equal(exported.app,'dog-poop-tracker');assert.deepEqual(exported.state,await state(p));
  const recoveryPromise=p.waitForEvent('download');await p.locator('#recovery-btn').click();assert.equal(fs.readFileSync(await (await recoveryPromise).path(),'utf8'),before);
  assert.deepEqual(p.errors,[]);await ctx.close();
 });
 await run('v2 migration retains original key; corrupt v3 is not overwritten',async()=>{
  const legacy={corners:corners.slice(0,2),markers:[{id:1700000000000,lat:36,lng:-82,cleaned:true}]};
  let {ctx,p}=await context({poop_tracker_v2:legacy});assert.equal((await state(p)).markers[0].source,'legacy');assert.deepEqual(JSON.parse(await p.evaluate(()=>localStorage.getItem('poop_tracker_v2'))),legacy);await ctx.close();
  ({ctx,p}=await context({poop_tracker_v3:'{bad'}));assert.equal(await p.locator('#storage-warning').isVisible(),true);await p.locator('#simple-map-btn').click();assert.equal(await p.evaluate(()=>localStorage.getItem('poop_tracker_v3')),'{bad');assert.deepEqual(p.errors,[]);await ctx.close();
 });
 await run('write failures and cross-tab conflicts are visible and do not replace saved data',async()=>{
  const {ctx,p}=await context();await p.locator('#simple-map-btn').click();const before=await p.evaluate(()=>localStorage.getItem('poop_tracker_v3'));
  await p.evaluate(()=>{Storage.prototype.setItem=function(){throw new DOMException('full','QuotaExceededError')}});
  await p.locator('#manual-btn').click();await p.locator('#tap-add').click();assert.match(await p.locator('#storage-warning').innerText(),/NOT saved/);assert.equal(await p.evaluate(()=>localStorage.getItem('poop_tracker_v3')),before);
  await p.reload();await p.evaluate(()=>localStorage.setItem('poop_tracker_v3',JSON.stringify({...window.PT.getState(),settings:{snapGrid:true,manualYard:true}})));await p.locator('#manual-btn').click();await p.locator('#tap-add').click();assert.match(await p.locator('#storage-warning').innerText(),/another tab/);assert.equal(JSON.parse(await p.evaluate(()=>localStorage.getItem('poop_tracker_v3'))).markers.length,0);await ctx.close();
 });
 await run('phone and desktop light/dark layouts, keyboard, contrast and screenshots',async()=>{
  const demo=seeded();demo.markers=[[.25,.3],[.7,.5],[.45,.75]].map(([u,v],i)=>({id:String(i),lat:null,lng:null,u,v,acc:null,cleaned:false,createdAt:1790942400000+i*60000,updatedAt:1790942400000,source:'manual',adjusted:false}));
  for(const [name,width,height]of [['phone',390,844],['small-phone',320,667],['desktop',1365,900]])for(const theme of ['light','dark']){
   const {ctx,p}=await context({poop_tracker_v3:demo,theme},{viewport:{width,height}});await samples(p);
   assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
   const sizes=await p.locator('#mark-btn, #manual-btn, #btn-calibrate, #btn-data, #themeToggle').evaluateAll(els=>els.map(e=>e.getBoundingClientRect().height));assert.ok(sizes.every(h=>h>=44));
   const contrast=await p.evaluate(()=>{
    const css=getComputedStyle(document.documentElement);
    const lum=key=>{const hex=css.getPropertyValue(key).trim().replace('#','');const rgb=[0,2,4].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722};
    return [['--text','--bg'],['--text-muted','--surface'],['--accent-dark','--accent'],['--marker-dirty','--grass'],['--grass-border','--grass']].map(([a,b])=>(Math.max(lum(a),lum(b))+.05)/(Math.min(lum(a),lum(b))+.05));
   });assert.ok(contrast.every(r=>r>=4.5),`Text contrast ratios: ${contrast}`);
   await p.screenshot({path:path.join(out,`after-${name}-${theme}.png`)});
   await p.locator('.marker-info').first().click();await p.locator('#ma-clean').focus();await p.keyboard.press('Enter');assert.equal((await state(p)).markers.filter(m=>m.cleaned).length,1);
   assert.deepEqual(p.errors,[]);await ctx.close();
  }
 });
 await run('Cloudflare redirect: repair the prior cached shell before explicit update activation',async()=>{
  legacyWorker=true;
  const {ctx,p}=await context(null,{serviceWorkers:'allow'});await p.evaluate(()=>navigator.serviceWorker.ready);await p.waitForFunction(()=>!!navigator.serviceWorker.controller);
  await p.locator('#simple-map-btn').click();await p.locator('#manual-btn').click();await p.locator('#tap-add').click();await p.locator('#ma-done').click();
  const redirected=()=>p.evaluate(async()=>{const c=await caches.open('poop-tracker-v3-2026.10.02-review2');return (await c.match(new URL('./index.html',location.href).href)).redirected});
  assert.equal(await redirected(),true);
  legacyWorker=false;await p.evaluate(async()=>{const r=await navigator.serviceWorker.getRegistration();await r.update()});await p.locator('#update-btn').waitFor({state:'visible'});
  assert.equal(await redirected(),false); // The old active worker can reload while the new worker waits.
  await p.reload();assert.equal((await state(p)).markers.length,1);
  await p.locator('#update-btn').click();await p.waitForFunction(()=>document.getElementById('update-notice').hidden);
  await ctx.setOffline(true);await p.reload();assert.equal((await state(p)).markers.length,1);
  assert.deepEqual(p.errors,[]);await ctx.close();
 });
 await run('offline reload, scoped cache cleanup, update activation and failed install recovery',async()=>{
  const {ctx,p}=await context(null,{serviceWorkers:'allow'});await p.evaluate(()=>navigator.serviceWorker.ready);await p.waitForFunction(()=>!!navigator.serviceWorker.controller);
  await p.locator('#simple-map-btn').click();await p.locator('#manual-btn').click();await p.locator('#tap-add').click();await p.locator('#ma-done').click();
  await p.evaluate(()=>caches.open('another-south-fork-app').then(c=>c.put('/sentinel',new Response('keep'))));
  await ctx.setOffline(true);await p.goto(base+'?offline=1');assert.equal((await state(p)).markers.length,1);await p.locator('#manual-btn').click();await p.locator('#tap-add').click();assert.equal((await state(p)).markers.length,2);await p.locator('#ma-done').click();
  await ctx.setOffline(false);swGeneration++;
  await p.evaluate(async()=>{const r=await navigator.serviceWorker.getRegistration();await r.update()});await p.locator('#update-btn').waitFor({state:'visible'});
  await p.locator('#update-btn').click();await p.waitForFunction(()=>document.getElementById('update-notice').hidden);assert.equal((await state(p)).markers.length,2);
  assert.ok((await p.evaluate(()=>caches.keys())).includes('another-south-fork-app'));assert.ok(!(await p.evaluate(()=>caches.keys())).includes('poop-tracker-v3-2026.10.02-release1-test-0'));
  failAsset=true;swGeneration++;
  await p.evaluate(async()=>{const r=await navigator.serviceWorker.getRegistration();await r.update();await new Promise(resolve=>{if(!r.installing)return resolve();const w=r.installing;w.addEventListener('statechange',()=>{if(w.state==='redundant')resolve()})})});
  await ctx.setOffline(true);await p.reload();assert.equal((await state(p)).markers.length,2);assert.equal(await p.locator('#update-notice').isVisible(),false);failAsset=false;
  assert.deepEqual(p.errors,[]);await ctx.close();
 });
 // WebKit is an additional engine check, not a substitute for iPhone hardware.
 try{const wk=await webkit.launch({headless:true});await browser.close();browser=wk;await run('WebKit manual flow and reload',async()=>{const {ctx,p}=await context();await p.locator('#simple-map-btn').click();await p.locator('#manual-btn').click();await p.locator('#tap-add').click();await p.reload();assert.equal((await state(p)).markers.length,1);assert.deepEqual(p.errors,[]);await ctx.close()})}catch(e){if(/Executable doesn't exist/.test(e.message))results.push('WebKit unavailable: browser binary not installed');else throw e;}
 fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify(results,null,2));
})().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close();server.close()});
