import collections
import csv
import functools
import operator
from collections import Counter

import c_elegans_wiring.sub_modules.manipulation as manipulation
import c_elegans_wiring.sub_modules.graph.networkx_utils as networkx_utils
import c_elegans_wiring.sub_modules.graph.synapse as synapse
from c_elegans_wiring.sub_modules.options.user_settings import *


def get_relevant_cells_from_classes(G, from_nodes_class, to_nodes_class, all_neurons_list):
    from_nodes_list = get_neurons_in_class_name(G=G, classes_list=from_nodes_class,
                                                all_neurons_list=all_neurons_list,
                                                check_has_successors=True)
    to_nodes_list = get_neurons_in_class_name(G=G, classes_list=to_nodes_class,
                                              all_neurons_list=all_neurons_list)
    return from_nodes_list, to_nodes_list


# ##todo:extend using class dict
def get_neurons_in_class_name(G, classes_list, all_neurons_list, check_has_successors=False):
    neurons_list = []
    for class_name in classes_list:
        sublist = [neuron for neuron in all_neurons_list if
                   neuron.startswith(class_name)]  # will be from whatever rows are there
        for item in sublist:
            neurons_list.append(item)

    # #only those nodes that have successors/neighbours can have paths-> otherwise networkx returns error
    if check_has_successors:
        for neuron in neurons_list:
            has_successors = len(list(G.successors(neuron))) > 0
            if not has_successors:  # if doesnt have any path, remove the source from the graph
                neurons_list.remove(neuron)

    return neurons_list


def get_cells_from_class_list(class_list, classes_dict):
    cell_list = []
    for neuron_class in class_list:
        cell_list.extend(classes_dict[neuron_class])
    return cell_list


def get_class_from_cell_list(cell_list, all_neurons):
    classes_list = list(set([all_neurons[cell]['class'] for cell in cell_list]))
    return classes_list


def get_class_edge(cell_G, u_class, v_class, classes_dict):
    all_class_edges = []
    cell_edge_connections_counter = Counter()

    u_cells = classes_dict[u_class]
    v_cells = classes_dict[v_class]
    for u_cell in u_cells:
        for v_cell in v_cells:
            cell_edge_details = networkx_utils.find_edge_details(G=cell_G,
                                                                 from_node=u_cell, to_node=v_cell,
                                                                 is_sub_attr=False)
            all_class_edges.append(cell_edge_details)

    # we have a list of dict of all synapse details...we need to sum them up based on type of synapse
    for dct in all_class_edges:
        cell_edge_connections_counter.update(dct)
    return dict(cell_edge_connections_counter)


def get_node_connection_details(G, src_list, target_list, is_sub_attr=False):
    neuron_details = []
    sub_graph_nodes = list(G.nodes())

    for node in sub_graph_nodes:
        if (node in src_list) or (node in target_list):  # we do not want the source or target neurons here
            continue
        incoming_neuron_heads = find_incoming_neuron_heads(G=G, node=node, is_sub_attr=is_sub_attr)
        outgoing_neuron_heads = find_outgoing_neuron_heads(G=G, node=node, is_sub_attr=is_sub_attr)

        neuron_details.append({"name": node, "IN": incoming_neuron_heads, "OUT": outgoing_neuron_heads})
    return neuron_details


def find_incoming_neuron_heads(G, node, is_sub_attr):
    node_predecessors = list(G.predecessors(node))

    # to find for incoming neuron heads
    incoming_neuron_heads = {}
    incoming_synapse = []
    for prev_node in node_predecessors:
        pred_synapse = networkx_utils.find_edge_details(G=G,
                                                        from_node=prev_node, to_node=node,
                                                        is_sub_attr=is_sub_attr)
        incoming_synapse.append(pred_synapse)
    if len(incoming_synapse) > 0:
        incoming_neuron_heads = sum_values_with_same_key_in_list_of_dicts(lst=incoming_synapse)

    return incoming_neuron_heads


def find_outgoing_neuron_heads(G, node, is_sub_attr):
    # to find for outgoing neuron heads
    node_successors = list(G.successors(node))
    outgoing_neuron_heads = {}
    outgoing_synapse = []
    for next_node in node_successors:
        succ_synapse = networkx_utils.find_edge_details(G=G, from_node=node, to_node=next_node,
                                                        is_sub_attr=is_sub_attr)
        outgoing_synapse.append(succ_synapse)

    if len(outgoing_synapse) > 0:
        outgoing_neuron_heads = sum_values_with_same_key_in_list_of_dicts(lst=outgoing_synapse)

    return outgoing_neuron_heads


def sum_values_with_same_key_in_list_of_dicts(lst):
    counter_dict = dict(functools.reduce(operator.add,
                                         map(collections.Counter, lst)))
    return counter_dict


def generate_interneuron_csv_file(csv_path, neuron_details):
    with open(csv_path, 'w', newline='') as csv_file:
        synapse_types = list(sheet_name2synapse_map.values())
        synapse_types.append('mixed') ##todo:refactor
        csv_headers = synapse.get_synapse_headers_for_csv()
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader()
        for neuron in neuron_details:
            neuron_csv_dict = {'neuron_name': neuron['name']}
            in_values = []
            out_values = []
            all_synapse_count_list = list(map(lambda x: synapse.get_synapse_count(synapse_type=x, neuron=neuron),
                                              synapse_types))
            for synapse_count_list in all_synapse_count_list:
                in_synapse_key = synapse.get_in_synapse_string_with_type(synapse_type=synapse_count_list['type'])
                out_synapse_key = synapse.get_out_synapse_string_with_type(synapse_type=synapse_count_list['type'])
                neuron_csv_dict[in_synapse_key] = synapse_count_list['IN']
                neuron_csv_dict[out_synapse_key] = synapse_count_list['OUT']
                in_values.append(neuron_csv_dict[in_synapse_key])
                out_values.append(neuron_csv_dict[out_synapse_key])
            total_in_values = sum(in_values)
            total_out_values = sum(out_values)
            neuron_csv_dict['sum_of_synapses'] = total_in_values + total_out_values
            neuron_csv_dict['product_of_synapses'] = total_in_values * total_out_values
            writer.writerow(neuron_csv_dict)


def get_cell_pathways_for_class_paths(cell_paths, class_paths, all_neurons):
    relevant_cell_paths = []
    filtered_cell_paths = cell_paths.copy()
    filtered_cell_paths = manipulation.remove_none_from_list_of_lists(lst=filtered_cell_paths)

    filtered_class_paths = class_paths.copy()
    filtered_class_paths = manipulation.remove_none_from_list_of_lists(lst=filtered_class_paths)

    for path in filtered_cell_paths:
        cell_path_transformed_to_class_path = list(map(lambda element: all_neurons[element]['class'], path))
        if cell_path_transformed_to_class_path in filtered_class_paths:
            relevant_cell_paths.append(path)
    return relevant_cell_paths


def build_edges_csv(cell_paths, class_paths, all_neuron_details, edges_csv_path):
    # todo: uncomment
    cell_paths_for_class_grouping = get_cell_pathways_for_class_paths(
        cell_paths=cell_paths,
        class_paths=class_paths,
        all_neurons=all_neuron_details)
    generate_edges_csv_file(csv_path=edges_csv_path, path_list=cell_paths_for_class_grouping)


def generate_edges_csv_file(csv_path, path_list):
    with open(csv_path, 'w', newline='') as csv_file:
        fieldnames = ['paths']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for path in path_list:
            writer.writerow({'paths': path})
