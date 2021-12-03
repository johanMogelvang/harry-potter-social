from pandas.io.pytables import ClosedFileError
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

from app import app

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead

graph_style = {"maxHeight": "auto", "align":"center", "margin": "auto"}

df = pd.read_csv('HP_enriched_character_df.csv')

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Exploring the Dataset", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.P(children='This page is about understanding the data set collected from the HP Wiki Fandom and gaining valuable insights about the characters. '
                                    'All the characters that inhabit the wizarding world have been collected from the wiki-pages, together with some intersting features, '
                                    'such as their blood-status, school-house, species and gender.'
                                    '\n To get an overview of the dataset, the distribution of the features are shown below. '
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
                'backgroundColor': 'white',
                'color': 'black',
                'fontSize': 13,
                'font-family': 'Nunito Sans',
                'textAlign': 'left'
                }
        ),
    ],style={"justify-content":"center", 'width': '80vw','marginLeft':80}
    ),

    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("Feature distributions", className="text-center")
                    , className="mb-5 mt-5"
                )  
        ]),
        dbc.Row([
            dbc.Col(html.P("There are many values for some of the features, you can choose how many to display for each feature.")
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
        value='All values',
        #multi=True,
        style={'width': '50%', 'margin': 50}
        ),

        # Graph 
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
            dbc.Col(html.H5("Exploring the Network", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.P(children='The network has been created by using the characters as nodes. A characters is connected to another in the graph, if their wiki page links to each other character\'s page'
                                    ' Hereby, intersting insights about the relationships and the most central characters can be easily identified.'
                                        )
                    , className="mb-4")
        ]),
    ])
], style ={"justify-content":"center", 'width': '100vw', 'height':'100vh'}
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
    #stat_cols = [c.capitalize() for c in stat_cols] 

    df1 = df.rename(columns={'name':'Name','species': 'Species','gender':'Gender','house':'House','blood':'Blood-status'})
    all_cols = list(df1.columns)
    #all_cols = [c.capitalize() for c in all_cols] 

    if value == 'Statistics':
        columns = [{"name": i, "id": i} for i in stat_cols]
        data=df_stat.to_dict('records')
    else:
        columns = [{"name": i, "id": i} for i in all_cols]
        ixs = [df1.loc[df.name==name].index[0] for name in ['Harry Potter', 'Dobby','Vernon Dursley', "Newton Scamander"]]
        data=df1.loc[ixs] .to_dict('records')
    return data, columns

# page callbacks
# display pie charts and line charts to show number of cases or deaths
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
