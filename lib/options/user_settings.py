##################################################################

# A set of maps and relevant flags that are defined as setting

##################################################################

# RELEVANT SHEETS
sheet_name2synapse_map = {'hermaphrodite chemical': 'chemical'}  # for only chem
# sheet_name2synapse_map = {'hermaphrodite chemical':'chemical', 'hermaphrodite gap jn asymmetric':'electric'} #for
# both together

# EXCEL PARSING PARAMETERS
loc_suffix = ['R', 'L']
dv_suffix = ['D', 'V']
header_row = 2

# COLOR MAPS
# node colors
node_color = '#7B92AA'
src_color = '#CCD4BF'
dest_color = '#E5DB9C'

# edge colors
edge_type2color_map = {'chemical': '#DC828F',
                       'electric': '#BEB4CF'}  # green color edges for chemical; red for assymetric gap
