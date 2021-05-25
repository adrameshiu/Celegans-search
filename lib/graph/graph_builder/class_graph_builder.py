from lib.api import graph_api
from lib.graph import ConnectomeGraph
import lib.c_elegans as c_elegans


def build_class_graph_from_cell_graph(cell_graph_obj, figures_drawn_till_now, from_nodes_class, to_nodes_class,
                                      max_cutoff, class_grouping_intensity=2):
    if class_grouping_intensity == 1:
        figures_drawn_till_now = build_strong_class_graph(cell_graph_obj=cell_graph_obj,
                                                          figures_drawn_till_now=figures_drawn_till_now,
                                                          from_nodes_class=from_nodes_class,
                                                          to_nodes_class=to_nodes_class,
                                                          max_cutoff=max_cutoff)
    elif class_grouping_intensity == 2:
        figures_drawn_till_now = build_moderate_class_graph(cell_graph_obj=cell_graph_obj,
                                                            figures_drawn_till_now=figures_drawn_till_now,
                                                            from_nodes_class=from_nodes_class,
                                                            to_nodes_class=to_nodes_class,
                                                            max_cutoff=max_cutoff)
    elif class_grouping_intensity == 3:
        figures_drawn_till_now = build_lenient_class_graph(cell_graph_obj=cell_graph_obj,
                                                           figures_drawn_till_now=figures_drawn_till_now,
                                                           from_nodes_class=from_nodes_class,
                                                           to_nodes_class=to_nodes_class,
                                                           max_cutoff=max_cutoff)
    else:
        figures_drawn_till_now = group_classes_three_ways(cell_graph_obj=cell_graph_obj,
                                                          figures_drawn_till_now=figures_drawn_till_now,
                                                          from_nodes_class=from_nodes_class,
                                                          to_nodes_class=to_nodes_class,
                                                          max_cutoff=max_cutoff)
    return figures_drawn_till_now


def group_classes_three_ways(cell_graph_obj, figures_drawn_till_now, from_nodes_class, to_nodes_class, max_cutoff):
    figures_drawn_till_now = build_strong_class_graph(cell_graph_obj=cell_graph_obj,
                                                      figures_drawn_till_now=figures_drawn_till_now,
                                                      from_nodes_class=from_nodes_class,
                                                      to_nodes_class=to_nodes_class,
                                                      max_cutoff=max_cutoff)

    figures_drawn_till_now = build_moderate_class_graph(cell_graph_obj=cell_graph_obj,
                                                        figures_drawn_till_now=figures_drawn_till_now,
                                                        from_nodes_class=from_nodes_class,
                                                        to_nodes_class=to_nodes_class,
                                                        max_cutoff=max_cutoff)

    figures_drawn_till_now = build_lenient_class_graph(cell_graph_obj=cell_graph_obj,
                                                       figures_drawn_till_now=figures_drawn_till_now,
                                                       from_nodes_class=from_nodes_class,
                                                       to_nodes_class=to_nodes_class,
                                                       max_cutoff=max_cutoff)
    return figures_drawn_till_now


