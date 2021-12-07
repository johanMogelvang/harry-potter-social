from typing import Sized
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_gif_component as gif

from app import app

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
card_width = "25rem"

layout = html.Div([
    html.Div(
            [html.H2("Exploring the Wizarding World of J.K. Rowling with Network Science", style={'width': '100vw',
            'height': 'auto', 'color':'white'})],
            style={'position': 'absolute', 'top':'20vh', 'text-align': 'center'}
        ),
        html.Div(
            [html.Img(src="assets/hogwarts.jpg", style={'width': '100vw',
            'height': 'auto'})],
            style={'width':'100vh'}
        ),
        
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
            dbc.Col(html.H5(children="")
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children=
                                     "Welcome!"
                                     ""
                                     "..."
                                     "The main goal of this project is allowing you to dive into the social network of Harry Potter, Fantastical Beasts and all the side stories from the Wizarding World." 
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
            dbc.Card(
                [
                dbc.CardImg(src="assets/HPlogo.jpg", top = True), 
                dbc.CardBody([
                    dbc.CardLink(
                            html.H5("Exploratory Analysis",
                                #className="text-center"
                            ), 
                            href = "/exploratory", style={"text-decoration":"none"}
                        ),
                    html.P("Explore the features in the Wizarding World. "
                    "The Wizarding universe consists of characters from the Harry Potter world,"
                    "Fantastic Beasts and The Tales of Beedle the Bard, and their features. "
                    "You can explore more about all these amazing characters and the data."
                    , className = "card-text")
                    ]
                ), 
                ], 
                style = {'width':card_width},
            ),
            dbc.Card(
                [
                dbc.CardImg(src="assets/HPlogo.jpg", top = True), 
                dbc.CardBody([
                        dbc.CardLink(
                            html.H5("Network Analysis",
                                #className="text-center"
                            ), 
                            href = "/exploratory", style={"text-decoration":"none"}
                        ),
                    html.P("Explore the relationships in the Wizarding World."
                            "Have you ever wondered how all the characters in the Harry Potter books/ movies are connected? "
                            "Using network science it is possible to explore the interconnections between characters. "
                            "You can even use your imagination to examine relationships across school houses, family houses "
                            "or blood status. "
                    , className = "card-text")
                    ]
                ), 
                ],
                style = {'width':card_width},
            ),
                       dbc.Card(
                [
                dbc.CardImg(src="assets/HPlogo.jpg", top = True), 
                dbc.CardBody([
                    html.H5("Community detection"), 
                    html.P("What are the most important communities in the Wizarding World?"
                            "How strong/ connected are these groups. Are "
                    , className = "card-text")
                    ]
                ), 
                ],
                style = {'width':card_width},
            ),
            dbc.Card(
                [
                dbc.CardImg(src="assets/HPlogo.jpg", top = True), 
                dbc.CardBody([
                    html.H5("Text analysis"), 
                    html.P("Using language processing to examine different groups of characters in the Wizarding World. "
                    "What sets the different species apart? Are all pure-bloods really prejudices? (wordclouds, tf-idf etc)"
                    , className = "card-text")
                    ]
                ), 
                ],
                style = {'width':card_width},
            ),

            dbc.Card(
                [
                dbc.CardImg(src="assets/HPlogo.jpg", top = True), 
                dbc.CardBody([
                    html.H5("Sentiment Analysis"), 
                    html.P(" Sentiment for characters"
                    "Books vs movies,  characters in HP vs Fantastic beasts movies? "
                    , className = "card-text")
                    ]
                ), 
                ],
                style = {'width':card_width},
            ),

            dbc.Card(
                [
                dbc.CardImg(src="assets/HPlogo.jpg", top = True), 
                dbc.CardBody([
                    html.H5("Topic modelling"), 
                    html.P(" topics in the books vs movies"
                    "LDA etc. "
                    , className = "card-text")
                    ]
                ), 
                ],
                style = {'width':card_width},
            )
        ], justify = 'center', className ="mb-5"),

        dbc.Row([
            dbc.Col(html.P(" Enjoy!...  ", className="text-center")
                    , className="mb-5 mt-5")
        ]),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                            html.H5(
                                'Explainer notebook',
                                className="text-center"
                            ), 
                        html.P(
                            "Get the explainer notebook to dive more into the technical aspect of this project.",
                            className="card-text",
                            ),
                        dbc.Row([
                            dbc.Col(
                                dbc.Button(
                                    "Download the explainer notebook", 
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
                               html.H5(
                                'Our data',
                                className="text-center"
                            ), 
                        html.P(
                            "Get the cleaned dataset containing all characters, links and features .... and cleaned text data",
                            className="card-text",
                            ),
                        dbc.Row([
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
                            html.H5(
                                'Source data',
                                className="text-center"
                            ), 
                        html.P(
                            "link to HP fandom and the two github pages for books and movies. ",
                            className="card-text"
                            ),
                        dbc.Row([
                            dbc.Col(
                                dbc.Button(
                                    "Go to HP Wiki", 
                                    href="https://harrypotter.fandom.com/wiki/Main_Page",
                                    color="primary"
                                    ), 
                                className="mt-3"),
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