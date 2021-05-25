from lib.options.user_settings import *


##################################################################
# Given a neuron name, parse it to get the class name and location of the neuron
# This is based on our assumption that,
# - the first three characters always represent class name
# - the last character, if it has a direction, will be either left or right('L' or 'R')
# - the second last character, if it has a location, will be either Dorsal or Ventral, ie. front or back('D' or 'V')
##################################################################
def parse_neuron_name(neuron_name):
    class_string = neuron_name
    loc_string = None

    if len(neuron_name) > 3:
        post_classname_characters = neuron_name[3:]
        last_character = post_classname_characters[-1] if len(post_classname_characters) > 0 else None
        second_last_character = post_classname_characters[-2] if len(post_classname_characters) > 1 else None

        if last_character and (last_character in loc_suffix):
            if second_last_character and (second_last_character in dv_suffix):
                loc_string = second_last_character + last_character
                class_string = neuron_name[:-2]
            else:
                loc_string = last_character
                class_string = neuron_name[:-1]

    return class_string, loc_string


def remove_none_from_list_of_lists(lst):
    filtered_list = [list(filter(None, sub_list)) for sub_list in lst]
    return filtered_list


