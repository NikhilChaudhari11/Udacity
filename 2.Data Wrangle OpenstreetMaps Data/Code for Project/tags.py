import xml.etree.ElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
	# YOUR CODE HERE
    if element.tag == "tag":
        # Obtain the k_value for the tag
        k_value = element.attrib['k']
        # Perform searches for the three patterns
        search_lower = re.search(lower,k_value)
        search_lower_colon = re.search(lower_colon,k_value)
        search_problemchars = re.search(problemchars,k_value)
        # Count the key_types
        if search_lower:
            keys["lower"] = keys["lower"]+1
        elif search_lower_colon:
            keys["lower_colon"] = keys["lower_colon"] +1
        elif search_problemchars:
            keys["problemchars"] = keys["problemchars"] +1
        else:
            keys["other"] = keys["other"] + 1
       
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

# Execution
keys = process_map('state-college_pennsylvania.osm')
pprint.pprint(keys)
