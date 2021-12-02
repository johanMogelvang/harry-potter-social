import dash_html_components as html
import dash_bootstrap_components as dbc


from app import app

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Text analysis", className="text-center")
                    , className="mb-5 mt-5")
        ])
    ]), 
])