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
                gif.GifPlayer(gif="assets/Sentiment/house_cup.gif", still='assets/Sentiment/house_cup_picture.jpg', autoplay = True),
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
                "their journey from being first-year students to seventh-year students. The characters evolve over time "
                "and the story becomes more elaborate and perhaps even more gloomy. This page will dive into "
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
        html.Div([
            html.H5("Movies"),
            html.Img(
            id = "sentiment_movies",
            src = "assets/Sentiment/chap_sentiment_movies.png", 
            style={'height': '100%', 'width': "90%"}
                )
            ],
        style = {'width': '50%', 'text-align': 'center'}),
        html.Div( [
            html.H5("Books"),
            html.Img(
                id = "sentiment_books",
                src = "assets/Sentiment/chap_sentiment_books.png", 
                style = {'height':'100%', 'width': "90%"}
            )],
            style = {'width': '50%', 'text-align': 'center'}), 
    ], style = {'width': '95vw', 'justify-content': 'center', 'display': 'flex', 'flex-wrap':'wrap', 'marginBottom': '60px'}
    ),

    html.Div([
        html.P(
            id = "text_chapters", style = {'marginLeft': 60, 'marginRight': 60}
        )
    ], style = {'justify-content': 'center', 'display': 'flex', 'flex-wrap':'wrap'}),

    #html.Div([
    #    html.H4("Examine the difference in scale of the sentiment scores between the movies and the books", className="text-center")
    #]),

    html.P(""),

    html.Div([
        html.Img(
            id = "boxplot_movies",
            src = "assets/Sentiment/boxplot_sentiment_movies.png", 
            style={'height': '45%', 'width': "45%"}
                )
        ,
        html.Img(
            id = "boxplot_books",
            src = "assets/Sentiment/boxplot_sentiment_books.png", 
            style = {'height':'45%', 'width': "45%"}
        )
        ], style = {'width': '100vw', 'justify-content': 'center', 'display': 'flex', 'flex-wrap':'wrap', 'marginTop':30}
    ),

    html.P(""),
    
    html.P(children = [
        html.Span(
        "Did you observe the large difference in scale of the sentiment scores between the movies and the books? "
        "The boxplots show the chapter based average sentiment score for the movies and books. Here it is possible "
        "to observe the outliers (chapters with an average sentiment score outside the upper and lower fence). "
        "It can be seen that for the 1st, 5th and 6th movies there are quite a few outliers. This could indicate that "\
        "Hollywood emphasises on emotions in the movies. As you know big emotions are what the viewers want. "\
        "Outliers are only present for the 1st and 5th book, with only 1 and 3 chapters as outliers respectivly. " \
        "When looking at the boxplot for the books it can be seen that "),
       html.Span("Harry Potter and the Goblet of Fire ", style= {"font-style": "italic"}),
       html.Span(
           "has the largest span in sentiment scores. This is the book where Harry falls in love for the first time, "\
           "has a fallout with Ron, enters the Triwizard Tournament and witnesses the return of Voldemort. "
       )
        ]
        , style = {'marginLeft': 60, 'marginRight': 60}
    ),
    # lower fence = Q3 - 1.5*IQR
    # upper fence = Q3 + 1.5*IQR

    #html.Div([
    #    html.H3("Do you want to dive deeper into the sentiment of the Harry Potter Books?", className="text-center")
    #]),
    
])

@app.callback([Output('sentiment_movies', 'src'),
              Output('sentiment_books', 'src'),
              Output('text_chapters', 'children')],
             [Input('sentiment_type', 'value')])

def update_figure(value):

    if value == 'Chapter based':
        src1 = "assets/Sentiment/chap_sentiment_movies.png"
        src2 = "assets/Sentiment/chap_sentiment_books.png"
        text = "A sentiment score has been found for all chapters in the seven books and scenes in the eight movies. " \
            "The most negative scene in the movies is \"Writting on the Wall\" this scene only includes the basilisk " \
            "saying \"Kill!\" and the sentiment score is therefore very negative. The most positive scene is in movie 1, "\
            "where Gryffindor wins the house cup for the first time in a long period. For the books the most negative chapter " \
            "is the one with Dumbledore's death and the flight of the Half-Blood prince. " \
            "The sentiment scores for the scenes in the movies are on a much larger scale than the sentiment scores for the chapters of the books. Does this surprise you? Perhaps " \
            "Hollywood increase the level of sadness/ happiness when producing the movies. " \
            "When looking at the development in sentiment scores for the books, it can be seen that the later books " \
            " do not have the same \"happy ending\" as book 1, 2, 3 and 4 have. They all end on a more gloomy node. However, the epilogue \"Nineteen Years Later\" in the last book, makes sure the series ends happily after all."
    else:
        src1 = "assets/Sentiment/char_sentiment_movies.png"
        src2 = "assets/Sentiment/char_sentiment_books.png"
        text = "Each of the top 10 most connected characters in the Harry Potter universe has an average sentiment score for "\
            "all the seven books and eight movies. It can be seen that in the movies there are some gaps for e.g. "\
            "Sirius Black and Voldemort. This is because the characters do not have any dialogue in that movie. " \
            "It is quite fun to observe the sentiment scores for the characters. Are they as you would expect? If you " \
            "are a Harry Potter fan, you might understand why Draco Malfoy has such a low sentiment score in "\
            "\"Harry Potter and the Dealthly Hallows\" (both the book and the movie)? The Malfoy family is being punished by "\
            "Lord Voldemort and Malfoy is very unhappy about his situation. In \"Harry Potter and the Half-Blood Prince\" "\
            "(the book) both Harry and Ron have the highest average sentiment score. Wonder if this has anything to do "\
            "with their crushes and relationships with Ginny and Lavender (and secretively Hermione). " 
    return src1, src2, text