def build_strong_class_graph(cell_graph_obj, figures_drawn_till_now, from_nodes_class, to_nodes_class, max_cutoff):
    class_graph_obj_strong = ConnectomeGraph()
    graph_api.build_class_main_graph(class_graph_obj=class_graph_obj_strong,
                                     cell_graph_obj=cell_graph_obj,
                                     from_nodes_class=from_nodes_class,
                                     to_nodes_class=to_nodes_class,
                                     class_grouping_intensity=1,
                                     dot_path='out_files/dot_files/main_class_graph_strong.dot',
                                     csv_path='out_files/neuron_info'
                                              '/inter_neuron_class_filtered_strong.csv')

    graph_api.filter_class_graph(class_graph_obj=class_graph_obj_strong,
                                 max_cutoff=max_cutoff,
                                 is_incremental=False)
    if class_graph_obj_strong.relevant_paths:
        cell_pathways_count_for_class = len(c_elegans.get_cell_pathways_for_class_paths(
            cell_paths=cell_graph_obj.relevant_paths,
            class_paths=class_graph_obj_strong.relevant_paths,
            all_neurons=cell_graph_obj.all_neuron_details))

        c_elegans.build_edges_csv(cell_paths=cell_graph_obj.relevant_paths,
                                  class_paths=class_graph_obj_strong.relevant_paths,
                                  all_neuron_details=cell_graph_obj.all_neuron_details,
                                  edges_csv_path='out_files/paths/complete_strong_class_paths.csv')

        class_graph_obj_strong.set_cell_pathways_count(cell_pathways_count=cell_pathways_count_for_class)

    if class_graph_obj_strong.main_graph:
        figures_drawn_till_now = figures_drawn_till_now + 1
        class_graph_obj_strong.draw_main_graph(figure_number=figures_drawn_till_now,
                                               plot_title="Complete Strong Grouped Class Graph")
    # if class_graph_obj_strong.sub_graph:
    #     figures_drawn_till_now = figures_drawn_till_now + 1
    #     class_graph_obj_strong.draw_sub_graph(figure_number=figures_drawn_till_now,
    #                                           plot_title="Maximal Strong Grouped Class Graph")

    # figures_drawn_till_now = graph_api.filter_class_graph(class_graph_obj=class_graph_obj_strong,
    #                                                       figure_number=figures_drawn_till_now,
    #                                                       plot_title="Minimal Strong Grouped Class Graph",
    #                                                       max_cutoff=max_cutoff,
    #                                                       is_maximal=False,
    #                                                       dot_path='out_files/dot_files/minimal_class_graph_strong.dot',
    #                                                       csv_path='out_files/neuron_info/minimal_class_filtered_strong.csv',
    #                                                       edges_csv_path='out_files/paths/minimal_class_filtered_strong_paths.csv')
    return figures_drawn_till_now


def build_moderate_class_graph(cell_graph_obj, figures_drawn_till_now, from_nodes_class, to_nodes_class, max_cutoff):
    class_graph_obj_moderate = ConnectomeGraph()
    graph_api.build_class_main_graph(class_graph_obj=class_graph_obj_moderate,
                                     cell_graph_obj=cell_graph_obj,
                                     from_nodes_class=from_nodes_class,
                                     to_nodes_class=to_nodes_class,
                                     class_grouping_intensity=2,
                                     dot_path='out_files/dot_files/main_class_graph_moderate.dot',
                                     csv_path='out_files/neuron_info'
                                              '/inter_neuron_class_filtered_moderate.csv')

    graph_api.filter_class_graph(class_graph_obj=class_graph_obj_moderate,
                                 max_cutoff=max_cutoff,
                                 is_incremental=False)
    if class_graph_obj_moderate.relevant_paths:
        cell_pathways_count_for_class = len(c_elegans.get_cell_pathways_for_class_paths(
            cell_paths=cell_graph_obj.relevant_paths,
            class_paths=class_graph_obj_moderate.relevant_paths,
            all_neurons=cell_graph_obj.all_neuron_details))

        c_elegans.build_edges_csv(cell_paths=cell_graph_obj.relevant_paths,
                                  class_paths=class_graph_obj_moderate.relevant_paths,
                                  all_neuron_details=cell_graph_obj.all_neuron_details,
                                  edges_csv_path='out_files/paths/complete_class_filtered_moderate_paths.csv')

        class_graph_obj_moderate.set_cell_pathways_count(cell_pathways_count=cell_pathways_count_for_class)

    if class_graph_obj_moderate:
        figures_drawn_till_now = figures_drawn_till_now + 1
        class_graph_obj_moderate.draw_main_graph(figure_number=figures_drawn_till_now,
                                                 plot_title="Complete Moderate Grouped Class Graph")
    # if class_graph_obj_moderate.sub_graph:
    #     figures_drawn_till_now = figures_drawn_till_now + 1
    #     class_graph_obj_moderate.draw_sub_graph(figure_number=figures_drawn_till_now,
    #                                             plot_title="Maximal Moderate Grouped Class Graph")

    # figures_drawn_till_now = graph_api.filter_class_graph(class_graph_obj=class_graph_obj_moderate,
    #                                                       figure_number=figures_drawn_till_now,
    #                                                       plot_title="Minimal Moderate Grouped Class Graph",
    #                                                       max_cutoff=max_cutoff,
    #                                                       is_maximal=False,
    #                                                       dot_path='out_files/dot_files/minimal_class_graph__moderate.dot',
    #                                                       csv_path='out_files/neuron_info/minimal_class_filtered_moderate.csv',
    #                                                       edges_csv_path='out_files/paths/minimal_class_filtered_moderate_paths.csv')
    return figures_drawn_till_now


