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
            options=[{'label': i, 'value': i} for i in ['Topics in the movies', 'Topics in the books']],
            value='Topics in the movies',
            labelStyle={'display': 'inline-block', 'marginLeft':80}
        ),
    ]),

    html.Div([
        html.Div([
            html.Iframe(id = "lda", src="/assets/Topics/lda_movies.html", style={"width":"100%", "height":"900px"}),
            ], style = {'width': '100%'}
        ),
        html.Div([
            html.P(id = 'text_lda', style = {'marginLeft':80, 'marginRight': 80})
            ], style = {'marginTop':'-100px'}
        )], style = {'width': '95vw', 'justify-content': 'center', 'display': 'flex', 
                     'flex-wrap':'wrap', 'marginLeft': '80px', 'marginBottom': 20}),
    
    html.Div([
        html.H1(""),
        html.H3(
            id = "text", style = {'marginLeft': 60, 'marginRight': 60, 'marginBottom': 40}
        )
    ], style = {'justify-content': 'center', 'display': 'flex', 'flex-wrap':'wrap'}),

    html.Div([
        html.Div([
            html.Iframe(id = "graph", src="/assets/Topics/G_topics_movies.html", style={"width":"100%", "height":"600px"})
        ], style = {'width': '45%', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'marginLeft': 60}),
        html.Div([
            html.P(id = "text_graph", style = {'marginLeft': 30, 'marginRight': 60}, 
            )
        ], style = {'width': '45%', 'height': '40vh', 'align': 'center'}, className="h-50")
    ], style = {'width': '95vw', 'height': '600px', 'justify-content': 'center', 'display': 'flex', 'flex-wrap':'wrap'})
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
                "Or do you have more domain knowledge than the LDA model? In the plot above each bubble represents a topic. "\
                "The larger the bubble, the higher percentage of the number of documents in the corpus is about that topic. "\
                "The further the bubbles are away from each other, the more different they are. "\
                "Try to examine topic 3. Here words such as: scrabbers, dementors, firebolt, buckbeak, expecto patronum etc. " \
                "occurs. These words are all very characteristic of the book \"Harry Potter and the Prisoner of Azkaban\".  "\
                "OBS. - Be aware that the this visualisation enumerates the topics according to size, where the topics in "\
                "the graph below is enumerated according to topic number given by the LDA. "
        
        text2 = "How are the topics and the books related?"
        src2 = "assets/Topics/G_topic_books.html"
        text3 = "In the graph each topic and each book is a node. The pink nodes are the books, and the teal nodes "\
                "are the topics. There is an edge between a topic and a book if the topic is in the book. " \
                "The width of the edge is dependent on how important the topic is for the given book. " \
                "Try to hover your curser over the topic nodes to see the 10 most important words in the topic. " \
                "If you do the same for the book nodes you will see the title of the book. " \
                "It can be seen that topic 10 is shared by book 1, 3, 4, 5 and 7, however this topic is less important for "\
                "book 1 and 3 than for the others (indicated by the thin edge). When hovering the curser over topic 10's node "\
                "it can be seen that the topic includes words such as champion, bagman, winky and house-elf which refers to "\
                "book 4 along with words such as: wormtail, dark_lord and department_mystery which can refer to both book 5 "\
                "and 7. What about the rest of the topics? Do you think they are informative? Would you be able to guess "\
                "which book(s) the topic is connected to?"
    else:
        src1 =  "assets/Topics/lda_movies.html"
        text1 = "Do you agree with the results regarding the most important topics for the movies? " \
                "Or do you have more domain knowledge than the LDA model? In the plot above each bubble represents a topic. "\
                "The larger the bubble, the higher percentage of the number of documents in the corpus is about that topic. "\
                "The further the bubbles are away from each other, the more different they are. "\
                "Try to examine topic 3. Here words such as: deatheater, gilliweed, unforgivable, maze, irish, durmstranf etc. " \
                "occurs. These words are all very characteristic of the movie \"Harry Potter and the Goblet of Fire\".  "\
                "OBS. - Be aware that the this visualisation enumerates the topics according to size, where the topics in "\
                "the graph below is enumerated according to topic number given by the LDA. "
        
        text2 = "How are the topics and the movies related?"
        src2 = "assets/Topics/G_topic_movies.html"
        text3 = "In the graph each topic and each movie is a node. The pink nodes are the movies, and the teal nodes "\
                "are the topics. There is an edge between a topic and a movie if the topic is in the movie. " \
                "The width of the edge is dependent on how important the topic is for the given movie. " \
                "Try to hover your curser over the topic nodes to see the 10 most important words in the topic. " \
                "If you do the same for the movie nodes you will see the title of the movie. " \
                "It can be seen that topic 21 is very important for movie 1. Topic 21 contains: harp, norbert and leviosa. "\
                "Do these words make sense to you? The most important topic for movie 3 is topic 12. When hovering the "\
                "curser over the node, it can be seen that the most meaningful words are betrayed, hippogriff and dog. "\
                "Do you think the topics are informative about the movies? Would you be able to guess "\
                "which movie(s) the topic is referring to?"
                
    return src1, text1, text2, src2, text3
