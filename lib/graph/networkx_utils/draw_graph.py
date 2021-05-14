import networkx as nx
import matplotlib.pyplot as plt
from lib.graph.networkx_utils.graph_details import *
from lib.graph.networkx_utils.export_options import *
from lib.graph.networkx_utils.graph_attributes import *


def draw_cell_graph(plot_title, cell_G, from_nodes_cells, to_nodes_cells):
    if len(cell_G.nodes()) < 100:
        pos = nx.multipartite_layout(cell_G, subset_key="layer")
    else:
        pos = nx.spring_layout(cell_G)

    node_color_values = color_nodes(G=cell_G, src_nodes=from_nodes_cells, target_nodes=to_nodes_cells)

    edge_colors = nx.get_edge_attributes(cell_G, 'color').values()
    edge_weights = nx.get_edge_attributes(cell_G, 'weight').values()

    plt.figure(plot_title)
    plt.title(plot_title)

    nx.draw(cell_G, pos, node_size=1000, node_color=node_color_values, edge_color=edge_colors, with_labels=True)


def draw_class_graph(plot_title, class_G, from_nodes_class, to_nodes_class, cell_pathways_count):
    if len(class_G.nodes()) < 100:
        pos = nx.multipartite_layout(class_G, subset_key="layer")
    else:
        pos = nx.spring_layout(class_G)

    node_color_values = color_nodes(G=class_G, src_nodes=from_nodes_class, target_nodes=to_nodes_class)

    edge_attr = nx.get_edge_attributes(class_G, 'attr_dict').values()
    # edge_colors = [edge['color'] for edge in edge_attr]
    # edge_colors = nx.get_edge_attributes(class_G,'color').values()
    # edge_weights = nx.get_edge_attributes(class_G,'weight').values()

    plt.figure(plot_title)
    plt.title(plot_title)

    nx.draw(class_G, pos, node_size=1000, node_color=node_color_values, with_labels=True)
    exclude_nodes = []
    exclude_nodes.extend(from_nodes_class)
    exclude_nodes.extend(to_nodes_class)
    interneurons_list, pathways_list = get_graph_details(G=class_G, exclude_nodes=exclude_nodes)
    write_plot_legend(G=class_G, pathways_count=cell_pathways_count, interneurons_count=len(interneurons_list))
