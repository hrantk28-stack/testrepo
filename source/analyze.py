from pathlib import Path
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, seaborn as sns, sqlite3,json, warnings
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score
warnings.filterwarnings('ignore')
ROOT=next(p for p in [Path(__file__).resolve().parents[1],Path(__file__).resolve().parents[2]] if (p/'data/dataset_part_2.csv').exists())
D=ROOT/'data'; C=ROOT/'charts'; C.mkdir(exist_ok=True)
df=pd.read_csv(D/'dataset_part_2.csv'); X=pd.read_csv(D/'dataset_part_3.csv'); Y=df.Class.to_numpy()
sns.set_theme(style='whitegrid',font_scale=1.08,palette=['#05A8AA','#F29D49']);plt.rcParams.update({'figure.dpi':130,'savefig.bbox':'tight'})
results={}
results['site']=df.groupby('LaunchSite').Class.agg(['count','sum','mean']).reset_index().to_dict('records')
results['orbit']=df.groupby('Orbit').Class.agg(['count','sum','mean']).reset_index().to_dict('records')
results['outcomes']=df.Outcome.value_counts().to_dict();results['years']=df.groupby(df.Date.str[:4]).Class.agg(['count','sum','mean']).reset_index().to_dict('records')
results['missing']=df.isna().sum().to_dict();results['dates']=[df.Date.min(),df.Date.max()]
def save(name):plt.tight_layout();plt.savefig(C/(name+'.png'));plt.close()
for a,b,name in [('FlightNumber','LaunchSite','flight_site'),('PayloadMass','LaunchSite','payload_site'),('FlightNumber','Orbit','flight_orbit'),('PayloadMass','Orbit','payload_orbit')]:
 plt.figure(figsize=(10.2,4.8));sns.scatterplot(data=df,x=a,y=b,hue='Class',palette={0:'#E88554',1:'#009D9E'},s=65,alpha=.85);plt.xlabel('Payload mass (kg)' if a=='PayloadMass' else 'Flight number');plt.ylabel('Launch site' if b=='LaunchSite' else 'Orbit');plt.legend(title='Landing class',loc='best');save(name)
o=df.groupby('Orbit').Class.agg(['mean','count']).sort_values('mean');plt.figure(figsize=(10.2,4.8));bars=plt.bar(o.index,o['mean']*100,color='#05A8AA');plt.ylim(0,119);plt.ylabel('Success rate (%)');plt.xlabel('Orbit');
for b,n in zip(bars,o['count']):plt.text(b.get_x()+b.get_width()/2,b.get_height()+2,f'n={n}',ha='center',fontsize=9)
save('orbit_success')
y=df.groupby(df.Date.str[:4]).Class.agg(['mean','count']);plt.figure(figsize=(10.2,4.8));plt.plot(y.index,y['mean']*100,'o-',color='#009D9E',lw=3);plt.ylim(-3,110);plt.xlabel('Year (no records in 2011)');plt.ylabel('Success rate (%)');
for i,(rate,n) in enumerate(zip(y['mean'],y['count'])):plt.annotate(f'n={n}',(i,rate*100),xytext=(0,10),textcoords='offset points',ha='center',fontsize=9)
save('yearly')
# Feature engineering tasks 7–8
features=df[['FlightNumber','PayloadMass','Orbit','LaunchSite','Flights','GridFins','Reused','Legs','LandingPad','Block','ReusedCount','Serial']]
encoded=pd.get_dummies(features,columns=['Orbit','LaunchSite','LandingPad','Serial','GridFins','Reused','Legs']).astype('float64')
encoded.to_csv(D/'features_rebuilt.csv',index=False);results['feature_match']=bool(set(encoded.columns)==set(X.columns) and np.allclose(encoded[X.columns],X));results['features_shape']=list(encoded.shape)
# SQL: preserve source labels, normalize only whitespace
sql=pd.read_csv(D/'Spacex.csv');sql=sql.map(lambda x:x.strip() if isinstance(x,str) else x)
con=sqlite3.connect(D/'spacex.sqlite');sql.to_sql('SPACEXTBL',con,index=False,if_exists='replace')
queries={
1:'SELECT DISTINCT Launch_Site FROM SPACEXTBL ORDER BY Launch_Site;',
2:"SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' ORDER BY Date LIMIT 5;",
3:"SELECT SUM(PAYLOAD_MASS__KG_) AS total_kg FROM SPACEXTBL WHERE Customer = 'NASA (CRS)';",
4:"SELECT AVG(PAYLOAD_MASS__KG_) AS average_kg FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%';",
5:"SELECT MIN(Date) AS first_ground_landing FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)';",
6:"SELECT DISTINCT Booster_Version FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000;",
7:"SELECT CASE WHEN Mission_Outcome LIKE 'Success%' THEN 'Success' ELSE 'Failure' END AS mission_result, COUNT(*) AS launches FROM SPACEXTBL GROUP BY mission_result;",
8:'SELECT DISTINCT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);',
9:"SELECT CASE substr(Date,6,2) WHEN '01' THEN 'January' WHEN '02' THEN 'February' WHEN '03' THEN 'March' WHEN '04' THEN 'April' WHEN '05' THEN 'May' WHEN '06' THEN 'June' WHEN '07' THEN 'July' WHEN '08' THEN 'August' WHEN '09' THEN 'September' WHEN '10' THEN 'October' WHEN '11' THEN 'November' WHEN '12' THEN 'December' END AS month, Landing_Outcome, Booster_Version, Launch_Site FROM SPACEXTBL WHERE substr(Date,1,4) = '2015' AND Landing_Outcome = 'Failure (drone ship)' ORDER BY Date;",
10:"SELECT Landing_Outcome, COUNT(*) AS launches, DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS rank FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY launches DESC, Landing_Outcome;"}
results['sql']={};out=[]
for k,q in queries.items():
 t=pd.read_sql(q,con);results['sql'][str(k)]=t.to_dict('records');out += [f'-- Task {k}',q,'-- '+t.to_string(index=False).replace('\n','\n-- '),'']
