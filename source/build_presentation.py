from pathlib import Path
import json,pandas as pd
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
ROOT=next(p for p in [Path(__file__).resolve().parents[1],Path(__file__).resolve().parents[2]] if (p/'data/dataset_part_2.csv').exists()); OUT=ROOT/'deliverables';OUT.mkdir(exist_ok=True);R=json.loads((ROOT/'data/results.json').read_text());slides=[]
def add(section,title,bullets=None,chart=None,table=None,subtitle=None,source=None):
 slides.append(dict(section=section,title=title,bullets=bullets or [],chart=chart,table=table,subtitle=subtitle,source=source or 'IBM Skills Network course datasets; independently recomputed for this project.'))
add('CAPSTONE PROJECT','Predicting Falcon 9\nfirst-stage landing outcomes',[
 'A reproducible data-science study of historical SpaceX launches',
 'Collection • Wrangling • SQL • Visual analytics • Machine learning',
 'Presenter: Hrant Ohannes Kasparian'],subtitle='DATA SCIENCE  /  HISTORICAL COHORTS 2010–2020')
add('01 / EXECUTIVE SUMMARY','Strong signals; limited evidence for deployment',[
 '90-launch modeling cohort: 60 successful landings (66.7%).',
 'Methods: archived API data, Pandas cleaning, SQLite, six EDA plots, Folium, Dash and four tuned classifiers.',
 'All four models score 15/18 = 83.3% test accuracy; the tree leads 10-fold CV at 87.7%.',
 'Critical risks: only 18 test launches, false-positive landings and possible time/booster leakage.',
 'Wikipedia retrieval is blocked; scraping code is supplied, not a fabricated scraped result.'])
add('02 / INTRODUCTION','Business question: can a first stage be recovered?',[
 'Objective: predict the course-defined binary landing class from launch and booster attributes.',
 'Why it matters: recovery can support reuse planning; this study does not estimate actual launch costs or savings.',
 'Success is a first-stage outcome, not payload-delivery mission success.',
 'Decision framing: avoid overconfidence when predicting a successful landing.',
 'Scope: historical educational snapshots, not current SpaceX performance.'])
add('03 / DATA CONTRACT','Three cohorts—not one interchangeable dataset',table=[['Cohort','Rows','Purpose / dates'],['API-derived model data','90','Wrangling, EDA, ML / 2010-06-04–2020-11-05'],['SQL source','101','Launch history queries / 2010-06-04–2020-12-06'],['Dash + Folium','56 each','Interactive visual analytics / older launch subset'],['Archived raw API','107','Collection audit / latest record 2020-11-16']],bullets=['Labels and launch-site spellings differ across cohorts. Never mix their denominators.'])
add('04 / COLLECTION — API','Archived API response → enriched launch table',[
 'GET /v4/launches/past → parse JSON → filter Falcon 9.',
 'Resolve rocket, launchpad, payload and core IDs through their v4 endpoints.',
 'Select single-payload/single-core launches; apply the lab cutoff; flatten launch metadata.',
 'Archived response: 107 launches, including 99 Falcon 9, 5 Falcon 1 and 3 Falcon Heavy.',
 'Live endpoint returned HTTP 522 here; modeling uses the frozen course CSVs, not a claimed live rebuild.'],source='Source: course API_call_spacex_api.json; API schema: github.com/r-spacex/SpaceX-API. GitHub: github.com/hrantk28-stack/SpaceX-Falcon9-Capstone')
add('05 / COLLECTION — WEB','Request → inspect → parse → normalize → validate',[
 'Task 1: request the June 9, 2021 Wikipedia revision (oldid 1027686922), check status and create BeautifulSoup.',
 'Task 2: find launch tables and clean <th> names; remove footnotes and normalize whitespace.',
 'Task 3: parse numbered launch rows; handle rowspans; build a DataFrame and export CSV.',
 'Expected fields: flight, date/time, booster, site, payload, mass, orbit, customer and both outcomes.',
 'Verified limit: HTTP 403 prevented extraction. No scraped row count is asserted.'],source='Source: attached web-scraping notebook; collection.py provides all three task solutions. GitHub: github.com/hrantk28-stack/SpaceX-Falcon9-Capstone')
