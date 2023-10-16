import dgidb
import network_graph as ng
from dash import dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import csv

def csv_to_list(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data_list.extend(row)
    return data_list

def generate_app():  
    genes = csv_to_list("dgidb-v5-genes.csv")
    plot = ng.generate_plotly(None)
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    set_app_layout(app,plot,genes)
    update_plot(app)
    update_selected_node(app)
    update_selected_node_display(app)
    update_neighbor_dropdown(app)
    #update_edge_info(app)

    if(__name__ == '__main__'):
        app.run_server(debug=True)

def set_app_layout(app,plot,genes):
    graph_display = dcc.Graph(
        id='network-graph',
        figure=plot,
        style={'width': '100%', 'height': '800px'}
    )
    
    genes_dropdown_display = dcc.Dropdown(
        id='gene-dropdown',
        options=[{'label': gene, 'value': gene} for gene in genes],
        multi=True
    )

    selected_node_display = dcc.Markdown(
        id='selected-node-text'
    )
    
    neighbors_dropdown_display = dcc.Dropdown(
        id='neighbor-dropdown',
        multi=False
    )

    edge_info_display = dcc.Markdown(
        id='edge-info-text'
    )
    
    app.layout = html.Div([
        # Variables
        dcc.Store(id='selected-node'),
        dcc.Store(id='graph'),

        # Layout
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    graph_display,
                    body=True,
                    style={'margin': '10px'}
                ),
                width=8
            ),
            dbc.Col([
                dbc.Card(
                    genes_dropdown_display,
                    body=True,
                    style={'margin': '10px'}
                ),
                dbc.Card(
                    selected_node_display,
                    body=True,
                    style={'margin': '10px'}
                ),
                dbc.Card(
                    neighbors_dropdown_display,
                    body=True,
                    style={'margin': '10px'}
                ),
                dbc.Card(
                    edge_info_display,
                    body=True,
                    style={'margin': '10px'}
                )],
                width=4
            )
        ])
    ])

def update_plot(app):
    @app.callback(
        [Output('graph', 'data'), Output('network-graph', 'figure')],
        Input('gene-dropdown', 'value')
    )
    def update(selected_genes):
        if(selected_genes is not None):
            gene_interactions = dgidb.get_interactions(selected_genes)
            updated_graph = ng.create_network(gene_interactions)
            updated_plot = ng.generate_plotly(updated_graph)
            return ng.generate_json(updated_graph), updated_plot
        return None, ng.generate_plotly(None)
    
def update_selected_node(app):
    @app.callback(
        Output('selected-node', 'data'),
        Input('network-graph', 'clickData')
    )
    def update(clickData):
        if clickData is not None and 'points' in clickData:
            selected_node = clickData['points'][0]
            return selected_node
        return dash.no_update

def update_selected_node_display(app):
    @app.callback(
        Output('selected-node-text', 'children'),
        Input('selected-node', 'data')
    )
    def update(selected_node):
        return selected_node['text']
        print(selected_node)

def update_neighbor_dropdown(app):
    @app.callback(
        Output('neighbor-dropdown', 'options'),
        Input('selected-node', 'data')
    )
    def update(selected_node):
        if(selected_node['curveNumber'] != 1):
            return selected_node['customdata']
        return dash.no_update

def update_edge_info(app):
    @app.callback(
        Output('edge-info-text', 'children'),
        [Input('selected-node', 'data'), Input('neighbor-dropdown', 'value')],
        State('graph', 'data')
    )
    def update(selected_node,selected_neighbor,graph):
        if(selected_node is not None and selected_node['curveNumber'] == 1):
            selected_data = selected_node['customdata']
            return "ID: " + str(selected_node['text']) + "\n\nApproval: " + str(selected_data[0]) + "\n\nScore: " + str(selected_data[1]) + "\n\nAttributes: " + str(selected_data[2]) + "\n\nSource: " + str(selected_data[3]) + "\n\nPmid: " + str(selected_data[4])
        if(selected_node is not None and selected_neighbor is not None):
            edge_node_id = None
            selected_node_is_gene = get_node_data_from_id(graph['nodes'], selected_node['text'])['isGene']
            selected_neighbor_is_gene = get_node_data_from_id(graph['nodes'], selected_neighbor)['isGene']
            if((selected_node_is_gene is True) and (selected_neighbor_is_gene is False)):
                edge_node_id = selected_node['text'] + " - " + selected_neighbor
            elif((selected_node_is_gene is False) and (selected_neighbor_is_gene is True)):
                edge_node_id = selected_neighbor + " - " + selected_node['text']
            else:
                return dash.no_update
            selected_data = get_node_data_from_id(graph['links'], edge_node_id)
            return "ID: " + str(selected_data['id']) + "\n\nApproval: " + str(selected_data['approval']) + "\n\nScore: " + str(selected_data['score']) + "\n\nAttributes: " + str(selected_data['attributes']) + "\n\nSource: " + str(selected_data['source']) + "\n\nPmid: " + str(selected_data['pmid'])
        return dash.no_update
    
def get_node_data_from_id(nodes, node_id):
    for node in nodes:
        if node['id'] == node_id:
            return node
    return None