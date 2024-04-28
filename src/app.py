import pandas as pd 
import dash 
from dash import dcc, html, Input, Output
import plotly.express as px
import datetime as dt 

# Init app

app = dash.Dash(__name__, title='Pandemic Impact Monitor')
server = app.server

# Import data

df = pd.read_csv("../Data/Pandemic Impact Monitor.csv", encoding='ISO-8859-1')

# Layout Section


df['Year'] = pd.to_datetime(df['Date']).dt.year

# Third division plot
fig_3rd_division = px.scatter(df, x="Consumer Confidence", y="Unemployment Rate", animation_frame="Year", animation_group="Services PMI",
                 color="Ticker", hover_name="Country", facet_col="Ticker",
                 log_x=True)
fig_3rd_division.update_xaxes(title="Confidence")

app.layout = html.Div([

    # First division
    html.Div([
        html.H2("Pandemic Impact Monitor - All In Hackathon"),
        html.A("Pandemic Impact Monitor Report", href='https://abdessamadtouzani-portfolio.netlify.app/assets/pandemic_impact_exploring.html', target='_blank')
    ], style={'marginTop': 10, 'textAlign':'center'}),

    # Second division (Costumer Confidence by country over time)
    html.Div([
        html.Label("Select Country"),
        dcc.Dropdown(options = [{'label': country, 'value': country} for country in df['Country'].unique()], value='switzerland', id='country'),
        dcc.Graph(id='lineplot')
    ]),

    # Third division Parallel coordinates
    html.Div([
        dcc.Graph(figure=fig_3rd_division)
    ]),

    # Fourth division
    html.Div([
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
])

# Layout End

# Controls for building the interactions

# Second division
@app.callback(
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

# Fourth Division
@app.callback(
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





if __name__ == '__main__':
    app.run_server(debug=True)