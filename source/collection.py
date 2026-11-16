"""Supplemental API and Wikipedia collection answers; network status is reported, not hidden."""
from pathlib import Path
import json,re,requests,pandas as pd
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data'
if not DATA.exists(): DATA=ROOT.parent/'data'
WIKI='https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922'
def api_collection(live=False):
 if live:
  response=requests.get('https://api.spacexdata.com/v4/launches/past',timeout=30);response.raise_for_status();launches=response.json()
 else:launches=json.loads((DATA/'API_call_spacex_api.json').read_text())
 flat=pd.json_normalize(launches)
 falcon=flat[flat.rocket=='5e9d0d95eda69973a809d1ec'].copy()
 # To build the lab's enriched table online, resolve IDs with GET /v4/rockets/{id},
 # /v4/payloads/{id}, /v4/launchpads/{id}, and /v4/cores/{id}.
 # Preserve only a single core and payload per launch, date <= 2020-11-13;
 # remove Falcon 1, renumber flights, then mean-impute missing payload mass.
 return flat,falcon

def scrape_wikipedia():
 # TASK 1 — GET and soup; fail explicitly on HTTP errors
 response=requests.get(WIKI,headers={'User-Agent':'Mozilla/5.0 (educational data-science project)'},timeout=30)
 response.raise_for_status();soup=BeautifulSoup(response.text,'html.parser')
 print('Page title:',soup.title.get_text(strip=True))
 tables=soup.find_all('table')
 # TASK 2 — match headers semantically, not a brittle table index
 wanted=[];column_names=[]
 for table in tables:
  header=table.find('tr');ths=header.find_all('th') if header else []
  names=[]
  for th in ths:
   th=BeautifulSoup(str(th),'html.parser')
   for ref in th.select('sup'):ref.decompose()
   names.append(re.sub(r'\s+',' ',th.get_text(' ',strip=True)).strip())
  if any('Flight' in x for x in names) and any('Payload mass' in x for x in names):
   wanted.append(table)
   if not column_names:column_names=names
 print('Column names:',column_names)
 # TASK 3 — pandas resolves rowspans/colspans; clean references and filter numbered launches
 from io import StringIO
 frames=[]
 for table in wanted:
  t=pd.read_html(StringIO(str(table)))[0]
  t.columns=[' '.join(map(str,c)) if isinstance(c,tuple) else str(c) for c in t.columns]
  flight=next((c for c in t if 'Flight' in c),None)
  if flight:
   t=t[t[flight].astype(str).str.match(r'^\d+(?:\s|$|\[)')]
   frames.append(t)
 if not frames:raise ValueError('No launch tables matched. Inspect the historical page structure.')
 df=pd.concat(frames,ignore_index=True).drop_duplicates()
 for col in df.select_dtypes('object'):
  df[col]=df[col].str.replace(r'\[[^\]]*\]','',regex=True).str.replace(r'\s+',' ',regex=True).str.strip()
 df.to_csv(DATA/'spacex_web_scraped.csv',index=False)
 return df
if __name__=='__main__':
 a,b=api_collection();print('Archived API records:',len(a),'Falcon 9:',len(b))
 try:print(scrape_wikipedia().head())
 except requests.RequestException as e:print('Scraping unavailable; no scraped observations claimed:',e)
