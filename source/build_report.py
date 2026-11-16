from pathlib import Path
import json, html, pandas as pd
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak,KeepTogether,Preformatted
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
ROOT=next(p for p in [Path(__file__).resolve().parents[1],Path(__file__).resolve().parents[2]] if (p/'data/dataset_part_2.csv').exists());R=json.load(open(ROOT/'data/results.json'));S=json.load(open(ROOT/'data/slide_content.json'));OUT=ROOT/'deliverables';OUT.mkdir(exist_ok=True)
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyCustom',fontName='Helvetica',fontSize=10,leading=15,spaceAfter=9,textColor=colors.HexColor('#203D53')));styles.add(ParagraphStyle(name='SmallCustom',fontSize=8,leading=11,spaceAfter=7));styles.add(ParagraphStyle(name='CodeCustom',fontName='Courier',fontSize=7,leading=9,spaceAfter=8));styles['Heading1'].textColor=colors.HexColor('#122D46');styles['Heading2'].textColor=colors.HexColor('#008C95')
story=[]
def p(t,sty='BodyCustom'):story.append(Paragraph(html.escape(str(t)).replace('\n','<br/>'),styles[sty]))
def h(t):p(t,'Heading1')
def table(rows,widths=None,size=8):
 cells=[[Paragraph(html.escape(str(v)),ParagraphStyle(name='ct',fontSize=size,leading=size+3,textColor=colors.white if ri==0 else colors.HexColor('#203D53'))) for v in row]for ri,row in enumerate(rows)]
 t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#122D46')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F0F5F9'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#008C95'))]));story.append(t);story.append(Spacer(1,10))
def img(name,maxh=270):
 from PIL import Image as PIL
 fn=ROOT/'charts'/(name+'.png');w,hh=PIL.open(fn).size;scale=min(475/w,maxh/hh);story.append(Image(str(fn),width=w*scale,height=hh*scale));story.append(Spacer(1,10))
def code(t):
 import textwrap
 lines=[]
 for line in t.splitlines():lines.extend(textwrap.wrap(line,width=100,replace_whitespace=False,drop_whitespace=False) or [''])
 for start in range(0,len(lines),32):story.append(Preformatted('\n'.join(lines[start:start+32]),styles['CodeCustom']))
def new():story.append(PageBreak())
h('SpaceX Falcon 9\nFirst-stage landing prediction');p('DETAILED REPORT AND QUESTION-BY-QUESTION ANSWERS','Heading2');p('Presenter: Hrant Ohannes Kasparian','Heading2');p('Prepared from the six supplied Python notebooks, Dash instructions and grading criteria. Analysis date: November 15, 2026.');p('This companion report expands the 37-slide PDF presentation with exact task answers, reproducible code, full SQL outputs, assumptions and limitations. It is not a current SpaceX operating-performance report.');img('flight_site',250)
p('Delivery status','Heading2');p('Computational analyses were run against the course datasets. The live API returned HTTP 522 and the specified historical Wikipedia page returned HTTP 403. The API audit uses the course archive. Web scraping has complete code, but no extracted data or verified row count. Road/rail proximity points are illustrative and unverified. Project repository: https://github.com/hrantk28-stack/SpaceX-Falcon9-Capstone.');new()
h('1. Executive summary and data provenance')
for s in S[1:4]:
 p(s['title'],'Heading2')
 for b in s['bullets']:p('• '+b)
 if s['table']:table(s['table'],[125,45,305])
