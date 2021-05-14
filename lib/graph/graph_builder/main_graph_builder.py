import lib.pre_processor as pre_processing
import lib.graph.networkx_utils as networkx_utils
import lib.c_elegans as c_elegans
import lib.graph.group_classes as group_classes
from lib.options.user_settings import *
import lib.logger as logger

import math
import networkx as nx


def build_main_class_graph(graph_obj, cell_G, class_grouping_intensity=3, dot_path=None, csv_path=None):
    classes_dict = graph_obj.neuron_classes
    class_edges_in_graph = group_classes.reduce_inter_neuron_classes(graph_obj=graph_obj,
                                                                     cell_G=cell_G,
                                                                     class_grouping_intensity=class_grouping_intensity)
    graph_obj.main_graph = networkx_utils.build_class_graph(cell_G=cell_G,
                                                            class_edges=class_edges_in_graph,
                                                            classes_dict=classes_dict)

    networkx_utils.remove_nodes_that_do_not_connect_source_to_target(G=graph_obj.main_graph,
                                                                     from_list=graph_obj.from_list,
                                                                     to_list=graph_obj.to_list)

    if graph_obj.main_graph:
        graph_obj.find_and_fill_layer_details(for_main_graph=True)

        if dot_path:
            networkx_utils.write_dot_file(G=graph_obj.main_graph,
                                          dot_path=dot_path)
        if csv_path:
            inter_class_details = c_elegans.get_node_connection_details(G=graph_obj.main_graph,
                                                                        src_list=graph_obj.from_list,
                                                                        target_list=graph_obj.to_list,
                                                                        is_sub_attr=True)
            c_elegans.generate_interneuron_csv_file(csv_path=csv_path, neuron_details=inter_class_details)


def build_sub_class_graph(graph_obj, dot_path=None, csv_path=None):
    graph_obj.find_and_fill_layer_details(for_main_graph=False)

    if dot_path:
        networkx_utils.write_dot_file(G=graph_obj.sub_graph,
                                      dot_path=dot_path)
    if csv_path:
        inter_class_details = c_elegans.get_node_connection_details(G=graph_obj.sub_graph,
                                                                    src_list=graph_obj.from_list,
                                                                    target_list=graph_obj.to_list,
                                                                    is_sub_attr=True)
        c_elegans.generate_interneuron_csv_file(csv_path=csv_path, neuron_details=inter_class_details)


def build_main_cell_graph(cell_graph_obj, excel_path, from_classes_list, to_classes_list):
    df_list = pre_processing.get_relevant_excel_sheets(excel_path=excel_path)
    main_graph, classes_dict, nodes_dict_list = build_excel_graphs(df_list=df_list)

    cell_graph_obj.main_graph = main_graph
    cell_graph_obj.neuron_classes = classes_dict
    cell_graph_obj.all_neuron_details = nodes_dict_list

    all_neuron_cells_in_combined_graph = cell_graph_obj.get_all_neurons_in_main_graph()
    from_nodes_list, to_nodes_list = c_elegans.get_relevant_cells_from_classes(G=cell_graph_obj.main_graph,
                                                                               from_nodes_class=from_classes_list,
                                                                               to_nodes_class=to_classes_list,
                                                                               all_neurons_list=all_neuron_cells_in_combined_graph)
    cell_graph_obj.set_input_nodes(from_nodes=from_nodes_list, to_nodes=to_nodes_list)
    print("Graph build complete!")
    logger.print_graph_details(G=cell_graph_obj.main_graph)


def build_sub_cell_graph(graph_obj, dot_path=None, csv_path=None):
    graph_obj.set_layers_for_nodes(for_main_graph=False)
    if dot_path:
        networkx_utils.write_dot_file(G=graph_obj.main_graph,
                                      dot_path=dot_path)
    if csv_path:
        inter_neuron_details = c_elegans.get_node_connection_details(G=graph_obj.sub_graph,
                                                                     src_list=graph_obj.from_list,
                                                                     target_list=graph_obj.to_list,
                                                                     is_sub_attr=False)
        logger.print_neuron_details(neuron_details=inter_neuron_details)
        c_elegans.generate_interneuron_csv_file(csv_path=csv_path, neuron_details=inter_neuron_details)

    if dot_path:
        networkx_utils.write_dot_file(G=graph_obj.sub_graph, dot_path=dot_path)


def build_excel_graphs(df_list):
    all_synapses_graph = None
    for df_dict in df_list:
        print("parsing sheet: ", df_dict['type'].capitalize())
        adjacency_df, all_neurons_cols, all_neurons_rows, nodes_dict_list, classes_dict = pre_processing.parse_excel_df(
            df=df_dict['df'], header_row=header_row)
        print("Building network for ", df_dict['type'].capitalize(), "...")
        G = build_sheet_network(weight_matrix=adjacency_df, all_neurons_cols=all_neurons_cols,
                                all_neurons_rows=all_neurons_rows, synapse_type=df_dict['type'])
        print("Built network for ", df_dict['type'].capitalize())
        if G:
            if not all_synapses_graph:
                all_synapses_graph = G
            else:
                all_synapses_graph = networkx_utils.combine_two_graphs(all_synapses_graph, G)

    return all_synapses_graph, classes_dict, nodes_dict_list


def build_sheet_network(weight_matrix, all_neurons_cols, all_neurons_rows, synapse_type):
    G = nx.MultiDiGraph()
    for node1 in all_neurons_rows:
        for node2 in all_neurons_cols:
            edge_weight = weight_matrix.loc[node1, node2]
            if not math.isnan(edge_weight):
                abs_edge_weight = abs(edge_weight)
                G.add_edge(node1, node2, color=edge_type2color_map[synapse_type], weight=abs_edge_weight, alpha=0.5,
                           edge_type=synapse_type)
    return G
