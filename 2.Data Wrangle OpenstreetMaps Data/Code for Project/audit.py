import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Trail", "Parkway", "Commons", 
            "Highway", "Park", "Way", "Freeway", "Circle", "Cove", "Alley", "Pike", "East", "West", "North", "South"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "ln": "Lane",
            "ln.": "Lane",
            "Ln": "Lane",
            "Ln.": "Lane",
            "Ave": "Avenue",
            "Avene":"Avenue",
            "Rd.":"Road",
            "Rd":"Road",
            "RD":"Road",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Cir":"Circle",
            "Blvd":"Boulevard",
            "Blvd.":"Boulevard",
            "Blvd,":"Boulevard",
            "Blvd.,":"Boulevard",
            "Cv":"Cove",
            "Hwy": "Highway",
            "Hwy.": "Highway",
            "Ct":"Court",
            "Ctr":"Court",
            "CR":"Court",
            "Ln":"Lane",
            "Pkwy":"Parkway",
            "Pky": "Parkway",
            "Pky.": "Parkway",
            "Fwy": "Freeway",
            "Fwy.": "Freeway",
            "E": "East",
            "W": "West",
            "N": "North",
            #"S": "South",
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

def update_name(name, mapping):
    # YOUR CODE HERE
    for element in mapping.keys():
        if re.search(r'\s*' + element + r'\s*(?!\S)', name):
            name = name.replace(element, mapping[element])
    return name

# Execution
OSMFILE = 'state-college_pennsylvania.osm'
st_types = audit(OSMFILE)
pprint.pprint(dict(st_types))

