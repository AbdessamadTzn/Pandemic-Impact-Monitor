import pandas as pd 
import dash 
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import datetime as dt 


dash.register_page(__name__, path='/')
try:
    df = pd.read_csv("../Data/Pandemic Impact Monitor.csv", encoding='ISO-8859-1')
except Exception as e:
    print(f'File reading error: {str(e)}')
    exit()

df['Year'] = pd.to_datetime(df['Date']).dt.year


layout = html.Div([
        html.Label("Select Country"),
        dcc.Dropdown(options = [{'label': country, 'value': country} for country in df['Country'].unique()], value='switzerland', id='country'),
        dcc.Graph(id='lineplot')
    ])

@callback(
    Output(component_id='lineplot', component_property='figure'),
    Input(component_id='country', component_property='value')
)
def line_chart(input_country):
    if input_country is None:
        return {}
    else:
        selected_country_data = df[df['Country'] == input_country]
        
        # Group the data by year and calculate the average consumer confidence for each year
        avg_consumer_confidence = selected_country_data.groupby('Year')['Consumer Confidence'].mean().reset_index()
        
        fig = px.line(avg_consumer_confidence, x='Year', y='Consumer Confidence', 
                      title=f'Average Consumer Confidence Trend for {input_country}')
        
        # Customize the plot layout 
        fig.update_layout(xaxis_title='Year', yaxis_title='Average Consumer Confidence')

        return fig