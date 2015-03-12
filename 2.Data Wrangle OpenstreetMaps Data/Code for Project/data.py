import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
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
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    node = {}
    created = {}
    address = {}
    node_refs = []
    pos = [0, 0]
    # you should process only 2 types of top level tags: "node" and "way"
    if element.tag == "node" or element.tag == "way" :
        if element.tag == "node":
            node["type"] = "node"
        elif element.tag == "way":
            node["type"] = "way"
        for key in element.attrib:
            if key in CREATED:   # Created regular attributes
                created[key] = element.attrib[key]
            elif key == "lat":
                pos[0] = float(element.attrib["lat"])
            elif key == "lon":
                pos[1] = float(element.attrib["lon"])
            else:
                node[key] = element.attrib[key]
        node["created"] = created   # attributes in the CREATED array should be added under a key "created"
        node["pos"] = pos          # attributes for latitude and longitude should be added to a "pos" array
        for tag in element.iter("tag"):
            k_value = tag.attrib["k"].strip()
            v_value = tag.attrib["v"].strip()
            # if second level tag "k" value contains problematic characters, it should be ignored
            if problemchars.search(k_value):
                continue
            # if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
            elif "addr:" in k_value:
                # if there is a second ":" that separates the type/direction of a street, the tag should be ignored
                if ":" not in k_value[5:]:
                    name = v_value
                    name = name.replace(",", "")
                    # if second level tag "k" value does not start with "addr:", but contains ":", you can process it same as any other tag
                    for word in name.split(" "):
                        if word in mapping.keys():
                            name = name.replace(word, mapping[word])
                    address[k_value[5:].strip()] = name
            elif k_value == "shop":
                node["amenity"] = v_value
            elif k_value == "sport":
                node["amenity"] = v_value
            elif k_value == "tourism":
                node["amenity"] = v_value
            else:
                 node[k_value] = tag.attrib["v"].strip()
        if address != {}:
            node["address"] = address
        for nd in element.iter("nd"):  # Add node_refs
            node_refs.append(nd.attrib["ref"])
        if node_refs != []:
            node["node_refs"] = node_refs
        return node
    else:
        return None

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

# Execution
data = process_map('state-college_pennsylvania.osm', False)
#pprint.pprint(data[0])