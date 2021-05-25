from lib.options.user_settings import *


def find_all_synapse_types_at_neuron(neuron):
    all_keys = []
    in_keys = list(neuron['IN'].keys())
    all_keys.extend(in_keys)
    out_keys = list(neuron['OUT'].keys())
    all_keys.extend(out_keys)
    all_keys = list(set(all_keys))  # to remove duplicates
    return all_keys


def get_synapse_count_string(synapse_type, neuron):
    synapse_string = synapse_type + " : "
    synapse_count_dict = get_synapse_count(synapse_type=synapse_type, neuron=neuron)
    synapse_string = synapse_string + '[' + str(synapse_count_dict.get('IN')) + ',' + str(
        synapse_count_dict.get('OUT')) + ']'
    return synapse_string


def get_synapse_count(synapse_type, neuron):
    synapse_count_dict = {'type': synapse_type,
                          'IN': neuron['IN'].get(synapse_type) if synapse_type in neuron['IN'] else 0,
                          'OUT': neuron['OUT'].get(synapse_type) if synapse_type in neuron['OUT'] else 0}
    return synapse_count_dict


def get_synapse_headers_for_csv():
    all_headers_list = ['neuron_name']
    synapse_types = list(sheet_name2synapse_map.values())
    synapse_types.append('mixed')  ##todo:refactor
    synapse_headers_list = list(
        map(lambda x: [get_in_synapse_string_with_type(synapse_type=x),
                       get_out_synapse_string_with_type(synapse_type=x)],
            synapse_types))
    for synapse_type in synapse_headers_list:
        all_headers_list.extend(synapse_type)
    all_headers_list.extend(['product_of_synapses', 'sum_of_synapses'])
    return all_headers_list


def get_in_synapse_string_with_type(synapse_type):
    return 'in_synapse_count' + '(' + synapse_type + ')'


def get_out_synapse_string_with_type(synapse_type):
    return 'out_synapse_count' + '(' + synapse_type + ')'
