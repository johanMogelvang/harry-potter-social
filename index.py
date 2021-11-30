import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app, server
# import all pages in the app
from apps import family_house, home, exploratory, text_analysis


nav = dbc.Nav(
    [
        dbc.NavLink("Home", href="/home"),
        dbc.NavLink("Exploratory", href="/exploratory"),
        dbc.NavLink("Network science", href="/family_house"),
        dbc.NavLink("Books vs. movies", href="/text_analysis"),
    ],
    pills=True,
    fill=True
)


nav_pages = dbc.Row(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/home")),
        dbc.NavItem(dbc.NavLink("Exploratory", href="/exploratory")),
        dbc.NavItem(dbc.NavLink("Network science", href="/family_house")),
        dbc.NavItem(dbc.NavLink("Books vs. movies", href="/text_analysis")),
    ],
    className="g-0 ms-auto flex-nowrap",# "g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center"
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
                        dbc.Col(html.Img(src="/assets/logo.png", height="50px")),
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
    if pathname == '/family_house':
        return family_house.layout
    elif pathname == '/exploratory':
        return exploratory.layout
    elif pathname == '/text_analysis':
        return text_analysis.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)