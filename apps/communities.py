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

fig = px.bar(df_barplot, x = "Size", y = "Communities", orientation = 'h', color = 'Colours', color_discrete_map="identity", template='simple_white')

fig.update_layout(title = dict(
                        text='<b>Sizes of communities - Louvian partition</b>',
                        x = 0.5,
                        font = dict(size=20)
                    ),
                  xaxis_title = 'Size', 
                  yaxis_title = 'Communities', 
                  width = 1400, height = 600)


cyto.load_extra_layouts()

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
            "communities might be? Will it be best to split the network into school houses? Blood status? Or something "
            "entirely different? This page will answer this, where we have examined partitions based on school houses, "
            "species, blood status and the Louvian partition. ", style = {'marginLeft': 60, 'marginRight': 60}
            ),
        html.H4("Properties of the different partitions", style = {'text-align': 'center'})
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

    html.Div([
        html.P("In the table the properties of the different partitions can be seen. Splitting the network into "
               "communities based on species is definitely not a good partition. But did you expect this? "
               "Out of these partitions the one which has the highest modularity score is the Louvian partition, "
               "with a modularity of almost 0.50. Are you interested in seeing the different sizes of the communties? "
               "Or how the network looks like when the nodes are coloured by community? "
        , style = {'marginLeft': 60, 'marginRight': 60, 'marginTop': 20}),
        ]
    ),

    # Barplot 
    html.Div([
        html.Div([
            dcc.Graph(id = 'plot_com_sizes', figure = fig),])
        ], style ={"display":"flex",'flex-wrap':'wrap', "justify-content":"center"}
    ),

    # indsæt graf farvet efter bedste partition
    # for the best partition of graph into communities
    # Network
    html.H3(children = ["The Wizarding Wolrd divided into communities"], style = {'text-align': 'center'}),
    
    html.Div([
        html.Div([
            html.H5(children = ["GCC network"], style = {'text-align': 'center'}),
            cyto.Cytoscape(
                id='cytoscape-com',
                layout={'name': 'preset'},
                        stylesheet = stylesheet_cyto,
                        elements = cyto_GCC['nodes'] + cyto_GCC['edges'] ,
                        style = {'width': '100%', 'height': '100%'}
                        )
                    ], style={'width': '45%', 'height': '100%'}),

            html.Div([
                html.Div([
                        html.H5(id = 'graph-title-com', children = ["Community 0"], style = {'text-align': 'center'}),
                        dcc.Slider(
                        id = 'network-slider',
                        min = 0,
                        max = len(communities)-1,
                        step = 1,
                        value = 0)
                    ], style = {'width': '100%'}),
                    html.Div([
                        html.Iframe(id = "com-graph", src="/assets/Communities/GCC_com_0.html", style={"width":"100%", "height":"500px"})
                        ], 
                    )
            ],  style={'width': '45%', 'height': '100%'})

        ], style ={"display": "flex", "justify-content": "center", "width": "95vw", "height" : "60vh", 'marginBottom': '100px'}),

    html.Div([
        html.P(children = [
            html.Span("Have you tried looking at the communities? Do they make sense? If you use the slider to go to "),
            html.Span("community 1 ", style= {"font-weight": "bold"}),
            html.Span("it can be seen that the largest nodes are "),
            html.Span("Newton Scamander, Gellert Grindewald, Nagini, Credence Barebone and Leta Lestrage. "
                    , style= {"font-style": "italic"} ),
            html.Span("With a little knowledge about the Wizarding World, you can identify these characters as belonging "\
                      "to the Fantastic Beasts universe, with ties to the Harry Potter universe. "),
            html.Span("You might discover other fascinating communities, if you explore the slider options. "),
            html.Span("Community 0 ", style= {"font-weight": "bold"}),
            html.Span("contains characters such as: "),
            html.Span("Hermione Granger, Severus Snape, Albus Dumbledore, Minerva McGonagall, "
                      "Draco Malfoy, Neville Longbottom ", style= {"font-style": "italic"}),
            html.Span("and other Hogwart's characters. "),
            html.Span("Community 7 ", style= {"font-weight": "bold"}),
            html.Span("consists of: "),
            html.Span("The Weasley family (Ron, Ginny, Fred, George, Percy, Molly, Arthur etc.), Alastor Moody, "
                      "Cornelious Fudge ", style= {"font-style": "italic"}),
            html.Span("and other ministry people amoungst others. "),
            html.Span("Harry Potter ", style= {"font-style": "italic"}),
            html.Span("is in "),
            html.Span("community 9. ", style= {"font-weight": "bold"}),
            ])
    ], style ={"display": "flex", "justify-content": "center", 'marginLeft': 60, 'marginRight': 60, 'marginTop': 20})
])

@app.callback([Output('com-graph', 'src')],
              [Output('graph-title-com', 'children')],
              [Input('network-slider', 'value')])
def update_graph(value):
    src = "/assets/Communities/GCC_com_{}.html".format(value)
    title = "Community {}".format(value)
    
    return src, title
