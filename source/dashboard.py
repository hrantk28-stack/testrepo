"""Run: python dashboard.py (datasets are included beside this source directory)."""
from pathlib import Path
import pandas as pd
from dash import Dash,dcc,html,Input,Output
import plotly.express as px
p=Path(__file__).resolve().parent.parent/'data'/'spacex_launch_dash.csv'
if not p.exists():p=Path(__file__).resolve().parents[2]/'data'/'spacex_launch_dash.csv'
df=pd.read_csv(p)
app=Dash(__name__)
app.layout=html.Div(style={'fontFamily':'Arial','background':'#F3F6FA','padding':'28px'},children=[
 html.H1('SpaceX | Launch outcome explorer',style={'color':'#153450'}),
 html.P('Historical course dataset • 56 launches • class 1 = successful landing'),
 dcc.Dropdown(id='site-dropdown',options=[{'label':'All Sites','value':'ALL'}]+[{'label':s,'value':s} for s in sorted(df['Launch Site'].unique())],value='ALL',placeholder='Select a Launch Site here',searchable=True),
 dcc.Graph(id='success-pie-chart'),html.H3('Payload range (kg)'),
 dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,marks={v:str(v) for v in range(0,10001,1000)},value=[0,10000]),
 dcc.Graph(id='success-payload-scatter-chart')])
@app.callback(Output('success-pie-chart','figure'),Input('site-dropdown','value'))
def pie(site):
 if site=='ALL':
  z=df[df['class']==1].groupby('Launch Site',as_index=False)['class'].sum()
  return px.pie(z,values='class',names='Launch Site',title='Share of successful launches by site (not success rate)')
 z=df[df['Launch Site']==site].copy();z['Outcome']=z['class'].map({0:'Not successful',1:'Successful'})
 return px.pie(z,names='Outcome',title=f'{site}: successful vs not successful')
@app.callback(Output('success-payload-scatter-chart','figure'),Input('site-dropdown','value'),Input('payload-slider','value'))
def scatter(site,bounds):
 z=df[df['Payload Mass (kg)'].between(*bounds)]
 if site!='ALL':z=z[z['Launch Site']==site]
 return px.scatter(z,x='Payload Mass (kg)',y='class',color='Booster Version Category',hover_data=['Launch Site','Flight Number'],title=f'Payload and landing class | {site} | {bounds[0]}–{bounds[1]} kg')
if __name__=='__main__':app.run(host='0.0.0.0',port=8050,debug=False)
