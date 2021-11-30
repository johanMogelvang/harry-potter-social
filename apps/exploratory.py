import dash_html_components as html
import dash_bootstrap_components as dbc


from app import app

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead

graph_style = {"maxHeight": "auto", "align":"center", "margin": "auto"}

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
<<<<<<< HEAD
    
    dbc.Row([
        html.Iframe(src="/assets/lda.html", style={"height": "1067px", "width": "100%"}) #style=dict(position="absolute",left="0", top="0", width="100%", height="100%"))
        ])

=======
    dbc.Container(
    html.Iframe(src="/assets/lda.html", style={"width":"100%", "height":"1067px"}),
    style=graph_style
    )
>>>>>>> origin/main
])

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)