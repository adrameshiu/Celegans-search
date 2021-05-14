import networkx as nx


def get_edge_subgraph(G, edges_list):
    sub_graph = None
    sub_graph = G.edge_subgraph(edges_list)
    return sub_graph


def get_node_subgraph(G, nodes_list):
    sub_graph = G.subgraph(nodes_list)
    return sub_graph


def combine_two_graphs(graph1, graph2):
    # Return a new graph of graph1 composed WITH graph2.
    new_graph = nx.compose(graph1, graph2)
    return new_graph
