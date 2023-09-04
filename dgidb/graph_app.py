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
    update_plot_from_dropdown(app)
    update_edge_text(app)

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

    edge_text = dcc.Markdown(
        id='edge-info'
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
            dbc.Col([
                dbc.Card(
                    dropdown_display,
                    body=True,
                    style={'margin': '10px'}
                ),
                dbc.Card(
                    edge_text,
                    body=True,
                    style={'margin': '10px'}
                )],
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
    
def update_edge_text(app):
    @app.callback(
        Output('edge-info', 'children'),
        [Input('network-graph', 'clickData')]
    )
    def update(clickData):
        if clickData and 'points' in clickData:
            selected_element = clickData['points'][0]
            selected_curve_number = selected_element.get('curveNumber')
            if(selected_curve_number == 1):
                selected_data = selected_element.get('customdata')
                return "Approval: " + str(selected_data[0]) + "\n\nScore: " + str(selected_data[1]) + "\n\nAttributes: " + str(selected_data[2]) + "\n\nSource: " + str(selected_data[3]) + "\n\nPmid: " + str(selected_data[4])
        return dash.no_update