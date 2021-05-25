import networkx as nx
from lib.options.user_settings import *


def set_node_attribute(G, node_label, attribute_name, value):
    nx.set_node_attributes(G, values={node_label: value}, name=attribute_name)


def set_edge_attribute(G, edge_tuple, attribute_name, value):
    nx.set_edge_attributes(G, values={edge_tuple: value}, name=attribute_name)


def color_nodes(G, src_nodes=None, target_nodes=None):
    node_color_values = []
    for node in G.nodes():
        if node in src_nodes:
            node_color_values.append(src_color)
        elif node in target_nodes:
            node_color_values.append(dest_color)
        else:
            node_color_values.append(node_color)

    return node_color_values
