import dgidb
import network_graph as ng

from dash import dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

def create_interactions_network():
    genes = ['BRAF','ABL1','BCR','PDGFRA']
    drugs = ['IMATINIB','OLARATUMAB','DASATINIB','NELOTINIB']
    
    gene_interactions = dgidb.get_interactions(genes)
    drug_interactions = dgidb.get_interactions(drugs,search='drugs')

    return ng.create_network(gene_interactions)

def save_graph():
    ng.save_graph()

def generate_app():  
    graph = create_interactions_network()
    plot = ng.generate_plotly(graph)

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    define_layout(app,graph,plot)
    select_from_graph(app)
    #filter_from_dropdown(app,graph)

    if(__name__ == '__main__'):
        app.run_server(debug=True)

def define_layout(app,graph,plot):
    graph_display = dcc.Graph(
        id='network-graph',
        figure=plot,
        style={'width': '100%', 'height': '800px'}
    )
    
    dropdown_display = dcc.Dropdown(
        id='node-dropdown',
        options=[{'label': node, 'value': node} for node in graph.nodes],
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
                width=9
            ),
            dbc.Col(
                dbc.Card(
                    dropdown_display,
                    body=True,
                    style={'margin': '10px'}
                ),
                width=3
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