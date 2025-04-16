import json
import os

def build_elements():
    if not os.path.isdir('src/static/elements'):
        os.makedirs('src/static/elements') # Make elements directory
    # TODO: refactor to use Jinja
    ui_config = json.load(open('cfg/ui_config.json'))
    config = json.load(open("cfg/config.json"))

    # Populate elements/ directory
    names = []
    for name, props in config["elements"].items():
        element_html = ui_config['element-opener'].replace("NAME", name) # Add opener e.g., opening tag of container
        # Iterate through element fields and add HTML objects
        for field_name, field_props in props["fields"].items():
            type = field_props["type"]
            element_html += ui_config['input-types'][type].replace("ID", field_name).replace("PLACEHOLDER", field_name.capitalize())

        element_html += ui_config['element-closer'] # e.g., closing tag of container

        # Write the HTMl to the correct file in elements/
        with open(f'src/static/elements/{name}.html', 'w') as file:
            file.write(element_html)

        names.append(name)

    # Return the created elements so that the backend can populate the navbar.
    return names