import networkx as nx


def print_user_parameters(args_obj):
    print("Finding path for-")
    print("From Neuron Classes: ", args_obj.from_nodes_class)
    print("To Neuron Classes: ", args_obj.to_nodes_class)
    print("Max Cutoff Depth: ", args_obj.max_cutoff)
    print("Class Grouping Intensity: ", args_obj.class_grouping_intensity)
    print("Show cell graph: ", args_obj.show_cell_graph)
    print()


def print_graph_details(G):
    edge_types = list(nx.get_edge_attributes(G, 'edge_type').values())
    print("Main Graph for has ", len(G.nodes()), " nodes and ",
          len(G.edges()), " edges   ||||  ", edge_types.count('chemical'),
          "chemical edges and ", edge_types.count('asymmetric gap'), " asymmetric gap synapses")


def print_neuron_details(neuron_details):
    for neuron in neuron_details:
        print(neuron['name'], "[", neuron['IN']['chemical'], ",", neuron['OUT']['chemical'],
              "]")  # todo:should be general for both synapses