p('Source register','Heading2')
base='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/'
for path in ['datasets/dataset_part_1.csv','datasets/dataset_part_2.csv','datasets/dataset_part_3.csv','datasets/spacex_launch_dash.csv','datasets/spacex_launch_geo.csv','datasets/API_call_spacex_api.json','labs/module_2/data/Spacex.csv']:p(base+path,'SmallCustom')
p('The supplied notebooks and instructions define the task wording. All numerical findings in this report are calculated from these downloaded, frozen course files. Dataset collection snapshots differ; no data were merged across the SQL, modeling and dashboard cohorts.');new()
h('2. Data collection: API and web scraping')
p('API workflow and verified archive','Heading2')
p('GET /v4/launches/past → normalize JSON → filter Falcon 9 rocket ID → resolve rocket/payload/launchpad/core references → select the lab cohort → clean payload values → export a table. The archived API has 107 records: 99 Falcon 9, 5 Falcon 1 and 3 Falcon Heavy. Its most recent record date is November 16, 2020. The lab-derived 90-row CSV ends November 5, 2020. The enrichment and exact 90-row rebuild were not rerun against the unavailable API; the prebuilt course CSV is the model source of truth.')
p('Web Task 1 — Request and create BeautifulSoup','Heading2')
code("response = requests.get(static_url, headers=headers, timeout=30)\nresponse.raise_for_status()\nsoup = BeautifulSoup(response.text, 'html.parser')\nprint(soup.title.get_text(strip=True))")
p('Observed answer: the requested revision (June 9, 2021; oldid 1027686922) returned HTTP 403, so a page title could not be verified. A denied response must not be parsed as launch data.')
p('Web Task 2 — Extract column names','Heading2')
p('Find launch tables, inspect the first header row, remove reference superscripts, then use get_text with a space separator and normalize whitespace. Use semantic header matching instead of assuming the third table will always contain launches. Expected schema from the supplied notebook: Flight No.; Date/time UTC; Version Booster; Launch site; Payload; Payload mass; Orbit; Customer; Launch outcome; Booster landing. These are template-expected names, not newly scraped observations.')
p('Web Task 3 — Create the launch DataFrame','Heading2')
p('Parse each matched launch table, resolve rowspans/colspans, keep numbered flight records, concatenate rows, remove bracketed citation noise and duplicates, and export CSV. The complete implementation is in source/collection.py. Execution stops at the HTTP error, so no web-extracted count or output CSV is claimed. Retry on a network with access to the original revision; do not substitute today’s page without documenting a changed cohort.');new()
h('3. Data wrangling: all four tasks')
p('Initial inspection','Heading2');p('The source contains 90 rows and 17 columns; the labeled version has 18 columns. LandingPad has 26 missing values (28.9%); other fields in the supplied labeled CSV are complete. Numerical features include payload, flight counts, block, coordinates and reuse count; categorical/Boolean fields include site, orbit, serial, landing pad and hardware indicators. The payload mean-imputation has already been applied upstream in the course file; raw missing payload counts cannot be recovered from it.')
p('Task 1 — Number of launches per site','Heading2');code("df['LaunchSite'].value_counts()")
table([['Site','Count'],*[[i['LaunchSite'],i['count']] for i in R['site']]],[340,135])
p('Task 2 — Orbit frequencies (excluding GTO as requested)','Heading2');code("df.loc[df['Orbit'] != 'GTO', 'Orbit'].value_counts()")
table([['Orbit','Count'],*[[i['Orbit'],i['count']] for i in sorted(R['orbit'],key=lambda x:-x['count']) if i['Orbit']!='GTO']],[340,135]);p('Non-GTO total = 63. GTO itself has 27 launches; it is retained for later full-cohort EDA/ML. GTO is not the same category as GEO.')
p('Task 3 — Outcome occurrence counts','Heading2');code("landing_outcomes = df['Outcome'].value_counts()")
table([['Outcome','Count'],*[[k,v] for k,v in R['outcomes'].items()]],[340,135])
p('Task 4 — Construct the landing label','Heading2');code("bad_outcome = {'False Ocean','False RTLS','False ASDS','None ASDS','None None'}\nlanding_class = [0 if value in bad_outcome else 1 for value in df['Outcome']]\ndf['Class'] = landing_class\ndf['Class'].mean()")
p('Answer: 60 positive labels, 30 negative labels; mean Class = 0.6666667 (66.7%). True Ocean contributes five positive records. Therefore this target measures the lab’s landing outcome, not whether the booster can be refurbished or flown again.');new()
h('4. EDA and feature engineering: all eight tasks')
for idx in range(10,16):
 s=S[idx];p(s['section']+' — '+s['title'],'Heading2')
 for b in s['bullets']:p('• '+b)
 img(s['chart'],230)
 if idx in [11,13]:new()
