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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
server = app.server
cyto.load_extra_layouts()

path = os.getcwd().replace("\\", "/")
with open(path + "/family_links_cyto.json") as json_file:
    links = json.load(json_file)


app.layout = html.Div([
    dcc.Slider(
        id='my-slider',
        min=1,
        max=len(links['nodes']),
        step=1,
        tooltip={"placement": "bottom", "always_visible": True},
        value=100,
    ),
    cyto.Cytoscape(
        id='cytoscape-hp-family',
        layout={'name': 'circle'}, #circle, #cose-bilkent
        #stylesheet=default_stylesheet,
        style={'width': '100%', 'height': '500px'},
        stylesheet=[
            # Class selectors
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
            }
        ],
        elements=links['nodes']+links['edges']
    ),
    dcc.Graph(id='live-update-bar-graph'),
    html.P(id='cytoscape-tapNodeData-output'),
    html.P(id='cytoscape-tapEdgeData-output'),
    html.P(id='cytoscape-mouseoverNodeData-output'),
    html.P(id='cytoscape-mouseoverEdgeData-output')
])

@app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
              Input('cytoscape-hp-family', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        return "You recently clicked/tapped on the individual: " + data['name']

@app.callback(Output('cytoscape-tapEdgeData-output', 'children'),
              Input('cytoscape-hp-family', 'tapEdgeData'))
def displayTapEdgeData(data):
    if data:
        return "You recently clicked/tapped the edge between " + \
               data['source'].upper() + " and " + data['target'].upper()

@app.callback(Output('cytoscape-hp-family', 'elements'),
              Output('live-update-bar-graph', 'figure'),
              Input('my-slider', 'value'),
              State('cytoscape-hp-family', 'elements'))
def update_elements(slider_value, elements):
    current_nodes, deleted_nodes = get_current_and_deleted_nodes(elements)
    difference = int(slider_value) - len(current_nodes)
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
    return px.bar(bar_list)


if __name__ == '__main__':
    app.run_server(debug=True)