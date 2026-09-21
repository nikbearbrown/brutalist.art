#!/usr/bin/env python3
"""Scripted-browser 4K capture of Medhavy Hub for medhavy-walkthrough.

Drives a saved human session (never types credentials) through a JSON step
plan, records native 3840x2160 video, masks names/emails in the DOM at capture
time (disclosed in capture/redaction.jsonl), and writes an action log.

  capture_admin.py REEL --run run-01 --plan plan.json [--state ~/.medhavy-walkthrough/brutalist-session.json]

Plan: {"base_url": "...", "context": "admin", "steps": [
  {"goto": "/admin"}, {"click_button": "Users"}, {"wait_ms": 2500},
  {"click_text": "Import"}, {"screenshot": "users"}, {"scroll": 800},
  {"fill_placeholder": ["e.g. 20260411_120000", "20260421_120000"]}, {"press": "Escape"} ]}
"""
import argparse, hashlib, json, shutil, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

MASK = r"""
(() => {
  const EMAIL=/[\w.+-]+@[\w-]+\.[\w.]+/g;
  const CODE=/\bCLS-[A-Z0-9]{4,10}\b/g;
  const NAME=/^(?:[A-Z][a-z]+|[A-Z]{2,})(?:[ .'-](?:[A-Z][a-z.]+|[A-Z]{2,}))+$/;
  const KEEP=/^(Nik Bear|Admin Dashboard|Admin Control Panel|View All Textbooks|Manage Textbooks|View Admins|Concept Maps|Access Requests|User Management|Admin Users|All Classes|All Textbooks|Textbook Management|Analytics Dashboard|Add Textbook|Open Textbook|Create Class|Grant Access|Most Engaged Users|Top Textbooks|Recent Activity|Platform Breakdown|Daily Active Users|Electron Microscopy|Quantum Mechanics|Physics|Total Users|Admin role locked)/;
  const SKIP=new Set(['BUTTON','SELECT','OPTION','A','H1','H2','H3','LABEL','TH']);
  const state = window.__mwMask || (window.__mwMask={emails:0,names:0,seen:new Map(),installed:false});
  const NAMES_ON = (window.__mwNameHosts||[]).includes(location.host);
  const textNodes=(root)=>{const out=[];const it=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let t;while((t=it.nextNode()))out.push(t);return out;};
  const maskNode=(t)=>{ if(!t.parentElement||SKIP.has(t.parentElement.tagName)) return; const s=t.nodeValue.trim(); if(!s||/^(student|instructor|admin|pending)$/.test(s)||KEEP.test(s)||/^Role:/i.test(s)||/@example\.edu/.test(s)||/^Learner \d+$/.test(s)) return;
      if(/^\d|^[A-Z]{2,4}-|^https?:|^\d+ (Students?|Instructors?)/.test(s)) return;
      t.nodeValue=t.nodeValue.replace(s,'Learner '+(++state.names)); };
  const walk=(root)=>{ if(!root) return; const nodes=textNodes(root); const cards=new Set(); const nameEls=new Set();
    for(const t of nodes){ if(t.nodeValue&&CODE.test(t.nodeValue)){ CODE.lastIndex=0; t.nodeValue=t.nodeValue.replace(CODE,'CLS-XXXXXX'); state.codes=(state.codes||0)+1; } CODE.lastIndex=0; }
    for(const t of nodes){ const v=t.nodeValue; if(!v||!v.includes('@')) continue;
      const nv=v.replace(EMAIL,m=>{ if(/@example\.edu$/.test(m)) return m; if(!state.seen.has(m)) state.seen.set(m,`learner${++state.emails}@example.edu`); return state.seen.get(m);});
      if(nv!==v){ t.nodeValue=nv; const el=t.parentElement; const c=(el&&el.parentElement&&el.parentElement!==document.body)?el.parentElement:el; cards.add(c); const prev=el&&el.previousElementSibling; if(prev&&!SKIP.has(prev.tagName)&&!/@/.test(prev.textContent)) nameEls.add(prev);} }
    if(NAMES_ON) for(const c of cards){ for(const t of textNodes(c)){ if(t.nodeValue.includes('@')) continue; const el=t.parentElement; if(!el||SKIP.has(el.tagName)) continue; const s=t.nodeValue.trim(); if(NAME.test(s)&&!KEEP.test(s)&&!/^Learner \d+$/.test(s)) t.nodeValue=t.nodeValue.replace(s,'Learner '+(++state.names)); } }
    if(NAMES_ON) for(const el of nameEls){ const ts=textNodes(el).filter(t=>t.nodeValue.trim()&&!/^Learner \d+$/.test(t.nodeValue.trim())&&!KEEP.test(t.nodeValue.trim())&&!/^(student|instructor|admin|pending)$/.test(t.nodeValue.trim())&&!/^Role:/i.test(t.nodeValue.trim())&&!/^\d|^https?:/.test(t.nodeValue.trim())); if(!ts.length) continue; ts[0].nodeValue='Learner '+(++state.names); for(let i=1;i<ts.length;i++) ts[i].nodeValue=''; }
    if(NAMES_ON) for(const t of nodes){ if(!t.parentElement||t.nodeValue.includes('@')) continue; const s=t.nodeValue.trim(); const el=t.parentElement;
      if(NAME.test(s)&&!KEEP.test(s)&&!SKIP.has(el.tagName)&&el.closest('td,li,tr,[class*=user],[class*=User],[class*=member],[class*=Member],[class*=student],[class*=Student],[class*=card],[class*=Card],[class*=row],[class*=Row],[class*=list],[class*=List],[class*=activity],[class*=Activity]')) t.nodeValue=t.nodeValue.replace(s,'Learner '+(++state.names)); } };
  const install=()=>{ if(state.installed||!document.body) return; state.installed=true; walk(document.body);
    new MutationObserver(ms=>{ let dirty=false; for(const r of ms){ if(r.type==='childList'&&r.addedNodes.length) dirty=true; } if(dirty&&!state.busy){ state.busy=true; try{ walk(document.body);} finally{ state.busy=false; } } })
      .observe(document.body,{childList:true,subtree:true}); };
  if(document.body) install(); else document.addEventListener('DOMContentLoaded',install,{once:true});
  window.__mwWalk=()=>walk(document.body);
  window.__mwLeaks=()=>{ const txt=document.body.innerText||''; const m=txt.match(EMAIL)||[]; const c=(txt.match(/\bCLS-[A-Z0-9]{4,10}\b/g)||[]).filter(x=>x!=='CLS-XXXXXX'); return m.filter(x=>!/@example\.edu$/.test(x)).length + c.length; };
})();
"""

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('reel', type=Path)
    ap.add_argument('--run', required=True)
    ap.add_argument('--plan', required=True, type=Path)
    ap.add_argument('--state', type=Path, default=Path.home() / '.medhavy-walkthrough' / 'brutalist-session.json')
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--no-session', action='store_true', help='fresh context, signed out (landing / sign-in / sign-up pages only; nothing is typed)')
    ap.add_argument('--css-size', default='3840x2160', help='CSS viewport WxH; with --dpr the physical capture stays 3840x2160')
    ap.add_argument('--dpr', type=float, default=1.0, help='device pixel ratio; css_size * dpr must equal 3840x2160')
    a = ap.parse_args()
    plan = json.loads(a.plan.read_text())
    reel = a.reel.resolve(); cap = reel / 'capture'; cap.mkdir(parents=True, exist_ok=True)
    tmp = cap / f'.{a.run}-raw'; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir()
    actions, redaction = [], []
    W, H = 3840, 2160
    cw, ch = (int(x) for x in a.css_size.lower().split('x'))
    assert abs(cw * a.dpr - W) < 1 and abs(ch * a.dpr - H) < 1, 'css_size * dpr must equal 3840x2160'
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True, args=[f'--window-size={cw},{ch}', f'--force-device-scale-factor={a.dpr}'])
        c = b.new_context(storage_state=None if a.no_session else str(a.state), viewport={'width': cw, 'height': ch}, device_scale_factor=a.dpr,
                          record_video_dir=str(tmp), record_video_size={'width': W, 'height': H})
        from urllib.parse import urlparse
        c.add_init_script(f"window.__mwNameHosts={json.dumps([urlparse(plan['base_url']).netloc])};")
        c.add_init_script(MASK)
        p = c.new_page(); t0 = time.time(); pages = [p]
        def log(action, detail):
            actions.append({'t_ms': int((time.time() - t0) * 1000), 'action': action, 'selector_or_text': detail, 'url_after': p.url})
        leaks_seen = 0
        def note_mask(step):
            nonlocal leaks_seen
            p.evaluate('window.__mwWalk && window.__mwWalk()')
            m = p.evaluate('({e:(window.__mwMask||{}).emails||0, n:(window.__mwMask||{}).names||0, leaks: window.__mwLeaks ? window.__mwLeaks() : -1})')
            leaks_seen += max(m['leaks'], 0)
            redaction.append({'t_ms': int((time.time() - t0) * 1000), 'step': step, 'masked_emails': m['e'], 'masked_names': m['n'], 'raw_emails_or_codes_visible': m['leaks'], 'method': 'dom-text-substitution-at-capture'})
        for i, s in enumerate(plan['steps']):
            if 'goto' in s:
                p.goto(plan['base_url'] + s['goto'], wait_until='networkidle', timeout=60000); p.evaluate(MASK); p.evaluate('window.__mwWalk()'); log('goto', s['goto'])
            elif 'click_button' in s:
                loc = p.get_by_role('button', name=s['click_button'], exact=True)
                if loc.count() == 0:  # accessible name may carry a count/badge after the label
                    loc = p.get_by_role('button', name=s['click_button'], exact=False)
                loc.first.scroll_into_view_if_needed(); loc.first.click(timeout=10000); log('click', s['click_button'])
            elif 'click_text' in s:
                p.get_by_text(s['click_text'], exact=True).first.click(timeout=10000); log('click', s['click_text'])
            elif 'fill_placeholder' in s:
                ph, val = s['fill_placeholder']; p.get_by_placeholder(ph).first.fill(val); log('fill', ph)
            elif 'press' in s:
                p.keyboard.press(s['press']); log('press', s['press'])
            elif 'scroll' in s:
                p.mouse.wheel(0, s['scroll']); log('scroll', str(s['scroll']))
            elif 'hover_button' in s:
                p.get_by_role('button', name=s['hover_button'], exact=True).first.hover(); log('hover', s['hover_button'])
            elif 'open_textbook' in s:
                card = p.locator(f"text={s['open_textbook']}").first.locator('xpath=ancestor::*[.//button[contains(., "Open Textbook")]][1]')
                with c.expect_page(timeout=15000) as pi:
                    card.get_by_role('button', name='Open Textbook').first.click()
                newp = pi.value; newp.wait_for_load_state('networkidle', timeout=60000)
                pages.append(newp); p = newp; p.evaluate(MASK); p.evaluate('window.__mwWalk()'); log('open_textbook', s['open_textbook'])
            elif 'type_placeholder' in s:
                ph, val = s['type_placeholder']; box = p.get_by_placeholder(ph).first; box.click(); box.type(val, delay=s.get('delay_ms', 45)); log('type', ph)
            elif 'type_active' in s:
                p.keyboard.type(s['type_active'], delay=s.get('delay_ms', 45)); log('type_active', s['type_active'])
            elif 'scroll_in' in s:
                sel, dy = s['scroll_in']; p.locator(sel).first.hover(); p.mouse.wheel(0, dy); log('scroll_in', f'{sel} {dy}')
            elif 'click_link' in s:
                p.get_by_role('link', name=s['click_link'], exact=False).first.click(timeout=10000); p.wait_for_load_state('networkidle', timeout=60000); log('click_link', s['click_link'])
            elif 'wait_for_text' in s:
                p.get_by_text(s['wait_for_text'], exact=False).first.wait_for(timeout=s.get('timeout_ms', 90000)); log('wait_for_text', s['wait_for_text'])
            elif 'wait_settled' in s:
                # wait until the page text stops changing (streaming AI answer), capped
                last = ''; stable = 0; capms = s.get('timeout_ms', 120000); t1 = time.time()
                while (time.time() - t1) * 1000 < capms:
                    p.wait_for_timeout(1500); cur = p.evaluate('document.body.innerText.length')
                    stable = stable + 1 if cur == last else 0; last = cur
                    if stable >= s.get('stable_ticks', 3): break
                log('wait_settled', str(int((time.time() - t1) * 1000)))
            elif 'wait_ms' in s:
                p.wait_for_timeout(s['wait_ms']); log('wait', str(s['wait_ms']))
            elif 'screenshot' in s:
                p.screenshot(path=str(cap / f'{a.run}-{s["screenshot"]}.png')); log('screenshot', s['screenshot'])
            else:
                raise SystemExit(f'unknown step {i}: {s}')
            p.wait_for_timeout(s.get('settle_ms', 400)); note_mask(i)
        log('end', ''); vids = [pg.video.path() for pg in pages]; c.close(); b.close()
    if leaks_seen:
        shutil.rmtree(tmp)
        for f in cap.glob(f'{a.run}-*.png'): f.unlink()
        raise SystemExit(f'LEAK: {leaks_seen} raw email sightings across steps; capture discarded. Fix the mask before rerunning.')
    outs = []
    for i, webm in enumerate(vids):
        webm = Path(webm); suffix = '' if i == 0 else f'-p{i+1}'
        mp4 = cap / f'{a.run}{suffix}.mp4'; outs.append(mp4)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(webm), '-c:v', 'libx264', '-preset', 'medium', '-crf', '14',
                        '-pix_fmt', 'yuv420p', '-r', str(a.fps), '-an', str(mp4)], check=True)
    shutil.rmtree(tmp); mp4 = outs[0]
    (cap / f'{a.run}-actions.jsonl').write_text('\n'.join(json.dumps(x) for x in actions) + '\n')
    with open(cap / 'redaction.jsonl', 'a') as f:
        for r in redaction: f.write(json.dumps({'capture': a.run, **r}) + '\n')
    probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,duration', '-of', 'json', str(mp4)],
                           capture_output=True, text=True, check=True)
    st = json.loads(probe.stdout)['streams'][0]
    print(json.dumps({'run': a.run, 'path': str(mp4.relative_to(reel)), 'pages': [str(o.relative_to(reel)) for o in outs], 'sha256': sha256(mp4), 'width': st['width'], 'height': st['height'], 'css_size': a.css_size, 'dpr': a.dpr,
                      'duration_s': float(st['duration']), 'context': plan.get('context', 'admin'), 'method': 'scripted-browser',
                      'actions': len(actions), 'masked_final': redaction[-1] if redaction else None}, indent=1))

if __name__ == '__main__':
    sys.exit(main())
