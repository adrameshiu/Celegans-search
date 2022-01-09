import networkx as nx
import matplotlib.pyplot as plotter
from c_elegans_wiring.sub_modules.graph.networkx_utils.graph_details import *
from c_elegans_wiring.sub_modules.graph.networkx_utils.export_options import *
from c_elegans_wiring.sub_modules.graph.networkx_utils.graph_attributes import *


def draw_cell_graph(plot_title, cell_G, from_nodes_cells, to_nodes_cells):
    # not plotting on main graph as we need to show synapses with both electric and chemical together
    G = build_cell_graph_combining_multi_edges(cell_G=cell_G)

    if len(G.nodes()) < 100:
        pos = nx.multipartite_layout(G, subset_key="layer")
    else:
        pos = nx.spring_layout(G)

    node_color_values = color_nodes(G=G, src_nodes=from_nodes_cells, target_nodes=to_nodes_cells)

    edge_colors = nx.get_edge_attributes(G, 'color').values()
    edge_weights = nx.get_edge_attributes(G, 'weight').values()

    plotter.figure(plot_title)
    plotter.title(plot_title)

    nx.draw(G, pos, node_size=1000, node_color=node_color_values, edge_color=edge_colors, with_labels=True)


def draw_class_graph(plot_title, class_G, from_nodes_class, to_nodes_class, cell_pathways_count):
    if len(class_G.nodes()) < 100:
        pos = nx.multipartite_layout(class_G, subset_key="layer")
    else:
        pos = nx.spring_layout(class_G)

    node_color_values = color_nodes(G=class_G, src_nodes=from_nodes_class, target_nodes=to_nodes_class)

    edge_attr = nx.get_edge_attributes(class_G, 'attr_dict').values()
    edge_colors = nx.get_edge_attributes(class_G, 'color').values()
    # edge_colors = [edge['color'] for edge in edge_attr]
    # edge_colors = nx.get_edge_attributes(class_G,'color').values()
    # edge_weights = nx.get_edge_attributes(class_G,'weight').values()

    plotter.figure(plot_title)
    plotter.title(plot_title)

    nx.draw(class_G, pos, node_size=1000, node_color=node_color_values, edge_color=edge_colors, with_labels=True)
    exclude_nodes = []
    exclude_nodes.extend(from_nodes_class)
    exclude_nodes.extend(to_nodes_class)
    interneurons_list, pathways_list = get_graph_details(G=class_G, exclude_nodes=exclude_nodes)
    write_plot_legend(G=class_G, pathways_count=cell_pathways_count, interneurons_count=len(interneurons_list))


def build_cell_graph_combining_multi_edges(cell_G):
    frozen_cell_graph = nx.freeze(cell_G)
    G = nx.MultiDiGraph(frozen_cell_graph)
    edges = get_graph_edges(G=G, with_data=True)
    # todo : refactor
    # edges_with_both_synapse_types = [edge for edge in edges if get_edge_type(G=cell_G, from_node=edge[0], to_node=edge[1], data=edge[2])]
    # print(edges)
    return G