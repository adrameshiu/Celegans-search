from lib.api import api_alpha
import lib.graph.graph_builder as graph_builder


def build_cell_main_graph(cell_graph_obj, excel_path, from_nodes_class, to_nodes_class):
    print("Building Cell Graph...")
    api_alpha.build_main_cell_graph(cell_graph_obj=cell_graph_obj,
                                    excel_path=excel_path,
                                    from_classes_list=from_nodes_class, to_classes_list=to_nodes_class)


def filter_cell_graph(cell_graph_obj, max_cutoff, figure_number, is_maximal=True, dot_path=None, csv_path=None):
    cell_graph_obj.sub_graph = api_alpha.filter_graph(graph_obj=cell_graph_obj,
                                                      max_cutoff=max_cutoff,
                                                      is_incremental=False,
                                                      is_maximal=is_maximal)
    if cell_graph_obj.relevant_paths:
        cell_graph_obj.cell_pathways_count = len(cell_graph_obj.relevant_paths)
    graph_builder.build_sub_cell_graph(graph_obj=cell_graph_obj,
                                       dot_path=dot_path,
                                       csv_path=csv_path)
    # figure_number = figure_number + 1
    # cell_graph_obj.draw_main_graph(figure_number=figure_number, plot_title="Main Cell Graph")
    #
    # figure_number = figure_number + 1
    # cell_graph_obj.draw_sub_graph(figure_number=figure_number, plot_title="Sub Cell Graph")
    return figure_number


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
