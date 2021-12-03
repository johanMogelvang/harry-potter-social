from pandas.io.pytables import ClosedFileError
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table
import networkx as nx
import dash_cytoscape as cyto
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import json
import pickle 

from app import app

df = pd.read_csv('HP_enriched_character_df.csv').drop(columns=["name"])

cols = [col.capitalize() if col!= "blood" else "Blood-status" for col in df.columns]
attribute_dict = [{'label':col, "value": col} for col in cols]
attribute_options_default = [{'label':h, "value": h} for h in pd.unique(df.house)]

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("Analysing groups of characters in the Wizarding World", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.P(children=[
                html.Span('The Wizarding World is populated by many distinct groups of characters and species that each have their own important features. '
                          'But what sets the different groups apart? What are the defining characteristics of e.g. a House Elf or a Giant? Are pure-bloods truly different from half-bloods? '
                          'All these questions and more can be investigated by examining the top words for the different groups. ' 
                          "Using natural language processing, the text from the characters' wiki-pages have been processed and the most important words have been determined using "
                        ),
                html.Strong("term frequency-inverse document frequency (TF-IDF) "), 
                html.Span("to score the words for each group. "
                          "The results can be visualized as word-clouds where the size of each word indicate the importance of that word to the group."
                        )
                ])
            ),
        ]),
        dbc.Row([
            dbc.Col(html.P(children=[
                html.Span("First choose which attribute, you want to examine. Then choose which values you want to compare, e.g. "),
                html.Em("Humans and Centaurs "),
                html.Span("or "),
                html.Em("Gryffindor and Slytherin" ),
                html.Span(".")
                    ])
                )
            ])
    ]),
     # choose between which attribute
    html.Div([
        dcc.Dropdown(
            id='attribute_for_wordclouds',
            options=
                attribute_dict,
            value='House',
            style={'width': '50%', 'marginTop': 30,'marginBottom': 20,'marginLeft': 120}
        ),
        dcc.Dropdown(
            id='word_cloud_options',
            options=
                attribute_options_default,
            value="",#'Gryffindor',
            multi=True,
            style={'width': '70%', 'marginTop': 30,'marginBottom': 20,'marginLeft': 0}
        )
    ], style=dict(display='flex')),

    html.Div(
        id = 'word-cloud-images', children =[ 
        html.Img(
            id = 'word-cloud-image',
            src="",#"/assets/Wordclouds/wordcloud_Gryffindor.png",
            style=dict(width="50%", 
                    height="50%")
            )
        ]
    )
])

@app.callback(
            [Output('word_cloud_options', 'options')],
            [Input('attribute_for_wordclouds', 'value')],
            )
def update_dropdown(value):
    # in the df "blood-status is simply blood so rename this
    value = value.lower()
    if value == "blood-status":
        value = "blood"

    attribute_options = [{'label':h, "value": h} for h in pd.unique(df[value])]
    return  [attribute_options]

@app.callback(
            [Output('word-cloud-images', 'children')],
            [Input('attribute_for_wordclouds', 'value')],
            [Input('word_cloud_options', 'value')],
            )

def update_wordclouds(attribute, options):
    children = []

    for val in options: 
        if val == "unknown":
            attr_dict = {"Blood-status":"blood","Species":"species","Gender":"gender","House":"house"}
            attr = attr_dict[attribute]
            val = attr+"_"+val
        wordcloud = "/assets/Wordclouds/"+str(val)+".png"
        children.append(html.Img(id = 'word-cloud-image',
                                    src=wordcloud,
                                    style=dict(width="45%", 
                                    height="45%")
                                )
                         )
    return  [children]
   
