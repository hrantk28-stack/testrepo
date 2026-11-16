"""Capture local Dash and Folium screenshots after starting the dashboard and static server.
Requires a Playwright Chromium install, or Chromium Headless Shell on PATH.
From project root: python -m http.server 8000; python source/dashboard.py
"""
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright
ROOT=next(p for p in [Path(__file__).resolve().parents[1],Path(__file__).resolve().parents[2]] if (p/'data').exists())
CH=ROOT/'charts';CH.mkdir(exist_ok=True)
relative=Path(__file__).resolve().parent.relative_to(ROOT).as_posix()
with sync_playwright() as p:
 args={'headless':True,'args':['--no-sandbox']}
 exe=shutil.which('chromium-headless-shell')
 if exe:args['executable_path']=exe
 browser=p.chromium.launch(**args);page=browser.new_page(viewport={'width':1440,'height':1000})
 page.goto('http://127.0.0.1:8050',wait_until='domcontentloaded');page.locator('.js-plotly-plot').first.wait_for();page.screenshot(path=str(CH/'dashboard_all.png'),full_page=True)
 page.locator('#site-dropdown').click();page.get_by_role('listbox').get_by_text('KSC LC-39A',exact=True).click();page.get_by_text('KSC LC-39A: successful vs not successful',exact=False).first.wait_for();page.screenshot(path=str(CH/'dashboard_ksc.png'),full_page=True)
 page.set_viewport_size({'width':1320,'height':720})
 for name in ['launch_map','proximity_map']:
  page.goto(f'http://127.0.0.1:8000/{relative}/{name}.html',wait_until='domcontentloaded');page.locator('.leaflet-tile-loaded').first.wait_for();page.screenshot(path=str(CH/(name+'.png')))
  if name=='launch_map':
   for _ in range(3):
    loc=page.locator('.leaflet-marker-icon.marker-cluster');vals=loc.all_inner_texts()
    if not vals:break
    idx=max(range(len(vals)),key=lambda j:int(vals[j].strip() or 0));loc.nth(idx).click();page.wait_for_timeout(600)
   page.screenshot(path=str(CH/'launch_records.png'))
 browser.close()
