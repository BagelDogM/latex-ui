import json

def assign_element_properties(elements):
    """
    Assign the approriate bucket and function (compile-to) from the config file to each point
    depending on their type.
    """
    elements_config = json.load(open("cfg/config.json"))['elements']

    for element in elements:
        element['bucket'] = elements_config[element['type']]['bucket']
        element['compile-to'] = elements_config[element['type']]['compile-to']

    return elements