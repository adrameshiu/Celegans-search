# from networkx.drawing.nx_agraph import write_dot
#import matplotlib as plt
import pydot
import networkx as nx
import matplotlib.pyplot as plotter


def write_dot_file(G, dot_path):
    #write_dot(G, dot_path)
    graph = nx.drawing.nx_pydot.to_pydot(G)
    graph.write_dot(dot_path)
    #graph.write_png(dot_path)


def write_plot_legend(G, pathways_count, interneurons_count):
    pathways_string = "Pathways\nCount:{val}".format(val=pathways_count)
    interneurons_string = "Interneurons\nCount:{val}".format(val=interneurons_count)
    plotter.legend([pathways_string, interneurons_string])