def build_lenient_class_graph(cell_graph_obj, figures_drawn_till_now, from_nodes_class, to_nodes_class, max_cutoff):
    class_graph_obj_lenient = ConnectomeGraph()
    graph_api.build_class_main_graph(class_graph_obj=class_graph_obj_lenient,
                                     cell_graph_obj=cell_graph_obj,
                                     from_nodes_class=from_nodes_class,
                                     to_nodes_class=to_nodes_class,
                                     class_grouping_intensity=3,
                                     dot_path='out_files/dot_files/main_class_graph_lenient.dot',
                                     csv_path='out_files/neuron_info'
                                              '/inter_neuron_class_filtered_lenient.csv')

    graph_api.filter_class_graph(class_graph_obj=class_graph_obj_lenient,
                                 max_cutoff=max_cutoff,
                                 is_incremental=False)
    if class_graph_obj_lenient.relevant_paths:
        cell_pathways_count_for_class = len(c_elegans.get_cell_pathways_for_class_paths(
            cell_paths=cell_graph_obj.relevant_paths,
            class_paths=class_graph_obj_lenient.relevant_paths,
            all_neurons=cell_graph_obj.all_neuron_details))

        c_elegans.build_edges_csv(cell_paths=cell_graph_obj.relevant_paths,
                                  class_paths=class_graph_obj_lenient.relevant_paths,
                                  all_neuron_details=cell_graph_obj.all_neuron_details,
                                  edges_csv_path='out_files/paths/complete_class_filtered_lenient_paths.csv')

        class_graph_obj_lenient.set_cell_pathways_count(cell_pathways_count=cell_pathways_count_for_class)

    if class_graph_obj_lenient.main_graph:
        figures_drawn_till_now = figures_drawn_till_now + 1
        class_graph_obj_lenient.draw_main_graph(figure_number=figures_drawn_till_now,
                                                plot_title="Complete Lenient Grouped Class Graph")
    # if class_graph_obj_lenient.sub_graph:
    #     figures_drawn_till_now = figures_drawn_till_now + 1
    #     class_graph_obj_lenient.draw_sub_graph(figure_number=figures_drawn_till_now,
    #                                            plot_title="Maximal Lenient Grouped Class Graph")

    # figures_drawn_till_now = graph_api.filter_class_graph(class_graph_obj=class_graph_obj_lenient,
    #                                                       figure_number=figures_drawn_till_now,
    #                                                       plot_title="Minimal Lenient Grouped Class Graph",
    #                                                       max_cutoff=max_cutoff,
    #                                                       is_maximal=False,
    #                                                       dot_path='out_files/dot_files/minimal_class_graph_lenient.dot',
    #                                                       csv_path='out_files/neuron_info/minimal_class_filtered_lenient.csv',
    #                                                       edges_csv_path='out_files/paths/minimal_class_filtered_lenient_paths.csv')
    return figures_drawn_till_now
