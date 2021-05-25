import networkx as nx
from lib.manipulation import *
import lib.graph.synapse as synapse


def print_user_parameters(args_obj):
    print("Finding path for-")
    print("From Neuron Classes: ", args_obj.from_nodes_class)
    print("To Neuron Classes: ", args_obj.to_nodes_class)
    print("Max Cutoff Depth: ", args_obj.max_cutoff)
    print("Class Grouping Intensity: ", args_obj.class_grouping_intensity)
    print("Show cell graph: ", args_obj.show_cell_graph)
    print("Synapse types: ", args_obj.synapse_types)
    print()


def print_graph_details(G):
    edge_types = list(nx.get_edge_attributes(G, 'edge_type').values())
    print("Main Graph for has ", len(G.nodes()), " nodes and ",
          len(G.edges()), " edges   ||||  ", edge_types.count('chemical'),
          "chemical edges and ", edge_types.count('asymmetric gap'), " asymmetric gap synapses")


def print_neuron_details(neuron_details):
    for neuron in neuron_details:
        neuron_string = neuron['name'] + ' -> '
        all_keys = synapse.find_all_synapse_types_at_neuron(neuron)
        for synapse_type in all_keys:
            synapse_string = synapse.get_synapse_count_string(synapse_type=synapse_type, neuron=neuron)
            neuron_string = neuron_string + '   ' + synapse_string
        print(neuron_string)
