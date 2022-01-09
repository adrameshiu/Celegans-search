import networkx as nx


def remove_node(G, node):
    G.remove_node(node)


def remove_nodes_with_no_edges(G):
    frozen_sub_graph = nx.freeze(G)  # might affect main graph otherwise
    G_new = nx.MultiDiGraph(frozen_sub_graph)

    # removing nodes that have no successors or predecessors connected by edges
    nodes_to_remove = []
    for node in G_new.nodes():
        if len(list(G_new.predecessors(node))) == 0 and len(list(G_new.successors(node))) == 0:
            nodes_to_remove.append(node)

    for node in nodes_to_remove:
        remove_node(G=G_new, node=node)
    return G_new


def remove_leaf_nodes_that_are_not_source_or_target(G, from_list, to_list):
    removed_nodes = []
    all_nodes_in_graph = list(G.nodes())
    for node in all_nodes_in_graph:
        if node not in from_list and node not in to_list:
            if G.in_degree(node) == 0 or G.out_degree(node) == 0:
                remove_node(G=G, node=node)
                removed_nodes.append(node)
    return removed_nodes


def remove_nodes_that_do_not_connect_source_to_target(G, from_list, to_list):
    nodes_removed = remove_leaf_nodes_that_are_not_source_or_target(G=G, from_list=from_list, to_list=to_list)
    while len(nodes_removed) > 0:
        nodes_removed = remove_leaf_nodes_that_are_not_source_or_target(G=G, from_list=from_list, to_list=to_list)


def remove_nodes_without_layers(G):
    graph_node_details = list(G.nodes(data=True))
    for node, data in graph_node_details:
        has_layer_attr = 'layer' in data
        if not has_layer_attr:
            remove_node(G, node)
