import c_elegans_wiring.sub_modules.graph.networkx_utils as networkx_utils
import c_elegans_wiring.sub_modules.c_elegans as c_elegans


def reduce_inter_neuron_classes(graph_obj, cell_G, class_grouping_intensity):
    class_edges_in_graph = []
    all_neurons = graph_obj.all_neuron_details
    classes_dict = graph_obj.neuron_classes
    source_classes = graph_obj.from_list

    neuron_cells_considered = []

    u_classes = source_classes
    u_cells = c_elegans.get_cells_from_class_list(class_list=u_classes, classes_dict=classes_dict)

    v_cells = networkx_utils.get_successor_list(G=cell_G, src_nodes_list=u_cells)

    next_cells_set = set(v_cells)

    # while there are successors-> target class wont have successors
    while len(v_cells) > 0 and len(next_cells_set) > 0:
        neuron_cells_considered.extend(u_cells)
        v_classes = c_elegans.get_class_from_cell_list(cell_list=v_cells, all_neurons=all_neurons)
        class_edges_in_layer = group_classes(cell_G=cell_G, u_classes=u_classes, v_classes=v_classes,
                                             classes_dict=classes_dict,
                                             class_grouping_intensity=class_grouping_intensity)
        class_edges_in_graph.extend(class_edges_in_layer)

        # continue iteratively by setting u as v and finding v
        u_classes = v_classes
        u_cells = v_cells
        v_cells = networkx_utils.get_successor_list(G=cell_G, src_nodes_list=u_cells)
        next_cells_set = set(v_cells) - set(neuron_cells_considered)

    unique_edges_in_graph = list(set(class_edges_in_graph))
    return unique_edges_in_graph


def group_classes(cell_G, u_classes, v_classes, classes_dict, class_grouping_intensity=3):
    class_edges = []

    for u_class in u_classes:
        for v_class in v_classes:
            if check_class_edge(cell_G=cell_G,
                                u_class=u_class, v_class=v_class,
                                classes_dict=classes_dict,
                                class_grouping_intensity=class_grouping_intensity):
                class_edges.append((u_class, v_class))
    return class_edges


def check_class_edge(cell_G, u_class, v_class, classes_dict, class_grouping_intensity):
    does_class_edge_exist = False
    if class_grouping_intensity == 1:
        does_class_edge_exist = check_class_edge_strong(G=cell_G, u=u_class, v=v_class,
                                                        classes_dict=classes_dict)
    elif class_grouping_intensity == 2:
        does_class_edge_exist = check_class_edge_type_moderate(G=cell_G, u=u_class, v=v_class,
                                                               classes_dict=classes_dict)
    elif class_grouping_intensity == 3:
        does_class_edge_exist = check_class_edge_type_lenient(G=cell_G, u=u_class, v=v_class,
                                                              classes_dict=classes_dict)
    return does_class_edge_exist


def check_class_edge_strong(G, u, v, classes_dict):
    u_cells = classes_dict[u]
    v_cells = classes_dict[v]
    should_include_edge = True
    for u_cell in u_cells:
        for v_cell in v_cells:
            if not networkx_utils.check_if_edge_exists(G=G, from_node=u_cell, to_node=v_cell):
                should_include_edge = False
    return should_include_edge


def check_class_edge_type_moderate(G, u, v, classes_dict):
    u_cells = classes_dict[u]
    v_cells = classes_dict[v]
    should_include_edge = False
    for u_cell in u_cells:
        source_cell_has_path = False
        for v_cell in v_cells:
            if networkx_utils.check_if_edge_exists(G=G, from_node=u_cell, to_node=v_cell):
                source_cell_has_path = True

        if source_cell_has_path:
            should_include_edge = True
        else:
            should_include_edge = False
            break  # means some source does not have path to target-> no edge

    return should_include_edge


def check_class_edge_type_lenient(G, u, v, classes_dict):
    u_cells = classes_dict[u]
    v_cells = classes_dict[v]
    should_include_edge = False
    for u_cell in u_cells:
        for v_cell in v_cells:
            if networkx_utils.check_if_edge_exists(G=G, from_node=u_cell, to_node=v_cell):
                should_include_edge = True
    return should_include_edge
