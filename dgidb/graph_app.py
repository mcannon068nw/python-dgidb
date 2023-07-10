import dgidb
import network_graph as ng

from dash import dash, dcc, html

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
    
    app = dash.Dash(__name__)
    
    app.layout = html.Div(
        dcc.Graph(figure=plot)
    )

    if __name__ == '__main__':
        app.run_server(debug=True)