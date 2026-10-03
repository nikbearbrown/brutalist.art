"""Archive the 24 selected public SVG references and their license. No bulk crawl."""
from pathlib import Path
import json, hashlib
from datetime import date
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1] / 'assets' / 'isocons-24'
NAMES = ['Dataset','Dataset linked','Layers','Quick reference','Terminal','Linked services',
         'Deployed code','Network node','Person raised hand','Person check','Handshake',
         'Partner exchange','Policy','Shield lock','Shield question','VPN key',
         'Data check double','Search check 2','Track changes','Receipt','Account tree',
         'Arrow split','Rebase','Conveyor belt']

def main():
    out = ROOT / 'references'; out.mkdir(parents=True, exist_ok=True)
    browser_path = Path(__file__).resolve().parents[4] / 'runtime/remotion/node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=str(browser_path))
        page = browser.new_page(viewport={'width':1440,'height':1000})
        page.goto('https://www.isocons.app/',wait_until='networkidle')
        page.get_by_role('button',name='License',exact=True).click()
        text = page.locator('body').inner_text().split('License Agreement')[-1]
        assert 'CC BY 4.0' in text
        (out/'license-panel.txt').write_text(f'https://www.isocons.app/ — retrieved {date.today().isoformat()}\nLicense Agreement\n'+text)
        page.get_by_role('button',name='Close',exact=True).click()
        records=[]
        for name in NAMES:
            page.locator('input').first.fill(name)
            page.wait_for_timeout(800)
            svg=page.locator('p').evaluate_all('''(els,name)=>{
              const e=els.find(e=>e.textContent.trim().toLowerCase()===name.toLowerCase());
              return e?.parentElement.parentElement.querySelector('svg')?.outerHTML;
            }''',name)
            if not svg: raise RuntimeError('Missing source: '+name)
            slug=name.lower().replace(' ','-')
            (out/f'{slug}.svg').write_text(svg+'\n')
            records.append({'id':slug,'source_name':name,'source_url':'https://www.isocons.app/',
                'license':'CC-BY-4.0','reference_sha256':hashlib.sha256((svg+'\n').encode()).hexdigest(),
                'adaptation':'Simplified native-vector redraw; changed geometry, stroke, palette, and animation rig. Not a verbatim SVG conversion.'})
            print(slug,flush=True)
        (ROOT/'manifest.json').write_text(json.dumps({'count':len(records),'props':records},indent=2)+'\n')
        browser.close()

if __name__=='__main__': main()
