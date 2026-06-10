#!/usr/bin/env python3
"""
index.html oluşturur — tamamen bağımsız çevrimdışı dua kartları uygulaması.
CDN yok, ağ bağlantısı yok, harici dosya yok. iPhone’da doğrudan Safari ile açılabilir.

Kullanım:
    python build_standalone_flashcards.py

Veri kaynağı: ../duas_repo/data/
Çıktı:        index.html
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'duas_repo', 'data'))
OUT_DIR = os.path.join(SCRIPT_DIR, 'dist')
OUT_FILE = os.path.join(OUT_DIR, 'index.html')


def load_json(name):
    with open(os.path.join(DATA_DIR, name), encoding='utf-8') as f:
        return json.load(f)


def normalize_duas():
    duas_en = load_json('duas.json')
    duas_ar = load_json('duas.ar.json')
    sections_en = load_json('sections.json')
    sections_ar = load_json('sections.ar.json')

    sec_en = {s['id']: s['title'] for s in sections_en}
    sec_ar = {s['id']: s['title'] for s in sections_ar}
    ar_map = {d['id']: d.get('text', '') for d in duas_ar}

    result = []
    for i, d in enumerate(duas_en):
        did = d.get('id', i + 1)
        sid = d.get('sectionId', '')
        result.append({
            'id': did,
            'sectionId': sid,
            'sectionTitle': sec_en.get(sid, d.get('sectionTitle', '')),
            'sectionTitleAr': sec_ar.get(sid, ''),
            'text': d.get('text', ''),
            'arabic': ar_map.get(did, '')
        })
    return result


HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#064e3b">
<title>1000 Dua – Arefe</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root{
  --bg:#f0fdf4;--surface:#fff;--card:#fff;
  --hdr:#064e3b;--hdr-txt:#a7f3d0;--hdr-sub:#6ee7b7;
  --txt:#111827;--txt-muted:#6b7280;--txt-soft:#374151;
  --accent:#059669;--accent-h:#047857;
  --accent-lite:#d1fae5;--border:#d1fae5;--border2:#e5e7eb;
  --shadow:0 4px 24px rgba(6,78,59,.10);
  --btn:#064e3b;--btn-txt:#fff;
  --in-bg:#fff;--in-border:#d1fae5;
  --badge-bg:#d1fae5;--badge-txt:#065f46;
  --bar-bg:#d1fae5;--bar-fill:#059669;
  --fav:#ef4444;--fav-bg:#fef2f2;
  --arabic:#1e3a2f;
  --del:#ef4444;
  --personal:#7c3aed;--personal-lite:#ede9fe;--personal-border:#c4b5fd;
}
@media(prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#0a0f14;--surface:#111827;--card:#1a2535;
    --hdr:#0d1f16;--hdr-txt:#6ee7b7;--hdr-sub:#34d399;
    --txt:#f1f5f9;--txt-muted:#94a3b8;--txt-soft:#cbd5e1;
    --accent:#34d399;--accent-h:#10b981;
    --accent-lite:#064e3b;--border:#1e3a2f;--border2:#1e293b;
    --shadow:0 4px 24px rgba(0,0,0,.45);
    --btn:#065f46;--btn-txt:#d1fae5;
    --in-bg:#1a2535;--in-border:#1e3a2f;
    --badge-bg:#064e3b;--badge-txt:#6ee7b7;
    --bar-bg:#1e3a2f;--bar-fill:#34d399;
    --fav:#f87171;--fav-bg:#450a0a;
    --arabic:#a7f3d0;
    --del:#f87171;
    --personal:#a78bfa;--personal-lite:#2e1065;--personal-border:#4c1d95;
  }
}
[data-theme="dark"]{
  --bg:#0a0f14;--surface:#111827;--card:#1a2535;
  --hdr:#0d1f16;--hdr-txt:#6ee7b7;--hdr-sub:#34d399;
  --txt:#f1f5f9;--txt-muted:#94a3b8;--txt-soft:#cbd5e1;
  --accent:#34d399;--accent-h:#10b981;
  --accent-lite:#064e3b;--border:#1e3a2f;--border2:#1e293b;
  --shadow:0 4px 24px rgba(0,0,0,.45);
  --btn:#065f46;--btn-txt:#d1fae5;
  --in-bg:#1a2535;--in-border:#1e3a2f;
  --badge-bg:#064e3b;--badge-txt:#6ee7b7;
  --bar-bg:#1e3a2f;--bar-fill:#34d399;
  --fav:#f87171;--fav-bg:#450a0a;
  --arabic:#a7f3d0;
  --del:#f87171;
  --personal:#a78bfa;--personal-lite:#2e1065;--personal-border:#4c1d95;
}
[data-theme="light"]{
  --bg:#f0fdf4;--surface:#fff;--card:#fff;
  --hdr:#064e3b;--hdr-txt:#a7f3d0;--hdr-sub:#6ee7b7;
  --txt:#111827;--txt-muted:#6b7280;--txt-soft:#374151;
  --accent:#059669;--accent-h:#047857;
  --accent-lite:#d1fae5;--border:#d1fae5;--border2:#e5e7eb;
  --shadow:0 4px 24px rgba(6,78,59,.10);
  --btn:#064e3b;--btn-txt:#fff;
  --in-bg:#fff;--in-border:#d1fae5;
  --badge-bg:#d1fae5;--badge-txt:#065f46;
  --bar-bg:#d1fae5;--bar-fill:#059669;
  --fav:#ef4444;--fav-bg:#fef2f2;
  --arabic:#1e3a2f;
  --del:#ef4444;
  --personal:#7c3aed;--personal-lite:#ede9fe;--personal-border:#c4b5fd;
}

html,body{height:100%}
body{
  font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  background:var(--bg);color:var(--txt);
  -webkit-font-smoothing:antialiased;
  padding-bottom:env(safe-area-inset-bottom,0px);
  overscroll-behavior:none;
}

/* ── HEADER ── */
header{
  position:sticky;top:0;z-index:20;
  background:var(--hdr);
  display:flex;align-items:center;justify-content:space-between;
  padding:10px 12px;
  padding-top:calc(10px + env(safe-area-inset-top,0px));
  padding-left:calc(12px + env(safe-area-inset-left,0px));
  padding-right:calc(12px + env(safe-area-inset-right,0px));
  box-shadow:0 2px 10px rgba(0,0,0,.25);
  gap:8px;
}
.logo{display:flex;align-items:center;gap:8px;min-width:0;flex:1}
.logo-moon{font-size:1.4rem;line-height:1;color:var(--hdr-txt);flex-shrink:0}
.logo-text{display:flex;flex-direction:column;min-width:0}
.logo-title{font-size:1rem;font-weight:700;color:var(--hdr-txt);letter-spacing:.01em;line-height:1.2;white-space:nowrap}
.logo-sub{font-size:.65rem;color:var(--hdr-sub);opacity:.9;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap}
.hdr-btns{display:flex;gap:5px;flex-shrink:0}
.icon-btn{
  width:36px;height:36px;
  background:rgba(255,255,255,.12);
  border:1px solid rgba(255,255,255,.18);
  border-radius:8px;
  color:var(--hdr-txt);font-size:.9rem;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;transition:background .15s;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
  user-select:none;
  font-weight:600;
}
.icon-btn:active{background:rgba(255,255,255,.3)}

/* ── CONTROLS ── */
.controls{
  background:var(--surface);
  border-bottom:1px solid var(--border2);
  padding:10px 14px 0;
  padding-left:calc(14px + env(safe-area-inset-left,0px));
  padding-right:calc(14px + env(safe-area-inset-right,0px));
}

/* Mode toggle */
.mode-row{display:flex;gap:6px;margin-bottom:8px}
.mode-btn{
  flex:1;height:36px;
  border-radius:50px;
  border:1.5px solid var(--border2);
  background:var(--in-bg);color:var(--txt-muted);
  font-size:.82rem;font-weight:600;cursor:pointer;
  transition:all .15s;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
}
.mode-btn.on{background:var(--btn);border-color:var(--btn);color:var(--btn-txt)}
.mode-btn.personal-on{background:var(--personal);border-color:var(--personal);color:#fff}

/* Search */
.search-wrap{position:relative;margin-bottom:8px}
.search-input{
  width:100%;
  padding:10px 40px 10px 14px;
  background:var(--in-bg);
  border:1.5px solid var(--in-border);
  border-radius:50px;
  color:var(--txt);font-size:.95rem;
  outline:none;
  -webkit-appearance:none;
  transition:border .15s,box-shadow .15s;
}
.search-input:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-lite)}
.search-input::placeholder{color:var(--txt-muted)}
.clear-btn{
  position:absolute;right:12px;top:50%;transform:translateY(-50%);
  background:none;border:none;
  color:var(--txt-muted);font-size:1rem;
  cursor:pointer;padding:6px;display:none;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
}
.clear-btn.visible{display:block}

/* Filter row */
.filter-row{display:flex;gap:8px;align-items:center;margin-bottom:8px}
.section-select{
  flex:1;
  padding:8px 28px 8px 12px;
  background:var(--in-bg);
  border:1.5px solid var(--in-border);
  border-radius:50px;
  color:var(--txt);font-size:.82rem;
  outline:none;
  -webkit-appearance:none;appearance:none;
  cursor:pointer;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%236b7280'/%3E%3C/svg%3E");
  background-repeat:no-repeat;
  background-position:right 10px center;
  touch-action:manipulation;
}
.fav-filter-btn{
  padding:8px 12px;
  border-radius:50px;
  border:1.5px solid var(--border);
  background:var(--in-bg);
  color:var(--txt-muted);
  font-size:.82rem;
  cursor:pointer;white-space:nowrap;
  transition:all .15s;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
}
.fav-filter-btn.on{background:var(--fav);border-color:var(--fav);color:#fff}

/* Font size row */
.fontsize-row{
  display:flex;align-items:center;gap:8px;
  margin-bottom:8px;justify-content:center;
}
.fs-btn{
  width:36px;height:32px;
  background:var(--in-bg);border:1.5px solid var(--in-border);
  border-radius:8px;color:var(--txt);
  cursor:pointer;font-weight:700;font-size:.85rem;
  display:flex;align-items:center;justify-content:center;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
  transition:background .1s;
  flex-shrink:0;
}
.fs-btn:active{background:var(--accent-lite)}
.fs-label{
  font-size:.78rem;color:var(--txt-muted);
  min-width:80px;text-align:center;font-weight:500;
}

/* Filter status */
.filter-status{
  min-height:20px;padding-bottom:6px;
  text-align:center;font-size:.77rem;
  color:var(--txt-muted);line-height:20px;
}

/* ── ADD DUA PANEL ── */
.add-panel{
  background:var(--surface);
  border-bottom:2px solid var(--personal-border);
  padding:14px;
  padding-left:calc(14px + env(safe-area-inset-left,0px));
  padding-right:calc(14px + env(safe-area-inset-right,0px));
  display:none;
}
.add-panel.visible{display:block}
.add-panel-title{
  font-size:.9rem;font-weight:700;color:var(--personal);
  margin-bottom:10px;
}
.add-field{margin-bottom:8px}
.add-field label{
  display:block;font-size:.75rem;font-weight:600;
  color:var(--txt-muted);margin-bottom:4px;letter-spacing:.03em;text-transform:uppercase;
}
.add-textarea{
  width:100%;min-height:60px;
  padding:10px 12px;
  background:var(--in-bg);border:1.5px solid var(--in-border);
  border-radius:10px;color:var(--txt);font-size:.95rem;
  outline:none;resize:vertical;
  font-family:system-ui,-apple-system,sans-serif;
  -webkit-appearance:none;
  transition:border .15s;
  line-height:1.5;
}
.add-textarea.rtl{
  direction:rtl;text-align:right;
  font-family:"Geeza Pro","Arabic Typesetting","Noto Naskh Arabic",system-ui,sans-serif;
  font-size:1.1rem;line-height:1.9;
}
.add-textarea:focus{border-color:var(--personal);box-shadow:0 0 0 3px var(--personal-lite)}
.add-textarea::placeholder{color:var(--txt-muted)}
.add-input{
  width:100%;padding:10px 12px;
  background:var(--in-bg);border:1.5px solid var(--in-border);
  border-radius:50px;color:var(--txt);font-size:.9rem;
  outline:none;-webkit-appearance:none;
  transition:border .15s;
}
.add-input:focus{border-color:var(--personal)}
.add-actions{display:flex;gap:8px;margin-top:10px}
.add-save-btn{
  flex:1;height:44px;
  background:var(--personal);color:#fff;
  border:none;border-radius:50px;
  font-size:.9rem;font-weight:700;cursor:pointer;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
  transition:opacity .15s;
}
.add-save-btn:active{opacity:.75}
.add-cancel-btn{
  height:44px;padding:0 20px;
  background:var(--surface);color:var(--txt-muted);
  border:1.5px solid var(--border2);border-radius:50px;
  font-size:.9rem;cursor:pointer;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
}

/* ── CARD AREA ── */
.card-area{
  padding:14px 14px 8px;
  padding-left:calc(14px + env(safe-area-inset-left,0px));
  padding-right:calc(14px + env(safe-area-inset-right,0px));
  display:flex;flex-direction:column;align-items:center;
}
.card{
  width:100%;max-width:640px;
  background:var(--card);
  border-radius:16px;
  box-shadow:var(--shadow);
  border:1px solid var(--border);
  padding:18px 18px 14px;
  transition:opacity .12s ease;
  will-change:opacity;
}
.card.personal-card{border-color:var(--personal-border)}
.card.fading{opacity:.35}
.card-top{
  display:flex;align-items:flex-start;justify-content:space-between;
  gap:8px;margin-bottom:14px;
}
.section-badge{
  background:var(--badge-bg);color:var(--badge-txt);
  font-size:.72rem;font-weight:600;
  padding:4px 11px;border-radius:50px;
  line-height:1.4;
  max-width:calc(100% - 100px);
  word-break:break-word;
}
.section-badge.personal-badge{
  background:var(--personal-lite);color:var(--personal);
}
.section-badge-ar{
  font-size:.65rem;opacity:.75;
  display:block;margin-top:1px;
  direction:rtl;
}
.card-btns{display:flex;gap:6px;flex-shrink:0}
.fav-btn,.del-btn{
  width:42px;height:42px;
  border-radius:50%;
  border:2px solid var(--border);
  background:var(--surface);
  font-size:1.1rem;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;transition:all .15s;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
}
.fav-btn{color:var(--txt-muted)}
.fav-btn.on{background:var(--fav-bg);border-color:var(--fav);color:var(--fav)}
.del-btn{color:var(--del);border-color:var(--border2);font-size:.9rem}
.del-btn:active{background:#fef2f2;border-color:var(--del)}

.arabic-text{
  font-size:1.45rem;line-height:1.95;
  direction:rtl;text-align:right;
  color:var(--arabic);
  margin-bottom:16px;
  word-spacing:.06em;
  font-family:"Geeza Pro","Arabic Typesetting","Noto Naskh Arabic","Traditional Arabic",system-ui,sans-serif;
}
.english-text{
  font-size:.96rem;line-height:1.68;
  color:var(--txt-soft);
  border-top:1px solid var(--border);
  padding-top:13px;
  margin-bottom:4px;
}
.card-num{
  text-align:center;
  font-size:.72rem;
  color:var(--txt-muted);
  margin-top:10px;
  letter-spacing:.04em;
}

.no-results{
  width:100%;max-width:640px;
  padding:48px 20px;
  text-align:center;
  color:var(--txt-muted);
  font-size:.95rem;line-height:1.65;
}
.add-first-btn{
  display:inline-block;margin-top:14px;
  padding:10px 22px;
  background:var(--personal);color:#fff;
  border:none;border-radius:50px;
  font-size:.88rem;font-weight:700;cursor:pointer;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
}

/* ── NAV ── */
.nav-row{
  padding:6px 14px;
  padding-left:calc(14px + env(safe-area-inset-left,0px));
  padding-right:calc(14px + env(safe-area-inset-right,0px));
  display:flex;align-items:center;gap:10px;
  max-width:640px;margin:0 auto;width:100%;
}
.nav-btn{
  min-width:80px;height:50px;
  background:var(--btn);color:var(--btn-txt);
  border:none;border-radius:50px;
  font-size:.88rem;font-weight:600;
  cursor:pointer;
  transition:background .15s,opacity .15s;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
  flex-shrink:0;
}
.nav-btn:active{opacity:.75}
.nav-btn:disabled{opacity:.35;cursor:default}
.progress-wrap{flex:1;display:flex;flex-direction:column;align-items:center;gap:5px}
.progress-text{font-size:.82rem;color:var(--txt-muted);font-weight:500}
.progress-bar{
  width:100%;height:5px;
  background:var(--bar-bg);border-radius:50px;overflow:hidden;
}
.progress-fill{
  height:100%;background:var(--bar-fill);
  border-radius:50px;transition:width .2s ease;
}

/* ── BOTTOM ROW ── */
.bottom-row{
  padding:6px 14px 14px;
  padding-left:calc(14px + env(safe-area-inset-left,0px));
  padding-right:calc(14px + env(safe-area-inset-right,0px));
  display:flex;gap:10px;justify-content:center;
  max-width:640px;margin:0 auto;width:100%;
}
.random-btn,.reset-btn{
  flex:1;max-width:200px;height:44px;
  border-radius:50px;
  font-size:.87rem;font-weight:600;
  cursor:pointer;
  transition:opacity .15s;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
}
.random-btn{background:var(--accent-lite);color:var(--accent);border:2px solid var(--accent-lite)}
.reset-btn{background:var(--surface);color:var(--txt-muted);border:2px solid var(--border2)}
.random-btn:active,.reset-btn:active{opacity:.7}

/* Add Dua floating button (personal mode) */
.add-dua-btn{
  position:fixed;
  bottom:calc(16px + env(safe-area-inset-bottom,0px));
  right:calc(16px + env(safe-area-inset-right,0px));
  width:52px;height:52px;
  background:var(--personal);color:#fff;
  border:none;border-radius:50%;
  font-size:1.6rem;font-weight:300;line-height:1;
  box-shadow:0 4px 16px rgba(124,58,237,.4);
  cursor:pointer;display:none;
  align-items:center;justify-content:center;
  z-index:15;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
}
.add-dua-btn.visible{display:flex}
.add-dua-btn:active{opacity:.8}

/* ── INFO MODAL ── */
.modal-overlay{
  display:none;
  position:fixed;inset:0;z-index:100;
  background:rgba(0,0,0,.55);
  align-items:center;justify-content:center;
  padding:20px;
  padding-top:calc(20px + env(safe-area-inset-top,0px));
}
.modal-overlay.visible{display:flex}
.modal-box{
  background:var(--card);
  border-radius:16px;
  padding:24px 20px 20px;
  max-width:420px;width:100%;
  box-shadow:0 20px 60px rgba(0,0,0,.3);
}
.modal-title{
  font-size:1.05rem;font-weight:700;
  color:var(--txt);margin-bottom:4px;
}
.modal-subtitle{
  font-size:.78rem;color:var(--accent);
  margin-bottom:14px;font-weight:600;
  letter-spacing:.04em;text-transform:uppercase;
}
.modal-body{
  font-size:.88rem;color:var(--txt-soft);
  line-height:1.65;margin-bottom:18px;
}
.modal-body p{margin-bottom:8px}
.modal-body p:last-child{margin-bottom:0}
.modal-divider{
  border:none;border-top:1px solid var(--border2);
  margin:16px 0;
}
.linkedin-btn{
  width:100%;height:46px;
  background:#0077b5;color:#fff;
  border:none;border-radius:50px;
  font-size:.9rem;font-weight:700;
  cursor:pointer;margin-bottom:10px;
  display:flex;align-items:center;justify-content:center;gap:8px;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
  text-decoration:none;
}
.linkedin-btn:active{opacity:.8}
.modal-close-btn{
  width:100%;height:42px;
  background:var(--surface);color:var(--txt-muted);
  border:1.5px solid var(--border2);border-radius:50px;
  font-size:.88rem;font-weight:600;cursor:pointer;
  -webkit-tap-highlight-color:transparent;
  touch-action:manipulation;
}
.modal-close-btn:active{opacity:.7}

/* ── RESPONSIVE ── */
@media(min-width:480px){
  .card{padding:24px 24px 18px}
  .arabic-text{font-size:1.6rem}
  .english-text{font-size:1rem}
}
@media(min-width:768px){
  .card-area,.nav-row,.bottom-row,.controls{padding-left:20px;padding-right:20px}
}
</style>
</head>
<body>

<!-- HEADER -->
<header>
  <div class="logo">
    <span class="logo-moon">☽</span>
    <div class="logo-text">
      <span class="logo-title">1000 Dua</span>
      <span class="logo-sub">Arefe Koleksiyonu</span>
    </div>
  </div>
  <div class="hdr-btns">
    <button class="icon-btn" id="fsDownBtn" type="button" title="Yazıyı küçült">A-</button>
    <button class="icon-btn" id="fsUpBtn"   type="button" title="Yazıyı büyüt">A+</button>
    <button class="icon-btn" id="infoBtn"   type="button" title="Hakkında">ℹ</button>
    <button class="icon-btn" id="themeBtn"  type="button" title="Temayı değiştir">☀</button>
  </div>
</header>

<!-- CONTROLS -->
<div class="controls">
  <div class="mode-row">
    <button class="mode-btn on" id="modeMain"     type="button">📖 1000 Dua</button>
    <button class="mode-btn"   id="modePersonal"  type="button">✍️ Benim Dualarım</button>
  </div>
  <div class="search-wrap">
    <input class="search-input" type="search" id="searchInput"
      placeholder="Dua ara…"
      autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
    <button class="clear-btn" id="clearSearch" type="button" aria-label="Temizle">✕</button>
  </div>
  <div class="filter-row">
    <select class="section-select" id="sectionSelect" aria-label="Bölüme göre filtrele"></select>
    <button class="fav-filter-btn" id="favFilterBtn" type="button">♡ Favoriler</button>
  </div>
  <div class="fontsize-row">
    <span class="fs-label" id="fsLabel">Yazı boyutu: Orta</span>
  </div>
  <div class="filter-status" id="filterStatus"></div>
</div>

<!-- ADD DUA PANEL (personal mode) -->
<div class="add-panel" id="addPanel">
  <div class="add-panel-title">✍️ Kişisel Dua Ekle</div>
  <div class="add-field">
    <label>Türkçe / Çeviri <span style="color:var(--del)">*</span></label>
    <textarea class="add-textarea" id="addEnglish" placeholder="Duayı Türkçe veya dilediğiniz dilde yazın…" rows="3"></textarea>
  </div>
  <div class="add-field">
    <label>Arapça (isteğe bağlı)</label>
    <textarea class="add-textarea rtl" id="addArabic" placeholder="أدخل الدعاء بالعربية (اختياري)" rows="3" dir="rtl" lang="ar"></textarea>
  </div>
  <div class="add-field">
    <label>Kategori / Konu (isteğe bağlı)</label>
    <input class="add-input" type="text" id="addCategory" placeholder="örn. Sağlık, Aile, İş…">
  </div>
  <div class="add-actions">
    <button class="add-save-btn"   id="addSaveBtn"   type="button">Duayı Kaydet</button>
    <button class="add-cancel-btn" id="addCancelBtn" type="button">İptal</button>
  </div>
</div>

<!-- CARD AREA -->
<div class="card-area">
  <div class="no-results" id="noResults" hidden></div>
  <div class="card" id="card">
    <div class="card-top">
      <div class="section-badge" id="sectionBadge"></div>
      <div class="card-btns">
        <button class="del-btn" id="delBtn" type="button" aria-label="Sil" hidden>🗑</button>
        <button class="fav-btn" id="favBtn" type="button" aria-label="Favori">♡</button>
      </div>
    </div>
    <div class="arabic-text" id="arabicText" dir="rtl" lang="ar"></div>
    <div class="english-text" id="englishText"></div>
    <div class="card-num" id="cardNum"></div>
  </div>
</div>

<!-- NAVIGATION -->
<div class="nav-row">
  <button class="nav-btn" id="prevBtn" type="button">◀ Önceki</button>
  <div class="progress-wrap">
    <div class="progress-text" id="progressText"></div>
    <div class="progress-bar" role="progressbar">
      <div class="progress-fill" id="progressFill"></div>
    </div>
  </div>
  <button class="nav-btn" id="nextBtn" type="button">Sonraki ▶</button>
</div>

<!-- BOTTOM ROW -->
<div class="bottom-row">
  <button class="random-btn" id="randomBtn" type="button">⚡ Rastgele</button>
  <button class="reset-btn"  id="resetBtn"  type="button">↺ Sıfırla</button>
</div>

<!-- FLOATING ADD BUTTON -->
<button class="add-dua-btn" id="addDuaBtn" type="button" title="Yeni dua ekle" aria-label="Dua ekle">+</button>

<!-- INFO MODAL -->
<div class="modal-overlay" id="infoModal">
  <div class="modal-box">
    <div class="modal-title">1000 Dua – Arefe Koleksiyonu</div>
    <div class="modal-subtitle">Çevrimdışı Dua Kartları Uygulaması</div>
    <div class="modal-body">
      <p>Bu uygulama, Arefe günü ve yıl boyunca tefekkür, ibadet ve dua için hazırlanmış 1.000 dua içerir. Tüm veriler yerel olarak gömülüdür — internet bağlantısı gerekmez.</p>
      <p>Duaların güvenilirliğini her zaman güvenilir İslami ilim kaynaklarıyla teyit edin. Bu uygulama kişisel manevi kullanım için sunulmuştur ve herhangi bir kurumla bağlantılı değildir.</p>
    </div>
    <hr class="modal-divider">
    <a class="linkedin-btn" href="https://www.reddit.com/user/Hanuonbenz/" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z"/></svg>
      Reddit Profilini Ziyaret Et
    </a>
    <button class="modal-close-btn" id="modalCloseBtn" type="button">Kapat</button>
  </div>
</div>

<script>
(function(){
'use strict';

/* ── EMBEDDED DATA ── */
var DUAS = __DUAS_DATA__;

/* ── FONT SIZE CONFIG ── */
var FS_LEVELS = [
  {label:'Çok Küçük', en:'0.80rem', ar:'1.15rem'},
  {label:'Küçük',   en:'0.88rem', ar:'1.28rem'},
  {label:'Orta',  en:'0.96rem', ar:'1.45rem'},
  {label:'Büyük',   en:'1.08rem', ar:'1.65rem'},
  {label:'Çok Büyük', en:'1.22rem', ar:'1.88rem'}
];
var FS_DEFAULT = 2;

/* ── STORAGE ── */
var LS = {
  get:function(k){try{return localStorage.getItem(k);}catch(e){return null;}},
  set:function(k,v){try{localStorage.setItem(k,v);}catch(e){}},
};

/* ── STATE ── */
var S = {
  filtered:[],
  idx:0,
  favorites:[],
  theme:'auto',
  sectionId:'',
  showFavOnly:false,
  query:'',
  mode:'main',        /* 'main' | 'personal' */
  personalDuas:[],
  fsLevel:FS_DEFAULT,
  addPanelOpen:false
};

/* ── SECTION MAP (main duas) ── */
var mainSectionMap = {};
DUAS.forEach(function(d){
  if (d.sectionId && !mainSectionMap[d.sectionId]){
    mainSectionMap[d.sectionId] = {id:d.sectionId, title:d.sectionTitle, titleAr:d.sectionTitleAr};
  }
});

/* ── HELPERS ── */
function isFav(id){return S.favorites.indexOf(id) >= 0;}
function addFav(id){if(!isFav(id))S.favorites.push(id);}
function delFav(id){S.favorites=S.favorites.filter(function(x){return x!==id;});}

function currentSource(){
  return S.mode==='personal' ? S.personalDuas : DUAS;
}

function getSectionMap(){
  if(S.mode==='main') return mainSectionMap;
  var m={};
  S.personalDuas.forEach(function(d){
    if(d.sectionId && !m[d.sectionId]){
      m[d.sectionId]={id:d.sectionId,title:d.sectionTitle,titleAr:''};
    }
  });
  return m;
}

function escHtml(s){
  return String(s)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}

/* ── PERSIST ── */
function persist(){
  var cur=S.filtered[S.idx];
  if(cur) LS.set('d_lid',String(cur.id));
  LS.set('d_favs',JSON.stringify(S.favorites));
  LS.set('d_theme',S.theme);
  LS.set('d_section',S.sectionId);
  LS.set('d_favOnly',S.showFavOnly?'1':'0');
  LS.set('d_query',S.query);
  LS.set('d_mode',S.mode);
  LS.set('d_personal',JSON.stringify(S.personalDuas));
  LS.set('d_fs',String(S.fsLevel));
}

function restoreState(){
  var favs=LS.get('d_favs');
  if(favs){try{S.favorites=JSON.parse(favs);}catch(e){}}
  var t=LS.get('d_theme');if(t)S.theme=t;
  var sec=LS.get('d_section');if(sec!==null)S.sectionId=sec;
  if(LS.get('d_favOnly')==='1')S.showFavOnly=true;
  var q=LS.get('d_query');if(q)S.query=q;
  var m=LS.get('d_mode');if(m==='personal')S.mode='personal';
  var pd=LS.get('d_personal');
  if(pd){try{S.personalDuas=JSON.parse(pd);}catch(e){}}
  var fs=parseInt(LS.get('d_fs'));
  if(!isNaN(fs)&&fs>=0&&fs<FS_LEVELS.length)S.fsLevel=fs;
}

/* ── THEME ── */
var themeBtn=document.getElementById('themeBtn');
function applyTheme(){
  var root=document.documentElement;
  if(S.theme==='dark'){root.setAttribute('data-theme','dark');themeBtn.textContent='☀';}
  else if(S.theme==='light'){root.setAttribute('data-theme','light');themeBtn.textContent='☾';}
  else{root.removeAttribute('data-theme');themeBtn.textContent=window.matchMedia&&window.matchMedia('(prefers-color-scheme:dark)').matches?'☀':'☾';}
}
themeBtn.addEventListener('click',function(){
  var o=['auto','dark','light'];
  S.theme=o[(o.indexOf(S.theme)+1)%o.length];
  applyTheme();persist();
});

/* ── FONT SIZE ── */
var fsLabel=document.getElementById('fsLabel');
function applyFontSize(){
  var lv=FS_LEVELS[S.fsLevel];
  document.getElementById('arabicText').style.fontSize=lv.ar;
  document.getElementById('englishText').style.fontSize=lv.en;
  fsLabel.textContent='Yazı boyutu: '+lv.label;
}
document.getElementById('fsDownBtn').addEventListener('click',function(){
  if(S.fsLevel>0){S.fsLevel--;applyFontSize();persist();}
});
document.getElementById('fsUpBtn').addEventListener('click',function(){
  if(S.fsLevel<FS_LEVELS.length-1){S.fsLevel++;applyFontSize();persist();}
});

/* ── MODE TOGGLE ── */
var btnMain=document.getElementById('modeMain');
var btnPersonal=document.getElementById('modePersonal');
var addDuaBtn=document.getElementById('addDuaBtn');

function applyModeUI(){
  var personal=S.mode==='personal';
  btnMain.classList.toggle('on',!personal);
  btnPersonal.classList.toggle('personal-on',personal);
  btnPersonal.classList.toggle('on',false);
  btnMain.classList.toggle('personal-on',false);
  addDuaBtn.classList.toggle('visible',personal);
}

function switchMode(mode){
  S.mode=mode;
  S.sectionId='';
  S.showFavOnly=false;
  S.query='';
  document.getElementById('searchInput').value='';
  document.getElementById('clearSearch').classList.remove('visible');
  favFilterBtn.classList.remove('on');
  favFilterBtn.textContent='♡ Favoriler';
  closeAddPanel();
  applyModeUI();
  rebuildSectionSelect();
  applyFilter(null);
  render();
  persist();
}

btnMain.addEventListener('click',function(){if(S.mode!=='main')switchMode('main');});
btnPersonal.addEventListener('click',function(){if(S.mode!=='personal')switchMode('personal');});

/* ── SECTION SELECT ── */
var sectionSelect=document.getElementById('sectionSelect');
function rebuildSectionSelect(){
  var src=currentSource();
  var total=src.length;
  var sm=getSectionMap();
  var secs=Object.values(sm);
  sectionSelect.innerHTML='<option value="">Tümü ('+(S.mode==='personal'?'Benim ':'')+total+' dua)</option>'+
    secs.map(function(s){return '<option value="'+s.id+'">'+escHtml(s.title)+'</option>';}).join('');
  if(S.sectionId) sectionSelect.value=S.sectionId;
}

sectionSelect.addEventListener('change',function(){
  S.sectionId=this.value;
  applyFilter();render();persist();
});

/* ── FILTER ── */
function computeFiltered(){
  var src=currentSource();
  var q=S.query.trim().toLowerCase();
  return src.filter(function(d){
    if(S.sectionId&&d.sectionId!==S.sectionId)return false;
    if(S.showFavOnly&&!isFav(d.id))return false;
    if(q){
      if(d.text.toLowerCase().indexOf(q)<0&&
         d.arabic.toLowerCase().indexOf(q)<0&&
         d.sectionTitle.toLowerCase().indexOf(q)<0)return false;
    }
    return true;
  });
}

function applyFilter(keepId){
  var prevId=(keepId!==undefined)?keepId:(S.filtered[S.idx]?S.filtered[S.idx].id:null);
  S.filtered=computeFiltered();
  if(prevId!==null&&S.filtered.length>0){
    var ni=-1;
    for(var i=0;i<S.filtered.length;i++){if(S.filtered[i].id===prevId){ni=i;break;}}
    S.idx=ni>=0?ni:0;
  } else {S.idx=0;}
}

/* ── RENDER ── */
var elCard=document.getElementById('card');
var elNoRes=document.getElementById('noResults');
var elBadge=document.getElementById('sectionBadge');
var elArabic=document.getElementById('arabicText');
var elEnglish=document.getElementById('englishText');
var elCardNum=document.getElementById('cardNum');
var elFavBtn=document.getElementById('favBtn');
var elDelBtn=document.getElementById('delBtn');
var elPrev=document.getElementById('prevBtn');
var elNext=document.getElementById('nextBtn');
var elProgTxt=document.getElementById('progressText');
var elProgFil=document.getElementById('progressFill');
var elStatus=document.getElementById('filterStatus');
var favFilterBtn=document.getElementById('favFilterBtn');

function render(){
  var personal=S.mode==='personal';

  if(S.filtered.length===0){
    elCard.hidden=true;
    elNoRes.hidden=false;
    if(personal&&S.personalDuas.length===0){
      elNoRes.innerHTML='<div>Henüz kişisel dua yok.</div><button class="add-first-btn" id="addFirstBtn" type="button">+ İlk Duanı Ekle</button>';
      var afb=document.getElementById('addFirstBtn');
      if(afb)afb.addEventListener('click',openAddPanel);
    } else if(S.showFavOnly){
      elNoRes.textContent='Henüz favori yok. Herhangi bir duada ♥ simgesine dokunun.';
    } else {
      elNoRes.textContent='Aramanızla eşleşen dua yok.';
    }
    elProgTxt.textContent='0 / 0';
    elProgFil.style.width='0%';
    elStatus.textContent='';
    elPrev.disabled=true;elNext.disabled=true;
    return;
  }

  elCard.hidden=false;elNoRes.hidden=true;

  var d=S.filtered[S.idx];
  var total=S.filtered.length;
  var pos=S.idx+1;

  elBadge.innerHTML=escHtml(d.sectionTitle||'Kişisel Dua')+
    (d.sectionTitleAr?'<span class="section-badge-ar">'+escHtml(d.sectionTitleAr)+'</span>':'');
  elBadge.className='section-badge'+(personal?' personal-badge':'');

  elArabic.textContent=d.arabic||'';
  elArabic.style.display=d.arabic?'':'none';

  elEnglish.textContent=d.text||'';
  elEnglish.style.paddingTop=d.arabic?'':'0';
  elEnglish.style.borderTop=d.arabic?'':'none';

  elCardNum.textContent=(personal?'Benim Duam':'Dua')+(personal?'':', #'+d.id+' / 1000');

  elCard.className='card'+(personal?' personal-card':'');

  var fav=isFav(d.id);
  elFavBtn.textContent=fav?'♥':'♡';
  elFavBtn.classList.toggle('on',fav);

  elDelBtn.hidden=!personal;

  elProgTxt.textContent=pos+' / '+total;
  elProgFil.style.width=(pos/total*100).toFixed(1)+'%';

  elPrev.disabled=S.idx===0;
  elNext.disabled=S.idx===total-1;

  var sm=getSectionMap();
  var parts=[];
  if(S.sectionId&&sm[S.sectionId])parts.push(sm[S.sectionId].title);
  if(S.showFavOnly)parts.push('Favoriler');
  if(S.query.trim())parts.push('"'+S.query.trim()+'"');
  elStatus.textContent=parts.length?total+' dua · '+parts.join(' · '):'';
}

/* ── NAVIGATION ── */
function flashGo(idx){
  if(idx<0||idx>=S.filtered.length)return;
  S.idx=idx;
  elCard.classList.add('fading');
  requestAnimationFrame(function(){
    render();
    requestAnimationFrame(function(){elCard.classList.remove('fading');});
  });
  persist();
}
function next(){flashGo(S.idx+1);}
function prev(){flashGo(S.idx-1);}
function random(){
  if(S.filtered.length<2)return;
  var ni;do{ni=Math.floor(Math.random()*S.filtered.length);}while(ni===S.idx);
  flashGo(ni);
}

document.getElementById('nextBtn').addEventListener('click',next);
document.getElementById('prevBtn').addEventListener('click',prev);
document.getElementById('randomBtn').addEventListener('click',random);

document.getElementById('resetBtn').addEventListener('click',function(){
  S.query='';S.sectionId='';S.showFavOnly=false;
  document.getElementById('searchInput').value='';
  document.getElementById('clearSearch').classList.remove('visible');
  sectionSelect.value='';
  favFilterBtn.classList.remove('on');
  favFilterBtn.textContent='♡ Favoriler';
  applyFilter(null);render();persist();
});

/* ── FAVORITE ── */
elFavBtn.addEventListener('click',function(){
  var d=S.filtered[S.idx];if(!d)return;
  if(isFav(d.id))delFav(d.id);else addFav(d.id);
  if(S.showFavOnly&&!isFav(d.id))applyFilter();
  render();persist();
});

/* ── DELETE (personal) ── */
elDelBtn.addEventListener('click',function(){
  var d=S.filtered[S.idx];if(!d)return;
  if(!confirm('Bu kişisel dua silinsin mi?'))return;
  S.personalDuas=S.personalDuas.filter(function(x){return x.id!==d.id;});
  delFav(d.id);
  rebuildSectionSelect();
  applyFilter(null);
  render();persist();
});

/* ── FAV FILTER ── */
favFilterBtn.addEventListener('click',function(){
  S.showFavOnly=!S.showFavOnly;
  favFilterBtn.classList.toggle('on',S.showFavOnly);
  favFilterBtn.textContent=S.showFavOnly?'♥ Favoriler':'♡ Favoriler';
  applyFilter();render();persist();
});

/* ── SEARCH ── */
var searchInput=document.getElementById('searchInput');
var clearBtn=document.getElementById('clearSearch');
var searchTimer;
searchInput.addEventListener('input',function(){
  S.query=this.value;
  clearBtn.classList.toggle('visible',S.query.length>0);
  clearTimeout(searchTimer);
  searchTimer=setTimeout(function(){applyFilter();render();persist();},220);
});
clearBtn.addEventListener('click',function(){
  searchInput.value='';S.query='';clearBtn.classList.remove('visible');
  applyFilter();render();persist();
});

/* ── ADD PANEL ── */
var addPanel=document.getElementById('addPanel');
function openAddPanel(){
  S.addPanelOpen=true;
  addPanel.classList.add('visible');
  addDuaBtn.style.display='none';
  document.getElementById('addEnglish').focus();
}
function closeAddPanel(){
  S.addPanelOpen=false;
  addPanel.classList.remove('visible');
  if(S.mode==='personal')addDuaBtn.style.display='';
  document.getElementById('addEnglish').value='';
  document.getElementById('addArabic').value='';
  document.getElementById('addCategory').value='';
}

addDuaBtn.addEventListener('click',openAddPanel);
document.getElementById('addCancelBtn').addEventListener('click',closeAddPanel);

document.getElementById('addSaveBtn').addEventListener('click',function(){
  var eng=document.getElementById('addEnglish').value.trim();
  var ar=document.getElementById('addArabic').value.trim();
  var cat=document.getElementById('addCategory').value.trim();
  if(!eng){alert('Lütfen en azından Türkçe / çeviri metnini girin.');return;}
  var id=Date.now();
  var sid=cat?cat.toLowerCase().replace(/\s+/g,'-'):'personal';
  var newDua={id:id,sectionId:sid,sectionTitle:cat||'Kişisel Dua',sectionTitleAr:'',text:eng,arabic:ar};
  S.personalDuas.push(newDua);
  closeAddPanel();
  rebuildSectionSelect();
  applyFilter(id);
  render();persist();
});

/* ── INFO MODAL ── */
var infoModal=document.getElementById('infoModal');
document.getElementById('infoBtn').addEventListener('click',function(){
  infoModal.classList.add('visible');
});
document.getElementById('modalCloseBtn').addEventListener('click',function(){
  infoModal.classList.remove('visible');
});
infoModal.addEventListener('click',function(e){
  if(e.target===infoModal)infoModal.classList.remove('visible');
});

/* ── KEYBOARD ── */
document.addEventListener('keydown',function(e){
  if(e.target===searchInput)return;
  if(e.key==='ArrowRight'){e.preventDefault();next();}
  else if(e.key==='ArrowLeft'){e.preventDefault();prev();}
  else if((e.key==='f'||e.key==='F')&&!infoModal.classList.contains('visible')){
    var d=S.filtered[S.idx];
    if(d){if(isFav(d.id))delFav(d.id);else addFav(d.id);render();persist();}
  }
  else if(e.key==='Escape')infoModal.classList.remove('visible');
});

/* ── SWIPE ── */
var swipeX=0,swipeY=0;
document.addEventListener('touchstart',function(e){
  swipeX=e.changedTouches[0].screenX;
  swipeY=e.changedTouches[0].screenY;
},{passive:true});
document.addEventListener('touchend',function(e){
  if(e.target.closest('select,input,button,textarea,a'))return;
  var dx=e.changedTouches[0].screenX-swipeX;
  var dy=e.changedTouches[0].screenY-swipeY;
  if(Math.abs(dx)>Math.abs(dy)&&Math.abs(dx)>48){
    if(dx<0)next();else prev();
  }
},{passive:true});

/* ── INIT ── */
restoreState();
applyTheme();
applyFontSize();
applyModeUI();

/* Restore UI controls */
if(S.showFavOnly){favFilterBtn.classList.add('on');favFilterBtn.textContent='♥ Favoriler';}
if(S.query){searchInput.value=S.query;clearBtn.classList.add('visible');}

rebuildSectionSelect();

/* Restore last position */
var lastId=null;
try{lastId=parseInt(LS.get('d_lid'));}catch(e){}
applyFilter(isNaN(lastId)?null:lastId);
if(!isNaN(lastId)&&S.filtered.length>0){
  var ni=-1;
  for(var i=0;i<S.filtered.length;i++){if(S.filtered[i].id===lastId){ni=i;break;}}
  if(ni>=0)S.idx=ni;
}
render();

})();
</script>
</body>
</html>'''


def main():
    print('Veri klasörü:', DATA_DIR)
    if not os.path.isdir(DATA_DIR):
        print('HATA: Veri klasörü bulunamadı:', DATA_DIR)
        sys.exit(1)

    duas = normalize_duas()
    print('Hazırlandı:', len(duas), 'dua')

    os.makedirs(OUT_DIR, exist_ok=True)
    duas_json = json.dumps(duas, ensure_ascii=False)
    html = HTML_TEMPLATE.replace('__DUAS_DATA__', duas_json)

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    size_kb = os.path.getsize(OUT_FILE) / 1024
    print('Oluşturuldu:', OUT_FILE, '(%.1f KB)' % size_kb)
    print('Tamamlandı.')


if __name__ == '__main__':
    main()
