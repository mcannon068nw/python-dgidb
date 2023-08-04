import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull as ch
import plotly.graph_objects as go
import matplotlib.colors as mcolors

def initalize_network(interactions):
    interactions_graph = nx.Graph()
    for int_gene, int_drug, int_score in zip(interactions['gene'], interactions['drug'], interactions['score']):
        interactions_graph.add_node(int_gene,connections=0,isGene=True)
        interactions_graph.add_node(int_drug,connections=0,isGene=False)
        interactions_graph.add_edge(int_gene,int_drug)
    return interactions_graph

def add_attributes(interactions_graph):
    add_num_edges_attribute(interactions_graph)
    add_node_attribute(interactions_graph)

def add_num_edges_attribute(interactions_graph):
    for node in interactions_graph.nodes:
        num_edges = interactions_graph.degree[node]
        interactions_graph.nodes[node]['connections'] = num_edges

def add_node_attribute(interactions_graph):
    for node in interactions_graph.nodes:
        is_gene = interactions_graph.nodes[node]['isGene']
        if(is_gene):
            set_color = "cyan"
            set_size = 10
        else:
            num_edges = interactions_graph.nodes[node]['connections']
            if(num_edges > 1):
                set_color = "orange"
                set_size = 5
            else: 
                set_color = "red"
        interactions_graph.nodes[node]['node_color'] = set_color
        interactions_graph.nodes[node]['node_size'] = set_size

def create_sub_graphs(interactions_graph):
    subgraphs = []
    for node in interactions_graph.nodes:
        node_isGene = interactions_graph.nodes[node]['isGene']
        if(node_isGene):
            node_neighbors = nx.all_neighbors(interactions_graph, node)
            subgraph_node_list1 = [node]
            subgraph_node_list2 = [node]
            for neighbor in node_neighbors:
                neighbor_connections = interactions_graph.nodes[neighbor]['connections']
                if(neighbor_connections == 1):
                    subgraph_node_list1.append(neighbor)
                if(neighbor_connections > 1):
                    subgraph_node_list2.append(neighbor)
            subgraph1 = interactions_graph.subgraph(subgraph_node_list1)
            subgraph2 = interactions_graph.subgraph(subgraph_node_list2)
            subgraphs.append(subgraph1)
            subgraphs.append(subgraph2)
    return subgraphs
            
def draw_graph(interactions_graph,pos):
    node_colors = [interactions_graph.nodes[node]['node_color'] for node in interactions_graph.nodes()]
    node_sizes = [interactions_graph.nodes[node]['node_size'] for node in interactions_graph.nodes()]
    nx.draw(interactions_graph, 
            pos=pos,
            node_size=node_sizes, 
            node_color=node_colors,
            width=0.05,
            edge_color='gray', 
            with_labels=True, 
            arrows=True,
            arrowstyle='-|>',
            arrowsize=2,
            font_size=0.1)

def draw_convex_hull(interactions_graph,pos):
    subgraphs = create_sub_graphs(interactions_graph)
    color_list = ["Red", "Orange", "Yellow", "Lime", "Green", "Aquamarine", "Cyan", "Indigo"]
    for subgraph, color in zip(subgraphs, color_list):
        node_group = list(subgraph.nodes())
        convexhull = ch([pos[node] for node in node_group])
        convex_hull_nodes = [node_group[i] for i in convexhull.vertices]
        polygon = plt.Polygon(
            [pos[node] for node in convex_hull_nodes],
            edgecolor=color, facecolor=color, 
            alpha=0.5, linewidth=1)
        plt.gca().add_patch(polygon)

def create_network(interactions):
    interactions_graph = initalize_network(interactions)
    add_attributes(interactions_graph)
    layout = nx.spring_layout(interactions_graph,seed=7)
    #draw_graph(interactions_graph,layout)
    #draw_convex_hull(interactions_graph,layout)
    return interactions_graph
    
def save_graph():
    plt.savefig("graph.jpg", dpi=3000)
    
