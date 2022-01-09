import c_elegans_wiring.sub_modules.graph.path_finder as path_finder
import c_elegans_wiring.sub_modules.graph.graph_builder as graph_builder


def build_main_cell_graph(cell_graph_obj, df_list, from_classes_list, to_classes_list):
    return graph_builder.build_main_cell_graph(cell_graph_obj=cell_graph_obj,
                                               df_list=df_list,
                                               from_classes_list=from_classes_list, to_classes_list=to_classes_list)


def filter_graph(graph_obj, max_cutoff, is_incremental=False, is_maximal=True):
    if is_incremental:
        if is_maximal:
            sub_graph, all_paths = path_finder.find_maximal_paths(graph_obj=graph_obj, max_cut_off=max_cutoff)
        else:
            sub_graph, all_paths = path_finder.find_minimal_paths(graph_obj=graph_obj, max_cut_off=max_cutoff)
    else:
        sub_graph, all_paths = path_finder.find_all_simple_paths_multiple(graph_obj=graph_obj, cut_off=max_cutoff)

    if all_paths:
        graph_obj.relevant_paths = all_paths
        graph_obj.fill_layers_from_paths()
    return sub_graph
