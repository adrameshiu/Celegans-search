from argparse import ArgumentParser


class ArgsCLI:

    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        self.parser = ArgumentParser()
        self.parser.add_argument("--list",
                                 nargs='+',
                                 help="specifies elements in list one after other")
        self.parser.add_argument("--i",
                                 type=int,
                                 help="specifies an integer input")

    def parse(self):
        return self.parser.parse_args()
