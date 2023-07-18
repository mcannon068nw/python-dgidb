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
    app.layout = html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dcc.Graph(
                        figure=plot,
                        style={'width': '100%', 'height': '800px'}
                    ),
                    body=True,
                    style={'margin': '10px'}
                ),
                width=9
            ),
            dbc.Col(
                dbc.Card(
                    html.Div("<Placeholder>"),
                    body=True,
                    style={'margin': '10px'}
                ),
                width=3
            ),
        ])
    ])

    if __name__ == '__main__':
        app.run_server(debug=True)

def update_graph():
    print("A")
    