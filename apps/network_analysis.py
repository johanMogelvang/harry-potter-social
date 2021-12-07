import os
import json
import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import networkx as nx
import pandas as pd
import plotly.graph_objects as go



from app import app

# app = dash.Dash(__name__)
# server = app.server
cyto.load_extra_layouts()

cyto_default_style = [
            # Class selectors
            {
                'selector': 'node',
                'style': {
                'content': 'data(id)',
                'height': 25,
                'width' : 25,
                }
            },
            {
                'selector': 'edge',
                'style': {
                'width' : 1,
                }
            },
            {
                'selector': '.Hufflepuff',
                'style': {
                    'background-color': 'blue',
                    'line-color': 'blue'
                }
            },
            {
                'selector': '.Ravenclaw',
                'style': {
                    'background-color': 'orange',
                    'line-color': 'orange'
                }
            },
            {
                'selector': '.Gryffindor',
                'style': {
                    'background-color': 'red',
                    'line-color': 'red'
                }
            },
            {
                'selector': '.Slytherin',
                'style': {
                    'background-color': 'green',
                    'line-color': 'green'
                }
            },
            {
                'selector': '.unknown',
                'style': {
                    'background-color': 'purple',
                    'line-color': 'purple'
                }
            },
            # {
            # 'selector': ':selected',
            #     'css': {
            #         'background-color': 'SteelBlue',
            #         'line-color': 'black',
            #         'target-arrow-color': 'black',
            #         'source-arrow-color': 'black',
            #         'text-outline-width': 3,
            #         "z-index": "999",
            #         'text-outline-color': 'orange'
            #         }
            # },
        ]

path = os.getcwd().replace("\\", "/")
with open(path + "/family_links_cyto.json") as json_file:
    links = json.load(json_file)
#Get bi-directional edge data
with open(path + "/family_links.json") as json_file:
    family_links = json.load(json_file)

#Load into nx object
dic = {    'data': [],
    'directed': False,
    'multigraph': False,
    'elements': links}
G=nx.cytoscape_graph(dic)
#Sort components by size
components_sorted = sorted(nx.connected_components(G), key=len, reverse=True)
G2 = G.subgraph(set().union(*sorted(nx.connected_components(G), key=len, reverse=True)[:5]))
links = nx.cytoscape_data(G2)['elements']
for node in links['nodes']:
    node.update({'classes': node['data']['house']})

#print(links['nodes']['data'])
#Agg graphs
houses = ['unknown',
 'Hufflepuff',
 'Slytherin',
 'Gryffindor',
 'Ravenclaw',
 'Thunderbird',
 'Pukwudgie',
 'Horned',
 'Wampus']

layout = html.Div([            
                html.Div([
                    html.Div([
                        html.H1("Network analysis"),
                        ], style={'text-align': 'center', "justify-content": "center", 'width':'100vw'}
                    ),
                    html.Div([
                                html.H5("""On this page you can explore the familial relationships between the characters of the harry potter universe.
                                On this page you can explore the familial relationships between the characters of the harry potter universe.On this page you can explore the familial relationships between the
                                 characters of the harry potter universe.On this page you can explore the familial relationships between the characters of th
                                 e harry potter universe.On this page you can explore the familial relationships between th
                                 e characters of the harry potter universe.On this page you can explore
                                  the familial relationships between the characte
                                  rs of the harry potter universe."""),
                    ], style={'width':'30vw', 'text-align': 'center'}), 
                ], style = {"justify-content": "center", 'width':'100vw'}),
                html.Div([
                    html.Div([
                        dcc.Slider(
                        id='my-slider',
                        min=1,
                        max=len(components_sorted),
                        step=1,
                        tooltip={"placement": "bottom", "always_visible": True},
                        value=5,
                        ),
                    cyto.Cytoscape(
                        id='cytoscape-hp-family',
                        layout={'name': 'cose-bilkent',
                            'nodeDimensionsIncludeLabels': 'true',
                            #'idealEdgeLength': 3,
                            'edgeElasticity': '1',
                            'numIter': 10000,
                            #'idealEdgeLength': '1',
                            'nodeRepulsion': '9000',}, #circle, #close-bilkent
                        #stylesheet=default_stylesheet,
                        stylesheet=cyto_default_style,
                        elements=links['nodes']+links['edges'],
                        style={'width': '100%', 'height': '100%', }
                        )
                    ], style={'width': '40%', 'height': '100%'}),
                    html.Div([
                        dcc.Graph(id='live-update-bar-graph'),
                        html.H5('The family the of selected character:', id='selected-character-text'),
                        dcc.Graph(id='live-character-network-graph'),
                    ],  style={'width': '40%', 'height': '100%', 'text-align': 'center'})
            ], style ={"display": "flex", "justify-content": "center", "width": "95vw", "height" : "60vh"}),
            html.Div([
                    html.H1("Aggregated graphs"),
                    html.H5("Explore the relationships on a more global scale")
                ],
                style={'marginTop': '10vh'}),
            html.Div([
                    # cyto.Cytoscape(
                    #     id='cytoscape-agg-houses',
                    #     layout={'name': 'circle'}, #circle, #close-bilkent
                    #     #stylesheet=default_stylesheet,
                    #     stylesheet=cyto_default_style,
                    #     elements=links['nodes']+links['edges'],
                    #     style={'width': '100%', 'height': '100%'}
                    #     )
            ], style ={"display": "flex", "justify-content": "center", "width": "95vw", "height" : "60vh"}),
            html.A(children=0, id="style-refresher"),
            html.H1("refreshed:", id="refresh-id"),
])

