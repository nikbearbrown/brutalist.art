"""Archive only this candidate batch's 25 source SVGs and its public license."""
from pathlib import Path
import json, hashlib
from datetime import date
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
NAMES=['Prompt suggestion','Question exchange','Token','Filter','Sort','Dynamic form',
 'Responsive layout','Sliders','Toggle on','Settings Accessibility','Highlight keyboard focus',
 'Data alert','Sync Problem','Undo','Settings backup restore','Deployed code history',
 'View Kanbab','Timeline','Query Stats','Data table','Quiz','Local library','Lab research','Map','Flag']
def main():
 out=R/'candidate-props/references';out.mkdir(parents=True,exist_ok=True)
 exe=R.parents[1]/'runtime/remotion/node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell'
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path=str(exe));page=browser.new_page()
  page.goto('https://www.isocons.app/',wait_until='networkidle')
  page.get_by_role('button',name='License',exact=True).click()
  license=page.locator('body').inner_text().split('License Agreement')[-1]
  assert 'CC BY 4.0' in license
  (out/'license-panel.txt').write_text(f'https://www.isocons.app/ — retrieved {date.today()}\nLicense Agreement\n'+license)
  page.get_by_role('button',name='Close',exact=True).click();records=[]
  for name in NAMES:
   page.locator('input').first.fill(name);page.wait_for_timeout(700)
   svg=page.locator('p').evaluate_all('(els,name)=>els.find(e=>e.textContent.trim().toLowerCase()===name.toLowerCase())?.parentElement.parentElement.querySelector("svg")?.outerHTML',name)
   assert svg,name
   slug=name.lower().replace(' ','-');raw=(svg+'\n').encode();(out/f'{slug}.svg').write_bytes(raw)
   records.append(dict(id=slug,source_name=name,source_url='https://www.isocons.app/',license='CC-BY-4.0',reference_sha256=hashlib.sha256(raw).hexdigest(),adaptation='Simplified native-vector redraw: changed geometry, palette, component separation and motion. Candidate only; not approved for shared library.'))
   print(slug,flush=True)
  (out.parent/'manifest.json').write_text(json.dumps(dict(count=25,status='candidate-review',props=records),indent=2)+'\n');browser.close()
if __name__=='__main__':main()
