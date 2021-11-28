import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_gif_component as gif

from app import app

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Exploring the Wizarding World of J.K. Rowling with Network Science", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        #dbc.Row([
        #    dbc.Col(html.Img(src="/assets/logo.png", 
        #                    height="50px"), style={'textAlign': 'center'}),
        #    ]),
       
        dbc.Row([
            dbc.Col(
                gif.GifPlayer(gif="assets/HP.gif", still='assets/HP_cristmas_gif.png', autoplay =True),
                width = "100px",
                style={'textAlign': 'center'}
            )
        ]),

        dbc.Row([
            dbc.Col(html.H5(children='This app marks my very first attempt at using Plotly, Dash and Bootstrap! '
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(
                html.H5(children='It consists of two main pages: Global, which gives an overview of the COVID-19 cases and deaths around the world, '
                                     'Singapore, which gives an overview of the situation in Singapore after different measures have been implemented by the local government.')
                    , className="mb-5")
        ]),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dbc.CardLink(
                            html.H3(
                                'Explore the features in the Wizarding World',
                                className="text-center"
                            ), 
                            href = "/exploratory"
                        ),
                        html.P(
                            "The Wizarding universe consists of characters from the Harry Potter world, "
                            "Fantastic Beasts and The Tales of Beedle the Bard, and their features. "
                            "You can explore more about all these amazing characters and the data. ",
                            className="card-text",
                            ),
                        dbc.Row([
                            #dbc.Col(
                            #    dbc.Button(
                            #        "Explore more", 
                            #        href="/exploratory",
                            #        color="primary"
                            #        ), 
                            #    className="mt-3"),
                            dbc.Col(
                                dbc.Button(
                                    "Get the data", 
                                    href="https://harrypotter.fandom.com/wiki/Main_Page",
                                    color="primary"
                                    ), 
                                className="mt-3"
                                )
                        ],
                        justify = 'align-right'),
                    ]),
                body=True, color="dark", outline=True), 
            style={"center": "2px"}),

            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dbc.CardLink(
                            html.H3(
                                'Explore the relationships between the characters in the Wizarding World',
                                className="text-center"
                            ), 
                            href = "/family_house"
                        ),
                        html.P(
                            "Have you ever wondered how all the characters in the Harry Potter books/ movies are connected? "
                            "Using network science it is possible to explore the interconnections between characters. "
                            "You can even use your imagination to examine relationships across school houses, family houses "
                            "or blood status. ",
                            className="card-text",
                            ),
                        dbc.Row([
                            #dbc.Col(
                            #    dbc.Button(
                            #        "Explore more", 
                            #        href="/family_house",
                            #        color="primary"
                            #        ), 
                            #    className="mt-3"),
                            dbc.Col(
                                dbc.Button(
                                    "Get the data", 
                                    href="https://harrypotter.fandom.com/wiki/Main_Page",
                                    color="primary"
                                    ), 
                                className="mt-3"
                                )
                        ],
                        justify = 'align-right'),
                    ]),
                body=True, color="dark", outline=True), 
            style={"center": "2px"}),

            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dbc.CardLink(
                            html.H3(
                                'Explore the difference between the books and movie scripts',
                                className="text-center"
                            ), 
                            href = "/text_analysis"
                        ),
                        html.P(
                            "How does the sentiment change across the seven books? How does the sentiment change "
                            "across the eight movies? Are there any differences? Do the topics in the books differ "
                            "from those in the movies? ...... ",
                            className="card-text"
                            ),
                        dbc.Row([
                            #dbc.Col(
                            #    dbc.Button(
                            #        "Explore more", 
                            #        href="/text_analysis",
                            #        color="primary"
                            #        ), 
                            #    className="mt-3"),
                            dbc.Col(
                                dbc.Button(
                                    "Get the data - books", 
                                    href="https://github.com/formcept/whiteboard/tree/master/nbviewer/notebooks/data/harrypotter",
                                    color="primary"
                                    ), 
                                className="mt-3"
                                ),
                            dbc.Col(
                                dbc.Button(
                                    "Get the data - movies", 
                                    href="https://github.com/kornflex28/hp-dataset",
                                    color="primary"
                                    ), 
                                className="mt-3"
                                ),
                        ],
                        justify = 'align-right'),
                    ]),
                body=True, color="dark", outline=True), 
            style={"center": "2px"}),
        ], justify = 'start', className="mb-5"),
    ])

])

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)