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
import networkx as nx

from app import app

df = pd.read_csv('assets/Communities/table_communities.csv')

df_barplot = pd.read_csv('assets/Communities/best_partition_barplot.csv')

with open("assets/Communities/GCC_com.pickle", 'rb') as f:
    GCC = pickle.load(f)

with open("assets/Communities/cyto_GCC_com.json", 'rb') as f:
    cyto_GCC = json.load(f)

h = 350
w = 500

fig = px.bar(df_barplot, x = "Size", y = "Communities", orientation = 'h', color = 'Colours', color_discrete_map="identity")

fig.update_layout(title = "Sizes of communities in the best partition",
                   xaxis_title = 'Size', 
                   yaxis_title = 'Communities', width = 1400, height = 600)


cyto.load_extra_layouts()
#stylesheet_cyto = ?
default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)',
            'width': "30%",
            'height': "50%"
        }
    }
]

communities = list(set(nx.get_node_attributes(GCC, 'community').values()))
max_degree = max([cyto_GCC['nodes'][i]['size'] for i in range(0,len(cyto_GCC['nodes']))])

stylesheet_cyto = [
            # Class selectors
            *[{
                'selector': str(i),
                'style': {
                    'background-color': 'data(community_colour)',
                    'line-color': 'data(community_colour)'
                }
            } for i in communities],
           
            {
                'selector': 'node',
                'style': {
                    'width': 'mapData(size, 0,'+str(max_degree)+', 1000, 15000)',
                    'height': 'mapData(size, 0,' +str(max_degree)+', 1000, 15000)', 
                    'content': 'data(label)',
                    'font-size': "12px",
                    "text-valign":"center", 
                    "text-halign":"center", 
                    'line-color': 'purple'
                }
            },
            {
                'selector': 'edges',
                'style': {'opacity': 0.2}}
        ]


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
            dcc.Graph(id = 'plot_com_sizes', figure = fig),])
        ], style ={"display":"flex",'flex-wrap':'wrap', "justify-content":"center"}
    ),

    # indsæt graf farvet efter bedste partition
    # for the best partition of graph into communities
    # Network
    html.Div([
        cyto.Cytoscape(
            id='cytoscape-graph',
            layout={'name': 'preset'},
            #stylesheet=default_stylesheet,
            style={'width': '45%', 'height': '600px'},
            stylesheet=stylesheet_cyto,
            elements=cyto_GCC['nodes'] + cyto_GCC['edges']  
        ),
            html.P(id='cytoscape-tapNodeData-output-explore'),
            html.P(id='cytoscape-tapEdgeData-output-explore'),
            html.P(id='cytoscape-mouseoverNodeData-output-explore'),
            html.P(id='cytoscape-mouseoverEdgeData-output-explore'),

    ], style ={"display":"flex",'flex-wrap':'wrap', "justify-content":"center"}
    ),
]),

