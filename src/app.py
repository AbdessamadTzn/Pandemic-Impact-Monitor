import dash 
from dash import dcc, html, Input, Output, clientside_callback, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd

'''
For auth...TODO
import dash_auth 
USER_PASS_MAPPING = {
    "ADMIN":"ADMIN",
    "Developer":"Developer",
    "User":"User"
}
'''

load_figure_template(["minty", "minty_dark"])

px.defaults.template = "ggplot2"

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" ]

# Init

app = dash.Dash(__name__, title='Pandemic Impact Monitor', external_stylesheets=external_css)

# app.dash_auth(app, USER_PASS_MAPPING)

server = app.server
try:
    df = pd.read_csv("../Data/Pandemic Impact Monitor.csv", encoding='ISO-8859-1')
except Exception as e:
    print(f'File reading error: {str(e)}')
    exit()

df['Year'] = pd.to_datetime(df['Date']).dt.year



app.layout = html.Div(
    [
        # main app framework
        html.Div([
        html.H2("Pandemic Impact Monitor", className="text-dark text-center fw-bold fs-1", style={'font-size':20}),
        html.A("Pandemic Impact Monitor Report", href='https://abdessamadtouzani-portfolio.netlify.app/assets/pandemic_impact_exploring.html', target='_blank')
        ], style={'marginTop': 10, 'textAlign':'center'}),
        # html.Br(),
        # html.Div([
        #     dcc.Link(page['name'], href=page['path'], className="btn btn-dark m-2 fs-5")
        #     for page in dash.page_registry.values()
        # ]),
        html.Br(),
        html.Div([
        html.Label("Select Country"),
        dcc.Dropdown(options = [{'label': country, 'value': country} for country in df['Country'].unique()], value='switzerland', id='country'),
        dcc.Graph(id='lineplot')
    ]),
    ], style={'align-items':'center', 'textAlign':'center'}
)



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
                    template="minty",
                    title=f'Average Consumer Confidence Trend for {input_country}')
        
        # Customize the plot layout 
        fig.update_layout(xaxis_title='Year', yaxis_title='Average Consumer Confidence')

        return fig


if __name__ == '__main__':
    app.run_server(debug=True)