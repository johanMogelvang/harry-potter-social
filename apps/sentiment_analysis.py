import dash_html_components as html
import dash_bootstrap_components as dbc


from app import app

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Sentiment analysis of the books and movies", className="text-center")
                    , className="mb-5 mt-5")
        ]),

        dbc.Row([
            dbc.Col(
                html.Img(src="assets/logo.png", style={'textAlign': 'center'}),
                width = "50px",
                style={'textAlign': 'center'}
            ), 
        ]),

        dbc.Row([
            dbc.Col(html.P(
                ".... Through the books and movies, we follow Harry Potter and the other students at Hogwarts on "
                "their journey from being first years to seventh year students. The characters evolve over time "
                "and the story told becomes more elaborate and perhaps even more gloomy. This page will dive into "
                "the world of sentiment analysis for both the seven books and the eight movies. "
                                     )
                    , className="mb-4")
            ]),
    ]),

    html.Div([
        html.Img(
            src = "assets/chap_sentiment_movies.png", 
            style={'height': '45%', 
                    'width': "45%"}
                ),
        html.Img(
            src = "assets/chap_sentiment_books.png", 
            style = {'height':'45%', 'width': "45%"}
        )
        ], style = {'width': '100vw', 'justify-content': 'center', 'display': 'flex'}
    )
])