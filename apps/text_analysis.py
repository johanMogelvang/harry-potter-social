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
                width = "auto",
                #style={'textAlign': 'center'}
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
    #html.Iframe(src="/assets/lda.html", style=dict(position="absolute",left="0", top="0", width="100%", height="100%"))

])