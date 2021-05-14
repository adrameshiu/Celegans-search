import networkx as nx
import lib.c_elegans as c_elegans


def build_class_graph(cell_G, class_edges, classes_dict):
    class_G = nx.MultiDiGraph()
    for u_class, v_class in class_edges:
        class_edge_attr = c_elegans.get_class_edge(cell_G=cell_G,
                                                   u_class=u_class, v_class=v_class,
                                                   classes_dict=classes_dict)
        total_number_of_connections = sum(list(class_edge_attr.values()))
        class_G.add_edge(u_class, v_class, weight=total_number_of_connections)
    return class_G
