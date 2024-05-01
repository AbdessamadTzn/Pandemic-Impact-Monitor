import pandas as pd 
import dash 
from dash import dcc, html, Input, Output
import plotly.express as px
import datetime as dt 



dash.register_page(__name__)

try:
    df = pd.read_csv("../Data/Pandemic Impact Monitor.csv", encoding='ISO-8859-1')
except Exception as e:
    print(f'File reading error: {str(e)}')
    exit()


df['Year'] = pd.to_datetime(df['Date']).dt.year

fig_3rd_division = px.scatter(df, x="Consumer Confidence", y="Unemployment Rate", animation_frame="Year", animation_group="Services PMI",
                 color="Ticker", hover_name="Country", facet_col="Ticker",
                 log_x=True)
fig_3rd_division.update_xaxes(title="Confidence")

layout = html.Div([
        html.Div([
        dcc.Graph(figure=fig_3rd_division)
    ])
])
