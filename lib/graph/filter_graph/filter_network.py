import lib.c_elegans as c_elegans
from collections import Counter

## CLASS BASED GRAPH MINIMIZATION
# path_with_classes = transform_cellPath_2_classPath(graph_obj.relevant_paths, inter_neurons, graph_obj.all_neurons)
#
# frequent_interneuron_classes = find_frequent_interneurons(paths=path_with_classes, src_list=graph_obj.from_list,
#                                                           trgt_list=graph_obj.to_list)
#
# print()
# print("frequent inter neuron classes")
# print(frequent_interneuron_classes)
#
# frequent_interneuron_cells = []
# for frequent_class in frequent_interneuron_classes:
#     frequent_interneuron_cells.extend(classes_dict[frequent_class])
#
# print("FREQ INTERNEURONS")
# print(frequent_interneuron_cells)
#
# sub_graph_nodes = graph_obj.from_list + frequent_interneuron_cells + graph_obj.to_list
# return sub_graph_nodes
