import dgidb
import network_graph as ng
from dash import dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

def generate_app():  
    genes = dgidb.get_gene_list()
    plot = ng.generate_plotly(None)

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    set_app_layout(app,plot,genes)
    update_plot_from_dropdown(app)

    if(__name__ == '__main__'):
        app.run_server(debug=True)

def set_app_layout(app,plot,genes):
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
    
def update_plot_from_dropdown(app):
    @app.callback(
        Output('network-graph', 'figure'),
        [Input('node-dropdown', 'value')]
    )
    def update(selected_genes):
        if(selected_genes is not None):
            gene_interactions = dgidb.get_interactions(selected_genes)
            updated_graph = ng.create_network(gene_interactions)
            updated_plot = ng.generate_plotly(updated_graph)
            return updated_plot
        return ng.generate_plotly(None)