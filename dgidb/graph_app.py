import dgidb
import network_graph as ng
from dash import dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import csv

def csv_to_list(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data_list.extend(row)
    return data_list

def save_graph():
    ng.save_graph()

def generate_app():  
    # ['BRAF','ABL1','BCR','PDGFRA']
    genes = csv_to_list("dgidb-v5-genes.csv")

    plot = ng.generate_plotly(None)
    
    plot.update_layout(
        showlegend=True
    )

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    define_layout(app,plot,genes)
    select_from_dropdown(app)
    #select_from_graph(app)

    if(__name__ == '__main__'):
        app.run_server(debug=True)

def define_layout(app,plot,genes):
    graph_display = dcc.Graph(
        id='network-graph',
        figure=plot,
        style={'width': '100%', 'height': '800px'}
    )
    
    dropdown_display = dcc.Dropdown(
        id='node-dropdown',
        options=[{'label': gene, 'value': gene} for gene in genes],
        multi=True
    )

    app.layout = html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    graph_display,
                    body=True,
                    style={'margin': '10px'}
                ),
                width=8
            ),
            dbc.Col(
                dbc.Card(
                    dropdown_display,
                    body=True,
                    style={'margin': '10px'}
                ),
                width=4
            )
        ])
    ])

def select_from_graph(app):
    @app.callback(
        Output('node-dropdown', 'value'),
        [Input('network-graph', 'clickData')]
    )
    def update(clickData):
        if clickData and 'points' in clickData:
            selected_node = clickData['points'][0]
            selected_node_name = selected_node.get('text', '')
            return selected_node_name
        return dash.no_update
    
def select_from_dropdown(app):
    @app.callback(
        Output('network-graph', 'figure'),
        [Input('node-dropdown', 'value')]
    )
    def update(value):
        if(value is not None):
            gene_interactions = dgidb.get_interactions(value)
            new_graph = ng.create_network(gene_interactions)
            plot = ng.generate_plotly(new_graph)
            return plot
        return ng.generate_plotly(None)