add('06 / WRANGLING','Define the target before interpreting “success”',[
 'Inspect shape, dtypes, missingness and categorical values before transforming.',
 'Class 0: False Ocean, False RTLS, False ASDS, None ASDS and None None.',
 'Class 1: True ASDS, True RTLS and True Ocean → 60/90 successes.',
 'True Ocean (5 records) counts as class 1 in the lab but does not prove recoverability or reuse.',
 '26/90 LandingPad values are missing (28.9%); missing pad dummies are all zero. Payload is already imputed in the course CSV.'],source='Source: dataset_part_1.csv and dataset_part_2.csv; analyze.py. GitHub: github.com/hrantk28-stack/SpaceX-Falcon9-Capstone')
add('07 / WRANGLING RESULTS','Counts expose sample imbalance',table=[['Launch site','Launches','Successful','Rate'],['CCAFS SLC 40','55','33','60.0%'],['KSC LC 39A','22','17','77.3%'],['VAFB SLC 4E','13','10','76.9%']],bullets=['Outcome counts: True ASDS 41; None None 19; True RTLS 14; False ASDS 6; True Ocean 5; False Ocean 2; None ASDS 2; False RTLS 1.','Wrangling Task 2 excludes GTO as instructed: 63 launches remain. EDA/ML retain the full 90-launch cohort.'])
add('08 / ORBIT COUNTS','Orbit frequency is not orbit success rate',table=[['Orbit','Count','Orbit','Count'],['GTO*','27','ISS','21'],['VLEO','14','PO','9'],['LEO','7','SSO','5'],['MEO','3','ES-L1','1'],['GEO','1','HEO','1'],['SO','1','TOTAL','90']],bullets=['*GTO is shown for cohort reconciliation; omit it for the wrangling task’s requested non-GTO count.'])
add('09 / EDA METHODOLOGY','Six views answer six different questions',[
 'Flight number × site: inspect experience and site mix.',
 'Payload × site: compare payload operating ranges.',
 'Orbit bars: compare average class, with sample-size labels.',
 'Flight number × orbit and payload × orbit: reveal mixed mission contexts.',
 'Yearly line: summarize changing performance; use year-specific denominators.',
 'Association only: experience, vehicle generation, payload and site are confounded.'],source='Source: dataset_part_2.csv; analyze.py and completed_answers.ipynb. GitHub: github.com/hrantk28-stack/SpaceX-Falcon9-Capstone')
add('10 / EDA — TASK 1','Later flights show more successful outcomes',[
 'CCAFS dominates the cohort (55/90) and includes the earliest unsuccessful landings.',
 'KSC begins later in the sequence, making site and experience difficult to separate.',
 'KSC: 17/22 successes; VAFB: 10/13. Their similar rates have different sample sizes.'],chart='flight_site')
add('11 / EDA — TASK 2','Payload envelopes vary by launch site',[
 'VAFB maximum observed payload: 9,600 kg—no launches above 10,000 kg in this cohort.',
 'CCAFS and KSC each reach 15,600 kg.',
 'Some masses are course-imputed; do not interpret every plotted value as a measured payload.'],chart='payload_site')
add('12 / EDA — TASK 3','Perfect rates are often small-sample artifacts',[
 'SSO: 5/5 = 100%. ES-L1, GEO and HEO each have only one successful observation.',
 'VLEO: 12/14 = 85.7%; GTO: 14/27 = 51.9%.',
 'SO: 0/1. Neither 0% nor 100% from one launch is a robust forecast.'],chart='orbit_success')
add('13 / EDA — TASK 4','Flight sequence and orbit context interact',[
 'LEO transitions from early class 0 observations toward later successes.',
 'GTO contains both classes across the flight sequence; it is not cleanly separable.',
 'FlightNumber is also a time proxy—not a causal measure of learning.'],chart='flight_orbit')
add('14 / EDA — TASK 5','Payload alone does not separate landing classes',[
 'GTO successes and failures overlap strongly in payload mass.',
 'VLEO launches carry 13,620–15,600 kg and achieve 12/14 successes.',
 'Mission energy, booster generation and landing plan matter; mass alone is insufficient.'],chart='payload_orbit')
add('15 / EDA — TASK 6','The annual trend improves—but not monotonically',[
 '2013: 0/3; 2017: 15/18 = 83.3%.',
 '2018 falls to 11/18 = 61.1%; 2019 reaches 9/10 = 90.0%.',
 '2020: 16/19 = 84.2%. The template’s “kept increasing” claim is contradicted by the data.',
 'No 2011 observations; do not interpolate a measured rate.'],chart='yearly')
