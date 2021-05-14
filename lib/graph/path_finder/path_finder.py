import lib.graph.networkx_utils as networkx_utils
import networkx as nx


def find_all_simple_paths_multiple(graph_obj, cut_off):
    combined_sub_graph = None
    all_paths = []

    from_list = graph_obj.from_list
    to_list = graph_obj.to_list
    main_graph = graph_obj.main_graph

    for from_node in from_list:
        for to_node in to_list:
            are_both_nodes_present = networkx_utils.check_if_node_exists(G=main_graph, node=from_node) and \
                                     networkx_utils.check_if_node_exists(G=main_graph, node=to_node)
            if are_both_nodes_present:
                all_paths_between_two_nodes = find_all_simple_paths(main_graph=main_graph, src=from_node, trgt=to_node,
                                                                    cut_off=cut_off)
                all_paths.extend(all_paths_between_two_nodes)
                nodes_list, edges_list = get_nodes_and_edges_in_path(paths=all_paths_between_two_nodes)
                sub_graph = networkx_utils.get_edge_subgraph(G=main_graph, edges_list=edges_list)

                if sub_graph:
                    if not combined_sub_graph:
                        combined_sub_graph = sub_graph
                    else:
                        combined_sub_graph = networkx_utils.combine_two_graphs(combined_sub_graph, sub_graph)

    return combined_sub_graph, all_paths


def find_maximal_paths(graph_obj, max_cut_off):
    combined_sub_graph = None
    all_paths = []
    route_found = []
    all_sub_paths_dict = {}

    from_list = graph_obj.from_list
    to_list = graph_obj.to_list
    main_graph = graph_obj.main_graph

    for cut_off in range(1, max_cut_off + 1):  # range is half open interval
        for from_node in from_list:
            for to_node in to_list:
                are_both_nodes_present = networkx_utils.check_if_node_exists(G=main_graph, node=from_node) and \
                                         networkx_utils.check_if_node_exists(G=main_graph, node=to_node)

                if are_both_nodes_present and (from_node, to_node) not in route_found:
                    relevant_paths_between_two_nodes = find_all_simple_paths(main_graph=main_graph,
                                                                             src=from_node, trgt=to_node,
                                                                             cut_off=cut_off)

                    if len(relevant_paths_between_two_nodes) > 0:
                        all_paths.extend(relevant_paths_between_two_nodes)
                        all_sub_paths_dict.setdefault(from_node, {}). \
                            setdefault(to_node, {}). \
                            update({"paths": relevant_paths_between_two_nodes,
                                    "path_count": len(relevant_paths_between_two_nodes)}
                                   )  # for each from and to with all paths between in dict

                        nodes_list, edges_list = get_nodes_and_edges_in_path(paths=relevant_paths_between_two_nodes)
                        sub_graph = networkx_utils.get_edge_subgraph(G=main_graph, edges_list=edges_list)

                        if sub_graph:
                            route_found.append((from_node, to_node))
                            if not combined_sub_graph:
                                combined_sub_graph = sub_graph
                            else:
                                combined_sub_graph = networkx_utils.combine_two_graphs(combined_sub_graph, sub_graph)

    if len(all_paths) == 0:
        return None, None

    return combined_sub_graph, all_paths


def find_minimal_paths(graph_obj, max_cut_off):
    combined_sub_graph = None
    all_paths = []
    route_found = []
    all_sub_paths_dict = {}

    from_list = graph_obj.from_list
    to_list = graph_obj.to_list
    main_graph = graph_obj.main_graph

    for cut_off in range(1, max_cut_off + 1):  # range is half open interval
        for from_node in from_list:
            for to_node in to_list:
                are_both_nodes_present = networkx_utils.check_if_node_exists(G=main_graph, node=from_node) and \
                                         networkx_utils.check_if_node_exists(G=main_graph, node=to_node)

                if are_both_nodes_present and (from_node, to_node) not in route_found:
                    if cut_off == 1:
                        relevant_paths_between_two_nodes = find_paths_with_cut_off_1(G=main_graph,
                                                                                     from_node=from_node,
                                                                                     to_node=to_node)
                    else:
                        relevant_paths_between_two_nodes = find_paths_with_cut_off_gt_1(G=main_graph,
                                                                                        from_node=from_node,
                                                                                        to_node=to_node,
                                                                                        cut_off=cut_off,
                                                                                        existing_paths=all_paths)

                    if len(relevant_paths_between_two_nodes) > 0:
                        all_paths.extend(relevant_paths_between_two_nodes)
                        all_sub_paths_dict.setdefault(from_node, {}). \
                            setdefault(to_node, {}). \
                            update({"paths": relevant_paths_between_two_nodes,
                                    "path_count": len(relevant_paths_between_two_nodes)}
                                   )  # for each from and to with all paths between in dict

                        nodes_list, edges_list = get_nodes_and_edges_in_path(paths=relevant_paths_between_two_nodes)
                        sub_graph = networkx_utils.get_edge_subgraph(G=main_graph, edges_list=edges_list)

                        if sub_graph:
                            route_found.append((from_node, to_node))
                            if not combined_sub_graph:
                                combined_sub_graph = sub_graph
                            else:
                                combined_sub_graph = networkx_utils.combine_two_graphs(combined_sub_graph, sub_graph)

    if len(all_paths) == 0:
        return None, None

    return combined_sub_graph, all_paths


def find_paths_with_cut_off_1(G, from_node, to_node):
    all_paths = find_all_simple_paths(main_graph=G, src=from_node, trgt=to_node, cut_off=1)
    return all_paths


def find_paths_with_cut_off_gt_1(G, from_node, to_node, cut_off, existing_paths):
    best_incremental_paths = []
    all_paths_between_two_nodes = find_all_simple_paths(main_graph=G, src=from_node,
                                                        trgt=to_node, cut_off=cut_off)
    if len(all_paths_between_two_nodes) > 0:
        best_incremental_paths = get_best_incremental_paths(from_node=from_node,
                                                            all_paths_between_two_nodes=all_paths_between_two_nodes,
                                                            existing_paths=existing_paths)

    return best_incremental_paths


# if path through interneuron already exists, use it; otherwise use the new paths
def get_best_incremental_paths(from_node, all_paths_between_two_nodes, existing_paths):
    path_excluding_source = [path[1:] for path in all_paths_between_two_nodes]
    existing_sub_path = [sub_path for sub_path in path_excluding_source if
                         sub_path in existing_paths]  # if there is an existing sub path already, just add that after inserting the from node at 0th element

    if len(existing_sub_path) > 0:
        path_using_existing_sub_path = []
        for sub_path in existing_sub_path:  # refactor
            sub_path.insert(0, from_node)
            path_using_existing_sub_path.append(sub_path)
        best_path_from_node = path_using_existing_sub_path
    else:
        best_path_from_node = all_paths_between_two_nodes
    return best_path_from_node


def find_all_simple_paths(main_graph, src, trgt, cut_off=None):
    simple_paths = list(nx.all_simple_paths(main_graph, source=src, target=trgt, cutoff=cut_off))
    return simple_paths


def get_nodes_and_edges_in_path(paths):
    nodes_list = paths  # todo:refactor
    edges_list = []
    for nodes_in_path in paths:
        for i in range(0, len(nodes_in_path) - 1):
            edges_list.append(
                (nodes_in_path[i], nodes_in_path[i + 1], 0))  # replace 0 with k when there are multiple edges

    return nodes_list, edges_list
