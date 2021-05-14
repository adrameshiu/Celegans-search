from networkx.drawing.nx_agraph import write_dot
import matplotlib.pyplot as plt


def write_dot_file(G, dot_path):
    write_dot(G, dot_path)


def write_plot_legend(G, pathways_count, interneurons_count):
    pathways_string = "Pathways\nCount:{val}".format(val=pathways_count)
    interneurons_string = "Interneurons\nCount:{val}".format(val=interneurons_count)
    plt.legend([pathways_string, interneurons_string])