add('16 / FEATURE ENGINEERING','90 observations → 83 numeric predictors',[
 'Tasks 7–8: one-hot encode Orbit, LaunchSite, LandingPad, Serial, GridFins, Reused and Legs.',
 'Retain FlightNumber, PayloadMass, Flights, Block and ReusedCount.',
 'Cast every feature to float64; rebuilt values match the provided 90 × 83 model matrix.',
 'Exclude Class and Outcome from predictors. Serial identifiers and repeated boosters still create leakage risks.',
 'For production: audit when Flights/ReusedCount were measured; remove any post-launch information.'])
add('17 / SQL METHODOLOGY','SQLite audit: ten queries, one explicit contract',[
 'Load the 101-row CSV into SPACEXTBL and trim string whitespace.',
 'Use DISTINCT, LIKE, SUM/AVG/MIN/MAX, GROUP BY, a subquery and date filtering.',
 'Task 4 interprets “F9 v1.1” as a version family: LIKE \'F9 v1.1%\'.',
 'Task 7 groups all Success-prefixed mission labels; landing outcome is a different field.',
 'Complete SQL and row-level outputs are included in the detailed report.'],source='Source: Spacex.csv; sql_answers.sql. GitHub: github.com/hrantk28-stack/SpaceX-Falcon9-Capstone')
add('18 / SQL — TASKS 1–5','Launch sites, payload totals and first ground landing',table=[['Task','Verified answer'],['1 / Unique sites','CCAFS LC-40; CCAFS SLC-40; KSC LC-39A; VAFB SLC-4E'],['2 / First 5 CCA% dates','2010-06-04; 2010-12-08; 2012-05-22; 2012-10-08; 2013-03-01'],['3 / NASA (CRS) payload','45,596 kg'],['4 / F9 v1.1 family average','2,534.67 kg'],['5 / First ground-pad success','2015-12-22']],bullets=['Task 2 uses ORDER BY Date for reproducibility. Full five records appear in the report.'])
add('19 / SQL — TASKS 6–9','Do not confuse mission success with landing success',[
 'Task 6: drone-ship successes, 4,000 < mass < 6,000 kg: F9 FT B1022, B1026, B1021.2 and B1031.2.',
 'Task 7: 100 mission successes and 1 in-flight failure; Success (payload status unclear) is included in success.',
 'Task 8: maximum payload = 15,600 kg; 12 booster-version records match (all B5). Full list in appendix.',
 'Task 9: January 2015—F9 v1.1 B1012; April 2015—F9 v1.1 B1015. Both drone-ship failures at CCAFS LC-40.'])
add('20 / SQL — TASK 10','Early landing outcomes: “no attempt” is largest',table=[['Landing outcome','Count','Dense rank'],*[ [x['Landing_Outcome'],str(x['launches']),str(x['rank'])] for x in R['sql']['10'] ]],bullets=['Inclusive interval: June 4, 2010 through March 20, 2017; 31 launches. Ties share rank.'])
add('21 / INTERACTIVE VISUAL ANALYTICS','Folium explains location; Dash explains filters',[
 'Folium: site circles, red/green launch markers, marker clusters, MousePosition and distance lines.',
 'Dash: searchable site dropdown, all-site success-share pie and selected-site outcome pie.',
 'A 0–10,000 kg RangeSlider filters payload scatter; booster category is encoded by color.',
 'PDF views are static screenshots. The source package contains the runnable interactive app and maps.',
 'Dash/Folium use 56 records—not the 90-row modeling cohort.'],source='Source: spacex_launch_geo.csv and spacex_launch_dash.csv. GitHub: github.com/hrantk28-stack/SpaceX-Falcon9-Capstone')
add('22 / FOLIUM — TASK 1','Launch sites are coastal, not on the Equator',[
 'The course locations span about 28.6°N to 34.6°N: none are equatorial.',
 'Florida sites appear on the Atlantic side; VAFB is on the Pacific side.',
 'Coastal geography is consistent with downrange ocean corridors; it does not establish site-selection causality.',
 'Coordinates and site labels are used exactly as supplied, not independently surveyed.'],chart='launch_map',source='Source: course geo CSV; Folium screenshot; basemap © OpenStreetMap contributors.')
