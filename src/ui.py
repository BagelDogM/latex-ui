import json
import os
from jinja2 import Environment, BaseLoader

def build_elements():
    if not os.path.isdir('src/static/elements'):
        os.makedirs('src/static/elements') # Make elements directory
    # TODO: refactor to use Jinja
    ui_config = json.load(open('cfg/ui_config.json'))
    config = json.load(open("cfg/config.json"))

    # Populate elements/ directory
    names = []
    for name, props in config["elements"].items():
        env = Environment(loader=BaseLoader()).from_string(ui_config['element-opener']) # for string replacement
        element_html = env.render(name=name) # Add opener e.g., opening tag of container - string replacement via Jinja

        # Iterate through element fields and add HTML objects
        for field_name, field_props in props["fields"].items():
            type = field_props["type"]
            env = Environment(loader=BaseLoader()).from_string(ui_config['input-types'][type]) # for string replacement
            element_html += env.render(name=field_name)

        env = Environment(loader=BaseLoader()).from_string(ui_config['element-closer']) # for string replacement
        element_html += env.render(name=name) # e.g., closing tag of container

        # Write the HTMl to the correct file in elements/
        with open(f'src/static/elements/{name}.html', 'w') as file:
            file.write(element_html)

        names.append(name)

    # Return the created elements so that the backend can populate the navbar.
    return names