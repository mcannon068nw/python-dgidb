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

def generate_app():  
    genes = csv_to_list("dgidb-v5-genes.csv")
    plot = ng.generate_plotly(None)

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    set_app_layout(app,plot,genes)
    update_plot(app)
    #update_selected_node(app)
    #update_edge_info(app)
    #update_neighbor_dropdown(app)

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

    neighbors_dropdown_display = dcc.Dropdown(
        id='neighbor-dropdown',
        multi=False
    )

    edge_info = dcc.Markdown(
        id='edge-info'
    )
    
    app.layout = html.Div([
        # Variables
        dcc.Store(id='graph'),
        dcc.Store(id='selected-node'),
        
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
                    neighbors_dropdown_display,
                    body=True,
                    style={'margin': '10px'}
                ),
                dbc.Card(
                    edge_info,
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
        global graph
        if(selected_genes is not None):
            gene_interactions = dgidb.get_interactions(selected_genes)
            updated_graph = ng.create_network(gene_interactions)
            updated_plot = ng.generate_plotly(updated_graph)
            return updated_graph,updated_plot
        return None,ng.generate_plotly(None)
    
def update_selected_node(app):
    @app.callback(
        Output('selected-node', 'data'),
        Input('network-graph', 'clickData')
    )
    def update(clickData):
        if clickData is not None and 'points' in clickData:
            selected_element = clickData['points'][0]
            print(selected_element)
            return selected_element
        return dash.no_update

def update_edge_info(app):
    @app.callback(
        Output('edge-info', 'children'),
        [Input('network-graph', 'clickData'), Input('neighbor-dropdown', 'value')]
    )
    def update(clickData,selected_genes,selected_neighbors):
        if clickData is not None and 'points' in clickData:
            selected_element = clickData['points'][0]
            print(selected_element)
            if(selected_element['curveNumber'] == 1):
                selected_data = selected_element['customdata']
                return "Approval: " + str(selected_data[0]) + "\n\nScore: " + str(selected_data[1]) + "\n\nAttributes: " + str(selected_data[2]) + "\n\nSource: " + str(selected_data[3]) + "\n\nPmid: " + str(selected_data[4])
        if(selected_neighbors is not None):
            #print(selected_neighbors)
            #selected_data = graph.nodes[selected_neighbors]['customdata']
            return dash.no_update
        return dash.no_update

def update_neighbor_dropdown(app):
    @app.callback(
        Output('neighbor-dropdown', 'options'),
        Input('network-graph', 'clickData')
    )
    def update(clickData):
        if clickData is not None and 'points' in clickData:
            selected_element = clickData['points'][0]
            if(selected_element['curveNumber'] != 1):
                return ng.get_neighbors(graph,selected_element['text'])
        return dash.no_update