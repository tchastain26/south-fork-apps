const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const html = fs.readFileSync('tools/dog-poop-tracker/index.html','utf8');
const sandbox={module:{exports:{}}};
vm.runInNewContext(html.match(/<script id="pt-core">([\s\S]*?)<\/script>/)[1],sandbox);
const C=sandbox.module.exports;
const origin={lat:36,lng:-82};
const corners=[[0,25],[20,25],[20,0],[0,0]].map(([x,y])=>({...C.fromLocal(x,y,origin),acc:3,samples:8,capturedAt:1000,legacy:false}));
const yard=C.makeYard(corners);
const sample=(x,y,t=10000,acc=4)=>({...C.fromLocal(x,y,origin),t,acc});
const state=()=>({...C.emptyState(),corners});
test('rotated and skewed quadrilaterals round trip at corners and interior',()=>{
 for(const points of [[[0,25],[20,25],[20,0],[0,0]],[[0,20],[20,30],[30,0],[10,-10]],[[0,20],[15,22],[20,0],[0,0]]]){
  const y=C.makeYard(points.map(([x,y])=>C.fromLocal(x,y,origin)));assert.equal(y.valid,true);
  for(const [u,v]of [[0,0],[1,0],[1,1],[0,1],[.2,.8],[.5,.5]]){const ll=C.latLngFromUV(y,u,v),uv=C.uvFromLatLng(y,ll.lat,ll.lng);assert.ok(Math.abs(uv.u-u)<1e-7);assert.ok(Math.abs(uv.v-v)<1e-7);}
 }
});
test('rejects line, crossing, near duplicate and invalid coordinate yards',()=>{
 for(const pts of [[[0,0],[10,0],[20,0],[30,0]],[[0,0],[20,20],[0,20],[20,0]],[[0,0],[1,0],[20,20],[0,20]]])assert.equal(C.makeYard(pts.map(([x,y])=>C.fromLocal(x,y,origin))).valid,false);
 assert.equal(C.makeYard([{lat:95,lng:0},...corners.slice(1)]).valid,false);
});
test('outside positions stay outside instead of being silently clamped',()=>{const p=C.latLngFromUV(yard,1.5,.5);assert.equal(C.uvFromLatLng(yard,p.lat,p.lng).inside,false)});
test('old, future, duplicate and invalid samples cannot produce a usable fix',()=>{
 for(const samples of [[sample(0,0,1)],[sample(0,0,12000)],[sample(0,0,10000,100)],[{lat:95,lng:0,t:10000,acc:3}]])assert.equal(C.computeFix(samples,10000).ok,false);
 assert.equal(C.computeFix([sample(0,0),sample(0,0)],10000).grade,'acquiring');
});
test('robust median rejects an outlier even if it claims much better accuracy',()=>{
 const samples=[0,.1,-.1,.2].map((x,i)=>sample(x,0,10000-i*100,5));samples.push(sample(100,100,9950,1));
 const f=C.computeFix(samples,10000);assert.equal(f.rejected,1);assert.ok(Math.hypot(C.toLocal(f.lat,f.lng,origin).x,C.toLocal(f.lat,f.lng,origin).y)<1);assert.ok(f.accuracy>=5);
});
test('repeated fixes do not claim improved device confidence',()=>{const f=C.computeFix([0,1,2,3].map(i=>sample(0,0,10000-i*500,12)),10000);assert.ok(Math.abs(f.accuracy-12)<1e-9);assert.equal(f.grade,'poor');});
test('short window drops previous location after walking and keeps stale age honest',()=>{const f=C.computeFix([sample(0,0,1000),sample(20,0,9800),sample(20,0,9900)],10000);assert.equal(f.sampleCount,2);assert.equal(f.ageMs,100);assert.ok(Math.abs(C.toLocal(f.lat,f.lng,origin).x-20)<.01)});
test('uncertainty geometry uses both axes and does not cap large radii',()=>{const a=C.uncertaintyEllipse(yard,.5,.5,100);assert.ok(Math.max(a.rx,a.ry)>1000);assert.ok(a.rx!==a.ry);});
test('v2 complete, empty and partial yards migrate without losing markers',()=>{
 for(const cs of [[],corners.slice(0,2),corners]){const m=C.parseBackup({corners:cs,markers:[{id:1700000000000,lat:36,lng:-82,cleaned:true}]});assert.equal(m.version,3);assert.equal(m.markers.length,1);assert.equal(m.markers[0].source,'legacy');assert.equal(m.markers[0].acc,null);assert.equal(m.corners.filter(Boolean).length,cs.length);}
});
test('v3 backup round trip retains manual settings, adjustments, accuracy and dates',()=>{
 const s=state();s.settings.snapGrid=true;s.settings.manualYard=true;s.markers.push({id:'a',lat:36,lng:-82,u:.2,v:.3,acc:8,cleaned:true,createdAt:1000,updatedAt:2000,source:'gps',adjusted:true});
 assert.equal(JSON.stringify(C.parseBackup({app:'dog-poop-tracker',schema:3,state:s})),JSON.stringify(s));
});
test('malformed, unrelated and unsupported backups are refused',()=>{
 for(const raw of [{},[],null,{version:4,corners,markers:[]},{state:state(),app:'other',schema:3},{...state(),settings:{snapGrid:'false'}},{...state(),corners:[null]}])assert.throws(()=>C.parseBackup(raw));
});
test('invalid marker data cannot be dropped silently during import',()=>{
 const marker={id:'a',lat:36,lng:-82,u:.5,v:.5,acc:4,cleaned:false,source:'gps'};
 for(const changes of [{lat:100},{lng:200},{acc:-1},{cleaned:'false'},{source:'bad'},{createdAt:1e25},{source:'manual',u:5},{id:''}])assert.throws(()=>C.parseBackup({...state(),markers:[{...marker,...changes}]}));
 assert.throws(()=>C.parseBackup({...state(),markers:[marker,marker]}));
});
