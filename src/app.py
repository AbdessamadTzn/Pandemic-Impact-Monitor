import dash 
from dash import dcc, html, Input, Output, clientside_callback, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px

import dash_auth

load_figure_template(["minty", "minty_dark"])

px.defaults.template = "ggplot2"

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

# Init

USER_PASS_MAPPING = {
    "ADMIN":"ADMIN",
    "Developer":"Developer",
    "User":"User"
}

app = dash.Dash(__name__, title='Pandemic Impact Monitor', use_pages=True, external_stylesheets=external_css)
auth = dash_auth.BasicAuth(app, USER_PASS_MAPPING)
server = app.server



app.layout = html.Div(
    [
        # main app framework
        html.Div([
        html.H2("Pandemic Impact Monitor - All In Hackathon", className="text-dark text-center fw-bold fs-1", style={'font-size':20}),
        html.A("Pandemic Impact Monitor Report", href='https://abdessamadtouzani-portfolio.netlify.app/assets/pandemic_impact_exploring.html', target='_blank')
        ], style={'marginTop': 10, 'textAlign':'center'}),
        html.Br(),
        html.Div([
            dcc.Link(page['name'], href=page['path'], className="btn btn-dark m-2 fs-5")
            for page in dash.page_registry.values()
        ]),
        html.Br(),


        # content of each page
        dash.page_container
    ], style={'align-items':'center', 'textAlign':'center'}
)

if __name__ == '__main__':
    app.run_server(debug=True)