p('Tasks 7–8 — One-hot encoding and float conversion','Heading2');code("features = df[['FlightNumber','PayloadMass','Orbit','LaunchSite','Flights',\n               'GridFins','Reused','Legs','LandingPad','Block','ReusedCount','Serial']]\nfeatures_one_hot = pd.get_dummies(features, columns=['Orbit','LaunchSite','LandingPad',\n                                  'Serial','GridFins','Reused','Legs'])\nfeatures_one_hot = features_one_hot.astype('float64')\nfeatures_one_hot.to_csv('features_rebuilt.csv', index=False)")
p(f"Result: {R['features_shape'][0]} rows × {R['features_shape'][1]} columns; all float64. Column-aligned values match dataset_part_3.csv: {R['feature_match']}. With dummy_na=False, missing LandingPad produces zero in every pad column. Outcome and Class are not included as predictors.")
p('All annual results','Heading2');table([['Year','Successes','Launches','Rate'],*[[i['Date'],i['sum'],i['count'],f"{i['mean']:.1%}"]for i in R['years']]],[95,125,125,130]);new()
h('5. SQL: all ten questions with full results')
p('Implementation assumptions','Heading2');p('SQLite is used, matching the notebook filename. Trim leading/trailing whitespace from text values before loading. Date strings use ISO format. For Task 4 the version prefix selects the v1.1 family, including serial suffixes. For Task 7 success-prefixed mission outcomes are grouped as successful; this is explicitly not a landing success calculation. Dense rank is used for Task 10, with inclusive endpoints.')
queries=(Path(__file__).resolve().parent/'sql_answers.sql').read_text()
import re
qmap={int(m.group(1)):m.group(2).strip() for m in re.finditer(r'-- Task (\d+)\n(.*?;)',queries,re.S)}
questions=['Unique launch sites','Five records with launch sites beginning CCA','Total payload for NASA (CRS)','Average payload for the F9 v1.1 family','First successful ground-pad landing date','Drone-ship-success boosters with 4,000 < payload < 6,000 kg','Successful and failed mission counts','All booster versions carrying the maximum payload','2015 failed drone-ship landings by month','Rank landing outcomes, June 4, 2010–March 20, 2017']
for k,q in enumerate(questions,1):
 p(f'Task {k} — {q}','Heading2');code(qmap[k]);rows=R['sql'][str(k)]
 if k==2:
  for i,row in enumerate(rows,1):
   p('Record '+str(i),'Heading3');table([['Field','Value'],*[[kk,v] for kk,v in row.items()]],[125,350])
 else:
  cols=list(rows[0]);table([cols,*[[r[c] if not isinstance(r[c],float) else f'{r[c]:,.4f}' for c in cols] for r in rows]],[475/len(cols)]*len(cols),8)
 if k in [2,5,8]:new()
