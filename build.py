import json, datetime, os
funds=json.load(open('data/funds.json'))
deals=json.load(open('data/deals.json'))
newsletters=json.load(open('data/newsletters.json')) if os.path.exists('data/newsletters.json') else {"pulled":"","sources":[],"editions":[],"deals_this_week":[]}
BUILD_DATE="August 11, 2026"

funds_js=json.dumps(funds, ensure_ascii=False)
deals_js=json.dumps(deals, ensure_ascii=False)
nl_js=json.dumps(newsletters, ensure_ascii=False)

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Gamma Waves · Sports Fund Deal Tracker</title>
<style>
:root{
  --bg:#f4f7fb; --bg2:#eef2f8; --panel:#ffffff; --panel2:#f3f6fb; --border:#e2e8f1;
  --text:#111a2b; --muted:#5c6a7c; --faint:#93a0b1; --ink2:#39465a;
  --accent:#2f4fc3; --accent-dim:#dbe4fb; --violet:#7b4fd0; --coral:#dc6050; --warm:#dc6050; --link:#2f4fc3;
  --brand:linear-gradient(90deg,#1F4FC3,#5653C7,#8A57BF,#B35B88,#DC6050);
  --shadow:0 1px 2px rgba(16,25,43,.06),0 8px 22px rgba(16,25,43,.08);
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1240px;margin:0 auto;padding:0 20px}
header.top{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.92);border-bottom:1px solid var(--border);backdrop-filter:blur(8px)}
.top .wrap{display:flex;align-items:center;gap:16px;padding:14px 20px}
.brand{display:flex;align-items:center;gap:11px;font-weight:700;font-size:16px;letter-spacing:.2px}
.brand .dot{width:22px;height:22px;border-radius:6px;background:linear-gradient(135deg,#1F4FC3,#8A57BF 55%,#DC6050);box-shadow:0 0 0 3px rgba(69,113,230,.15)}
.gradbar{height:3px;background:var(--brand)}
.brand small{display:block;font-weight:500;font-size:11px;color:var(--muted);letter-spacing:.3px}
.top .spacer{flex:1}
.updated{font-size:12px;color:var(--muted)}
.updated b{color:var(--text);font-weight:600}
.searchbox{position:relative}
.searchbox input{background:var(--panel);border:1px solid var(--border);color:var(--text);border-radius:9px;padding:9px 12px 9px 32px;width:250px;font-size:13px;outline:none}
.searchbox input:focus{border-color:var(--accent-dim)}
.searchbox svg{position:absolute;left:10px;top:9px;opacity:.5}
.tabs{display:flex;gap:4px;margin-left:6px}
.tab{padding:8px 14px;border-radius:9px;color:var(--muted);cursor:pointer;font-weight:600;font-size:13px;border:1px solid transparent}
.tab:hover{color:var(--text)}
.tab.active{background:var(--panel2);color:var(--text);border-color:var(--border)}

.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:22px 0 6px}
.stat{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:14px 16px}
.stat .n{font-size:26px;font-weight:750;letter-spacing:-.5px}
.stat .l{font-size:11.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px;margin-top:2px}
.stat.warm .n{color:var(--warm)}
.stat.accent .n{color:var(--accent)}

.analytics{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:14px 0 4px}
.card{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:15px 16px}
.card h3{margin:0 0 12px;font-size:12px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);font-weight:700}
.bar-row{display:flex;align-items:center;gap:9px;margin:6px 0;font-size:12.5px}
.bar-row .lab{width:112px;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex-shrink:0}
.bar-track{flex:1;background:var(--bg2);border-radius:5px;height:9px;overflow:hidden}
.bar-fill{height:100%;background:linear-gradient(90deg,#1F4FC3,#8A57BF);border-radius:5px}
.bar-row .val{width:24px;text-align:right;color:var(--muted);flex-shrink:0}

.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:18px 0 14px;padding:14px;background:var(--panel);border:1px solid var(--border);border-radius:12px}
.controls .grp{display:flex;flex-direction:column;gap:5px}
.controls label{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;font-weight:600}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{padding:5px 11px;border-radius:20px;background:var(--bg2);border:1px solid var(--border);color:var(--muted);cursor:pointer;font-size:12px;font-weight:600;user-select:none}
.chip:hover{color:var(--text)}
.chip.on{background:var(--accent-dim);border-color:var(--accent);color:#22397f}
select,.mini-btn{background:var(--bg2);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:8px 10px;font-size:13px;outline:none;cursor:pointer}
.toggle{display:flex;align-items:center;gap:7px;cursor:pointer;font-size:12.5px;color:var(--text);font-weight:600;user-select:none}
.toggle input{accent-color:var(--accent)}
.spacer{flex:1}
.btn{background:var(--accent);color:#fff;border:none;border-radius:9px;padding:9px 15px;font-weight:700;font-size:13px;cursor:pointer}
.btn:hover{filter:brightness(1.08)}
.btn.ghost{background:var(--panel2);color:var(--text);border:1px solid var(--border)}
.count-line{color:var(--muted);font-size:12.5px;margin:2px 2px 14px}
.count-line b{color:var(--text)}

.feed{display:grid;grid-template-columns:1fr 1fr;gap:13px;padding-bottom:60px}
.deal{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:15px 16px;display:flex;flex-direction:column;gap:9px;box-shadow:var(--shadow)}
.deal:hover{border-color:#c3ccdb;box-shadow:0 2px 6px rgba(16,25,43,.08),0 12px 28px rgba(16,25,43,.10)}
.deal .h{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
.deal .fund{font-weight:700;font-size:13px;color:var(--accent);cursor:pointer}
.deal .fund:hover{text-decoration:underline}
.deal .date{font-size:11.5px;color:var(--faint);white-space:nowrap;flex-shrink:0}
.deal .company{font-size:17px;font-weight:700;letter-spacing:-.2px}
.deal .meta{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.tag{font-size:11px;font-weight:650;padding:3px 9px;border-radius:6px;background:var(--bg2);border:1px solid var(--border);color:var(--muted)}
.tag.stage{background:rgba(123,79,208,.11);border-color:rgba(123,79,208,.28);color:#6b3fc0}
.tag.amount{background:rgba(47,79,195,.10);border-color:rgba(47,79,195,.26);color:#2f4fc3}
.tag.region{background:transparent}
.deal .sum{font-size:13px;color:var(--ink2);line-height:1.55}
.deal .drow{display:flex;gap:9px;font-size:12px;line-height:1.5}
.deal .drow .k{color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.4px;font-size:10px;min-width:62px;flex-shrink:0;padding-top:2px}
.deal .drow .v{color:var(--ink2);flex:1}
.deal .drow .v .inv{color:var(--accent);cursor:pointer;font-weight:600}
.deal .drow .v .inv:hover{text-decoration:underline}
.deal .foot{display:flex;justify-content:space-between;align-items:center;margin-top:2px;padding-top:9px;border-top:1px solid var(--border)}
.deal .src{font-size:11.5px;color:var(--muted)}
.dot-sep{color:var(--faint)}

/* directory */
.dir{padding-bottom:60px}
.dir table{width:100%;border-collapse:collapse;font-size:13px}
.dir th{text-align:left;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:9px 10px;border-bottom:1px solid var(--border);position:sticky;top:64px;background:var(--bg)}
.dir td{padding:10px;border-bottom:1px solid var(--border);vertical-align:top}
.dir tr:hover td{background:var(--panel)}
.dir .fname{font-weight:700;cursor:pointer}
.dir .fname:hover{color:var(--accent)}
.pill{display:inline-block;font-size:11px;padding:2px 8px;border-radius:12px;background:var(--bg2);border:1px solid var(--border);color:var(--muted)}
.pill.deals{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
.pill.warm{background:rgba(224,112,92,.15);border-color:rgba(224,112,92,.38);color:var(--coral)}
.pill.up,.tag.up{background:rgba(42,167,155,.14);border-color:rgba(42,167,155,.42);color:#1f8a80}
.pill.peer,.tag.peer{background:rgba(47,79,195,.13);border-color:rgba(47,79,195,.4);color:#2f4fc3}
.pill.down,.tag.down{background:rgba(220,96,80,.14);border-color:rgba(220,96,80,.42);color:#c0503f}
.rchip.up.on{background:rgba(42,167,155,.16);border-color:#2aa79b;color:#1c7a72}
.rchip.peer.on{background:rgba(47,79,195,.16);border-color:#2f4fc3;color:#22397f}
.rchip.down.on{background:rgba(220,96,80,.16);border-color:#dc6050;color:#a5432f}
.hqtxt{color:var(--muted);font-size:12px}

/* newsletters */
.nl{padding-bottom:60px}
.nl-head{margin:4px 0 16px}
.nl-title{margin:0;font-size:18px}
.nl-sub{color:var(--muted);font-size:13px;margin-top:3px}
.nl-deals{display:flex;flex-direction:column;gap:8px;margin-bottom:28px}
.nl-deal{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:12px 14px;box-shadow:var(--shadow)}
.nl-dmain{display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.nl-co{font-weight:700;font-size:15px}
.nl-dmeta{color:var(--muted);font-size:12.5px;margin-top:4px}
.nl-src{color:var(--accent);font-weight:600}
.nl-link{color:var(--link);cursor:pointer;font-weight:600;margin-left:4px}
.nl-link:hover{text-decoration:underline}
.nl-badge{font-size:10px;font-weight:700;padding:2px 8px;border-radius:12px;background:var(--bg2);border:1px solid var(--border);color:var(--muted);text-transform:uppercase;letter-spacing:.4px}
.nl-badge.add{background:rgba(42,167,155,.14);border-color:rgba(42,167,155,.42);color:#1f8a80}
.nl-badge.trk{background:rgba(47,79,195,.12);border-color:rgba(47,79,195,.36);color:#2f4fc3}
.nl-h3{font-size:12px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);margin:8px 2px 12px;font-weight:700}
.nl-digest{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:28px}
.nl-card{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:14px 16px}
.nl-cardhead{font-weight:700;font-size:14px;color:var(--accent);margin-bottom:10px}
.nl-ed{padding:9px 0;border-top:1px solid var(--border)}
.nl-ed:first-of-type{border-top:none;padding-top:0}
.nl-edtop{display:flex;justify-content:space-between;align-items:center}
.nl-eddate{font-size:11.5px;color:var(--faint);font-weight:600}
.nl-edtitle{font-size:13px;font-weight:600;margin:3px 0 5px}
.nl-eddeals{margin:0;padding-left:18px;color:var(--ink2);font-size:12.5px;line-height:1.6}
.nl-sources{display:flex;flex-wrap:wrap;gap:8px}
.nl-source{font-size:12px;padding:5px 10px;border-radius:8px;background:var(--panel);border:1px solid var(--border);color:var(--text)}
.nl-source em{color:var(--muted);font-style:normal;font-size:11px;text-transform:capitalize}
.nl-source.paywalled em{color:var(--coral)}
.nl-source.readable em{color:#1f8a80}
@media(max-width:900px){.nl-digest{grid-template-columns:1fr}}

/* heat map */
.heat{padding-bottom:60px;overflow-x:auto}
.heat table{border-collapse:separate;border-spacing:3px;font-size:12px;margin-top:4px}
.heat thead th{font-weight:700;color:var(--muted);padding:6px 6px;text-align:center;font-size:11px;text-transform:uppercase;letter-spacing:.4px}
.heat thead th.rowh{text-align:left;color:var(--text)}
.heat .rowlab{text-align:left;font-weight:600;padding:2px 12px 2px 4px;white-space:nowrap;color:var(--text);font-size:12.5px}
.heat .cell{width:74px;height:40px;display:flex;align-items:center;justify-content:center;border-radius:7px;font-weight:700;font-size:13px;border:1px solid var(--border)}
.heat .tot{color:var(--muted);font-weight:700;text-align:center;padding:0 6px}
.heat tr.totrow td{padding-top:6px}
.heat-legend{display:flex;align-items:center;gap:7px;margin:14px 2px;font-size:12px;color:var(--muted)}
.heat-legend .sw{width:28px;height:13px;border-radius:3px;border:1px solid var(--border)}
.hc-title{margin:6px 2px 12px;font-size:12px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);font-weight:700}
.heat-chart{margin:2px 0 26px;padding:16px 18px;background:var(--panel);border:1px solid var(--border);border-radius:12px}
.hc-row{display:flex;align-items:center;gap:12px;margin:6px 0}
.hc-lab{width:150px;font-size:12.5px;font-weight:600;color:var(--text);text-align:right;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hc-track{flex:1;display:flex;height:22px;border-radius:5px;background:var(--bg2);overflow:hidden}
.hc-fill{display:flex;height:100%}
.hc-seg{height:100%}
.hc-val{width:26px;font-size:12px;color:var(--muted);font-weight:700;flex-shrink:0}
.hc-legend{display:flex;flex-wrap:wrap;gap:14px;margin:14px 0 2px 162px;font-size:12px;color:var(--muted)}
.hc-legend span{display:flex;align-items:center;gap:6px}
.hc-legend i{width:11px;height:11px;border-radius:3px;display:inline-block}

/* modal */
.modal-bg{position:fixed;inset:0;background:rgba(4,7,11,.72);display:none;align-items:center;justify-content:center;z-index:60;padding:20px}
.modal-bg.show{display:flex}
.modal{background:var(--panel);border:1px solid var(--border);border-radius:16px;max-width:640px;width:100%;max-height:88vh;overflow:auto;box-shadow:var(--shadow)}
.modal .mh{display:flex;justify-content:space-between;align-items:center;padding:18px 20px;border-bottom:1px solid var(--border);position:sticky;top:0;background:var(--panel)}
.modal .mh h2{margin:0;font-size:17px}
.modal .mb{padding:20px}
.x{cursor:pointer;color:var(--muted);font-size:22px;line-height:1;background:none;border:none}
.field{margin-bottom:13px}
.field label{display:block;font-size:12px;color:var(--muted);margin-bottom:5px;font-weight:600}
.field input,.field select,.field textarea{width:100%;background:var(--bg2);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:9px 11px;font-size:13px;outline:none;font-family:inherit}
.field textarea{min-height:70px;resize:vertical}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.note{font-size:12px;color:var(--muted);background:var(--bg2);border:1px solid var(--border);border-left:3px solid var(--warm);border-radius:8px;padding:10px 12px;margin-bottom:14px}
.fund-deal{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:12px;margin-bottom:10px}
.fund-deal .company{font-size:15px}
.kv{display:flex;gap:8px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin:6px 0}
.kv b{color:var(--text);font-weight:600}
.empty{text-align:center;color:var(--muted);padding:50px 20px}
.contacts-box{font-size:12.5px;color:var(--ink2);line-height:1.7}
footer{border-top:1px solid var(--border);color:var(--faint);font-size:12px;padding:20px;text-align:center}
@media(max-width:900px){.stats{grid-template-columns:repeat(2,1fr)}.analytics{grid-template-columns:1fr}.feed{grid-template-columns:1fr}.searchbox input{width:150px}}
</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <div class="brand"><span class="dot"></span><div>Sports Fund Deal Tracker<small>Gamma Waves Partners · intelligence portal</small></div></div>
    <div class="tabs">
      <div class="tab active" data-view="feed" onclick="setView('feed')">Deal Feed</div>
      <div class="tab" data-view="heat" onclick="setView('heat')">Heat Map</div>
      <div class="tab" data-view="nl" onclick="setView('nl')">Newsletters</div>
      <div class="tab" data-view="dir" onclick="setView('dir')">Funds Directory</div>
    </div>
    <div class="spacer"></div>
    <div class="searchbox">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
      <input id="search" placeholder="Search deals, funds, sectors…" oninput="render()"/>
    </div>
    <button class="btn" onclick="openAdd()">+ Add</button>
  </div>
  <div class="gradbar"></div>
</header>

<div class="wrap">
  <div class="stats" id="stats"></div>
  <div class="analytics" id="analytics"></div>
  <div class="controls" id="controls"></div>
  <div class="count-line" id="countline"></div>
  <div id="feedView" class="feed"></div>
  <div id="heatView" class="heat" style="display:none"></div>
  <div id="nlView" class="nl" style="display:none"></div>
  <div id="dirView" class="dir" style="display:none"></div>
</div>

<div class="modal-bg" id="modal" onclick="if(event.target===this)closeModal()">
  <div class="modal"><div class="mh"><h2 id="modalTitle"></h2><button class="x" onclick="closeModal()">×</button></div><div class="mb" id="modalBody"></div></div>
</div>

<footer>Seeded with publicly-reported deals (2023–2026) for tracked funds · Built for Gamma Waves Partners · Last refreshed __BUILD_DATE__</footer>

<script>
const FUNDS = __FUNDS__;
const DEALS = __DEALS__;
const NEWSLETTERS = __NL__;
const HAS_CONTACTS = FUNDS.some(f=>(f.contact&&f.contact.name)||f.affinity_contacts);
const HAS_WARM = FUNDS.some(f=>f.warm);
const BUILD_DATE = "__BUILD_DATE__";

// ---- date parsing for sort ----
const MONTHS={january:1,february:2,march:3,april:4,may:5,june:6,july:7,august:8,september:9,october:10,november:11,december:12};
function dateVal(s){ if(!s)return 0; s=s.toLowerCase(); let y=(s.match(/(20\d\d)/)||[])[1]; let m=0; for(const k in MONTHS){if(s.includes(k)){m=MONTHS[k];break;}} let day=(s.replace(/20\d\d/,'').match(/\b(\d{1,2})\b/)||[])[1]||0; return y?parseInt(y)*10000+m*100+parseInt(day):0; }
DEALS.forEach(d=>d._dv=dateVal(d.date));

// ---- sector color (accessible categorical) ----
const SECTOR_HUES=[222,250,275,315,12,32,182,150,196,338,210,290];
function sectorColor(s){let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))>>>0;const hue=SECTOR_HUES[h%SECTOR_HUES.length];return `hsl(${hue} 62% 45%)`;}

const REGIONS=[...new Set(FUNDS.map(f=>f.region))].sort();
const TYPES=[...new Set(FUNDS.map(f=>f.type_group))].sort();
const SECTORS=[...new Set(DEALS.map(d=>d.sector))].sort();
const RELS=['Upstream','Peers','Downstream'];
function relCls(r){return r==='Upstream'?'up':r==='Peers'?'peer':r==='Downstream'?'down':'';}
const ROUND_ORDER=['Angel Investment','Pre Seed','Seed','Series A','Series B','Series C','Series D+','Acquisition/Buyout','Other'];
const STAGES=ROUND_ORDER.filter(r=>DEALS.some(d=>d.round===r));

let state={view:'feed', regions:new Set(), types:new Set(), rels:new Set(), round:'', sector:'', warm:false, tracked:false, sort:'recent'};

function esc(s){return (s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
const _n=s=>(s||'').toLowerCase().replace(/[^a-z0-9]/g,'');
const FUNDIDX={}; FUNDS.forEach(f=>{FUNDIDX[_n(f.name)]=f.id;});
function findFundId(name){const k=_n(name);if(FUNDIDX[k]!=null)return FUNDIDX[k];for(const kk in FUNDIDX){if(k&&kk.length>4&&(kk.includes(k)||k.includes(kk)))return FUNDIDX[kk];}return null;}
function investorsHtml(d){const arr=(d.investors&&d.investors.length)?d.investors:[d.fund_name];return arr.map(nm=>{const fid=findFundId(nm);return fid!=null?`<span class="inv" onclick="openFund(${fid})">${esc(nm)}</span>`:`<span>${esc(nm)}</span>`;}).join(', ');}

// ---- filtering ----
function filteredDeals(){
  const q=(document.getElementById('search').value||'').toLowerCase();
  let ds=DEALS.filter(d=>{
    if(state.regions.size&&!state.regions.has(d.region))return false;
    if(state.types.size&&!state.types.has(d.type_group))return false;
    if(state.rels.size&&!state.rels.has(d.rel))return false;
    if(state.round&&d.round!==state.round)return false;
    if(state.sector&&d.sector!==state.sector)return false;
    if(state.warm){const f=FUNDS.find(x=>x.id===d.fund_id);if(!f||!f.warm)return false;}
    if(q){const blob=(d.fund_name+' '+d.company+' '+d.sector+' '+d.summary+' '+d.stage).toLowerCase();if(!blob.includes(q))return false;}
    return true;
  });
  if(state.sort==='recent')ds.sort((a,b)=>b._dv-a._dv);
  if(state.sort==='amount')ds.sort((a,b)=>parseAmt(b.amount)-parseAmt(a.amount));
  return ds;
}
function parseAmt(a){if(!a)return 0;let m=a.match(/([\d.]+)\s*([bmk])/i);if(!m)return 0;let n=parseFloat(m[1]);let u=m[2].toLowerCase();return n*(u=='b'?1e9:u=='m'?1e6:1e3);}

function filteredFunds(){
  const q=(document.getElementById('search').value||'').toLowerCase();
  return FUNDS.filter(f=>{
    if(state.regions.size&&!state.regions.has(f.region))return false;
    if(state.types.size&&!state.types.has(f.type_group))return false;
    if(state.rels.size&&!state.rels.has(f.rel))return false;
    if(state.warm&&!f.warm)return false;
    if(state.tracked&&!f.tracked)return false;
    if(state.sector){if(!DEALS.some(d=>d.fund_id===f.id&&d.sector===state.sector))return false;}
    if(q){const blob=(f.name+' '+f.type+' '+f.hq+' '+f.mandate+' '+(f.affinity_contacts||'')).toLowerCase();if(!blob.includes(q))return false;}
    return true;
  });
}

// ---- rendering ----
function renderStats(){
  const withDeals=FUNDS.filter(f=>f.tracked).length;
  const y26=DEALS.filter(d=>d._dv>=202600).length;
  const warm=FUNDS.filter(f=>f.warm).length;
  const s=[
    ['accent',FUNDS.length,'Funds tracked'],
    ['accent',DEALS.length,'Deals logged'],
    ['',withDeals,'Funds w/ deals'],
    ['',y26,'Deals in 2026'],
  ];
  if(HAS_WARM) s.push(['warm',warm,'Warm relationships']);
  document.getElementById('stats').innerHTML=s.map(x=>`<div class="stat ${x[0]}"><div class="n">${x[1]}</div><div class="l">${x[2]}</div></div>`).join('');
}
function barCard(title,pairs){
  const max=Math.max(...pairs.map(p=>p[1]),1);
  return `<div class="card"><h3>${title}</h3>${pairs.map(p=>`<div class="bar-row"><span class="lab" title="${esc(p[0])}">${esc(p[0])}</span><span class="bar-track"><span class="bar-fill" style="width:${Math.round(p[1]/max*100)}%"></span></span><span class="val">${p[1]}</span></div>`).join('')}</div>`;
}
function renderAnalytics(){
  const ds=state.view==='heat'?DEALS:filteredDeals();
  const bySector={},byRegion={},byMonth={};
  ds.forEach(d=>{bySector[d.sector]=(bySector[d.sector]||0)+1;byRegion[d.region]=(byRegion[d.region]||0)+1;
    if(d._dv){const key=d.date.match(/(20\d\d)/)?d.date.replace(/^[A-Za-z]+\s/,m=>m):d.date;byMonth[d.date]=(byMonth[d.date]||0)+1;}});
  const topSector=Object.entries(bySector).sort((a,b)=>b[1]-a[1]).slice(0,6);
  const regionP=Object.entries(byRegion).sort((a,b)=>b[1]-a[1]);
  const monthP=Object.entries(byMonth).sort((a,b)=>dateVal(b[0])-dateVal(a[0])).slice(0,6);
  document.getElementById('analytics').innerHTML=barCard('Top sectors (filtered)',topSector)+barCard('By geography',regionP)+barCard('Most recent activity',monthP);
}
function renderControls(){
  const c=document.getElementById('controls');
  c.innerHTML=`
   <div class="grp"><label>Geography</label><div class="chips" id="regionChips">${REGIONS.map(r=>`<span class="chip ${state.regions.has(r)?'on':''}" onclick="toggleSet('regions','${esc(r)}')">${esc(r)}</span>`).join('')}</div></div>
   ${state.view==='dir'?`<div class="grp"><label>Fund type</label><div class="chips" id="typeChips">${TYPES.map(t=>`<span class="chip ${state.types.has(t)?'on':''}" onclick="toggleSet('types','${esc(t)}')">${esc(t)}</span>`).join('')}</div></div>`:''}
   ${state.view==='dir'?`<div class="grp"><label>Investment stage</label><div class="chips">${RELS.map(t=>`<span class="chip rchip ${relCls(t)} ${state.rels.has(t)?'on':''}" onclick="toggleSet('rels','${t}')">${t}</span>`).join('')}</div></div>`:''}
   ${state.view!=='dir'?`<div class="grp"><label>Stage</label><select onchange="state.round=this.value;render()"><option value="">All stages</option>${STAGES.map(s=>`<option ${state.round===s?'selected':''}>${esc(s)}</option>`).join('')}</select></div>`:''}
   <div class="grp"><label>Sector</label><select onchange="state.sector=this.value;render()"><option value="">All sectors</option>${SECTORS.map(s=>`<option ${state.sector===s?'selected':''}>${esc(s)}</option>`).join('')}</select></div>
   <div class="grp"><label>Sort</label><select onchange="state.sort=this.value;render()"><option value="recent">Most recent</option><option value="amount">Largest amount</option></select></div>
   <div class="spacer"></div>
   ${HAS_WARM?`<label class="toggle"><input type="checkbox" ${state.warm?'checked':''} onchange="state.warm=this.checked;render()"/>Warm only</label>`:''}
   <label class="toggle" id="trackedToggle" style="${state.view==='dir'?'':'display:none'}"><input type="checkbox" ${state.tracked?'checked':''} onchange="state.tracked=this.checked;render()"/>With deals only</label>
   <button class="mini-btn" onclick="clearFilters()">Clear</button>`;
}
function renderFeed(){
  const ds=filteredDeals();
  document.getElementById('countline').innerHTML=`Showing <b>${ds.length}</b> deal${ds.length!=1?'s':''}${activeFilterText()}`;
  const el=document.getElementById('feedView');
  if(!ds.length){el.innerHTML='<div class="empty">No deals match these filters. Try clearing them, or add a deal with the “+ Add” button.</div>';return;}
  el.innerHTML=ds.map(d=>`
   <div class="deal">
     <div class="h"><span class="company">${esc(d.company)}</span><span class="date">${esc(d.date||'—')}</span></div>
     <div class="meta">
       ${d.stage?`<span class="tag stage">${esc(d.stage)}</span>`:''}
       <span class="tag sector" style="color:${sectorColor(d.sector)};border-color:${sectorColor(d.sector)}44">${esc(d.sector)}</span>
       <span class="tag region">${esc(d.region)}</span>
       ${d.amount&&d.amount!=='Undisclosed'&&!d.financials?`<span class="tag amount">${esc(d.amount)}</span>`:''}
     </div>
     <div class="sum">${esc(d.desc_simple||d.summary)}</div>
     <div class="drow"><span class="k">Investors</span><span class="v">${investorsHtml(d)}</span></div>
     ${d.founders?`<div class="drow"><span class="k">Founders</span><span class="v">${esc(d.founders)}</span></div>`:''}
     ${d.employees?`<div class="drow"><span class="k">Team</span><span class="v">${esc(d.employees)} employees</span></div>`:''}
     ${d.financials?`<div class="drow"><span class="k">Metrics</span><span class="v">${esc(d.financials)}</span></div>`:''}
     <div class="foot"><span class="src">${esc(d.source_name||'Source')}</span>${d.source_url?`<a href="${esc(d.source_url)}" target="_blank" rel="noopener">Read source ↗</a>`:''}</div>
   </div>`).join('');
}
function renderDir(){
  const fs=filteredFunds().slice().sort((a,b)=>(b.deal_count-a.deal_count)||a.name.localeCompare(b.name));
  document.getElementById('countline').innerHTML=`Showing <b>${fs.length}</b> fund${fs.length!=1?'s':''}${activeFilterText()}`;
  const el=document.getElementById('dirView');
  el.innerHTML=`<table><thead><tr><th>Fund</th><th>Investment stage</th><th>Type</th><th>Geography</th><th>HQ</th><th>Deals</th>${HAS_CONTACTS?'<th>Contacts</th>':''}</tr></thead><tbody>
   ${fs.map(f=>`<tr>
     <td><span class="fname" onclick="openFund(${f.id})">${esc(f.name)}</span> ${f.warm?'<span class="pill warm">warm</span>':''}</td>
     <td>${f.rel?`<span class="pill ${relCls(f.rel)}">${esc(f.rel)}</span>`:'<span class="pill">—</span>'}</td>
     <td><span class="pill">${esc(f.type_group)}</span></td>
     <td>${esc(f.region)}</td>
     <td class="hqtxt">${esc(f.hq||'—')}</td>
     <td>${f.deal_count?`<span class="pill deals">${f.deal_count}</span>`:'<span class="pill">0</span>'}</td>
     ${HAS_CONTACTS?`<td class="hqtxt">${esc(shortContacts(f))}</td>`:''}
   </tr>`).join('')}
  </tbody></table>`;
}
function shortContacts(f){let a=[];if(f.contact&&f.contact.name)a.push(f.contact.name);if(f.affinity_contacts){a.push(f.affinity_contacts.split(';')[0].trim());}return [...new Set(a)].slice(0,2).join(' · ')||'—';}
function activeFilterText(){let p=[];if(state.regions.size)p.push([...state.regions].join('/'));if(state.types.size)p.push([...state.types].join('/'));if(state.rels.size)p.push([...state.rels].join('/'));if(state.round)p.push(state.round);if(state.sector)p.push(state.sector);if(state.warm)p.push('warm');if(state.tracked)p.push('with deals');return p.length?` · filtered by ${esc(p.join(', '))}`:'';}

function renderHeat(){
  const ds=DEALS;
  const rtot={},secTot={},cell={};
  REGIONS.forEach(r=>rtot[r]=0);
  ds.forEach(d=>{secTot[d.sector]=(secTot[d.sector]||0)+1;rtot[d.region]=(rtot[d.region]||0)+1;const k=d.sector+'|'+d.region;cell[k]=(cell[k]||0)+1;});
  const cols=REGIONS.filter(r=>rtot[r]>0).sort((a,b)=>rtot[b]-rtot[a]);
  let sects=Object.keys(secTot).sort((a,b)=>secTot[b]-secTot[a]);
  const TOPN=18; let other=[];
  if(sects.length>TOPN){other=sects.slice(TOPN);sects=sects.slice(0,TOPN);}
  const rows=sects.map(s=>({s,row:cols.map(r=>cell[s+'|'+r]||0)}));
  if(other.length)rows.push({s:'Other ('+other.length+' sectors)',row:cols.map(r=>other.reduce((n,s)=>n+(cell[s+'|'+r]||0),0))});
  let maxCell=1; rows.forEach(x=>x.row.forEach(v=>{if(v>maxCell)maxCell=v;}));
  const bg=v=>v?`rgba(47,79,195,${(0.14+0.80*(v/maxCell)).toFixed(2)})`:'transparent';
  const fg=v=>v?((0.14+0.80*(v/maxCell))>0.55?'#fff':'#1a2740'):'var(--faint)';
  document.getElementById('countline').innerHTML=`Heat map of <b>${ds.length}</b> deals — sector × geography${activeFilterText()}. Darker = more deals.`;
  if(!ds.length){document.getElementById('heatView').innerHTML='<div class="empty">No deals match these filters.</div>';return;}
  const RC={'North America':'#2f4fc3','Europe':'#8a57bf','UK':'#dc6050','Asia-Pacific':'#2aa79b','Middle East':'#d9a05b','Latin America':'#c85b9c'};
  const chartRows=rows.slice(0,12);
  const maxTot=Math.max(...chartRows.map(x=>x.row.reduce((a,b)=>a+b,0)),1);
  let chart='<div class="heat-chart"><div class="hc-title">Deals by sector, split by geography</div>';
  chartRows.forEach(x=>{const t=x.row.reduce((a,b)=>a+b,0);
    chart+=`<div class="hc-row"><div class="hc-lab" title="${esc(x.s)}">${esc(x.s)}</div><div class="hc-track"><div class="hc-fill" style="width:${(t/maxTot*100).toFixed(1)}%">`+
      cols.map((c,i)=>x.row[i]?`<div class="hc-seg" style="width:${(x.row[i]/t*100).toFixed(1)}%;background:${RC[c]||'#8896a6'}" title="${esc(c)}: ${x.row[i]}"></div>`:'').join('')+
      `</div></div><div class="hc-val">${t}</div></div>`;});
  chart+='<div class="hc-legend">'+cols.map(c=>`<span><i style="background:${RC[c]||'#8896a6'}"></i>${esc(c)}</span>`).join('')+'</div></div>';
  let h=chart+'<div class="hc-title">Full grid — deal count by sector × geography</div><table><thead><tr><th class="rowh">Sector × Geography</th>'+cols.map(c=>`<th>${esc(c)}</th>`).join('')+'<th>Total</th></tr></thead><tbody>';
  rows.forEach(x=>{const t=x.row.reduce((a,b)=>a+b,0);
    h+='<tr><td class="rowlab">'+esc(x.s)+'</td>'+x.row.map(v=>`<td><div class="cell" style="background:${bg(v)};color:${fg(v)}">${v||''}</div></td>`).join('')+`<td class="tot">${t}</td></tr>`;});
  h+='<tr class="totrow"><td class="rowlab tot">Total</td>'+cols.map(c=>`<td class="tot">${rtot[c]}</td>`).join('')+`<td class="tot">${ds.length}</td></tr>`;
  h+='</tbody></table><div class="heat-legend"><span>Fewer</span><span class="sw" style="background:rgba(47,79,195,.16)"></span><span class="sw" style="background:rgba(47,79,195,.45)"></span><span class="sw" style="background:rgba(47,79,195,.72)"></span><span class="sw" style="background:rgba(47,79,195,.95)"></span><span>More</span></div>';
  document.getElementById('heatView').innerHTML=h;
}
function gotoDeal(company){document.getElementById('search').value=company;setView('feed');}
function renderNL(){
  const nl=NEWSLETTERS||{}; const el=document.getElementById('nlView');
  const byNL={}; (nl.editions||[]).forEach(e=>{(byNL[e.newsletter]=byNL[e.newsletter]||[]).push(e);});
  let h=`<h3 class="nl-h3">Recent editions</h3><div class="nl-digest">`;
  Object.keys(byNL).forEach(name=>{
    h+=`<div class="nl-card"><div class="nl-cardhead">${esc(name)}</div>`+byNL[name].map(e=>`<div class="nl-ed"><div class="nl-edtop"><span class="nl-eddate">${esc(e.date)}</span>${e.url?`<a href="${esc(e.url)}" target="_blank" rel="noopener">open ↗</a>`:''}</div><div class="nl-edtitle">${esc(e.title)}</div>${(e.deals&&e.deals.length)?`<ul class="nl-eddeals">`+e.deals.map(d=>`<li>${esc(d)}</li>`).join('')+`</ul>`:''}</div>`).join('')+`</div>`;});
  h+=`</div>`;
  h+=`<h3 class="nl-h3">Sources</h3><div class="nl-sources">`+(nl.sources||[]).map(s=>`<span class="nl-source ${esc(s.status)}" title="${esc(s.note||'')}">${esc(s.name)} <em>${esc((s.status||'').replace('-',' '))}</em></span>`).join('')+`</div>`;
  el.innerHTML=h;
}
function render(){
  renderStats();renderAnalytics();
  const tt=document.getElementById('trackedToggle');if(tt)tt.style.display=state.view==='dir'?'':'none';
  const noFilters=state.view==='heat'||state.view==='nl';
  document.getElementById('controls').style.display=noFilters?'none':'flex';
  document.getElementById('countline').style.display=noFilters?'none':'block';
  const isnl=state.view==='nl';
  document.getElementById('stats').style.display=isnl?'none':'grid';
  document.getElementById('analytics').style.display=isnl?'none':'grid';
  const fv=document.getElementById('feedView'),dv=document.getElementById('dirView'),hv=document.getElementById('heatView'),nv=document.getElementById('nlView');
  fv.style.display=dv.style.display=hv.style.display=nv.style.display='none';
  if(state.view==='feed'){fv.style.display='grid';renderFeed();}
  else if(state.view==='heat'){hv.style.display='block';renderHeat();}
  else if(state.view==='nl'){nv.style.display='block';renderNL();}
  else{dv.style.display='block';renderDir();}
}
function setView(v){state.view=v;document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.view===v));renderControls();render();}
function toggleSet(key,val){state[key].has(val)?state[key].delete(val):state[key].add(val);renderControls();render();}
function clearFilters(){state.regions.clear();state.types.clear();state.rels.clear();state.round='';state.sector='';state.warm=false;state.tracked=false;document.getElementById('search').value='';renderControls();render();}

// ---- fund modal ----
function openFund(id){
  const f=FUNDS.find(x=>x.id===id);if(!f)return;
  const ds=DEALS.filter(d=>d.fund_id===id).sort((a,b)=>b._dv-a._dv);
  document.getElementById('modalTitle').textContent=f.name;
  let contactsHtml='';
  const parts=[];
  if(f.contact&&f.contact.name){parts.push(`<b>${esc(f.contact.name)}</b>${f.contact.role?' — '+esc(f.contact.role):''}${f.contact.email?' · '+esc(f.contact.email):''}`);}
  if(f.affinity_contacts)parts.push('<span style="color:var(--muted)">Affinity:</span> '+esc(f.affinity_contacts));
  contactsHtml=parts.length?`<div class="contacts-box">${parts.join('<br>')}</div>`:'<span style="color:var(--faint)">No contacts on file</span>';
  document.getElementById('modalBody').innerHTML=`
    <div class="kv">${f.rel?`<span class="pill ${relCls(f.rel)}">${esc(f.rel)}</span>`:''}<span class="pill">${esc(f.type_group)}</span><span class="pill">${esc(f.region)}</span>${f.warm?'<span class="pill warm">warm relationship</span>':''}${f.website?`<a href="${(f.website.startsWith('http')?'':'https://')+esc(f.website)}" target="_blank" rel="noopener">website ↗</a>`:''}</div>
    ${f.hq?`<div class="kv"><span>📍 ${esc(f.hq)}</span>${f.stage?`<span>· ${esc(f.stage)}</span>`:''}</div>`:''}
    ${f.mandate?`<p style="color:var(--ink2);font-size:13px">${esc(f.mandate)}</p>`:''}
    ${parts.length?`<div class="field"><label>Contacts</label>${contactsHtml}</div>`:''}
    <div class="field"><label>Tracked deals (${ds.length})</label>
      ${ds.length?ds.map(d=>`<div class="fund-deal"><div class="company">${esc(d.company)} <span style="font-size:12px;color:var(--faint)">${esc(d.date||'')}</span></div>
        <div class="kv"><span class="tag sector" style="color:${sectorColor(d.sector)}">${esc(d.sector)}</span>${d.stage?`<span class="tag stage">${esc(d.stage)}</span>`:''}${d.amount&&d.amount!=='Undisclosed'?`<span class="tag amount">${esc(d.amount)}</span>`:''}</div>
        <div style="font-size:12.5px;color:var(--ink2)">${esc(d.summary)}</div>${d.source_url?`<div style="margin-top:6px"><a href="${esc(d.source_url)}" target="_blank" rel="noopener">${esc(d.source_name||'source')} ↗</a></div>`:''}</div>`).join(''):'<div class="note">No deals logged yet for this fund. The daily scan will populate this as public deals appear — or add one manually.</div>'}
    </div>
    <button class="btn ghost" onclick="openAddDeal(${f.id})">+ Add a deal for ${esc(f.name)}</button>`;
  showModal();
}

// ---- add fund / deal ----
function openAdd(){
  document.getElementById('modalTitle').textContent='Add to tracker';
  document.getElementById('modalBody').innerHTML=`
   <div class="note">Added here they appear immediately in this view. To make additions permanent for your team, use the “Export” button so the next daily build picks them up (this prototype keeps changes in-memory only).</div>
   <div class="tabs" style="margin-bottom:14px"><div class="tab active" onclick="swAdd(this,'f')">New fund</div><div class="tab" onclick="swAdd(this,'d')">New deal</div></div>
   <div id="addFund">
     <div class="field"><label>Fund name *</label><input id="nf_name"/></div>
     <div class="frow"><div class="field"><label>Fund type</label><select id="nf_type">${TYPES.map(t=>`<option>${esc(t)}</option>`).join('')}</select></div>
       <div class="field"><label>Geography</label><select id="nf_region">${REGIONS.map(r=>`<option>${esc(r)}</option>`).join('')}</select></div></div>
     <div class="frow"><div class="field"><label>HQ location</label><input id="nf_hq"/></div><div class="field"><label>Website</label><input id="nf_web"/></div></div>
     <div class="field"><label>Mandate / thesis</label><textarea id="nf_mandate"></textarea></div>
     <div class="field"><label>Key contact (name &lt;email&gt;)</label><input id="nf_contact"/></div>
     <button class="btn" onclick="addFund()">Add fund</button>
   </div>
   <div id="addDeal" style="display:none">${dealFormHtml('')}</div>`;
  showModal();
}
function swAdd(tab,which){tab.parentNode.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));tab.classList.add('active');document.getElementById('addFund').style.display=which=='f'?'block':'none';document.getElementById('addDeal').style.display=which=='d'?'block':'none';}
function dealFormHtml(preFund){
  return `<div class="field"><label>Fund *</label><select id="nd_fund">${FUNDS.slice().sort((a,b)=>a.name.localeCompare(b.name)).map(f=>`<option value="${f.id}" ${f.id==preFund?'selected':''}>${esc(f.name)}</option>`).join('')}</select></div>
   <div class="frow"><div class="field"><label>Company *</label><input id="nd_company"/></div><div class="field"><label>Sector</label><input id="nd_sector" placeholder="e.g. Sports Performance"/></div></div>
   <div class="frow"><div class="field"><label>Stage</label><input id="nd_stage" placeholder="Seed, Series A…"/></div><div class="field"><label>Date</label><input id="nd_date" placeholder="e.g. June 2026"/></div></div>
   <div class="field"><label>Amount</label><input id="nd_amount" placeholder="$10M"/></div>
   <div class="field"><label>Summary</label><textarea id="nd_summary"></textarea></div>
   <div class="frow"><div class="field"><label>Source name</label><input id="nd_srcname"/></div><div class="field"><label>Source URL</label><input id="nd_srcurl"/></div></div>
   <button class="btn" onclick="addDeal()">Add deal</button>`;
}
function openAddDeal(fid){document.getElementById('modalTitle').textContent='Add a deal';document.getElementById('modalBody').innerHTML=`<div class="note">In-memory only in this prototype — export to persist.</div>`+dealFormHtml(fid);showModal();}
let nextFundId=Math.max(...FUNDS.map(f=>f.id))+1;
let nextDealId=Math.max(...DEALS.map(d=>d.id))+1;
function addFund(){const n=document.getElementById('nf_name').value.trim();if(!n){alert('Name required');return;}
  const c=document.getElementById('nf_contact').value.trim();
  FUNDS.push({id:nextFundId++,name:n,type:document.getElementById('nf_type').value,type_group:document.getElementById('nf_type').value,region:document.getElementById('nf_region').value,hq:document.getElementById('nf_hq').value,website:document.getElementById('nf_web').value,mandate:document.getElementById('nf_mandate').value,contact:c?{name:c,role:'',email:'',linkedin:''}:null,affinity_contacts:'',warm:false,deal_count:0,tracked:false});
  closeModal();setView('dir');}
function addDeal(){const fid=parseInt(document.getElementById('nd_fund').value);const f=FUNDS.find(x=>x.id===fid);const co=document.getElementById('nd_company').value.trim();if(!co){alert('Company required');return;}
  const d={id:nextDealId++,fund_id:fid,fund_name:f.name,region:f.region,type_group:f.type_group,company:co,sector:document.getElementById('nd_sector').value||'Other',stage:document.getElementById('nd_stage').value,date:document.getElementById('nd_date').value,amount:document.getElementById('nd_amount').value,summary:document.getElementById('nd_summary').value,source_name:document.getElementById('nd_srcname').value,source_url:document.getElementById('nd_srcurl').value};
  d._dv=dateVal(d.date);DEALS.push(d);f.deal_count=(f.deal_count||0)+1;f.tracked=true;closeModal();setView('feed');}

function showModal(){document.getElementById('modal').classList.add('show');}
function closeModal(){document.getElementById('modal').classList.remove('show');}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});

renderControls();render();
</script>
</body>
</html>'''

html=html.replace('__FUNDS__',funds_js).replace('__DEALS__',deals_js).replace('__NL__',nl_js).replace('__BUILD_DATE__',BUILD_DATE)
open('/home/claude/out_portal/Sports_Fund_Deal_Tracker.html','w').close() if False else None
import os
os.makedirs('public',exist_ok=True)
with open('public/index.html','w') as fh:
    fh.write(html)
print('Built public/index.html —', len(html), 'bytes')
