import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app, server
# import all pages in the app
from apps import family_house, home, exploratory, text_analysis, network_analysis, topic_modelling, communities, sentiment_analysis


nav = dbc.Nav(
    [
        dbc.NavLink("Home", href="/home"),
        dbc.NavLink("Exploratory", href="/exploratory"),
        dbc.NavLink("Network science", href="/network_analysis"),
        dbc.NavLink("Community detection", href="/communities"),
        dbc.NavLink("Text Analysis", href="/text_analysis"),
        dbc.NavLink("Sentiment Analysis", href="/sentiment_analysis"),
        dbc.NavLink("Topic modelling", href="/topic_modelling"),
    ],
    pills=True,
    fill=True
)


#dbc.Row( [ dbc.Col(html.Div("One of three columns"), width=3),
# dbc.Col(html.Div("One of three columns")), dbc.Col(html.Div("One of three columns"), width=3), ] )



NAVBAR_STYLE={"background-repeat": "no-repeat",
"background-position": "right top",
"background-size": "300px 30px",
"height":"10%","position":"fixed",
"top":"0","border":"3px solid",
"width":"100%",
"z-index": "999"}

CONTENT_STYLE={"margin-top":"5%"}

navbar = dbc.Navbar(
    html.Div(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/HP_snitch_gold.png", height="60px")),
                        dbc.Col(dbc.NavbarBrand("The Universe of Harry Potter", className="ml-2")),
                        dbc.Col(width="auto"),
                        dbc.Col(width="auto"),
                        dbc.Col(width="auto"),
                        dbc.Col(width="auto"),
                        dbc.Col(width="auto"),
                        dbc.Col(width="auto"),
                        dbc.Col(width="auto"),
                        dbc.Col(width="auto"),
                        dbc.Col(width="auto"),
                        dbc.Col(nav, width={"size":"auto", "order": "last"}, align="center"),
                    ],
                    align="center",
                ),
                href="/home",
                style={"text-decoration":"none"}
            ),
            #dbc.NavbarToggler(id="navbar-toggler2"),
            #nav,
        ]
    ),
    color="primary",
    dark=True,
    className="g-0",#"mb-4",
    style=NAVBAR_STYLE,
)


def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', style=CONTENT_STYLE)
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/exploratory':
        return exploratory.layout
    elif pathname == '/text_analysis':
        return text_analysis.layout
    elif pathname == '/sentiment_analysis':
        return sentiment_analysis.layout
    elif pathname == '/communities':
        return communities.layout
    elif pathname == '/network_analysis':
        return network_analysis.layout
    elif pathname == '/topic_modelling':
        return topic_modelling.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)