p('Task 7 label sensitivity','Heading2');p('After whitespace trimming, exact mission labels are Success: 99, Success (payload status unclear): 1, and Failure (in flight): 1. The binary grouped answer is 100 successes and 1 failure. In the untrimmed source, “Success ” is a separate one-row text value. For Task 8, every maximum-mass row is B5; the full list above preserves source serial/version spacing.');new()
h('6. Folium: markers, outcomes and proximity')
p('Task 1 — Mark all sites','Heading2');p('The map uses each distinct site-label/coordinate combination from the 56-row geography dataset. Circle markers name the sites. No site lies on the Equator: the latitude range is approximately 28.6°–34.6°N. The locations are coastal. Florida and California are shown as separate geographic launch regions. Coordinates are taken from the supplied course table; their accuracy is not independently established.')
table([['Site','Latitude','Longitude'],*[[i['Launch Site'],f"{i['Lat']:.6f}",f"{i['Long']:.6f}"]for i in R['geo_sites']]],[235,120,120]);img('launch_map',240)
p('Task 2 — Launch outcome markers','Heading2');p('Each of 56 launch records receives a green marker for Class 1 or a red marker for Class 0, with flight/date/outcome in the popup. MarkerCluster handles coincident coordinates. Site results are KSC LC-39A: 10/13 (76.9%); CCAFS LC-40: 7/26 (26.9%); CCAFS SLC-40: 3/7 (42.9%); VAFB SLC-4E: 4/10 (40.0%). CCAFS labels are not collapsed, preserving the assignment dataset rather than silently changing the denominator.');new()
p('Task 3 — Calculate point-to-point distances','Heading2');p('Use MousePosition to read point coordinates, then calculate haversine distance with Earth radius 6,373 km, matching the lab. A PolyLine joins the site to each reference location. Origin: the course CCAFS LC-40 location (28.56230197, −80.57735648).')
code('a = sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2\ndistance_km = 6373 * 2 * atan2(sqrt(a), sqrt(1-a))  # radians')
table([['Reference point','Latitude','Longitude','Distance km'],*[[k,f"{v['lat']:.5f}",f"{v['lon']:.5f}",f"{v['distance_km']:.3f}"]for k,v in R['proximity'].items()]],[215,85,85,90]);img('proximity_map',245)
p('What can and cannot be concluded','Heading2');p('Coastline: the sample coastline point is approximately 0.58 km away, consistent with coastal siting. Cities: the selected Titusville reference center is about 23.16 km away, showing separation from that particular point, not a safety-boundary calculation. Railways/highways: the supplied data do not contain rail or road geometry; the displayed corridor points are illustrative, unverified coordinate examples. Distances to them are mathematically correct but do not establish distance to the nearest railway or highway. A defensible final proximity analysis would validate the points in a basemap/GIS, use actual feature geometry and report nearest geodesic distances. Coastal corridors may reduce population exposure, but no causal siting conclusion or safety certification is supported.');new()
h('7. Plotly Dash: all four tasks and five questions')
p('Task 1 — Dropdown','Heading2');p('The app defines a searchable site-dropdown with default value ALL, an All Sites option plus each distinct launch site, and a descriptive placeholder.')
p('Task 2 — Pie callback','Heading2');p('Input: site-dropdown.value. Output: success-pie-chart.figure. For ALL, group successful rows by site; the result is share of all successes. For one selected site, show successful versus not-successful launch counts. These pies answer different questions.')
p('Task 3 — Payload range slider','Heading2');p('payload-slider spans 0–10,000 kg, uses a 1,000 kg step and defaults to the entire range. The input table has no payloads above the chosen maximum.')
p('Task 4 — Scatter callback','Heading2');p('Inputs: selected site and inclusive payload bounds. Filter both conditions, then plot payload versus Class with booster category as color and site/flight hover details. ALL removes only the site filter. Browser validation confirmed all-site and KSC-specific rendering; both callback functions were additionally checked programmatically for their filters.')
img('dashboard_all',360);new()
p('All five interpretive questions','Heading2')
for idx in [25,26,27]:
 for b in S[idx]['bullets']:p('• '+b)
