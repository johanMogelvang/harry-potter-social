from pandas.io.pytables import ClosedFileError
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import dash_cytoscape as cyto
import json
import pickle 

from app import app

df = pd.read_csv('assets/table_communities.csv')
h = 350
w = 500
df_barplot = pd.read_csv('assets/best_partition_barplot.csv')


fig = px.bar(df_barplot, x = "Count", y = "Communities", orientation = 'h', color = 'Colours')

fig.update_layout(title = "Sizes of communities in the best partition",
                   xaxis_title = 'Count', 
                   yaxis_title = 'Communities',width = 1000)

# for the best partition of grapg into communities
with open("cyto_GCC_com.json", 'rb') as f:
    cyto_GCC_com = json.load(f)

#stylesheet_cyto = ?

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Community Detection", className="text-center")
                    , className="mb-5 mt-5")
        ])
    ]), 
    html.Div([
        html.P("The Wizarding World is a large network of many different characters connected across different family houses, "
            "school houses etc. Have you thought about what the best way to split the network of the Wizarding World into "
            "communities? Will it be best to split the network into school houses? Blood status? Or something entirely "
            "different? This page will answer this, where we have examined partitions based on school houses, species, "
            "blood status and the Louvian partition. ", style = {'marginLeft': 60, 'marginRight': 60}
            ),
    ]),
    # Table (communities) 
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'scroll',
                        'whitespace':'normal',
                        'height': 'auto',
                        'lineHeight': '15px',
                        'padding': 10},#table-layout': 'fixed'
            style_header={'backgroundColor': '#25597f', 'color': 'white'},
            style_cell={
                'backgroundColor': 'whitesmoke',
                'color': 'black',
                'fontSize': 13,
                'font-family': "sans-serif",#'Nunito Sans',
                'textAlign': 'left'
                }, 
                style_as_list_view=True
        ),
    ],style={"justify-content":"center", 'width': '80vw','marginLeft':80}
    ),

    html.P("", style = {'marginLeft': 60, 'marginRight': 60}),

    # Graph 
    html.Div([
        html.Div([
            dcc.Graph(id = 'boxplot_partition', figure = fig),])
        ], style ={"display":"flex",'flex-wrap':'wrap', "justify-content":"center"}
    ),
    # indsæt graf farvet efter bedste partition
    html.Div([
            cyto.Cytoscape(
                id='cytoscape-graph',
                layout={'name': 'preset'},
                #stylesheet=default_stylesheet,
                style={'width': '45%', 'height': '600px'},
                stylesheet=stylesheet_cyto,
                elements=cyto_G['nodes'] + cyto_G['edges']  # Denne her skal i funktion  
            ),
                html.P(id='cytoscape-tapNodeData-output-explore'),
                html.P(id='cytoscape-tapEdgeData-output-explore'),
                html.P(id='cytoscape-mouseoverNodeData-output-explore'),
                html.P(id='cytoscape-mouseoverEdgeData-output-explore'),

        ], style ={"display":"flex",'flex-wrap':'wrap', "justify-content":"center"}
     ),
]),

