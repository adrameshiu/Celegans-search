import networkx as nx
import lib.c_elegans as c_elegans
from lib.options.user_settings import *


def build_class_graph(cell_G, class_edges, classes_dict):
    class_G = nx.MultiDiGraph()
    for u_class, v_class in class_edges:
        class_edge_attr = c_elegans.get_class_edge(cell_G=cell_G,
                                                   u_class=u_class, v_class=v_class,
                                                   classes_dict=classes_dict)
        total_number_of_connections = sum(list(class_edge_attr.values()))
        user_synapse_type = get_user_synapse_type(edge_keys=list(class_edge_attr.keys()))
        class_G.add_edge(u_class, v_class,
                         color=edge_type2color_map[user_synapse_type],
                         weight=total_number_of_connections,
                         edge_type=user_synapse_type,
                         graph_type='class_graph')

    return class_G


def get_user_synapse_type(edge_keys):
    if len(edge_keys) > 1:
        return 'multiple'
    else:
        return edge_keys[0]