add('23 / FOLIUM — TASK 2','Clustered launch records reveal site-level outcomes',[
 '56 launch markers: green = class 1, red = class 0; coincident markers cluster.',
 'KSC LC-39A: 10/13 successful; CCAFS LC-40: 7/26.',
 'VAFB SLC-4E: 4/10; CCAFS SLC-40: 3/7.',
 'CCAFS LC-40 and SLC-40 are retained as distinct course labels; they refer to the same named complex across eras.'],chart='launch_records',source='Source: geo CSV and launch_map.html; basemap © OpenStreetMap contributors.')
add('24 / FOLIUM — TASK 3','Proximity analysis: calculated, not surveyed',[
 'From course CCAFS LC-40 point: selected coastline point ≈0.58 km; Titusville reference center ≈23.16 km.',
 'Illustrative road-corridor point ≈0.55 km; rail-corridor point ≈1.31 km. Feature identity is unverified.',
 'Distances are haversine point-to-point, not road routes or validated nearest-feature distances.',
 'Conclusion: coastal access and city separation are plausible; nearest railway/highway claims remain unverified.'],chart='proximity_map',source='Source: course coordinates + explicitly illustrative reference points; OpenStreetMap basemap. See report caveats.')
add('25 / DASH — IMPLEMENTATION','A working dashboard, not a mock-up',[
 'All-site view counts only successful launches for the pie.',
 'Selected-site view compares class 1 with class 0.',
 'Payload range and site selection jointly filter the scatter.',
 'Both callbacks were browser-tested; this is a screenshot of the running local app.'],chart='dashboard_all',source='Source: dashboard.py; screenshot of live local Dash application. GitHub: github.com/hrantk28-stack/SpaceX-Falcon9-Capstone')
add('26 / DASH — QUESTIONS 1–2','KSC leads both success count and success rate',[
 'Q1: KSC LC-39A has 10 successes—the largest count.',
 'Q2: KSC LC-39A also has the highest rate: 10/13 = 76.9%.',
 'All-site pie: KSC contributes 10/24 = 41.7% of successes. This is not its site success rate.'],chart='dash_pies')
add('27 / DASH — QUESTIONS 3–4','Payload-bin rankings depend on the definition',[
 'Using fixed 1,000 kg bins, highest observed rate: (3,000, 4,000] kg, 8/11 = 72.7%.',
 'Lowest nonempty bin: (6,000, 7,000] kg, 0/4 = 0%.',
 'Exclude empty bins from ranking; (7,000, 9,000] kg has no observations.',
 'Zero payload values may mean unknown mass. Binning is descriptive, not a recommended operating threshold.'],chart='payload_bins')
add('28 / DASH — QUESTION 5','B5 wins on rate—but has only one observation',[
 'B5: 1/1 = 100%; FT: 16/24 = 66.7%; B4: 6/11 = 54.5%.',
 'v1.1: 1/15 = 6.7%; v1.0: 0/5 = 0%.',
 'FT is strongest among categories with at least five observations in this sample.',
 'Later booster versions are confounded with calendar time, mission mix and landing capability.'],chart='dash_scatter')
add('29 / PREDICTIVE ANALYSIS','One holdout, four tuned classifiers, two protocols',[
 'Tasks 1–3: Y = Class.to_numpy(); 80/20 split, random_state=2 → 72 train and 18 test.',
 'Tasks 4–11: tune logistic regression, SVM, decision tree and KNN using 10-fold CV.',
 'Course reproduction: standardize before split, as instructed. This leaks preprocessing information.',
 'Preferred sensitivity run: StandardScaler inside a Pipeline, fitted separately within each CV fold.',
 'Compatibility fix: deprecated tree max_features=auto is equivalent to sqrt for classification; set seed=2.'])
