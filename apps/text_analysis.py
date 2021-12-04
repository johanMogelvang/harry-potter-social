from pandas.io.pytables import ClosedFileError
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State
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
                          'All these questions and more can be investigated by examining the most important words for the different groups. ' 
                          "Using natural language processing, the texts from the characters' wiki-pages have been processed and the top words have been determined using "
                        ),
                html.Strong("term frequency-inverse document frequency (TF-IDF) "), 
                html.Span("to score the words for each group. You can read more about this in the explainer notebook."
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
            style={'width': '50%', 'marginTop': 10,'marginBottom': 0,'marginLeft': 120}
        ),
        dcc.Dropdown(
            id='word_cloud_options',
            options=
                attribute_options_default,
            value=['Slytherin','Gryffindor'],
            multi=True,
            style={'width': '70%', 'marginTop': 10,'marginBottom': 0,'marginLeft': 0}
        )
    ], style=dict(display='flex')),

    # IMAGES
    html.Div(
        id = 'word-cloud-images', 
        children = [ 
        html.Img(
            src=""
            )
    ], style={'textAlign': 'center'}
    ),
    # COMMENTS
    html.Div([
        dcc.Markdown(
            id = 'comments-on-wordclouds', children = [""]
            )
    ],style = {'width':"90vw","marginLeft":"5vw", "justify-content":"center"}
    )
])

@app.callback(
            [Output('word_cloud_options', 'options')],
            [Output('comments-on-wordclouds', 'children')],
            [Input('attribute_for_wordclouds', 'value')],
            )
def update_dropdown(value):
    # in the df "blood-status is simply blood so rename this
    if not value:
        return [[]]

    # convert to lower and make sure it matches the feature in the dataframe
    value = value.lower()
    if value == "blood-status":
        value = "blood"

    # if the user chooses species, then sort by frequency (as there are A LOT of species)
    if value == "species":
        df_options = df[value]
        df_options = list(df[value].value_counts().index)
    else: 
        df_options = list(pd.unique(df[value]))

    # Remove unknown from options (except for gender)
    if value != "gender":
        df_options.remove('unknown')

    # Define options
    attribute_options = [{'label':h, "value": h} for h in df_options]

    # Text to display depending on chosen attribute
    if value == "blood":
        text = ["The blood-status of a character plays an important role in the Harry Potter series. Voldemort and his Deatheaters believe that only pure-blood (a wizard with two wizard parents) should be allowed to learn magic. "
                "They also consider muggles (non-magic people) and muggle-borns (wizards born to muggle parents) to be inferior to wizards and believe that wizards should rule over muggles. "
               "Overall, there is a lot of prejudice in the wizarding world about blood-status. However, since the wiki-pages are written in (mostly) neutral language, this is not very clear from the wordclouds."
               "One exception is the word *mudblood* in the Muggle-born, which is a very offensize term. " 
               "Instead, the wordclouds seem to reference traits about the characters of that specific blood-type, e.g. there are many words in the Muggle-born category, which can be connected with Hermione. "
               "Voldemort and Harry Potter are both half-bloods, which might explain why *powerfull, kill* and *skill* are important words here. Words such as *prophecy, prediction* and *divination* also reference the prophecy there exists between these two characters. "

                ]
    if value == "house":
        text = ["In the Wizarding World a character's house is a very important identifier and often means that the character posses specific traits. "
                "The stereotypes are that Gryffindors are brave and noble, Hufflepuffs are friendly and hard-working, Ravenclaws are clever and wise while Slytherins are mostly characterised as mean and bigoted. "
                "The houses also have specific objects and historican events associated with them. "
                "It can be observed that e.g. the word *Locket* is very important to both Gryffindor and Slytherin. "
                "This must reference Slytherins locket, which three major Gryffindors (Ron, Hermione and Harry) destroy as part of their quest to defeat Voldemort. "
                "In the Slytherin wordcloud *mudblood* and *bloodline* are also very important words, which could suggest that Slytherins indeed are prejudiced and arrogant. If you look closer, there are also words such as *murdering, taunted, torturing, disowned* and *aristocracy*, which overall give a negative impression of Slytherin as a house. " 
                "The other wordclouds seem to mostly refer to important characters and events associated with this house. Especially the Hufflepuff wordcloud is very influenced by the most famous Hufflepuff, Newton Scamander, who has a magically-expanded *suitcase* where he among other things has a *obscurus* and a wide variety of magical beasts."

                "\n \nThere are also some American characters such as Queenie Goldstein (from the Fanastic Beasts and Where to Find Them movies), "
                "who went to Ilvermorny (the American equivalent of Hogwarts). You can dive more into these American houses by examining their wordclouds."
                ]
    if value == "species":
        text = ["There are many different species in the dataset. The four most common are Humans followed by Goblins, House-elfs and Giants, "
                "and it can be seen that the wordclouds have captured some very distinct characteristics for each species."
                
                "\n \n * What sets **Humans** apart from the other species in the Wizarding World is mainly the right to bear a *wand*, which is why this is the most important word for humans. "
                "Another important word is *charm* which is a group of spells, thus also referincing the magical abilities of the humans. "

                "\n \n* **Goblins** are skilled metalsmiths and bankers, who to some extent control the wizarding economy. This is clearly referenced in the wordcloud where top-words are *bank*, *sword* and *security*. "
                
                "\n \n* **House-elfs** are servants (or slaves) to wizarding families, which is referenced by words such as *worked*, *kitchen*, *job*, *cleaning* and *clothes*. Dobby becoming a free elf is also clearly referenced. "
                "It is also possible to find titles that the house elves address their masters by such as *snr (senior), jnr (junior)* and *mistress*."

                "\n \n* **Giants** are rather violent creatures living in the mountains. One exception is Hagrid's half-brother Grawp who he attempts to teach English (see the word *brother* and *English* in the wordcloud). The chief of the giants is called the *Gurg*, which explains why this is such an important word."
                ]
    if value == "gender":
        text = ["The male and female wordclouds seem very similar, as the most important words for both are e.g. *relationship* and *love*. This indicated that this is perhaps not the most interesting partitioning of the characters as the characters are described quite similar regardless if they are male or female. "
                "However, one thing to note is that *husband* and *marriage* are important words in the female wordcloud - a female character's spouse is clearly often mentioned in relation to them!"
        ]

    return  [attribute_options, text]

@app.callback(
            [Output('word-cloud-images', 'children')],
            [Input('attribute_for_wordclouds', 'value')],
            [Input('word_cloud_options', 'value')]
            )

def update_wordclouds(attribute, options):
    children = []
    attr_dict = {"Blood-status":"blood","Species":"species","Gender":"gender","House":"house"}

    for val in options:
        if val == "unknown":
            attr = attr_dict[attribute]
            val = attr+"_"+val
        wordcloud = "/assets/Wordclouds/"+str(val)+".png"
        children.append(html.Img(id = 'word-cloud-image',
                                    src=wordcloud,
                                    style=dict(width="40%", 
                                        height="40%", margin = 20)
                                )
                         )
    if (not attribute):
        children = []


    return  [children]
   
