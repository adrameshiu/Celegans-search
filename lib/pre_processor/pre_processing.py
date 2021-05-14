# parse the excel sheet containing the adjacency matrices and get the neurons and weights corresponding to them

import pandas as pd
from lib.manipulation import *


# Given an excel sheet path, extract all the sheets present and only return a list that contains the sheets defined in
def get_relevant_excel_sheets(excel_path):
    print(sheet_name2synapse_map)
    xlsx = pd.ExcelFile(excel_path)
    df_all_sheets = pd.read_excel(xlsx, sheet_name=None, index_col=None, header=None)
    df_list = []
    for key in df_all_sheets.keys():
        if key in sheet_name2synapse_map.keys():
            df_list.append({'type': sheet_name2synapse_map[key], 'df': df_all_sheets[key]})
    return df_list


# From the dataframe of each relevant sheet, extract the adjacency matrices and other required fields
# refer notebook for more details
def parse_excel_df(df, header_row):
    # since each cell group is merged in the first two columns, we fill forward to apply them cell wise
    df[0] = pd.Series(df[0]).fillna(method='ffill')
    df[1] = pd.Series(df[1]).fillna(method='ffill')

    adjacency_df = df[(header_row + 1):]
    adjacency_df.columns = df.iloc[header_row]

    all_neurons_cols = list(adjacency_df.columns.dropna())

    adjacency_df = adjacency_df.rename(columns={adjacency_df.columns[0]: 'Unknown_col_names'})

    adjacency_df.set_index("Unknown_col_names", inplace=True)

    neuron_tuple_index_series = list(adjacency_df.index.values)

    nodes_dict_list = {}
    node_names_list = []
    classes_dict = {}
    for tup in neuron_tuple_index_series:
        if not pd.isnull(
                tup[2]):  # condition to check if there is name, as null value could be present in the last column
            neuron_organ = tup[0]
            neuron_group = tup[1]
            neuron_name = tup[2]
            class_name, location = parse_neuron_name(neuron_name=neuron_name)
            neuron_node = {neuron_name: {"organ": neuron_organ,
                                         "group": neuron_group,
                                         "label": neuron_name,
                                         "class": class_name,
                                         "location": location}}

            neurons_in_class = classes_dict[class_name] if class_name in classes_dict else []

            nodes_dict_list.update(neuron_node)
            node_names_list.append(neuron_name)
            neurons_in_class.append(neuron_name)
            classes_dict[class_name] = neurons_in_class

    # rows denote source and columns denote targets
    neurons_that_have_no_out_degree = list(set(all_neurons_cols) - set(node_names_list))
    for dest_neuron_name in neurons_that_have_no_out_degree:
        class_name, location = parse_neuron_name(neuron_name=dest_neuron_name)
        neuron_node = {dest_neuron_name: {"label": dest_neuron_name,
                                          "class": class_name,
                                          "location": location}}

        neurons_in_class = classes_dict[class_name] if class_name in classes_dict else []

        nodes_dict_list.update(neuron_node)
        neurons_in_class.append(dest_neuron_name)
        classes_dict[class_name] = neurons_in_class

    adjacency_df.drop(adjacency_df.tail(1).index,
                      inplace=True)  # drop last rows which is just the adjacency labels again

    adjacency_df.insert(1, "Neuron_name", node_names_list, True)
    adjacency_df.set_index("Neuron_name", inplace=True)

    neurons_row_index = list(adjacency_df.index.dropna().values)

    return adjacency_df, all_neurons_cols, neurons_row_index, nodes_dict_list, classes_dict