# Index alignment based on section names, not chart indexing
p('Exact answers','Heading2');p('Q1: KSC LC-39A has the largest successful-launch count, 10. Q2: KSC LC-39A has the highest success rate, 10/13 = 76.9%. Q3: using explicit fixed 1,000 kg bins, (3,000, 4,000] kg has the highest observed rate, 8/11 = 72.7%. Q4: the lowest nonempty bin is (6,000, 7,000] kg, 0/4 = 0%. Q5: B5 has the highest rate, 1/1 = 100%, but is not a robust winner; FT has 16/24 = 66.7% and is strongest among categories with at least five observations.')
table([['Payload bin kg','Successes','Count','Rate'],*[[i['bin'],i['sum'],i['count'],'No data' if i['mean'] is None else f"{i['mean']:.1%}"] for i in R['dash_bins']]],[190,95,95,95]);p('Intervals are right-inclusive; the first bin includes zero. Zero payload may represent unknown mass. Empty bins are excluded from rate rankings. Changing bin boundaries changes the answer; the assignment does not specify unique boundaries.');img('dash_pies',220);new()
h('8. Predictive analysis: all twelve tasks')
p('Tasks 1–3 — Target, standardization and split','Heading2');code("Y = data['Class'].to_numpy()\ntransform = StandardScaler()\nX_scaled = transform.fit_transform(X)  # course reproduction only\nX_train,X_test,Y_train,Y_test = train_test_split(\n    X_scaled,Y,test_size=0.2,random_state=2)")
p('Y is a one-dimensional NumPy array of length 90, generated from the Series selected with one bracket. The template wording asks for both a NumPy array and a Pandas Series; selecting the Series first and then converting resolves that inconsistency. Training has 72 launches; test has 18 (12 positive, 6 negative). Scaling before splitting follows the course but leaks test distribution information. The preferred sensitivity run instead uses Pipeline(StandardScaler(), estimator) inside GridSearchCV on the raw split.')
p('Tasks 4–11 — Model training and evaluation','Heading2');p('Task pairs: 4–5 logistic regression; 6–7 SVM; 8–9 decision tree; 10–11 KNN. Every search uses cv=10, scoring=accuracy, the supplied hyperparameter ranges, test_size=0.2 and random_state=2. SVM retains the duplicated rbf entry from the lab. For modern scikit-learn, tree max_features=auto is replaced by its former classifier equivalent sqrt (duplicate configurations removed); tree random_state=2 is fixed. Logistic regression max_iter=2000 is used for convergence. Full grids are in analyze.py.')
for mode in ['Course reproduction','Fold-safe scaling']:
 p(mode,'Heading2');mm=[x for x in R['models'] if x['mode']==mode]
 table([['Model','CV accuracy','Test accuracy','Precision','Recall','F1'],*[[m['model'],f"{m['cv_accuracy']:.4f}",f"{m['test_accuracy']:.4f}",f"{m['precision']:.3f}",f"{m['recall']:.3f}",f"{m['f1']:.3f}"]for m in mm]],[140,75,75,65,60,60])
 for m in mm:p(m['model']+' best parameters: '+json.dumps(m['params']),'SmallCustom')