@app.callback(Output('selected-character-text', 'children'),
              Input('cytoscape-hp-family', 'tapNodeData'),)
def displayTapNodeData(nodedata):
    if nodedata:
        return "The family of " + nodedata['id'] + ":"
    return "The family of the selected character:"

@app.callback(Output('live-character-network-graph', 'figure'),
              Input('cytoscape-hp-family', 'tapNode'),)
def displayTapNodeData2(nodedata):
    char_list = []
    chars = set()
    if nodedata:
        for node in links['nodes']:
            for edge in nodedata['edgesData']:
                if edge['target'] == node['data']['id']:
                    if edge['target'] not in chars:
                        char_list.append(node)
                        chars.add( edge['target'])
            for edge in nodedata['edgesData']:
                if edge['source'] == node['data']['id']:
                    if edge['source'] not in chars:
                        char_list.append(node)
                        chars.add( edge['target'])
        return get_graph(char_list)
    return go.Figure()

@app.callback(Output('cytoscape-hp-family', 'elements'),
              Output('live-update-bar-graph', 'figure'),
              Input('my-slider', 'value'),
              State('cytoscape-hp-family', 'elements'))
def update_elements(slider_value, elements):
    current_nodes, deleted_nodes = get_current_and_deleted_nodes(elements)
    difference = int(slider_value) - len(current_nodes)

    subgraph = G.subgraph(set().union(*sorted(nx.connected_components(G), key=len, reverse=True)[:slider_value]))
    cy_elements = nx.cytoscape_data(subgraph)['elements']
    for node in cy_elements['nodes']:
        node.update({'classes': node['data']['house']})
    return [cy_elements['nodes'] + cy_elements['edges'], get_graph(cy_elements['nodes'])]
    # If the slider value has increased
    if difference >= 1:
        for i in range(difference):
            # We pop one node from deleted nodes and append it to nodes list.
            current_nodes.append(deleted_nodes.pop())
            # Get valid edges -- both source and target nodes are in the current graph
            cy_edges = get_current_valid_edges(current_nodes, links['edges'])
        return [cy_edges + current_nodes, get_graph(current_nodes)]

    # If the remove button was clicked most recently and there are nodes to remove
    elif difference < 0:
        for i in range(-difference):
            current_nodes.pop()
            cy_edges = get_current_valid_edges(current_nodes, links['edges'])
        return [cy_edges + current_nodes, get_graph(current_nodes)]

    # Neither have been clicked yet (or fallback condition)
    return [elements, get_graph(elements['nodes'])]

def get_current_valid_edges(current_nodes, all_edges):
    """Returns edges that are present in Cytoscape:
    its source and target nodes are still present in the graph.
    """
    valid_edges = []
    node_ids = {n['data']['id'] for n in current_nodes}

    for e in all_edges:
        if e['data']['source'] in node_ids and e['data']['target'] in node_ids:
            valid_edges.append(e)
    return valid_edges

