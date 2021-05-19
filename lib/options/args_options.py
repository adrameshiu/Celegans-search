from argparse import ArgumentParser
import lib.logger as logger


class ArgsCLI:

    def __init__(self):
        self._init_parser()
        # default values
        self.from_nodes_class = ['ADE', 'ADF', 'ADL', 'AFD', 'ASE', 'ASG', 'ASH', 'ASI', 'ASJ', 'ASK', 'AUA', 'AWA',
                                 'AWB', 'AWC',
                                 'BAG', 'CEP', 'PDE']
        self.to_nodes_class = ['AVA']
        self.max_cutoff = 2
        self.class_grouping_intensity = 2
        self.show_cell_graph = False

    def _init_parser(self):
        self.parser = ArgumentParser()
        self.parser.add_argument("--f",
                                 nargs='+',
                                 help="specifies a list of FROM NEURON CLASSES to find path from as source(default "
                                      "specified in code taken otherwise)")
        self.parser.add_argument("--t",
                                 nargs='+',
                                 help="specifies a list of TO NEURON CLASSES to find path to as target(default "
                                      "specified in code taken otherwise)")
        self.parser.add_argument("--show_cell",
                                 type=bool,
                                 help="flag to decide whether to show the cell graph or not(default- false)")
        self.parser.add_argument("--cgi",
                                 type=int,
                                 help="specifies the class grouping intensity\n"
                                      "Options are"
                                      "\n\t1-Strong"
                                      "\n\t2-Moderate(default)"
                                      "\n\t3-Lenient"
                                      "\n\t0-Show all graphs")
        self.parser.add_argument("--c",
                                 type=int,
                                 help="specifies the max distance cutoff depth to search till(default- 2)")

    def parse(self):
        input_args = self.parser.parse_args()
        self.get_input_data_from_args(input_args=input_args)

    def get_input_data_from_args(self, input_args):
        if input_args.f:
            self.from_nodes_class = input_args.f
        if input_args.t:
            self.to_nodes_class = input_args.t
        if input_args.c:
            self.max_cutoff = input_args.c
        if input_args.cgi or input_args.cgi == 0:  # otherwise 0 is getting considered as none by args
            self.class_grouping_intensity = input_args.cgi
        if input_args.show_cell:
            self.show_cell_graph = input_args.show_cell

        logger.print_user_parameters(self)