def generate_plotly(graph):
    layout = go.Layout(
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    fig = go.Figure(layout=layout)
    
    if(graph is not None):
        pos = nx.spring_layout(graph, seed=7)

        trace_nodes = create_trace_nodes(graph,pos)
        trace_edges = create_trace_edges(graph,pos)
        #trace_convex_hulls = create_trace_convex_hulls(graph,pos)

        fig.add_trace(trace_edges)
        #for trace_convex_hull in trace_convex_hulls:
            #fig.add_trace(trace_convex_hull)
        for trace_group in trace_nodes:
            fig.add_trace(trace_group)

    return fig

def create_trace_nodes(graph,pos):
    trace_nodes = []
    
    nodes_by_group = {
        'cyan': {'node_x': [], 'node_y': [], 'node_text': [], 'node_colors': []},
        'orange': {'node_x': [], 'node_y': [], 'node_text': [], 'node_colors': []},
        'red': {'node_x': [], 'node_y': [], 'node_text': [], 'node_colors': []}
    }

    for node in graph.nodes():
        node_color = graph.nodes[node]['node_color']
        node_size = graph.nodes[node]['node_size']
        x, y = pos[node]
        if(node_color == "cyan"):
            nodes_by_group['cyan']['node_x'].append(x)
            nodes_by_group['cyan']['node_y'].append(y)
            nodes_by_group['cyan']['node_text'].append(str(node))
            nodes_by_group['cyan']['node_colors'].append(node_color)
        if(node_color == "orange"):
            nodes_by_group['orange']['node_x'].append(x)
            nodes_by_group['orange']['node_y'].append(y)
            nodes_by_group['orange']['node_text'].append(str(node))
            nodes_by_group['orange']['node_colors'].append(node_color)
        if(node_color == "red"):
            nodes_by_group['red']['node_x'].append(x)
            nodes_by_group['red']['node_y'].append(y)
            nodes_by_group['red']['node_text'].append(str(node))
            nodes_by_group['red']['node_colors'].append(node_color)

    for key,value in nodes_by_group.items():
        trace_group = go.Scatter(
            x=value['node_x'],
            y=value['node_y'],
            mode='markers',
            marker=dict(
                symbol='circle',
                size=7,
                color=value['node_colors']
            ),
            text=value['node_text'],
            hoverinfo='text',
            visible=True,
            showlegend=True,
            name=key
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
        line=dict(width=1,color='gray'),
        hoverinfo='none',
        showlegend=False
    )

    return trace_edges

def create_trace_convex_hulls(graph,pos):
    trace_convex_hulls = []
    subgraphs = create_sub_graphs(graph)
    color_list = ["Red", "Orange", "Yellow", "Lime", "Green", "Aquamarine", "Cyan", "Indigo"]
    try:
        for subgraph, color in zip(subgraphs, color_list):
            points = [pos[node] for node in list(subgraph.nodes())]

            hull = ch(points)
            hull_vertices = hull.vertices.tolist()
            hull_vertices.append(hull_vertices[0])

            hull_x = [points[i][0] for i in hull_vertices]
            hull_y = [points[i][1] for i in hull_vertices]

            trace_convex_hull = go.Scatter(x=hull_x, 
                                        y=hull_y, 
                                        mode='none', 
                                        fill='toself', 
                                        fillcolor=add_opacity_to_color(color), 
                                        hoverinfo='none',
                                        showlegend=False)
            trace_convex_hulls.append(trace_convex_hull)
    except Exception:
        pass
    return trace_convex_hulls

def add_opacity_to_color(color_name, alpha=0.5):
    rgba = mcolors.to_rgba(color_name)
    return f"rgba({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)}, {alpha})"

def generate_subgraph_plotly(graph,value):
    node_set = set([value])
    neighbors = graph.neighbors(value)
    for neighbor in neighbors:
        node_set.add(neighbor)
    subgraph = graph.subgraph(list(node_set))
    return generate_plotly(subgraph,False)