(Path(__file__).resolve().parent/'sql_answers.sql').write_text('\n'.join(out))
# Exact notebook grid except deprecated tree auto -> sqrt; deterministic tree
models={
'Logistic regression':(LogisticRegression(max_iter=2000),{'C':[.01,.1,1],'penalty':['l2'],'solver':['lbfgs']}),
'SVM':(SVC(),{'kernel':['linear','rbf','poly','rbf','sigmoid'],'C':np.logspace(-3,3,5),'gamma':np.logspace(-3,3,5)}),
'Decision tree':(DecisionTreeClassifier(random_state=2),{'criterion':['gini','entropy'],'splitter':['best','random'],'max_depth':list(range(2,20,2)),'max_features':['sqrt'],'min_samples_leaf':[1,2,4],'min_samples_split':[2,5,10]}),
'KNN':(KNeighborsClassifier(),{'n_neighbors':list(range(1,11)),'algorithm':['auto','ball_tree','kd_tree','brute'],'p':[1,2]})}
# Two runs: course reproduction and leakage-safe sensitivity
results['models']=[];preds={}
for mode in ['Course reproduction','Fold-safe scaling']:
 xx=StandardScaler().fit_transform(X) if mode=='Course reproduction' else X
 a,b,c,d=train_test_split(xx,Y,test_size=.2,random_state=2)
 for name,(est,grid) in models.items():
  if mode=='Fold-safe scaling':
   est=Pipeline([('scale',StandardScaler()),('model',est)]);grid={'model__'+k:v for k,v in grid.items()}
  g=GridSearchCV(est,grid,cv=10,n_jobs=2,scoring='accuracy',error_score='raise');g.fit(a,c);p=g.predict(b)
  r={'mode':mode,'model':name,'cv_accuracy':float(g.best_score_),'test_accuracy':float(accuracy_score(d,p)),'precision':float(precision_score(d,p,zero_division=0)),'recall':float(recall_score(d,p)),'f1':float(f1_score(d,p)),'params':g.best_params_,'cm':confusion_matrix(d,p).tolist()};results['models'].append(r);print(r,flush=True)
  if mode=='Fold-safe scaling':preds[name]=(d,p)
