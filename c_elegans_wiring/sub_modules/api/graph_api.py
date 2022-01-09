from c_elegans_wiring.sub_modules.api import api_alpha
import c_elegans_wiring.sub_modules.graph.graph_builder as graph_builder


def build_cell_main_graph(cell_graph_obj, df_list, from_nodes_class, to_nodes_class):
    print("Building Cell Graph...")
    api_alpha.build_main_cell_graph(cell_graph_obj=cell_graph_obj,
                                    df_list=df_list,
                                    from_classes_list=from_nodes_class, to_classes_list=to_nodes_class)


def filter_cell_graph(cell_graph_obj, max_cutoff,
                      is_maximal=True, show_cell_graph=False,
                      output_folder=None):
    cell_graph_obj.sub_graph = api_alpha.filter_graph(graph_obj=cell_graph_obj,
                                                      max_cutoff=max_cutoff,
                                                      is_incremental=False,
                                                      is_maximal=is_maximal)
    if cell_graph_obj.relevant_paths:
        cell_graph_obj.cell_pathways_count = len(cell_graph_obj.relevant_paths)
    graph_builder.build_sub_cell_graph(graph_obj=cell_graph_obj,
                                       output_folder=output_folder)

    if show_cell_graph:
        cell_graph_obj.draw_sub_graph(plot_title="Filtered Cell Graph")
    return cell_graph_obj.sub_graph


def build_class_main_graph(class_graph_obj, cell_graph_obj, from_nodes_class, to_nodes_class,
                           class_grouping_intensity, dot_path=None, csv_path=None):
    class_graph_obj.set_is_class_graph(is_class_graph=True)
    class_graph_obj.set_input_nodes(from_nodes=from_nodes_class, to_nodes=to_nodes_class)
    class_graph_obj.set_neuron_classes(neuron_classes=cell_graph_obj.neuron_classes)
    class_graph_obj.set_neuron_details(all_neuron_details=cell_graph_obj.all_neuron_details)

    graph_builder.build_main_class_graph(graph_obj=class_graph_obj,
                                         cell_G=cell_graph_obj.sub_graph,
                                         class_grouping_intensity=class_grouping_intensity,
                                         dot_path=dot_path,
                                         csv_path=csv_path)


def filter_class_graph(class_graph_obj, max_cutoff, is_maximal=True, dot_path=None, is_incremental=True,
                       csv_path=None):
    class_graph_obj.sub_graph = api_alpha.filter_graph(graph_obj=class_graph_obj,
                                                       max_cutoff=max_cutoff,
                                                       is_incremental=is_incremental,
                                                       is_maximal=is_maximal)
    if class_graph_obj.sub_graph:
        graph_builder.build_sub_class_graph(class_graph_obj,
                                            dot_path=dot_path,
                                            csv_path=csv_path)
