import dash_html_components as html
import dash_bootstrap_components as dbc


from app import app

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to the Harry Potter dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='This page is about exploring the initial dataset'
                                     )
                    , className="mb-4")
            ]),
    ]),
    html.Iframe(src="/assets/GCC.html", style=dict(position="absolute",left="0", top="0", width="100%", height="100%"))

])