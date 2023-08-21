import networkx as nx
import plotly.graph_objects as go

def initalize_network(interactions):
    interactions_graph = nx.Graph()
    for int_gene, int_drug in zip(interactions['gene'], interactions['drug']):
        interactions_graph.add_node(int_gene,isGene=True)
        interactions_graph.add_node(int_drug,isGene=False)
        interactions_graph.add_edge(int_gene,int_drug)
    return interactions_graph

def add_node_attributes(interactions_graph):
    for node in interactions_graph.nodes:
        is_gene = interactions_graph.nodes[node]['isGene']
        if(is_gene):
            set_color = "cyan"
            set_size = 10
        else:
            degree = interactions_graph.degree[node]
            if(degree > 1):
                set_color = "orange"
                set_size = 7
            else: 
                set_color = "red"
                set_size = 7
        interactions_graph.nodes[node]['node_color'] = set_color
        interactions_graph.nodes[node]['node_size'] = set_size

def create_network(interactions):
    interactions_graph = initalize_network(interactions)
    add_node_attributes(interactions_graph)
    return interactions_graph

def generate_plotly(graph):
    layout = go.Layout(
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        showlegend=True
    )
    fig = go.Figure(layout=layout)
    
    if(graph is not None):
        pos = nx.spring_layout(graph, seed=7)

        trace_nodes = create_trace_nodes(graph,pos)
        trace_edges = create_trace_edges(graph,pos)

        fig.add_trace(trace_edges)
        for trace_group in trace_nodes:
            fig.add_trace(trace_group)

    return fig

def create_trace_nodes(graph,pos):
    nodes_by_group = {
        'cyan': {'node_x': [], 'node_y': [], 'node_text': [], 'node_color': [], 'node_size': [], 'legend_name': "genes"},
        'orange': {'node_x': [], 'node_y': [], 'node_text': [], 'node_color': [], 'node_size': [], 'legend_name': "multi-degree drugs"},
        'red': {'node_x': [], 'node_y': [], 'node_text': [], 'node_color': [], 'node_size': [], 'legend_name': "single-degree drugs"}
    }

    for node in graph.nodes():
        node_color = graph.nodes[node]['node_color']
        node_size = graph.nodes[node]['node_size']
        x, y = pos[node]
        nodes_by_group[node_color]['node_x'].append(x)
        nodes_by_group[node_color]['node_y'].append(y)
        nodes_by_group[node_color]['node_text'].append(str(node))
        nodes_by_group[node_color]['node_color'].append(node_color)
        nodes_by_group[node_color]['node_size'].append(node_size)

    trace_nodes = []
    for key,value in nodes_by_group.items():
        trace_group = go.Scatter(
            x=value['node_x'],
            y=value['node_y'],
            mode='markers',
            marker=dict(
                symbol='circle',
                size=value['node_size'],
                color=value['node_color']
            ),
            text=value['node_text'],
            hoverinfo='text',
            visible=True,
            showlegend=True,
            name=value['legend_name']
        )
        trace_nodes.append(trace_group)

    return trace_nodes

def create_trace_edges(graph,pos):
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    trace_edges = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode='lines',
        line=dict(width=0.5,color='gray'),
        hoverinfo='none',
        showlegend=False
    )

    return trace_edges