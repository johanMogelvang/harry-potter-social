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
            dbc.Col(html.H1("Topic Modelling", className="text-center")
                    , className="mb-5 mt-5")
        ]),

    dbc.Row([
            dbc.Col(html.P(children = [
                html.Span(
                    "Each book/ movie in the Harry Potter series has its own main topic such as the Triwizard Tournament in  "
                    "the book/ movie "),
                html.Span("Harry Potter and the Goblet of Fire. ", style={"font-style": "italic"}),
                html.Span("Furthermore, the whole Harry Potter series "
                    "have a topic which is part of every book/ movie, namely the inevitable return of Voldemort and the war "
                    "against evil. But at the same time the series contain scenes of love and friendship.  It is therefore "
                    "interesting to examine if any meaningful topics can be found from the movie scripts and the books. To find "
                    "the topics in the story a "
                    ),
                html.Span( "Latent Dirichlet Allocation (LDA) ", style={"font-weight": "bold"}),
                html.Span("model is used. The results are visualised below. "
                )]
            ), className="mb-4")
        ]),
    ]),

    html.Div([
         dcc.RadioItems(
            id='lda_type',
            options=[{'label': i, 'value': i} for i in ['Topics in the books', 'Topics in the movies']],
            value='Topics in the books',
            labelStyle={'display': 'inline-block', 'marginLeft':80}
        ),
    ]),

    html.Div([
        html.Div([
            html.Iframe(id = "lda", src="/assets/Topics/lda_books.html", style={"width":"100%", "height":"1000px"}),
            ], style = {'width': '100%'}
        ),
        html.Div([
            html.P(id = 'text_lda', style = {'marginLeft':80, 'marginRight': 80})
            ]
        )], style = {'width': '95vw', 'justify-content': 'center', 'display': 'flex', 
                     'flex-wrap':'wrap', 'marginLeft': '80px'}),
    
    html.Div([
        html.H3(
            id = "text", style = {'marginLeft': 60, 'marginRight': 60}
        )
    ], style = {'justify-content': 'center', 'display': 'flex', 'flex-wrap':'wrap'}),

    html.Div([
        html.Div([
            html.Iframe(id = "graph", src="/assets/Topics/G_topics_books.html", style={"width":"100%", "height":"800px"})
        ], style = {'width': '45%', 'text-align': 'center', 'marginLeft': 60}),
        html.Div([
            html.P(id = "text_graph", style = { 'marginRight': 60, 'display': 'inline-block', 'vertical-align': 'middle'}
            )
        ], style = {'width': '45%'})
    ], style = {'width': '95vw', 'justify-content': 'center', 'display': 'flex', 'flex-wrap':'wrap'})
])


@app.callback([Output('lda', 'src'),
              Output('text_lda', 'children'),
              Output('text', 'children'),
              Output('graph', 'src'),
              Output('text_graph', 'children')],
             [Input('lda_type', 'value')])

def update_figure(value):

    if value == 'Topics in the books':
        src1 = "assets/Topics/lda_books.html"
        text1 = "Do you agree with the results regarding the most important topics for the books? " \
                "Or do you have more domain knowledge than the LDA model? "
        
        text2 = "How are the topics and the books related?"
        src2 = "assets/Topics/G_topic_books.html"
        text3 = "In the graph each topic and each book is a node. The pink nodes are the books, and the teal nodes "\
                "are the topics. There is an edge between a topic and a book if the topic is in the book. " \
                "The width of the edge is dependent on how important the topic is for the given book. " \
                "Try to hover your curser over the topic nodes to see the 10 most important words in the topic. " \
                "If you do the same for the book nodes you will see the title of the book. " \
                "It can be seen that ..... "
    else:
        src1 =  "assets/Topics/lda_movies.html"
        text1 = "Do you agree with the results regarding the most important topics for the movies? " \
                "Or do you have more domain knowledge than the LDA model? "
        
        text2 = "How are the topics and the movies related?"
        src2 = "assets/Topics/G_topic_movies.html"
        text3 = "In the graph each topic and each movie is a node. The pink nodes are the movies, and the teal nodes "\
                "are the topics. There is an edge between a topic and a movie if the topic is in the movie. " \
                "The width of the edge is dependent on how important the topic is for the given movie. " \
                "Try to hover your curser over the topic nodes to see the 10 most important words in the topic. " \
                "If you do the same for the movie nodes you will see the title of the movie. " \
                "It can be seen that topic 8 is very important for movie 2. Have you "\
                "hovered your mouse over it? Do the words make sense? Do the topic fit with " \
                "movie 2? \"Salazar, parseltongue\" are quite describing of the movie.  "

    return src1, text1, text2, src2, text3
