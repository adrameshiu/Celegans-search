from lib import options
from lib.graph import ConnectomeGraph
from lib.api import graph_api
import lib.graph.graph_builder as class_graph_builder
import lib.graph.networkx_utils as networkx_utils

excel_path = "dataset/sheet2020.xlsx"


def main(args_obj):
    figures_drawn_till_now = 0
    cell_graph_obj = ConnectomeGraph()
    graph_api.build_cell_main_graph(cell_graph_obj=cell_graph_obj,
                                    excel_path=excel_path,
                                    from_nodes_class=args_obj.from_nodes_class, to_nodes_class=args_obj.to_nodes_class)

    figures_drawn_till_now = graph_api.filter_cell_graph(cell_graph_obj=cell_graph_obj,
                                                         max_cutoff=args_obj.max_cutoff,
                                                         figure_number=figures_drawn_till_now,
                                                         show_cell_graph=args_obj.show_cell_graph,
                                                         dot_path='out_files/dot_files/cell_graph.dot',
                                                         csv_path='out_files/neuron_info/inter_neuron_cells_filtered'
                                                                  '.csv')

    figures_drawn_till_now = class_graph_builder.build_class_graph_from_cell_graph(cell_graph_obj=cell_graph_obj,
                                                                                   figures_drawn_till_now=figures_drawn_till_now,
                                                                                   from_nodes_class=args_obj.from_nodes_class,
                                                                                   to_nodes_class=args_obj.to_nodes_class,
                                                                                   max_cutoff=args_obj.max_cutoff,
                                                                                   class_grouping_intensity=args_obj.class_grouping_intensity)
    networkx_utils.show_graphs()


if __name__ == '__main__':
    args_parser = options.ArgsCLI()
    args_parser.parse()
    main(args_parser)
