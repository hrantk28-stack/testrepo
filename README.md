# SpaceX Falcon 9 Landing Prediction

**Presenter: Hrant Ohannes Kasparian**

A data-science capstone covering data collection, wrangling, exploratory analysis, SQL, Folium maps, Plotly Dash and machine-learning prediction.

## Start here
- [PDF presentation](deliverables/SpaceX_Capstone_Presentation.pdf)
- [Editable PowerPoint](deliverables/SpaceX_Capstone_Presentation.pptx)
- [Detailed answers report](deliverables/SpaceX_Detailed_Answers_Report.pdf)
- [Executed notebook](completed_answers.ipynb)
- [Source code](source/)

## Main findings
- 90-launch modeling cohort; 60 positive landing labels.
- Four classifiers achieve 83.3% test accuracy (15/18).
- Decision tree leads cross-validation at 87.68%; all models tie on the test set.
- Historical Wikipedia extraction was blocked; road/rail proximity points remain illustrative. See the report for all limitations.

## Reproducibility and source notes
# Falcon 9 capstone — reproducible source package

Presenter: Hrant Ohannes Kasparian

Repository: https://github.com/hrantk28-stack/SpaceX-Falcon9-Capstone

## Contents
- `completed_answers.ipynb`: executed, 67-cell notebook covering every attached lab task and question.
- `source/analyze.py`: numerical analysis, full SQL, all six EDA plots, feature engineering, all four ML grids under course and fold-safe protocols, maps.
- `source/dashboard.py`: complete Dash tasks 1–4.
- `source/collection.py`: archived API audit and complete Wikipedia scraping tasks 1–3, with explicit HTTP-error handling.
- `source/sql_answers.sql`: ten executed queries and output comments.
- `source/build_presentation.py`, `source/build_report.py`: editable-PPTX and detailed-PDF generators.
- `source/capture_evidence.py`: local-browser screenshot capture.
- `source/launch_map.html`, `source/proximity_map.html`: interactive maps (internet access needed for tiles/scripts).
- `data/`: frozen IBM CSV/JSON inputs and recomputed results.
- `charts/`: evidence images, including screenshots of the actual running Dash/Folium outputs.
- `inputs/`: supplied question notebooks, Dash instructions and grading criteria.
- `requirements.txt`: versions used.

## Run from the extracted package root
Use a Python virtual environment. Tested in Python 3.13.

```bash
pip install -r requirements.txt
python source/analyze.py
python source/collection.py
python source/dashboard.py
# Open http://127.0.0.1:8050
```

Open `completed_answers.ipynb` in Jupyter for question-by-question code and outputs. The full cross-validation cell takes time; it is already executed.

To rebuild documents:
```bash
# In separate terminals if fresh screenshots are needed:
python source/dashboard.py
python -m http.server 8000
# If no system Chromium is present: playwright install chromium
python source/capture_evidence.py
python source/build_presentation.py
python source/build_report.py
# Requires LibreOffice to export the editable deck as PDF:
libreoffice --headless --convert-to pdf --outdir deliverables deliverables/SpaceX_Capstone_Presentation.pptx
```
The build scripts place newly generated documents inside `deliverables/`.

## Verified key results
- Modeling/EDA: 90 rows, 60 positive labels, 83 encoded features.
- All four tuned classifiers: test accuracy 15/18 = 83.3%.
- Decision tree leads 10-fold CV: 87.68%; no unique test winner.
- All test confusion matrices: [[3, 3], [0, 12]].
- SQL and dashboard use different cohorts (101 and 56 rows).
- The annual trend is not monotonically increasing.

## Important limitations — do not hide these on submission
1. Project repository: https://github.com/hrantk28-stack/SpaceX-Falcon9-Capstone. Presenter: Hrant Ohannes Kasparian.
2. The historical Wikipedia revision returned HTTP 403. Scraping logic is complete, but no extracted row count or output dataset is asserted. Retry the original page where accessible; do not silently replace it with current content.
3. The live SpaceX API returned HTTP 522. Raw API inspection uses the included course archive; numerical modeling uses course-provided CSVs, not a fresh live rebuild.
4. Road and railway reference points in the proximity illustration are not validated feature locations; no nearest-feature distance is established. Validate actual GIS geometries before asserting railway/highway proximity. Coastline/city results also refer to selected points, not routing or safety boundaries.
5. Course labels count True Ocean as success, which is not evidence of reusable recovery. Missing LandingPad is encoded as all-zero pad dummies. Source payload values were already imputed upstream.
6. Course reproduction scales before train/test split. The sensitivity analysis puts scaling inside CV folds, but chronological/booster-group leakage risks remain. Predictions are not operationally validated.

Sources: IBM Skills Network materials and frozen datasets identified in the report; API schema from r-spacex/SpaceX-API; OpenStreetMap basemap attribution retained in maps. Data are historical snapshots, not current operating statistics.