safe=[m for m in R['models'] if m['mode']=='Fold-safe scaling']
add('30 / MODEL RESULTS','Decision tree leads CV; all models tie on the test',table=[['Model','10-fold CV','Test accuracy','F1 / class 1'],*[[m['model'],f"{m['cv_accuracy']:.1%}",f"{m['test_accuracy']:.1%}",f"{m['f1']:.3f}"] for m in safe]],bullets=['Pipeline protocol. Every model: precision 0.800 and recall 1.000 for class 1.','Majority-class baseline on test: 12/18 = 66.7%. Model gain = 16.7 percentage points.'])
add('31 / MODEL COMPARISON','Rank using CV—not a tied test score',[
 'Decision tree CV = 87.7%; KNN = 84.8%; logistic regression = 84.6%; SVM = 82.1%.',
 'Course reproduction CV: tree 87.7%, SVM 84.8%, KNN 84.8%, logistic regression 84.6%.',
 'Moving scaling inside folds changes SVM tuning, not the 83.3% test result.',
 'Select the tree as the provisional CV leader; do not claim proven test superiority.'],chart='model_comparison')
add('32 / CONFUSION MATRICES','False positives are the unresolved operational risk',[
 'Every model returns the same test matrix: TN=3, FP=3, FN=0, TP=12.',
 'Three of six actual class 0 launches are predicted successful: false-positive rate = 50%.',
 'Recall of successful landings is 100%, but failure-class recall is only 50%.',
 '18 test records are too few for deployment assurance; one changed prediction moves accuracy by 5.6 points.'],chart='confusions')
add('33 / BEST MODEL','Provisional choice: a constrained decision tree',[
 'Best pipeline settings: criterion=gini, splitter=best, max_depth=8, max_features=sqrt.',
 'min_samples_leaf=2, min_samples_split=10, random_state=2.',
 'Highest CV score: 0.8768. Test score: 0.8333. A ranking, not proof of generalization.',
 'Next validation: time-ordered holdout and booster-group separation; remove serial IDs and audit prelaunch availability.',
 'Use calibrated probabilities and a false-positive-aware threshold before any operational decision.'])
add('34 / CONCLUSION','Separate prediction, recoverability and business value',[
 'Landing performance improves broadly over time, but annual setbacks and mission mix matter.',
 'KSC leads observed site rates; small samples prevent causal or universal rankings.',
 'Four classifiers beat a simple baseline, yet half of test failures are missed.',
 'Creative extension: two-stage modeling—first landing attempt/strategy, then success conditional on attempt.',
 'A business case also needs recovery condition, turnaround time and refurbishment cost—none are available here.'])
add('35 / DELIVERY CHECK','Project deliverables and transparent limitations',[
 'Completed: all computational lab answers, EDA figures, SQL results, dashboard callbacks, map markers and model evaluation.',
 'Included: PDF slides, editable PowerPoint, detailed Q&A report, executable source, notebook and frozen datasets.',
 'Blocked externally: historical Wikipedia extraction (HTTP 403); live API refresh (HTTP 522).',
 'Proximity road/rail points are illustrative, not a validated nearest-feature analysis.',
 'Project repository: github.com/hrantk28-stack/SpaceX-Falcon9-Capstone — presenter Hrant Ohannes Kasparian.'])
add('36 / REFERENCES','Source register and reproducibility',[
 'Primary inputs: six attached notebooks, Dash lab instructions and grading-criteria image.',
 'IBM datasets: dataset_part_1/2/3.csv; Spacex.csv; spacex_launch_dash.csv; spacex_launch_geo.csv; archived API JSON.',
 'Dataset base: cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/',
 'API schema: github.com/r-spacex/SpaceX-API; Wikipedia revision oldid=1027686922 (June 9, 2021).',
 'Run order and package versions are documented in the source package. Analysis date: November 15, 2026.'],source='All numeric results are recomputed from the frozen course inputs; no current launch statistics are asserted.')
# Save content for report generation
(ROOT/'data/slide_content.json').write_text(json.dumps(slides,indent=2))
prs=Presentation();prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
NAVY='122D46';TEAL='008C95';GRAY='526578';BG='F5F8FC';ORANGE='E18A42'
def txt(s,x,y,w,h,text,size=20,color=NAVY,bold=False):
 tb=s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h));tf=tb.text_frame;tf.word_wrap=True;tf.margin_left=0;tf.margin_top=0;tf.margin_right=0;tf.margin_bottom=0
 for i,line in enumerate(str(text).split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.space_after=Pt(7);r=p.add_run();r.text=line;r.font.name='Aptos';r.font.size=Pt(size);r.font.bold=bold;r.font.italic=False;r.font.color.rgb=RGBColor.from_string(color)
 return tb
def rect(s,x,y,w,h,color):
 q=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h));q.fill.solid();q.fill.fore_color.rgb=RGBColor.from_string(color);q.line.fill.background();return q
