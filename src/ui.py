import json
import kdl
import os

def build_elements():
    os.makedirs('src/static/elements') # Make elements directory
    # TODO: refactor to use Jinja
    ui_config = kdl.parse(open('cfg/ui_config.kdl').read())
    with open("cfg/config.json") as file:
        config = json.load(file)

        # Populate elements/ directory
        names = []
        for name, props in config["elements"].items():
            element_html = ui_config.get('element-opener').args[0].replace("NAME", name) # Add opener e.g., opening tag of container
            # Iterate through element fields and add HTML objects
            for field_name, field_props in props["fields"].items():
                type = field_props["type"]
                element_html += ui_config.get(type).args[0].replace("ID", field_name).replace("PLACEHOLDER", field_name.capitalize())

            element_html += ui_config.get('element-closer').args[0] # e.g., closing tag of container

            # Write the HTMl to the correct file in elements/
            with open(f'src/static/elements/{name}.html', 'w') as file:
                file.write(element_html)

            names.append(name)

        # Return the created elements so that the backend can populate the navbar.
        return names