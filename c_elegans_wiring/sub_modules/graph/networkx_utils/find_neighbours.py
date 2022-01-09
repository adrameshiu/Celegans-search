def get_successor_list(G, src_nodes_list):
    successors_list = []
    for node in src_nodes_list:
        # since we are checking all possible cells from class, not necessary
        # that all of them are present in sub graph(might not have relevant path)
        if G.has_node(node):
            successors_list.extend(list(G.successors(node)))
    return list(set(successors_list))


def get_predecessor_list(G, target_nodes_list):
    predecessor_list = []
    for node in target_nodes_list:
        if G.has_node(node):
            predecessor_list.extend(list(G.predecessors(node)))
    return list(set(predecessor_list))

