import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
    # YOUR CODE HERE
    tags={}
    for event,element in ET.iterparse(filename):
        if event=='end':
            key = element.tag
            if key not in tags:
                tags[key] = 1
            else:
                tags[key] = tags[key] + 1
    return tags

# Execution
tags = count_tags('state-college_pennsylvania.osm')
pprint.pprint(tags)