def get_current_and_deleted_nodes(elements):
    """Returns nodes that are present in Cytoscape and the deleted nodes
    """
    current_nodes = []
    deleted_nodes = []

    # get current graph nodes
    for ele in elements:
        # if the element is a node
        if 'source' not in ele['data']:
            current_nodes.append(ele)

    # get deleted nodes
    node_ids = {n['data']['id'] for n in current_nodes}
    
    for n in links['nodes']:
        if n['data']['id'] not in node_ids:
            deleted_nodes.append(n)

    return current_nodes, deleted_nodes

def get_graph(node_elements):
    bar_list = []
    #color_list = ['purple', 'green', 'blue', 'red', 'orange', 'black', 'black', 'black', 'black']
    for node in node_elements:
        bar_list.append(node['data']['house'])

    frequency = {}

    # iterating over the list
    for item in bar_list:
        # checking the element in dictionary
        if item in frequency:
            # incrementing the counr
            frequency[item] += 1
        else:
            # initializing the count
            frequency[item] = 1

    colors = ['Grey'] * len(frequency.keys())
    for i, color in enumerate(colors):
        house = list(frequency.keys())[i]
        if house == 'unknown':
            colors[i] = "#800080"
        elif house == 'Slytherin':
            colors[i] = "#1A472A"
        elif house == "Hufflepuff":
            colors[i] = "#FFDB00"
        elif house == "Ravenclaw":
            colors[i] = "#0E1A40"
        elif house == "Gryffindor":
            colors[i] = "#740001"    
    return px.bar(x=frequency.keys(),y=frequency, color=colors, color_discrete_map="identity")


@app.callback(Output('cytoscape-hp-family', 'stylesheet'),
              [Input('cytoscape-hp-family', 'tapNode'),
              Input('cytoscape-hp-family', 'selectedNodeData'),
              Input('style-refresher', 'children'),])
def change_stylesheet_of_graph(node, selectedNodeData, style_refresher):
    ctx = dash.callback_context

    #If no node is tapped, return the default styling
    if not selectedNodeData:
        refresh_style = cyto_default_style.copy()
        return  refresh_style

    #If a node is selected, traverse the graph for connected nodes, and then change their color.
    cyto_style = [{
        "selector": 'node',
        'style': {
            'opacity': 0.3,
        }
    }, {
        'selector': 'edge',
        'style': {
            'opacity': 0.2,
            "curve-style": "bezier",
        }
    }, {
        "selector": 'node[id = "{}"]'.format(node['data']['id']),
        "style": {
            'background-color': 'orange',
            "border-color": "black",
            "border-width": 2,
            "border-opacity": 1,
            "opacity": 1,
            "content": "data(id)",
            "font-size": 20,
            'z-index': 9999
        }
    }]
    
    following_color = "black"
    follower_color = "black"
    for edge in node['edgesData']:
        if edge['source'] == node['data']['id']:
            cyto_style.append({
                "selector": 'node[id = "{}"]'.format(edge['target']),
                "style": {
                    'background-color': following_color,
                    'content': 'data(id)',
                    'opacity': 0.9
                }
            })
            cyto_style.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "line-color": following_color,
                    'opacity': 0.6,
                    'z-index': 5000
                }
            })

        if edge['target'] == node['data']['id']:
            cyto_style.append({
                "selector": 'node[id = "{}"]'.format(edge['source']),
                "style": {
                    'background-color': follower_color,
                    'opacity': 0.9,
                    'z-index': 9900,
                    'content': 'data(id)',
                }
            })
            cyto_style.append({
                "selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {
                    "line-color": follower_color,
                    'opacity': 6,
                    'z-index': 5000
                }
            })
            #         'background-color': 'SteelBlue',
            #         'line-color': 'black',
            #         'target-arrow-color': 'black',
            #         'source-arrow-color': 'black',
            #         'text-outline-width': 3,
            #         "z-index": "999",
            #         'text-outline-color': 'orange'
            #         }
    return cyto_style

if __name__ == '__main__':
    app.run_server(debug=True)