r=pd.DataFrame(results['models']);r.to_csv(D/'model_results.csv',index=False)
plt.figure(figsize=(10.2,4.8));safe=r[r['mode']=='Fold-safe scaling'];idx=np.arange(4);plt.bar(idx-.18,safe.cv_accuracy*100,.36,label='10-fold CV');plt.bar(idx+.18,safe.test_accuracy*100,.36,label='Test (18 launches)',color='#F29D49');plt.xticks(idx,safe.model);plt.ylim(0,110);plt.ylabel('Accuracy (%)');plt.legend();save('model_comparison')
fig,axs=plt.subplots(1,4,figsize=(13,3.5))
for ax,(name,(actual,p)) in zip(axs,preds.items()):sns.heatmap(confusion_matrix(actual,p),annot=True,fmt='d',cbar=False,cmap='Blues',ax=ax);ax.set_title(name);ax.set_xlabel('Predicted class');ax.set_ylabel('Actual class')
save('confusions')
results['test_counts']=pd.Series(d).value_counts().to_dict()
# Dash questions
z=pd.read_csv(D/'spacex_launch_dash.csv');results['dash_sites']=z.groupby('Launch Site')['class'].agg(['count','sum','mean']).reset_index().to_dict('records');results['dash_boosters']=z.groupby('Booster Version Category')['class'].agg(['count','sum','mean']).reset_index().to_dict('records')
z['bin']=pd.cut(z['Payload Mass (kg)'],range(0,10001,1000),include_lowest=True);bb=z.groupby('bin',observed=False)['class'].agg(['count','sum','mean']);results['dash_bins']=bb.reset_index().astype({'bin':str}).replace({np.nan:None}).to_dict('records')
fig,axs=plt.subplots(1,2,figsize=(11,4.6));ss=z.groupby('Launch Site')['class'].sum();axs[0].pie(ss,labels=ss.index,autopct='%1.1f%%',colors=['#009D9E','#F29D49','#233C64','#7EC9D3']);axs[0].set_title('Share of 24 successful launches');kk=z[z['Launch Site']=='KSC LC-39A']['class'].value_counts().sort_index();axs[1].pie(kk,labels=['Not successful','Successful'],autopct='%1.1f%%',colors=['#F29D49','#009D9E']);axs[1].set_title('KSC LC-39A: 10/13 = 76.9%');save('dash_pies')
plt.figure(figsize=(10.2,4.8));sns.scatterplot(data=z,x='Payload Mass (kg)',y='class',hue='Booster Version Category',style='Booster Version Category',s=95,alpha=.85);plt.yticks([0,1]);plt.ylabel('Landing class');plt.legend(bbox_to_anchor=(1.02,1),loc='upper left');save('dash_scatter')
bb=bb[bb['count']>0];plt.figure(figsize=(10.2,4.8));bars=plt.bar([str(i) for i in bb.index],bb['mean']*100,color='#009D9E');plt.xticks(rotation=25,ha='right');plt.ylabel('Success rate (%)');plt.ylim(0,100);plt.xlabel('Payload bin (kg; right-inclusive)');
for b,n in zip(bars,bb['count']):plt.text(b.get_x()+b.get_width()/2,b.get_height()+2,f'n={n}',ha='center',fontsize=10)
save('payload_bins')
# Geography
import folium
from folium.plugins import MarkerCluster,MousePosition
from math import radians,sin,cos,atan2,sqrt
g=pd.read_csv(D/'spacex_launch_geo.csv');sites=g[['Launch Site','Lat','Long']].drop_duplicates();results['geo_sites']=sites.to_dict('records')
m=folium.Map(location=[32,-96],zoom_start=4,tiles='OpenStreetMap');cluster=MarkerCluster(name='Launch outcomes').add_to(m)
for _,r0 in sites.iterrows():folium.CircleMarker([r0.Lat,r0.Long],radius=9,color='#009D9E',fill=True,tooltip=r0['Launch Site']).add_to(m)
for _,r0 in g.iterrows():folium.Marker([r0.Lat,r0.Long],popup=f"Flight {r0['Flight Number']} | {r0['Date']} | class={r0['class']}",icon=folium.Icon(color='green' if r0['class']==1 else 'red')).add_to(cluster)
MousePosition().add_to(m);folium.LayerControl().add_to(m);m.save(str(Path(__file__).resolve().parent/'launch_map.html'))
# Illustrative point-to-point proximity locations; not a nearest-feature GIS computation
p0=[28.562302,-80.577356]
points={'Atlantic coastline (sample point)':[28.56367,-80.57163],'Rail corridor (sample point)':[28.5720,-80.5850],'Road corridor (sample point)':[28.5620,-80.5830],'Titusville center (reference)':[28.6122,-80.8076]}
def distance(p,q):
 a,b,c,d=map(radians,[*p,*q]);h=sin((c-a)/2)**2+cos(a)*cos(c)*sin((d-b)/2)**2;return 6373*2*atan2(sqrt(h),sqrt(1-h))
results['proximity']={k:{'lat':v[0],'lon':v[1],'distance_km':distance(p0,v)} for k,v in points.items()}
near=folium.Map(location=p0,zoom_start=12,tiles='OpenStreetMap');folium.Marker(p0,tooltip='CCAFS LC-40').add_to(near)
for k,v in points.items():
 label=f'{k}: {distance(p0,v):.2f} km (straight line; illustrative point)';folium.Marker(v,tooltip=label).add_to(near);folium.PolyLine([p0,v],tooltip=label,color='#E88554').add_to(near)
MousePosition().add_to(near);near.save(str(Path(__file__).resolve().parent/'proximity_map.html'))
(ROOT/'data/results.json').write_text(json.dumps(results,indent=2,default=lambda x:int(x) if isinstance(x,np.integer) else float(x)))
print('DONE')
