from lib.graph.networkx_utils.find_neighbours import *


def add_layer_attribute(G, layers):
    for i in range(0, len(layers)):
        G.add_nodes_from(layers[i], layer=i)
    return G


def layer_graphs_backwards(G, target_list):
    discovered_graph_nodes = []
    discovered_graph_nodes.extend(target_list)

    reverse_layers = [target_list]
    predecessor_list = get_predecessor_list(G=G, target_nodes_list=target_list)
    undiscovered_predecessor_list = list(set(predecessor_list) - set(discovered_graph_nodes))
    discovered_graph_nodes.extend(predecessor_list)

    while len(undiscovered_predecessor_list) > 0:
        reverse_layers.append(undiscovered_predecessor_list)
        predecessor_list = get_predecessor_list(G=G, target_nodes_list=undiscovered_predecessor_list)
        undiscovered_predecessor_list = list(set(predecessor_list) - set(discovered_graph_nodes))
        discovered_graph_nodes.extend(predecessor_list)
    return reverse_layers
