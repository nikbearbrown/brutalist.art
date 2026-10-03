"""Exercise every catalog action and reset, plus small-screen layout."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent
chrome=root.parents[1]/'runtime/remotion/node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell'
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=str(chrome))
    page=browser.new_page(viewport={'width':1440,'height':1000})
    errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto((root/'index.html').as_uri())
    assert page.locator('article').count()==25
    before=page.locator('g[data-dx]').evaluate_all('(gs)=>gs.map(g=>g.getAttribute("transform"))')
    page.locator('button').evaluate_all('(bs)=>bs.forEach(b=>b.click())')
    page.wait_for_timeout(950)
    assert page.locator('button[aria-pressed="true"]').count()==25
    after=page.locator('g[data-dx]').evaluate_all('(gs)=>gs.map(g=>g.getAttribute("transform"))')
    assert sum(a!=b for a,b in zip(before,after))==25
    page.locator('button').evaluate_all('(bs)=>bs.forEach(b=>b.click())')
    page.wait_for_timeout(950)
    reset=page.locator('g[data-dx]').evaluate_all('(gs)=>gs.map(g=>g.getAttribute("transform"))')
    assert all(t=='translate(0 0)' for t in reset)
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert not errors
    browser.close()
report=dict(status='pass',cards=25,actions=25,resets=25,mobile_overflow=False,javascript_errors=errors)
(root/'catalog-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
