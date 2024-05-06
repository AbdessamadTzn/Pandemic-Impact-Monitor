import pandas as pd 
import dash 
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import datetime as dt



dash.register_page(__name__)


try:
    df = pd.read_csv("../Data/Pandemic Impact Monitor.csv", encoding='ISO-8859-1')
except Exception as e:
    print(f'File reading error: {str(e)}')
    exit()

df['Year'] = pd.to_datetime(df['Date']).dt.year

layout = html.Div([
html.Label('Select Year:'),
    dcc.Dropdown(
        id='year-dropdown',
        options=[
            {'label': str(year), 'value': year} for year in sorted(df['Year'].unique())
        ],
        value=df['Year'].min(),  # Default value is the minimum year in the data
        clearable=False
    ),
    html.Label('Select Country:'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': country, 'value': country} for country in sorted(df['Country'].unique())
        ],
        value='canada',  
        clearable=False
    ),
    dcc.Graph(id='choropleth-map')
    ])

@callback(
    Output('choropleth-map', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_choropleth_map(selected_year, selected_country):
    # Filter the DataFrame based on selected year and country
    filtered_data = df[(df['Year'] == selected_year) & (df['Country'] == selected_country)]
    
    # Create the choropleth map
    fig_choropleth = px.choropleth(filtered_data, 
                                    locations='Country', 
                                    locationmode='country names', 
                                    color='Unemployment Rate',
                                    hover_name='Country',
                                    color_continuous_scale='Viridis',
                                    #range_color=[0, max(df['Unemployment Rate'])],
                                    title=f'Unemployment Rate for {selected_country} in {selected_year}',
                                    labels={'Country': 'Country Name'}, 
                                    #color_continuous_scale=px.colors.sequential.Inferno,  # Logarithmic scale
                                    color_continuous_midpoint=0.5  # Midpoint of color scale
                                   )
    
    return fig_choropleth