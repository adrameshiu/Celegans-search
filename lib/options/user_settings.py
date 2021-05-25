##################################################################

# A set of maps and relevant flags that are defined as setting

##################################################################

# RELEVANT SHEETS
# sheet_name2synapse_map = {'hermaphrodite chemical': 'chemical'}  # for only chem
sheet_name2synapse_map = {'hermaphrodite chemical': 'chemical',
                          'hermaphrodite gap jn asymmetric': 'electric'}  # for

short_hand2synapse_map = {'c': 'chemical',
                          'e': 'electric'}
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
edge_type2color_map = {'chemical': '#264027',  # green for chemical
                       'electric': '#FFC370',  # yellow for electric
                       'multiple': '#856084'}  # purple for mix
