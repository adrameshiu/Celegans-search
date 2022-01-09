def check_if_node_exists(G, node):
    return G.has_node(node)


def check_if_edge_exists(G, from_node, to_node):
    return G.has_edge(from_node, to_node)


def get_graph_details(G, exclude_nodes=[], exclude_edges=[]):
    nodes_list = get_graph_nodes(G=G, exclude_nodes=exclude_nodes)
    edges_list = get_graph_edges(G=G, exclude_edges=exclude_edges)
    return nodes_list, edges_list


def get_graph_nodes(G, exclude_nodes=[]):
    nodes_list = list(G.nodes())
    nodes_list = list(set(nodes_list) - set(exclude_nodes))
    return nodes_list


def get_graph_edges(G, with_data=False, exclude_edges=[]):
    edges_list = list(G.edges(data=with_data))
    return edges_list


def get_edge_data(G, from_node, to_node):
    edge_data = G.get_edge_data(from_node, to_node, default=None)
    return edge_data


def get_edge_type(G, from_node, to_node, data=False):
    # print("FROM NODE:", from_node)
    # print("TO NODE:", to_node)
    edges = get_edge_data(G=G, from_node=from_node, to_node=to_node)
    #print(edges)
    return False


def find_edge_details(G, from_node, to_node, is_sub_attr=False):
    synapse = {}
    edge_details = get_edge_data(G=G, from_node=from_node, to_node=to_node)
    if edge_details:
        if not is_sub_attr:
            multi_edge_weights_in_edge = [e['weight'] for e in edge_details.values()]
            total_weight_in_edge = sum(multi_edge_weights_in_edge)
            number_of_synaptic_connections = total_weight_in_edge  # 0 considers only 1st edge appearing..need to reedit
            synapse[edge_details[0]['edge_type']] = number_of_synaptic_connections
        else:
            # todo:refactor for different types of edges
            print(edge_details)
            multi_edge_weights_in_edge = [e['weight'] for e in edge_details.values()]
            total_weight_in_edge = sum(multi_edge_weights_in_edge)
            number_of_synaptic_connections = total_weight_in_edge  # 0 considers only 1st edge appearing..need to reedit
            synapse['chemical'] = number_of_synaptic_connections
            # multi_edge_weights_in_edge = [e['attr_dict']['weight'] for e in edge_details.values()]
            # total_weight_in_edge = sum(multi_edge_weights_in_edge)
            # number_of_synaptic_connections = total_weight_in_edge  # 0 considers only 1st edge appearing..need to reedit
            # synapse[edge_details[0]['attr_dict']['edge_type']] = number_of_synaptic_connections

    return synapse