p('Task 12 — Best method','Heading2');p('All four methods tie on holdout accuracy at 15/18 = 83.3%. The decision tree is the provisional winner by training-set CV (87.68%), not a uniquely best test model. Its best settings are gini, best splitter, depth 8, sqrt features, minimum leaf 2 and minimum split 10. The fold-safe SVM selects a linear kernel with C=0.0316228 and gamma=0.001 (gamma is ignored by a linear kernel); the course-reproduction SVM selects sigmoid, C=1, gamma=0.0316228.');new()
p('Confusion matrix and class-level interpretation','Heading2');img('confusions',230);table([['Actual / predicted','Class 0','Class 1'],['Actual 0','3 true negatives','3 false positives'],['Actual 1','0 false negatives','12 true positives']],[195,140,140]);p('All four models produce this same matrix on the same 18 test records. Accuracy=83.3%; class 1 precision=12/15=80%; class 1 recall=12/12=100%; class 1 F1=88.9%; specificity/class 0 recall=3/6=50%; balanced accuracy=75%. Majority baseline=12/18=66.7%. False-positive rate=3/6=50%. One prediction changes the accuracy by 1/18=5.56 percentage points.')
p('Uncertainty and leakage','Heading2');p('A Wilson 95% interval for 15/18 accuracy is approximately 60.8%–94.2%, assuming independent identically distributed test observations; repeated boosters make even that assumption questionable. A random holdout does not establish future-launch performance. FlightNumber captures time; Serial and repeated booster histories may bridge training and test. LandingPad can encode landing strategy, and some core reuse metadata may have been updated after the launch. A fold-safe scaler fixes preprocessing leakage but does not fix these design issues. Use chronological and booster-group evaluation, restrict predictors to known-at-planning-time values, and consider an attempt/strategy model before a conditional landing-success model.');new()
h('9. Conclusions and grading-criteria crosswalk')
for b in S[-3]['bullets']:p('• '+b)
p('Recommended next steps','Heading2');p('Treat this as an educational prototype. Collect more recent, time-stamped prelaunch features; separate attempted landings from no-attempt cases; audit booster identifiers; conduct grouped temporal validation; calibrate predicted probabilities and use a threshold aligned to the cost of false positives. To estimate business value, obtain actual refurbishment costs and vehicle-condition data; do not infer savings from landing labels alone.')
table([['Rubric item','Where addressed / status'],['1.2 PDF slide deck','37-slide presentation PDF supplied'],['1.3 Executive summary','Slide 2; report section 1'],['1.4 Introduction','Slide 3'],['1.5 API collection','Slide 5; archived audit; live retrieval unavailable'],['1.6 Web scraping','Slide 6; full code; extraction blocked by HTTP 403'],['1.7 Wrangling','Slides 7–9; report section 3'],['1.8 EDA methods','Slide 10; all six result views'],['1.9 SQL methods','Slide 18; all 10 queries and full outputs'],['1.10 Interactive analytics','Slide 22; runnable Dash and Folium sources'],['1.11 EDA results','Slides 11–16'],['1.12 SQL results','Slides 19–21; report section 5'],['1.13 Folium results','Slides 23–25; road/rail proximity remains illustrative'],['1.14 Dash results','Slides 26–29; screenshots and exact rates'],['1.15 Predictive analysis','Slides 30–35; two protocols, four models, confusion matrices'],['GitHub requirement across items','github.com/hrantk28-stack/SpaceX-Falcon9-Capstone']],[150,325],8)
p('Submission caveat','Heading2');p('Do not claim a perfect grading-rubric score before resolving blocked scraping execution and validated nearest-feature proximity analysis. The deliverables explicitly disclose these limits rather than invent results.');new()
h('Appendix: reproducibility and environment')
p('Package layout','Heading2');p('The source ZIP contains source/ scripts, data/ frozen CSV/JSON inputs, completed_answers.ipynb, charts/ evidence and a README with run commands. Generated HTML maps are interactive when opened with internet access for their basemap and JavaScript dependencies. The PDF presentation itself is static.')
p('Run sequence','Heading2');code('pip install -r requirements.txt\npython source/analyze.py\npython source/collection.py  # reports HTTP failure explicitly if blocked\npython source/dashboard.py  # open http://127.0.0.1:8050\n# Open completed_answers.ipynb for task-level answers.')
p('Version register','Heading2')
import importlib.metadata as im
version_file = next((f for f in [ROOT/'requirements.txt', ROOT/'deliverables/requirements.txt'] if f.exists()), None)
recorded_versions = dict(line.strip().split('==',1) for line in version_file.read_text().splitlines() if '==' in line) if version_file else {}
for pkg in ['pandas','numpy','matplotlib','seaborn','scikit-learn','folium','dash','plotly','python-pptx','reportlab','beautifulsoup4','requests']:
 try: version = recorded_versions.get(pkg) or im.version(pkg)
 except im.PackageNotFoundError: version = 'See requirements.txt from original analysis'
 p(pkg+': '+version,'SmallCustom')
p('Provenance and usage','Heading2');p('Course materials and source datasets are attributed to IBM Skills Network and the authors named in the attached notebooks. Basemap attribution: © OpenStreetMap contributors. API reference repository: https://github.com/r-spacex/SpaceX-API. Historical Wikipedia request: https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922. Project GitHub repository: https://github.com/hrantk28-stack/SpaceX-Falcon9-Capstone.')
def footer(canvas,doc):
 canvas.setStrokeColor(colors.HexColor('#008C95'));canvas.line(48,43,547,43);canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#526578'));canvas.drawString(48,30,'FALCON 9 CAPSTONE | Historical course data | Recomputed November 2026');canvas.drawRightString(547,30,str(doc.page))
doc=SimpleDocTemplate(str(OUT/'SpaceX_Detailed_Answers_Report.pdf'),pagesize=(595.28,841.89),rightMargin=60,leftMargin=60,topMargin=48,bottomMargin=59,title='SpaceX Capstone: Detailed Answers and Reproducibility Report',author='Hrant Ohannes Kasparian')
doc.build(story,onFirstPage=footer,onLaterPages=footer);print('Report created')
