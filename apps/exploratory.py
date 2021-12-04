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

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
#cyto.load_extra_layouts()

graph_style = {"maxHeight": "auto", "align":"center", "margin": "auto"}

# Read data
df = pd.read_csv('HP_enriched_character_df.csv')

with open("G.pickle", 'rb') as f:
    G = pickle.load(f)

with open("GCC.pickle", 'rb') as f:
    GCC = pickle.load(f)

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Exploring the Dataset", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.P(children='This page is about understanding the data set collected from the HP Wiki Fandom and gaining valuable insights about the characters. '
                                    'All the characters that inhabit the wizarding world have been collected from the wiki-pages, together with some intersting features, '
                                    'such as their blood-status, school-house, species and gender. '
                                    'A selected part of the dataset can be seen below with some key statistics.'
                                     )
                    , className="mb-4")
        ]),
    ]),

    # Table with statistics 
    html.Div([
         dcc.RadioItems(
            id='table_type',
            options=[{'label': i, 'value': i} for i in ['Statistics', 'Table-data']],
            value='Statistics',
            labelStyle={'display': 'inline-block', 'marginLeft':10}
        ),
        dash_table.DataTable(
            id='datatable',
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

    dbc.Container([
        dbc.Row([
            html.H3("Distribution of features", className="text-center", style = {"marginTop":50, "marginBottom":10}
         )# , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.P("To get an overview of the dataset, the distribution of the features are shown below. There are many values for some of the features, you can choose how many to display for each feature.")
                )  
        ])
    ]),
    # choose between ALL options or top 5
    dcc.Dropdown(
        id='all_or_top_5',
        options=[
            {'label': 'All values', 'value': 'all_values'},
            {'label': 'Top 5 values', 'value': 'top_5'},
        ],
        value='top_5',
        #multi=True,
        style={'width': '50%', 'marginTop': 40,'marginBottom': 20,'marginLeft': 50}
        ),

        # Bar charts 
     html.Div([
            html.Div([(dcc.Graph(id = "bar_distribution_houses"))], style = {'width':'45%'}),
            html.Div([(dcc.Graph(id = "bar_distribution_species"))], style = {'width':'45%'}),
            html.Div([(dcc.Graph(id = "bar_distribution_blood"))], style = {'width':'45%'}),
            html.Div([(dcc.Graph(id = "bar_distribution_gender"))], style = {'width':'45%'})
        ], style ={"display":"flex",'flex-wrap':'wrap', "justify-content":"center"}
    ),
    #dbc.Row([
    #    dbc.Col(dcc.Graph(id = "distribution_gender"), width = 4),
    #    dbc.Col(dcc.Graph(id = "distribution_houses"), width = 4)
    #]),  
    dbc.Container([
        dbc.Row([
            html.H3("Exploring the Network", className="text-center")
        ]),
        dbc.Row([
            html.P(children='The network has been created using the characters as nodes and the links between the character pages as edges. '
                                    'By examining the Wizarding World as a network, the most central characters and most important relationships can easily be identified. '
                                    'The nodes have been colored according to which house they belong to and the node size is an indication of the number of connctions (this has been scaled as there is a very large difference between the number of connections). '
                                     'Choose whether you want to see the full network or only the Giant Connected Component (GCC) below. Zoom in on the nodes to see name and features for the nodes.'
                )
        ]),
        dbc.Row([
            html.P(children='Node that the graph takes a while to load due to its size. There is also some shaking because the solver used to determine the node position struggles to find a non-overlapping, stable layout. '
                )
        ])
    ]),
    dcc.RadioItems(
            id='graph_type',
            options=[{'label': i, 'value': i} for i in ['Full network', 'GCC']],
            value='Full network',
            labelStyle={'display': 'inline-block', 'marginLeft':120}
    ),
     html.Div(children = [
         # LEFT HAND SIDE
         html.Div([
             html.H5(id = 'graph-title',
                children = ["Network with "+ str(G.number_of_nodes())+ " nodes and "+ str(G.number_of_edges())+" edges"],
                className="text-center"
                ),
            html.P(id = 'graph-subtitle', 
                children=["Isolated nodes: "+str(len(list(nx.isolates(G))))],
                className="text-center"
                ), 
            html.Iframe(
                id = 'pyvis-graph',
                src="assets/GCC.html", 
                style={"width":"100%", 
                        "height":"600px"}
                        )
         ], style = {"width":"59%", "marginLeft":10}
         ),
        # RIGHT HAND SIDE  
        html.Div([
            # Degree distribution title
            html.H5(
                children = ["Degree distribution"],
                className="text-center"
                ),
            # Degree distribution plot
            dcc.Graph(id = "scatter_distribution") 
        ], style = {"width":"39%"}
        )
     ],style ={"display":"flex",'flex-wrap':'wrap', "justify-content":"center","marginTop":20, "marginBottom":10}
    ),

    dbc.Container([
        dbc.Row([
            html.P(children=[
                    html.Span('In the table below you can see the most connected characters in the network. '
                          "Do you think they are suprising? No, not really, but who is this Jacob's sibling? "
                          "This character is part of the videogame "),
                     html.Em("Harry Potter: Hogwarts Mystery, "),
                     html.Span("where the player can can take on the role of Jacob's sibling, a Hogwarts student before the time of Harry Potter.")
                   ]
            )
        ])
    ]),
    # Table with most connected 
    html.Div([
        html.Label("Top 5 characters by in- and out-degree", style = {'font-weight': 'bold', "justify-content":"center",'marginLeft':10}),
        dash_table.DataTable(
            id='degree-tabel',
            style_table={'overflowX': 'scroll',
                        'whitespace':'normal',
                        'height': 'auto',
                        'lineHeight': '15px',
                        'padding': 10},#table-layout': 'fixed'
            style_header={'backgroundColor': 'lightsteelblue', 'color': 'white'},
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
    dbc.Container([
        dbc.Row([
            html.P("Overall, we can see that the Wizarding World resembles a real-world network "
                    "with a few highly connected hubs such as Harry Potter and Voldemort, the main antagonist and protagonist of the Harry Potter world, "
                    "and many characters that only have very few connections. "
                    "If you want to learn more about the characteristics of the network, see the explainer notebook. Otherwise the next page in our website is about exploring the different ties and connections in our network even further."
            
            , className="text-center"
            , style = {"marginTop":20,'marginLeft':200, 'width':"65vw", "justify-content":"center"})
        ]
        )
    ]),
], style ={"justify-content":"center", 'width': '100vw', 'height':'90vh'}
)

@app.callback([Output('datatable', 'data'),
              Output('datatable', 'columns')],
             [Input('table_type', 'value')])

def update_columns(value):
    df_stat = df.describe().reset_index().rename(columns={'index': ''})
    df_stat.replace({"count":"Count",
                    "unique":"Unique values",
                    "top":"Top",
                    "freq":"Frequency"}, inplace = True)
    df_stat.rename(columns={'name':'Name','species': 'Species','gender':'Gender','house':'House','blood':'Blood-status'}, inplace =True)
    stat_cols = list(df_stat.columns)

    df1 = df.rename(columns={'name':'Name','species': 'Species','gender':'Gender','house':'House','blood':'Blood-status'})
    all_cols = list(df1.columns)

    if value == 'Statistics':
        columns = [{"name": i, "id": i} for i in stat_cols]
        data=df_stat.to_dict('records')
    else:
        columns = [{"name": i, "id": i} for i in all_cols]
        ixs = [df1.loc[df.name==name].index[0] for name in ['Harry Potter', 'Dobby','Vernon Dursley', "Newton Scamander"]]
        data=df1.loc[ixs] .to_dict('records')
    return data, columns

@app.callback([Output('bar_distribution_houses', 'figure'),
               Output('bar_distribution_species', 'figure'),
               Output('bar_distribution_blood', 'figure'),
               Output('bar_distribution_gender', 'figure')],
              [Input('all_or_top_5', 'value')])

def update_graph(choice):

    houses_freq = df.house.value_counts()#normalize = True)
    species_freq = df.species.value_counts()#normalize = True)
    blood_freq = df.blood.value_counts()#normalize = True)
    gender_freq = df.gender.value_counts()#normalize = True)

    # Get either all values or just top 10 
    if choice == "top_5":
        if len(houses_freq)>5:
            houses_freq = houses_freq[0:5]
        if len(species_freq)>5:
            species_freq = species_freq[0:5]
        if len(blood_freq)>5:
            blood_freq = blood_freq[0:5]

    df_houses_freq = houses_freq.rename_axis('House').reset_index(name='Count')
    df_species_freq = species_freq.rename_axis('Species').reset_index(name='Count')
    df_blood_freq = blood_freq.rename_axis('Blood status').reset_index(name='Count')
    df_gender_freq = gender_freq.rename_axis('Gender').reset_index(name='Count')

    # Get colors for house
    color_houses = []
    for house in houses_freq.index:
        if house == "Gryffindor":
            color_houses.append('#740001')
        elif house == "Slytherin":
            color_houses.append('#1A472A')
        elif house == "Hufflepuff":
            color_houses.append('#FFDB00')
        elif house == "Ravenclaw":
            color_houses.append('#222F5B')
        elif house == "unknown":
            color_houses.append('#5D5D5D')
        else: color_houses.append('lightgrey')

    h = 350
    w = 500

    fig = go.Figure(
        px.bar(df_houses_freq, x="House", y = "Count", 
                                height=h,
                                width=w,
                                color_discrete_map="identity", 
                                color = color_houses, 
                                title = "School house")
        )
    margin_val = 30
    fig.update_layout(showlegend=False,
                      margin=dict(l=margin_val, r=margin_val, t=margin_val, b=margin_val))

    fig2 = go.Figure(
        px.bar(df_species_freq, x="Species", y = "Count",
                    height=h,
                    width=w,
                    title = "Species")
        )
    fig2.update_layout(showlegend=False,
                      margin=dict(l=margin_val, r=margin_val, t=margin_val, b=margin_val))

    fig3 = go.Figure(
        px.bar(df_blood_freq, x="Blood status", y = "Count",
                    height = h, 
                    width = w,
                    title = "Blood status")
        )
    fig3.update_layout(showlegend=False,
                      margin=dict(l=margin_val, r=margin_val, t=margin_val, b=margin_val))

    fig4 = go.Figure(
        px.bar(df_gender_freq, x="Gender", y = "Count",
                    height=h,
                    width=w,
                    title = "Gender")
        )
    fig4.update_layout(showlegend=False,
                      margin=dict(l=margin_val, r=margin_val, t=margin_val, b=margin_val))
    return fig, fig2, fig3, fig4

@app.callback([Output('scatter_distribution', 'figure')],
              #[Output('cytoscape-graph', 'elements')],
              [Output('pyvis-graph', 'src')],
              [Output('graph-title', 'children')],
              [Output('graph-subtitle', 'children')],
              [Input('graph_type', 'value')])

def update_network(value):

    # Decide if using full network or GCC
    if value == 'Full network': 
        graph = G
        src = 'assets/G.html'
    else: 
        graph = GCC
        src = 'assets/GCC.html'

    # Get degree values from graph 
    in_degree_vals = list(nx.get_node_attributes(graph,'in_degree').values())
    out_degree_vals = list(nx.get_node_attributes(graph,'out_degree').values())

    # Get hist values
    hist_in, bins_in = np.histogram(in_degree_vals, bins = np.arange(np.min(in_degree_vals), np.max(in_degree_vals) + 2))
    centered_in = (bins_in[:-1] + bins_in[1:]) / 2
    hist_out, bins_out = np.histogram(out_degree_vals, bins = np.arange(np.min(out_degree_vals), np.max(out_degree_vals) + 2))
    centered_out = (bins_out[:-1] + bins_out[1:]) / 2

    # Adjust size of nodes (set it to zero if the hist-value is 0 i.e. there is no observation here)
    marker_size_in = [8 if val>0 else 0 for val in hist_in]
    marker_size_out = [8 if val>0 else 0 for val in hist_out]

    df_in_degree = pd.DataFrame({"In-degree": hist_in, "Count": centered_in})
    df_out_degree = pd.DataFrame({"Out-degree": hist_out, "Count": centered_out})

    # Make figure
    fig = make_subplots(rows=2, cols=1)

    marker_layout_in = dict(size=marker_size_in,color = "blue", line_width=1,opacity = 0.5)
    marker_layout_out = dict(size=marker_size_out,color = "red", line_width=1,opacity = 0.5)

    # Add traces
    fig.add_trace(go.Scatter(x=df_in_degree["Count"], y=df_in_degree["In-degree"],
                        mode='markers',
                        marker=marker_layout_in,
                        hoverinfo='none',
                        name='In-degree', 
                        legendgroup = '1'),
                row=1, col=1
                )
    fig.add_trace(go.Scatter(x=df_out_degree["Count"], y=df_out_degree["Out-degree"],
                        mode='markers',
                        marker=marker_layout_out,
                        hoverinfo='none',
                        name='Out-degree', 
                        legendgroup = '1'),
                row=1, col=1
                )
    fig.add_trace(go.Scatter(x=df_in_degree["Count"], y=df_in_degree["In-degree"],
                    mode='markers',
                        marker=marker_layout_in,
                        hoverinfo='none',
                        name='In-degree', 
                        legendgroup = '2'),
                row=2, col=1
                )
    fig.add_trace(go.Scatter(x=df_out_degree["Count"], y=df_out_degree["Out-degree"],
                        mode='markers',
                        marker=marker_layout_out,
                        hoverinfo='none',
                        name='Out-degree',
                        legendgroup = '2'),
                row=2, col=1
                )

    # Update xaxis properties
    fig.update_xaxes(title_text="Degree", row=1, col=1)
    fig.update_xaxes(title_text="log(Degree)", row=2, col=1, type="log")

    # Update yaxis properties
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="log(Count)", row=2, col=1, type="log")

    # Update title and height
    fig.update_layout(height=700)

    fig.update_layout(
        legend=dict(
            itemsizing= "constant",
            font=dict(
                #family="Courier",
                size=18,
                color   ="black"
            ),
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99, 
            bgcolor = 'rgba(0,0,0,0)'
        ),
        legend_tracegroupgap = 250
        #title=dict(
        #    font=dict(
        #        #family="Courier",
        #        size=20,
        #        color="black"
        #    )   
        #) 
    )

    title = "Network with "+ str(graph.number_of_nodes())+ " nodes and "+ str(graph.number_of_edges())+" edges"
    subtitle = "Isolated nodes: "+str(len(list(nx.isolates(graph))))

    return [go.Figure(fig),src, title, subtitle] #{'data': fig.data, 'layout': fig.layout}

@app.callback([Output('degree-tabel', 'data'),
              Output('degree-tabel', 'columns')],
             [Input('graph_type', 'value')])

def update_degree_table(value):
     # Decide if using full network or GCC
    if value == 'Full network': 
        graph = G
    else: 
        graph = GCC

    # Get degree values from graph 
    in_degree_vals = nx.get_node_attributes(graph,'in_degree')
    out_degree_vals = nx.get_node_attributes(graph,'out_degree')

    sorted_in_degree_dict = {k: v for k, v in sorted(in_degree_vals.items(), key=lambda item: item[1], reverse = True)}
    sorted_out_degree_dict = {k: v for k, v in sorted(out_degree_vals.items(), key=lambda item: item[1], reverse = True)}

    top5_in = list(sorted_in_degree_dict.items())[:5]
    top5_out = list(sorted_out_degree_dict.items())[:5]
    top5_in = [str(tup[0])+": "+str(tup[1]) for tup in top5_in]
    top5_out = [str(tup[0])+": "+str(tup[1]) for tup in top5_out]

    df_degree = pd.DataFrame({"In-degree":top5_in,"Out-degree":top5_out}, index = range(1,6))

    columns = [{"name": i, "id": i} for i in df_degree.columns]
    data = df_degree.to_dict('records')

    return data, columns
