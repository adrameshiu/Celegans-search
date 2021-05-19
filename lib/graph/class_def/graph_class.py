import lib.graph.networkx_utils as networkx_utils


class ConnectomeGraph:

    def __init__(self):
        self.main_graph = None
        self.sub_graph = None
        self.minimal_graph = None
        self.maximal_graph = None
        self.from_list = None
        self.to_list = None
        self.neuron_classes = None
        self.all_neuron_details = None
        self.relevant_paths = None
        self.layers = None
        self.is_class_graph = False
        self.cell_pathways_count = 0

    def set_is_class_graph(self, is_class_graph):
        self.is_class_graph = is_class_graph

    def set_input_nodes(self, from_nodes, to_nodes):
        self.from_list = from_nodes
        self.to_list = to_nodes

    def set_neuron_classes(self, neuron_classes):
        self.neuron_classes = neuron_classes

    def set_neuron_details(self, all_neuron_details):
        self.all_neuron_details = all_neuron_details

    def set_cell_pathways_count(self, cell_pathways_count):
        self.cell_pathways_count = cell_pathways_count

    def get_all_neurons_in_main_graph(self):
        return list(self.main_graph.nodes())

    def get_all_neurons_in_sub_graph(self):
        return list(self.sub_graph_view.nodes())

    def draw_main_graph(self, figure_number, plot_title):
        if self.is_class_graph:
            networkx_utils.draw_class_graph(plot_title=plot_title,
                                            from_nodes_class=self.from_list, to_nodes_class=self.to_list,
                                            class_G=self.main_graph, cell_pathways_count=self.cell_pathways_count)
        else:
            networkx_utils.draw_cell_graph(figure_number=figure_number, plot_title=plot_title,
                                           cell_G=self.main_graph,
                                           from_nodes_cells=self.from_list, to_nodes_cells=self.to_list)

    def draw_sub_graph(self, plot_title):
        if self.is_class_graph:
            networkx_utils.draw_class_graph(plot_title=plot_title,
                                            from_nodes_class=self.from_list, to_nodes_class=self.to_list,
                                            class_G=self.sub_graph, cell_pathways_count=self.cell_pathways_count)
        else:
            networkx_utils.draw_cell_graph(plot_title=plot_title,
                                           cell_G=self.sub_graph,
                                           from_nodes_cells=self.from_list, to_nodes_cells=self.to_list)

    def fill_layers_from_paths(self):
        all_paths = self.relevant_paths
        max_length = max(map(len, all_paths))  # mapping length to entire list
        for layer in all_paths:
            while len(layer) < max_length:
                # to zip, we need all lists to be of the same length..
                # so lets INSERT none as a value in the current last element
                # pushes the previous last element one position forward
                layer.insert(-1,
                             None)
        layered_nodes = list(zip(*all_paths))

        # convert to set to get unique elements and then back to get a list-> also need to exclude none
        layered_nodes = [list(set(filter(None, layer))) for layer in
                         layered_nodes]
        self.layers = layered_nodes

    def find_and_fill_layer_details(self, for_main_graph=True):
        self.fill_layers_backwards(for_main_graph=for_main_graph)
        self.set_layers_for_nodes(for_main_graph=for_main_graph)
        self.remove_class_nodes_without_layers(for_main_graph=for_main_graph)

    def fill_layers_backwards(self, for_main_graph):
        if for_main_graph:
            layers = networkx_utils.layer_graphs_backwards(G=self.main_graph, target_list=self.to_list)
        else:
            layers = networkx_utils.layer_graphs_backwards(G=self.sub_graph, target_list=self.to_list)
        layers.reverse()  # the list we get is in reverse
        self.layers = layers

    def set_layers_for_nodes(self, for_main_graph):
        if for_main_graph:
            gph = self.main_graph
        else:
            gph = self.sub_graph
        layers = self.layers
        for i in range(0, len(layers)):
            for node in layers[i]:
                networkx_utils.set_node_attribute(G=gph, node_label=node, attribute_name='layer', value=i)

    def remove_class_nodes_without_layers(self, for_main_graph):
        if for_main_graph:
            gph = self.main_graph
        else:
            gph = self.sub_graph
        networkx_utils.remove_nodes_without_layers(G=gph)
