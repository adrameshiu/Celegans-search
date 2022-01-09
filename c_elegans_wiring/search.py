import os
import pkg_resources
import pandas as pd

from c_elegans_wiring.sub_modules.graph import ConnectomeGraph, networkx_utils, graph_builder
from c_elegans_wiring.sub_modules.api import graph_api
from c_elegans_wiring.sub_modules.options.user_settings import *


def read_wiring_adjacency_matrix(synapse_types):
    stream = pkg_resources.resource_stream(__name__, 'data/sheet2020.xlsx')
    df_all_sheets = pd.read_excel(stream, sheet_name=None, index_col=None, header=None)
    df_list = []
    for key in df_all_sheets.keys():
        if key in sheet_name2synapse_map.keys():
            if sheet_name2synapse_map[key] in synapse_types:
                df_list.append({'type': sheet_name2synapse_map[key], 'df': df_all_sheets[key]})
    return df_list


# synapse types is a list containing a subset of ['chemical', 'electric']
# returns graph object
# writes dot file and csv

def get_filtered_cell_graph(from_nodes_class, to_nodes_class,
                            synapse_types=['chemical', 'electric'],
                            max_cutoff=2,
                            view_graph=False,
                            output_folder=None):
    cell_graph_obj = ConnectomeGraph()
    df_list = read_wiring_adjacency_matrix(synapse_types)
    graph_api.build_cell_main_graph(cell_graph_obj=cell_graph_obj,
                                    df_list=df_list,
                                    from_nodes_class=from_nodes_class, to_nodes_class=to_nodes_class)

    filtered_cell_graph_object = graph_api.filter_cell_graph(cell_graph_obj=cell_graph_obj,
                                                             max_cutoff=max_cutoff,
                                                             show_cell_graph=True,
                                                             output_folder=output_folder)

    if view_graph:
        networkx_utils.show_graphs()

    return filtered_cell_graph_object


# synapse types is a list containing a subset of ['chemical', 'electric']
# returns graph object
# writes dot file and csv
# cgi->class grouping intensity(0 by default)
def get_filtered_class_graph(from_nodes_class, to_nodes_class,
                             synapse_types=['chemical', 'electric'],
                             max_cutoff=2, cgi=0,
                             view_graph=False,
                             output_folder=None):
    cell_graph_obj = ConnectomeGraph()
    df_list = read_wiring_adjacency_matrix(synapse_types)
    graph_api.build_cell_main_graph(cell_graph_obj=cell_graph_obj,
                                    df_list=df_list,
                                    from_nodes_class=from_nodes_class, to_nodes_class=to_nodes_class)

    filtered_cell_graph_object = graph_api.filter_cell_graph(cell_graph_obj=cell_graph_obj,
                                                             max_cutoff=max_cutoff,
                                                             show_cell_graph=True,
                                                             output_folder=output_folder)

    figures_drawn_till_now = graph_builder.class_graph_builder.build_class_graph_from_cell_graph(
                                        cell_graph_obj=cell_graph_obj,
                                        from_nodes_class=from_nodes_class,
                                        to_nodes_class=to_nodes_class,
                                        max_cutoff=max_cutoff,
                                        class_grouping_intensity=cgi,
                                        output_folder=output_folder)

    if view_graph:
        networkx_utils.show_graphs()
