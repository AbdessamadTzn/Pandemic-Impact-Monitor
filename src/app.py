import dash 
from dash import dcc, html, Input, Output


# Init

app = dash.Dash(__name__, title='Pandemic Impact Monitor', use_pages=True)
server = app.server

app.layout = html.Div(
    [
        # main app framework
        html.H2("Pnademic Impact Monitor - All In Open Source Hackathon", style={'textAlign':'center'}),
        html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'])
            for page in dash.page_registry.values()
        ]),
        html.Hr(),

        # content of each page
        dash.page_container
    ]
)



if __name__ == '__main__':
    app.run_server(debug=True)