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

card_img_style ={
    'width': '100%',
    'height': '15vw',
    'object-fit': 'cover'
}

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Exploring the Wizarding World of J.K. Rowling with Network Science", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children="")
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children=
                                     ["Welcome!",
                                     html.Br(),
                                     html.Br(),
                                     "The main goal of this project is to allow you to dive into the social network of Harry Potter, Fantastical Beasts and all the side stories from the Wizarding World. ",
                                     "You can explore many different aspects of the wizarding world, from investigating important relationships and central characters to analysing the development throughout the Harry Potter series with sentiment analysis. ",
                                     "Using interactive graphs you have the oppurtunity to dive into the wizarding world and find your own new insights. ",
                                     html.Br(),
                                     html.Br(),
                                     "The site has been split into multiple pages, so you can explore precisely what you find interesting. If you just want to explore, we recommend following the steps seen below:"
                                     ])
                    , className="mb-4 ", style={'position': 'absolute',
                                               'top': '150%',
                                               'left': '50%',
                                               'transform': 'translate(-50%, -50%)',
                                               'width':'60vw'
                                               })
            ])
    ], style={'position': 'absolute', 'top':'200px', 'text-align': 'center', 'color':'white', 'justify-content':'center', 'max-width':'100vw'}),
    # html.Div(
    #         [html.H2("Exploring the Wizarding World of J.K. Rowling with Network Science", style={'width': '100vw',
    #         'height': 'auto', 'color':'white'})],
    #         style={'position': 'absolute', 'top':'20vh', 'text-align': 'center'}
    #     ),
    html.Div(
            [html.Img(src="assets/home_page_test.jpg", style={'width': '100vw',
            'height': 'auto',
            'max-height':'1000px'})],
            style={'width':'100vh', 'margin-bottom':'5vh'}
    ),
    ##JOHAN


    dbc.Container([

        dbc.Row([
            dbc.Card(
                [
                dbc.CardImg(src="assets/logos/houses_distribution.png", top = True, style=card_img_style), 
                dbc.CardBody([
                    dbc.CardLink(
                            html.H5("Exploratory Analysis",
                                #className="text-center"
                            ), 
                            href = "/exploratory", style={"text-decoration":"none"}
                        ),
                    html.P("Explore the features in the Wizarding World. "
                    "The Wizarding universe consists of many different characters from the Harry Potter world, "
                    "Fantastic Beasts, The Tales of Beedle the Bard and many others. "
                    "You can explore more about all these amazing characters, their features and the data."
                    , className = "card-text")
                    ]
                ), 
                ], 
                style = {'width':card_width},
            ),
            dbc.Card(
                [
                dbc.CardImg(src="assets/logos/GCC.png", top = True, style=card_img_style), 
                dbc.CardBody([
                        dbc.CardLink(
                            html.H5("Network Analysis",
                                #className="text-center"
                            ), 
                            href = "/network_analysis", style={"text-decoration":"none"}
                        ),
                    html.P( "Have you ever wondered how all the characters in the Harry Potter books/ movies are connected? "
                            "Using network science it is possible to explore the interconnections between characters. "
                            "You can even examine relationships based on family ties or interactions between houses."
                    , className = "card-text")
                    ]
                ), 
                ],
                style = {'width':card_width},
            ),
                       dbc.Card(
                [
                dbc.CardImg(src="assets/logos/communities2.jpeg", style=card_img_style), 
                dbc.CardBody([
                    dbc.CardLink(
                            html.H5("Community Detection",
                                #className="text-center"
                            ), 
                            href = "/communities", style={"text-decoration":"none"}
                        ),
                    html.P("The Wizarding World is a large network of many different characters connected "\
                            "across different family houses, school houses etc. Have you ever wondered how the "\
                            "Wizarding World can be split into communities? We will partition the network into "\
                            "communities using four different partitions and examine how strong the communities are."
                    , className = "card-text")
                    ]
                ), 
                ],
                style = {'width':card_width},
            ),
            dbc.Card(
                [
                dbc.CardImg(src="assets/logos/Wordcloud_slytherin.png", top = True, style=card_img_style), 
                dbc.CardBody([
                    dbc.CardLink(
                            html.H5("Text Analysis",
                                #className="text-center"
                            ), 
                            href = "/text_analysis", style={"text-decoration":"none"}
                        ), 
                    html.P("Using language processing it is possible to examine different groups of characters in the "\
                    "Wizarding World. What sets the different species apart? Can we identify characteristics for different "
                    "groups from their WikiPages? Are all pure-bloods really prejudiced? And are Gryffindors really as brave "
                    "as they would like us to believe? "
                    , className = "card-text")
                    ]
                ), 
                ],
                style = {'width':card_width},
            ),

            dbc.Card(
                [
                dbc.CardImg(src="assets/logos/sentiment_analysis.jpg", top = True, style=card_img_style), 
                dbc.CardBody([
                    dbc.CardLink(
                            html.H5("Sentiment Analysis",
                                #className="text-center"
                            ), 
                            href = "/sentiment_analysis", style={"text-decoration":"none"}
                        ), 
                    html.P("Through the Harry Potter series we follow Harry through thick and thin, we experience "\
                        "his happiness and sadness and we watch him grow up and prepare himself for the war against "\
                        "Voldemort. You can here examine how the sentiment evolves over time through all eight movies and "\
                        "seven books. You can also explore how the sentiment for the top 10 most connected characters in the "\
                        "Harry Potter universe changes through the story. "
                    , className = "card-text")
                    ]
                ), 
                ],
                style = {'width':card_width},
            ),

            dbc.Card(
                [
                dbc.CardImg(src="assets/Topics/topics_homepage.png", top = True, style=card_img_style), 
                dbc.CardBody([
                    dbc.CardLink(
                            html.H5("Topic Modelling",
                                #className="text-center"
                            ), 
                            href = "/topic_modelling", style={"text-decoration":"none"}
                        ),
                    html.P(children = [
                        html.Span("Have you ever thought about which topics appear in the different books and movies?"\
                            "Of course there is the topic of Harry Potter vs. Voldemort. Can you think of other "\
                            "topics? Perhaps that of the Triwizard Tournament in "),
                        html.Span("Harry Potter and the Goblet of Fire? ", style= {"font-style": "italic"}),
                        html.Span("Try exploring this page to see which topics have been identified for the books "\
                                  "and the movies. Do you think they will differ? ")
                        ]
                    , className = "card-text")
                    ]
                ), 
                ],
                style = {'width':card_width},
            )
        ], justify = 'center', className ="mb-5", style={'top':'5vh'}),

        dbc.Row([
            dbc.Col(html.P("All the data on this webpage has been gathered from the Harry Potter Wiki, make sure to go and check the wiki site out below.", className="text-center")
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
                            "Get the explainer notebook to dive more into the technical aspect of this project. "
                            "You can view and download it by clicking on the button. ",
                            className="card-text",
                            ),
                        dbc.Row([
                            dbc.Col(
                                dbc.Button(
                                    "Examine the explainer notebook", 
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
                                className="text-center"),
                        html.P(
                            "Get the cleaned dataset containing all characters, links and features used for building the "
                            "network. Along with the movie-scripts and the books. ",
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
                            "Do you want to examine the original data? Below you will find a link to the Harry Potter fandom "
                            "as well as links to the raw data for books and movies. ",
                            className="card-text"
                            ),
                        dbc.Row([
                            dbc.Col(
                                dbc.Button(
                                    "HP Wiki", 
                                    href="https://harrypotter.fandom.com/wiki/Main_Page",
                                    color="primary"
                                    ), 
                                className="mt-3"),
                            dbc.Col(
                                dbc.Button(
                                    "Books", 
                                    href="https://github.com/neelk07/neelkothari/tree/master/blog/static/data/text",
                                    color="primary"
                                    ), 
                                className="mt-3"
                                ),
                            dbc.Col(
                                dbc.Button(
                                    "Movies", 
                                    href="https://github.com/Kornflex28/hp-dataset/tree/main/datasets",
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
    ]),
])

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)