def picture(s,file,x,y,w,h):
 from PIL import Image
 iw,ih=Image.open(file).size;scale=min(w/iw,h/ih);ww=iw*scale;hh=ih*scale;s.shapes.add_picture(str(file), Inches(x+(w-ww)/2), Inches(y+(h-hh)/2),width=Inches(ww),height=Inches(hh))
for i,d in enumerate(slides):
 s=prs.slides.add_slide(prs.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=RGBColor.from_string(NAVY if i==0 else BG)
 if i==0:
  txt(s,.7,.65,11,.4,'FALCON 9  /  FIRST-STAGE LANDING',16,'54D0CE',True)
  txt(s,.7,1.6,11.8,1.85,d['title'],44,'FFFFFF',True)
  txt(s,.75,4.0,10.8,1.6,'\n'.join(d['bullets']),21,'D6E4F2')
  txt(s,.75,6.65,11,.35,'HISTORICAL DATA • REPRODUCIBLE ANALYSIS • NOVEMBER 2026',12,'54D0CE',True)
 else:
  txt(s,.65,.35,12,.3,d['section'],12,TEAL,True)
  txt(s,.65,.85,12.05,.9,d['title'],29,NAVY,True)
  if d['chart']:
   rect(s,.55,1.85,8.45,4.7,'FFFFFF');picture(s,ROOT/'charts'/(d['chart']+'.png'),.65,1.95,8.25,4.5)
   rect(s,9.25,1.85,3.5,4.7,'E8F2F5')
   yy=2.05
   for bullet in d['bullets']:
    # Smaller chart-side commentary, with allocated height based on content
    h=max(.64,len(bullet)/31*.215+.13)
    txt(s,9.45,yy,3.08,h,'• '+bullet,16,NAVY);yy+=h+.13
  elif d['table']:
   rows=d['table'];top=1.95;ht=3.7 if len(rows)<=6 else 4.15
   table=s.shapes.add_table(len(rows),len(rows[0]), Inches(.7), Inches(top), Inches(11.9), Inches(ht)).table
   if len(rows[0])==2:table.columns[0].width=Inches(3.1);table.columns[1].width=Inches(8.8)
   for ri,row in enumerate(rows):
    for ci,v in enumerate(row):
     cell=table.cell(ri,ci);cell.text=str(v);cell.margin_left=Inches(.12);cell.margin_right=Inches(.1);cell.vertical_anchor=MSO_ANCHOR.MIDDLE;cell.fill.solid();cell.fill.fore_color.rgb=RGBColor.from_string(NAVY if ri==0 else ('FFFFFF' if ri%2 else 'EAF1F7'))
     for p in cell.text_frame.paragraphs:
      for r in p.runs:r.font.name='Aptos';r.font.size=Pt(16 if len(rows)>7 else 18);r.font.bold=ri==0;r.font.italic=False;r.font.color.rgb=RGBColor.from_string('FFFFFF' if ri==0 else NAVY)
   yy=top+ht+.23
   for b in d['bullets']:txt(s,.75,yy,11.85,.65,'• '+b,16,GRAY);yy+=.58
  else:
   yy=1.95
   for j,b in enumerate(d['bullets']):
    h=max(.63,len(b)/101*.31+.16)
    txt(s,.8,yy,.35,.35,f'{j+1:02d}',13,TEAL,True);txt(s,1.35,yy,11.1,h,b,21,NAVY);yy+=h+.20
  txt(s,.68,6.91,11.8,.36,d['source'],9,GRAY)
  txt(s,12.05,6.91,.6,.25,f'{i+1:02d}',10,TEAL,True)
 # Detailed speaker notes carry provenance / full commentary
 s.notes_slide.notes_text_frame.text=d['title']+'\n\n'+'\n\n'.join(d['bullets'])+'\n\n'+d['source']
prs.core_properties.title='Falcon 9 First-Stage Landing Prediction';prs.core_properties.subject='Completed data-science capstone analysis';prs.core_properties.author='Hrant Ohannes Kasparian'
prs.save(OUT/'SpaceX_Capstone_Presentation.pptx');print('Slides:',len(slides))
