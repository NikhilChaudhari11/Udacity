import xml.etree.ElementTree as ET

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        user_next = element.get("uid")
        if (user_next not in users) and (user_next != None):
            users.add(user_next)
        element.clear()

    return users

# Execution
users = process_map('state-college_pennsylvania.osm')
pprint.pprint(len(users))

