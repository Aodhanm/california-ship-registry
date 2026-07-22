#!/usr/bin/env python3
"""Generate the self-contained index.html viewer from data/*.csv.
Single-file pattern (the calendar's): all data embedded as JSON; Leaflet from
CDN for the map. Regenerate after any data change: python3 scripts/build_site.py
"""
import csv, json, os, html, subprocess, sys
g = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'check.py')])
if g.returncode != 0:
    sys.exit('GUARDS FAILED — index.html NOT rebuilt')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

visits = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'visits.csv'))))
ships = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'ships.csv'))))
gaz = {r['anchorage']: (float(r['lat']), float(r['lon']))
       for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'gazetteer.csv')))}

for v in visits:
    v['n_records'] = int(v['n_records'])
    v['citations'] = json.loads(v['citations'])

page = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>California Ship Registry, 1769–1846 (v0.2 draft)</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cg fill='none' stroke='%231f3a5f' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='16' cy='6' r='2.6'/%3E%3Cline x1='16' y1='9' x2='16' y2='27'/%3E%3Cline x1='10' y1='13' x2='22' y2='13'/%3E%3Cpath d='M6 19 a10 10 0 0 0 20 0'/%3E%3Cline x1='6' y1='19' x2='3.5' y2='16.5'/%3E%3Cline x1='6' y1='19' x2='8.5' y2='16.5'/%3E%3Cline x1='26' y1='19' x2='23.5' y2='16.5'/%3E%3Cline x1='26' y1='19' x2='28.5' y2='16.5'/%3E%3C/g%3E%3C/svg%3E">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
 body{font-family:Georgia,serif;margin:0;background:#f7f4ee;color:#222}
 header{background:#1f3a5f;color:#f7f4ee;padding:14px 22px}
 header h1{margin:0;font-size:1.35em;font-weight:normal}
 header .sub{font-size:.85em;opacity:.85}
 .banner{background:#b7791f;color:#fff;padding:6px 22px;font-size:.85em}
 nav{background:#2d4a73;padding:0 22px}
 nav button{background:none;border:none;color:#dce6f2;padding:10px 14px;cursor:pointer;font-size:.95em;font-family:inherit}
 nav button.on{background:#f7f4ee;color:#1f3a5f;border-radius:4px 4px 0 0}
 main{padding:16px 22px;max-width:1200px;margin:0 auto}
 .filters{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px;align-items:center}
 .filters input,.filters select{font-family:inherit;font-size:.9em;padding:5px 7px;border:1px solid #bbb;border-radius:4px;background:#fff}
 table{border-collapse:collapse;width:100%;font-size:.85em;background:#fff}
 th{background:#e8e2d4;text-align:left;padding:6px 8px;position:sticky;top:0;cursor:pointer}
 td{padding:6px 8px;border-top:1px solid #eee;vertical-align:top}
 tr:hover td{background:#fbf7ec}
 .vid{color:#888;font-size:.85em;white-space:nowrap}
 .draft{color:#b7791f;font-size:.78em}
 tr.st-draft td:first-child{border-left:3px solid #d9a84a}
 tr.st-reviewed td:first-child{border-left:3px solid #6a9fb5}
 tr.st-verified td:first-child{border-left:3px solid #2e8b57}
 .spark{height:16px;vertical-align:middle}
 .flag{font-variant:small-caps}
 .cite a{color:#1f5f8b;text-decoration:none;font-size:.85em}
 .count{margin:8px 0;color:#555;font-size:.85em}
 #map{height:560px;border:1px solid #ccc;border-radius:4px}
 .pane{display:none}.pane.on{display:block}
 .about{max-width:760px;line-height:1.55;font-size:.95em}
 .chartbar{fill:#2d4a73}
</style></head><body>
<header><h1>California Ship Registry, 1769&ndash;1846</h1>
<div class="sub">A registry of documented vessel visits to the Californias &middot; companion to the <i>Archives of California</i> calendar</div></header>
<div class="banner">v0.2 DRAFT (live for review) &mdash; machine-seeded from the C-A calendar + first curated expedition rows; most rows status=draft; Bancroft/Ogden/Russian source families pending (see About &amp; method)</div>
<nav>
 <button data-pane="visits" class="on">Visits (chronological)</button>
 <button data-pane="ships">Ships</button>
 <button data-pane="mappane">Map</button>
 <button data-pane="curve">Traffic curve</button>
 <button data-pane="copres">In port together</button>
 <button data-pane="about">About &amp; method</button>
</nav>
<main>
<div id="visits" class="pane on">
 <div class="filters">
  <input id="q" placeholder="search ship / text&hellip;" size="24">
  <select id="fFlag"><option value="">flag: all</option></select>
  <select id="fPurpose"><option value="">purpose: all</option></select>
  <select id="fOutcome"><option value="">outcome: all</option></select>
  <select id="fAnch"><option value="">anchorage: all</option></select>
  <input id="y1" placeholder="from yr" size="6" value="1767"><input id="y2" placeholder="to yr" size="6" value="1846">
 </div>
 <div class="count" id="count"></div>
 <table id="tbl"><thead><tr>
  <th>id</th><th>date</th><th>ship</th><th>flag</th><th>anchorage</th>
  <th>purpose</th><th>outcome</th><th>evidence</th></tr></thead>
 <tbody></tbody></table>
</div>
<div id="ships" class="pane">
 <div class="count" id="scount"></div>
 <table id="stbl"><thead><tr><th>ship</th><th>name variants (as written)</th><th>flag</th><th>seen</th><th>visits</th></tr></thead><tbody></tbody></table>
</div>
<div id="mappane" class="pane">
 <div class="filters"><select id="mapPurpose"><option value="">all purposes</option><option value="exploration">exploration only</option><option value="otter">otter</option><option value="supply">supply</option><option value="contraband">contraband</option><option value="warship">warship</option></select>
 <span class="count">circle size = documented visits at that anchorage (filtered)</span></div>
 <div id="map"></div>
</div>
<div id="curve" class="pane"><svg id="svg"></svg>
 <div class="count">Documented ship events per year by flag hint. Click a bar to open that year's visits. Dashed lines mark reference events. Draft data: this measures the archive's coverage as much as the traffic &mdash; the Bancroft and Ogden layers (v0.2&ndash;0.3) will begin to separate the two.</div></div>
<div id="copres" class="pane">
 <div class="filters"><select id="cpAnch"></select>
  <input id="cpY1" placeholder="from" size="6" value="1767"><input id="cpY2" placeholder="to" size="6" value="1846">
  <label style="font-size:.85em"><input type="checkbox" id="cpMulti" checked> only years with 2+ vessels (the encounters)</label></div>
 <div class="count">Vessels documented at the same anchorage in the same year &mdash; where encounters live. Year-level precision at this draft stage; the review pass will tighten to same-week where dates allow.</div>
 <div id="cpOut"></div>
</div>
<div id="about" class="pane about">
 <h2>About</h2>
 <p>The first machine-readable registry of documented vessel visits to the Californias, 1769&ndash;1846.
 Unit of record: the <b>visit</b> &mdash; one vessel, one anchorage, one time &mdash; each row carrying its evidence
 (currently: leaf-verified records of the Savage transcripts via the <a href="https://aodhanm.github.io/archives-of-california">Archives of California</a> calendar,
 with links to the manuscript scans). Fields and vocabularies: see CODEBOOK.md in this repository.</p>
 <p><b>v0.1 status.</b> Seeded from the calendar alone by a documented harvester. Every row is <i>draft</i>.
 Pending source families, in order: Bancroft's <i>History of California</i> narrative (1769&ndash;1824 &mdash; never before consolidated),
 Ogden&rsquo;s 1941 otter-trade appendix + Archer 1973, the Russian record (Gibson&ndash;Istomin, Khlebnikov, Tikhmenev, Ivashintsov),
 Howay and Cook cross-checks. Completeness is claimed for Alta California only; Baja rows are incidental after the 1804 division of the provinces.</p>
 <p><b>Absence of a row is not absence of a ship</b> &mdash; contraband was under-recorded by design; the asymmetry is a finding, not a flaw.</p>
</div>
</main>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const V=__VISITS__;const S=__SHIPS__;const G=__GAZ__;
const FLAGEMO={spain:'🇪🇸',usa:'🇺🇸',russia:'🇷🇺',britain:'🇬🇧',mexico:'🇲🇽',france:'🇫🇷',chile:'🇨🇱',peru:'🇵🇪',ecuador:'🇪🇨'};
function femo(f){return FLAGEMO[f]?FLAGEMO[f]+' ':''}
function opts(sel,vals){const s=document.getElementById(sel);[...new Set(vals)].filter(x=>x).sort().forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;s.appendChild(o)})}
opts('fFlag',V.map(v=>v.flag));opts('fAnch',V.map(v=>v.anchorage));
opts('fPurpose',V.flatMap(v=>v.purpose.split('|')));opts('fOutcome',V.flatMap(v=>v.outcome.split('|')));
function yr(v){return parseInt((v.date_from||'').slice(0,4))||null}
function render(){
 const q=document.getElementById('q').value.toLowerCase(),
 fF=document.getElementById('fFlag').value,fP=document.getElementById('fPurpose').value,
 fO=document.getElementById('fOutcome').value,fA=document.getElementById('fAnch').value,
 y1=parseInt(document.getElementById('y1').value)||0,y2=parseInt(document.getElementById('y2').value)||9999;
 const rows=V.filter(v=>{
  if(q&&!(v.ship_id+' '+v.name_as_written+' '+v.excerpt).toLowerCase().includes(q))return false;
  if(fF&&v.flag!==fF)return false;if(fA&&v.anchorage!==fA)return false;
  if(fP&&!v.purpose.split('|').includes(fP))return false;
  if(fO&&!v.outcome.split('|').includes(fO))return false;
  const y=yr(v);if(y&&(y<y1||y>y2))return false;if(!y&&(y1>0||y2<9999))return false;
  return true});
 document.getElementById('count').textContent=rows.length+' visits ('+rows.filter(r=>r.ship_id!=='(unnamed vessel)').length+' named)';
 const tb=document.querySelector('#tbl tbody');tb.innerHTML='';
 rows.slice(0,800).forEach(v=>{
  const tr=document.createElement('tr');tr.className='st-'+v.status;
  const cites=v.citations.map(c=>c.url?'<a href="'+c.url+'" target="_blank">C-A '+c.ca+' d'+c.doc+'</a>':(c.type+' '+(c.ref||''))).join(' · ');
  tr.innerHTML='<td class="vid">'+v.visit_id+' <span class="draft">'+v.status+'</span></td>'+
   '<td>'+(v.date_from||'—')+(v.date_to&&v.date_to!==v.date_from?'&nbsp;–&nbsp;'+v.date_to:'')+'</td>'+
   '<td><b>'+(v.ship_id==='(unnamed vessel)'?'<i>(unnamed)</i>':v.ship_id)+'</b>'+(v.name_as_written?'<br><span style="color:#777;font-size:.85em">as written: '+v.name_as_written+'</span>':'')+'</td>'+
   '<td class="flag">'+femo(v.flag)+(v.flag||'')+(v.flag_basis&&v.flag_basis!=='stated'&&v.flag?'<span style="color:#999" title="flag by hand adjudication (attested/inferred) — see codebook">†</span>':'')+'</td><td>'+(v.anchorage||'')+'</td>'+
   '<td>'+v.purpose.replace(/\\|/g,', ')+'</td><td>'+v.outcome.replace(/\\|/g,', ')+'</td>'+
   '<td class="cite">'+cites+'<br><span style="color:#888;font-size:.82em">'+v.excerpt+'</span></td>';
  tb.appendChild(tr)});
}
['q','fFlag','fPurpose','fOutcome','fAnch','y1','y2'].forEach(id=>document.getElementById(id).addEventListener('input',render));
render();
// ships
const yrsOf={};V.forEach(v=>{const y=yr(v);if(y&&v.ship_id)(yrsOf[v.ship_id]=yrsOf[v.ship_id]||[]).push(y)});
function spark(id){const ys=yrsOf[id];if(!ys)return'';
 const c={};ys.forEach(y=>c[y]=(c[y]||0)+1);const mx=Math.max(...Object.values(c));
 let o='<svg class="spark" width="160" height="16">';
 for(let y=1769;y<=1848;y++){if(c[y])o+='<rect x="'+((y-1769)*2)+'" y="'+(16-c[y]/mx*14)+'" width="1.6" height="'+(c[y]/mx*14)+'" fill="#2d4a73"/>'}
 return o+'</svg>'}
const stb=document.querySelector('#stbl tbody');
S.forEach(s=>{const tr=document.createElement('tr');
 tr.innerHTML='<td><b>'+s.ship_id+'</b></td><td>'+s.name_variants+'</td><td class="flag">'+femo(s.flag_guess)+(s.flag_guess||'')+'</td><td>'+(s.first_seen||'')+(s.last_seen&&s.last_seen!==s.first_seen?'–'+s.last_seen:'')+' '+spark(s.ship_id)+'</td><td>'+s.n_visits+'</td>';
 stb.appendChild(tr)});
document.getElementById('scount').textContent=S.length+' vessels (draft identities; variants preserved as written)';
// co-presence
(function(){
 const sel=document.getElementById('cpAnch');
 const anks=[...new Set(V.map(v=>v.anchorage).filter(x=>x))].sort();
 anks.forEach(a=>{const o=document.createElement('option');o.value=a;o.textContent=a;sel.appendChild(o)});
 sel.value='Monterey';
 function cp(){
  const a=sel.value,
   y1=parseInt(document.getElementById('cpY1').value)||1767,
   y2=parseInt(document.getElementById('cpY2').value)||1846,
   multi=document.getElementById('cpMulti').checked;
  const byYear={};
  V.forEach(v=>{const y=yr(v);
   if(v.anchorage!==a||!y||y<y1||y>y2)return;
   if(v.visit_type==='mention')return;
   (byYear[y]=byYear[y]||{});(byYear[y][v.ship_id]=byYear[y][v.ship_id]||[]).push(v)});
  const out=document.getElementById('cpOut');
  let html='',nYears=0,nEnc=0;
  Object.keys(byYear).sort().forEach(y=>{
   const byShip=byYear[y];
   const named=Object.keys(byShip).filter(k=>k!=='(unnamed vessel)');
   const isEnc=named.length>=2;
   if(multi&&!isEnc)return;
   nYears++;if(isEnc)nEnc++;
   html+='<div style="background:#fff;border:1px solid #e3ddce;border-radius:5px;padding:8px 12px;margin:8px 0'+(isEnc?';border-left:4px solid #1f3a5f':'')+'">'
    +'<b style="font-size:1.05em">'+y+'</b> — '+Object.keys(byShip).length+' vessels'+(isEnc?' <span style="color:#1f3a5f;font-size:.85em">⚓ encounter year</span>':'')
    +Object.keys(byShip).sort().map(sh=>'<p style="margin:5px 0"><b>'+(sh==='(unnamed vessel)'?'<i>(unnamed)</i>':sh)+'</b>'
      +(byShip[sh][0].flag?' <span class="flag">'+femo(byShip[sh][0].flag)+byShip[sh][0].flag+'</span>':'')
      +' — '+byShip[sh].map(v=>(v.date_from||'')+(v.outcome?' ('+v.outcome.split('|')[0]+')':'')).join('; ')
      +'<br><span style="color:#888;font-size:.85em">'+byShip[sh][0].excerpt+'</span></p>').join('')
    +'</div>'});
  out.innerHTML='<h3>'+a+', '+y1+'–'+y2+'</h3><div class="count">'+nYears+' years shown'+(multi?' (encounter years only — untick to see all)':' · '+nEnc+' encounter years')+'</div>'+
   (html||'<p style="color:#888">No matching years — widen the range or untick the encounters-only box.</p>');
 }
 ['cpY1','cpY2','cpMulti'].forEach(id=>document.getElementById(id).addEventListener('input',cp));
 sel.addEventListener('input',cp);cp();
})();
// tabs
document.querySelectorAll('nav button').forEach(b=>b.addEventListener('click',()=>{
 document.querySelectorAll('nav button').forEach(x=>x.classList.remove('on'));
 document.querySelectorAll('.pane').forEach(x=>x.classList.remove('on'));
 b.classList.add('on');document.getElementById(b.dataset.pane).classList.add('on');
 if(b.dataset.pane==='mappane'){if(!window._map)initMap();else setTimeout(()=>_map.invalidateSize(),50)}
}));
let _layer=null;
function drawMarkers(){
 if(_layer)_layer.remove();
 _layer=L.layerGroup().addTo(_map);
 const pf=document.getElementById('mapPurpose').value;
 const byA={};V.forEach(v=>{if(!v.anchorage||!G[v.anchorage])return;
  if(pf&&!v.purpose.split('|').includes(pf))return;
  (byA[v.anchorage]=byA[v.anchorage]||[]).push(v)});
 Object.entries(byA).forEach(([a,vs])=>{
  const[lat,lon]=G[a];
  const expl=vs.some(v=>v.purpose.split('|').includes('exploration'));
  L.circleMarker([lat,lon],{radius:4+Math.sqrt(vs.length)*2.2,color:pf==='exploration'?'#7a4a12':'#1f3a5f',fillColor:pf==='exploration'?'#b7791f':'#2d4a73',fillOpacity:.55})
   .bindPopup('<b>'+a+'</b><br>'+vs.length+' documented visits'+(pf?' ('+pf+')':'')+'<br>'+
     [...new Set(vs.map(v=>v.ship_id))].slice(0,14).join(', '))
   .addTo(_layer)});
}
// ── Historical period basemaps (David Rumsey / Allmaps georeferenced) ──
// TO ADD ONE: georeference the map (Rumsey Georeferencer -> "Get links" -> XYZ Link,
// or Allmaps editor), then paste its XYZ tile URL into `url` below. Entries whose
// url is still '' are silently skipped, so the map works before any are configured.
const HIST=[
 {name:"Duflot de Mofras, Côte de l'Amérique (1844)",
  url:"",  /* <- paste XYZ URL from davidrumsey.com/maps6332.html Georeferencer "Get links" */
  attribution:"Duflot de Mofras 1844 &middot; David Rumsey Map Collection", maxZoom:9},
 /* add more: Sutil y Mexicana 1802 coastal charts, per-port insets, etc. */
];
function initMap(){
 window._map=L.map('map').setView([34.5,-119.5],5);
 const osm=L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'&copy; OSM',maxZoom:18});
 const carto=L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{attribution:'&copy; OSM &copy; CARTO',subdomains:'abcd',maxZoom:19});
 osm.addTo(_map);
 const bases={'OpenStreetMap':osm,'Light (Carto)':carto};
 HIST.forEach(h=>{if(!h.url)return; bases[h.name]=L.tileLayer(h.url,{attribution:h.attribution,maxZoom:h.maxZoom||9});});
 L.control.layers(bases,null,{position:'topright'}).addTo(_map);
 // opacity slider — appears only when a historical base is selected
 let histActive=null;
 const op=L.control({position:'bottomright'});
 op.onAdd=function(){const d=L.DomUtil.create('div');d.style.cssText='background:#fff;padding:5px 8px;border:1px solid #ccc;border-radius:4px;font-size:11px;display:none';
  d.innerHTML='historical map opacity<br><input type="range" min="0" max="100" value="100" style="width:130px">';
  L.DomEvent.disableClickPropagation(d);
  d.querySelector('input').oninput=function(){if(histActive)histActive.setOpacity(this.value/100)};
  this._d=d;return d};
 op.addTo(_map);
 _map.on('baselayerchange',e=>{const isH=HIST.some(h=>h.name===e.name&&h.url);
  histActive=isH?e.layer:null; op._d.style.display=isH?'block':'none';
  if(isH){op._d.querySelector('input').value=100;e.layer.setOpacity(1);}});
 document.getElementById('mapPurpose').addEventListener('input',drawMarkers);
 drawMarkers();
}
// curve — full-width stacked bars, y-axis, annotations, click-to-filter
(function(){
 const byY={};V.forEach(v=>{const y=yr(v);if(!y||y<1769||y>1848)return;
  byY[y]=byY[y]||{};const f=v.flag||'unknown';byY[y][f]=(byY[y][f]||0)+1});
 const flags=['spain','usa','russia','britain','mexico','france','unknown'];
 const cols={spain:'#c0392b',usa:'#2d4a73',russia:'#1e7e34',britain:'#8e44ad',mexico:'#b7791f',france:'#16a085',unknown:'#a99'};
 const svg=document.getElementById('svg');const W=1140,H=520,mx=48,my=30,mb=46;
 svg.setAttribute('width',W);svg.setAttribute('height',H);
 let maxN=0;for(const y in byY){maxN=Math.max(maxN,Object.values(byY[y]).reduce((a,b)=>a+b,0))}
 const yrs=[];for(let y=1769;y<=1848;y++)yrs.push(y);
 const bw=(W-mx-10)/yrs.length, ph=H-my-mb;
 let out='';
 const step=maxN>40?10:5;
 for(let n=0;n<=maxN;n+=step){const gy=H-mb-n/maxN*ph;
  out+='<line x1="'+mx+'" y1="'+gy+'" x2="'+(W-8)+'" y2="'+gy+'" stroke="#ddd"/>'+
       '<text x="'+(mx-6)+'" y="'+(gy+4)+'" font-size="10" fill="#777" text-anchor="end">'+n+'</text>';}
 yrs.forEach((y,i)=>{let acc=0;const d=byY[y]||{};
  const tot=Object.values(d).reduce((a,b)=>a+b,0);
  flags.forEach(f=>{const n=d[f]||0;if(!n)return;
   const h=n/maxN*ph;
   out+='<rect class="yb" data-y="'+y+'" x="'+(mx+i*bw)+'" y="'+(H-mb-acc-h)+'" width="'+Math.max(bw-1.2,2)+'" height="'+h+'" fill="'+cols[f]+'" style="cursor:pointer"><title>'+y+' — '+f+': '+n+' (year total '+tot+')</title></rect>';acc+=h});
  if(y%5===0)out+='<text x="'+(mx+i*bw)+'" y="'+(H-mb+14)+'" font-size="10" fill="#555">'+y+'</text>';});
 const ann=[[1769,'Alta CA founded'],[1775,'Trinidad possession'],[1796,'the Otter — first US ship'],[1806,'Rezanov / the Juno'],[1812,'Ross founded'],[1813,'Mercury seized'],[1821,'Mexican independence'],[1834,'secularization'],[1846,'US conquest']];
 ann.forEach((a,k)=>{const y=a[0],label=a[1];const i=y-1769;const x=mx+i*bw;
  out+='<line x1="'+x+'" y1="'+my+'" x2="'+x+'" y2="'+(H-mb)+'" stroke="#999" stroke-dasharray="3,3"/>'+
       '<text x="'+(x+3)+'" y="'+(my+10+(k%3)*13)+'" font-size="9.5" fill="#666">'+label+'</text>';});
 let lx=mx;flags.forEach(f=>{out+='<rect x="'+lx+'" y="'+(H-16)+'" width="10" height="10" fill="'+cols[f]+'"/><text x="'+(lx+13)+'" y="'+(H-7)+'" font-size="11">'+f+'</text>';lx+=f.length*7+50;});
 svg.innerHTML=out;
 svg.addEventListener('click',e=>{const y=e.target.dataset&&e.target.dataset.y;if(!y)return;
  document.getElementById('y1').value=y;document.getElementById('y2').value=y;render();
  document.querySelectorAll('nav button').forEach(x=>x.classList.remove('on'));
  document.querySelectorAll('.pane').forEach(x=>x.classList.remove('on'));
  document.querySelector('nav button[data-pane=visits]').classList.add('on');
  document.getElementById('visits').classList.add('on');});
})();
</script></body></html>"""

page = page.replace('__VISITS__', json.dumps(visits, ensure_ascii=False, separators=(',', ':')))
page = page.replace('__SHIPS__', json.dumps(ships, ensure_ascii=False, separators=(',', ':')))
page = page.replace('__GAZ__', json.dumps(gaz, ensure_ascii=False, separators=(',', ':')))
open(os.path.join(ROOT, 'index.html'), 'w').write(page)
print(f"index.html written ({len(page)//1024} KB, {len(visits)} visits, {len(ships)} ships)")
