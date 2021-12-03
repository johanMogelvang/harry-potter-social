from pandas.io.pytables import ClosedFileError
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import dash_gif_component as gif

from app import app

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Sentiment analysis of the books and movies", className="text-center")
                    , className="mb-5 mt-5")
        ]),

        dbc.Row([
            dbc.Col(
                gif.GifPlayer(gif="assets/house_cup.gif", still='assets/house_cup_picture.jpg', autoplay = True),
                width = "100px",
                style={'textAlign': 'center'}
            ), 
        ]),

        dbc.Row([
            dbc.Col(html.H5(children="" 
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.P(
                "Through the books and movies, we follow Harry Potter and the other students at Hogwarts on "
                "their journey from being first year students to seventh year students. The characters evolve over time "
                "and the story told becomes more elaborate and perhaps even more gloomy. This page will dive into "
                "the world of sentiment analysis for both the seven books and the eight movies. Here you can explore the "
                "sentiment of the top 10 most connected characters through the story and a chapter based sentiment across "
                "the story. "
                                     )
                    , className="mb-4")
            ]),
    ]),

    html.Div([
        html.H3("Sentiments of the Harry Potter Books vs. Movies", className="text-center")
    ]),

    html.Div([
         dcc.RadioItems(
            id='sentiment_type',
            options=[{'label': i, 'value': i} for i in ['Chapter based', 'Character based']],
            value='Chapter based',
            labelStyle={'display': 'inline-block', 'marginLeft':80}
        ),
    ]),
    html.Div([
        html.H5("Movies", style = {'display': 'inline'}),
        html.H5("Books", style = {'display': 'inline'})],
        style = {'marginLeft': 80, 'marginRight': 80}),
    html.Div([
        html.Img(
            id = "sentiment_movies",
            src = "assets/chap_sentiment_movies.png", 
            style={'height': '45%', 'width': "45%"}
                )
        ,
        html.Img(
            id = "sentiment_books",
            src = "assets/chap_sentiment_books.png", 
            style = {'height':'45%', 'width': "45%"}
        )
        ], style = {'width': '100vw', 'justify-content': 'center', 'display': 'flex', 'flex-wrap':'wrap'}
    ),
    html.P(""),

    html.Div([
        html.P(
            id = "text_chapters", style = {'marginLeft': 60, 'marginRight': 60}
        )
    ], style = {'justify-content': 'center', 'display': 'flex', 'flex-wrap':'wrap'}),

    html.Div([
        html.H4("Examine the difference in scale of the sentiment scores between the movies and the books", className="text-center")
    ]),

    html.P(""),

    html.Div([
        html.Img(
            id = "boxplot_movies",
            src = "assets/boxplot_sentiment_movies.png", 
            style={'height': '45%', 'width': "45%"}
                )
        ,
        html.Img(
            id = "boxplot_books",
            src = "assets/boxplot_sentiment_books.png", 
            style = {'height':'45%', 'width': "45%"}
        )
        ], style = {'width': '100vw', 'justify-content': 'center', 'display': 'flex', 'flex-wrap':'wrap'}
    ),

    html.P(""),
    
    html.P(
        "Did you observe the large difference in scale of the sentiment scores between the movies and the books?"
        "The boxplot is showing the chapter based average sentiment score for the movies and books. We observe more "
        "outliers (chapters with an average sentiment score outside the upper and lower fence). This is especially "
        "the case for the 1st, 5th and 6th movie. Outliers are only present for 1st and 5th book, with only 1 and 3 "
        "chapters as outliers. ", style = {'marginLeft': 60, 'marginRight': 60}
    ),
    # lower fence = Q3 - 1.5*IQR
    # upper fence = Q3 + 1.5*IQR

    html.Div([
        html.H3("Do you want to dive deeper into the sentiment of the Harry Potter Books?", className="text-center")
    ]),
    
])

@app.callback([Output('sentiment_movies', 'src'),
              Output('sentiment_books', 'src'),
              Output('text_chapters', 'children')],
             [Input('sentiment_type', 'value')])

def update_figure(value):

    if value == 'Chapter based':
        src1 = "assets/chap_sentiment_movies.png"
        src2 = "assets/chap_sentiment_books.png"
        text = "A sentiment score has been found for all chapters in the seven books and scenes in the eight movies. " \
            "The most negative scene in the movies is \"Writting on the Wall\" this scene only includes the basilisk " \
            "saying \"Kill!\" and the sentiment score is therefore very negative. For the books the most negative chapter " \
            "is the one with Dumbledore's death and the flight of the Half-Blood prince. " \
            "The scenes in the movies have larger sentiment scores than the books. Does this seem surprise you? Perhaps " \
            "Hollywood increase the level of sadness/ happiness when producing the movies. " \
            "When looking at the development in sentiment scores for the books, it can be seen that for the later books " \
            "they do not have the same \"happy ending\" as book 1, 2, 3 and 4 have. They all end on a more gloomy node. "
    else:
        src1 = "assets/char_sentiment_movies.png"
        src2 = "assets/char_sentiment_books.png"
        text = "Each of the top 10 most connected characters in the Harry Potter universe has an average sentiment score for "\
            "all the seven books and eight movies. It can be seen that in the movies there are some gaps for e.g. "\
            "Sirius Black and Voldemort. This is because the characters do not have any dialogue in that movie. " \
            "It is quite fun to observe the sentiment scores for the characters. Are they as you would expect? If you " \
            "are a Harry Potter fan, you might understand why Draco Malfoy has such a low sentiment score in "\
            "\"Harry Potter and the Dealthly Hallows\" (both the book and the movie)? The Malfoy family is being punished by "\
            "Lord Voldemort and Malfoy is very unhappy about his situation. In \"Harry Potter and the Half-Blood Prince\" "\
            "(the book) both Harry and Ron have the highest on average sentiment score. Wonder if this have anything to do "\
            "with crushes and relationships with Ginny and Lavender (and secretively Hermione). " 
    return src1, src2, text