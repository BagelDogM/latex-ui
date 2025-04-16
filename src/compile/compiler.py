import json
from jinja2 import Environment, BaseLoader, FileSystemLoader

jinja_env_params = json.load(open("cfg/config.json"))["jinja"]

# def parse_string(string):
#     # Escape necessary characters and convert single linebreaks to \newline characters.
#     escape_characters = {
#         '\\': '\\textbackslash ',
#         '{': '\\{',
#         '}': '\\}',
#         '%': '\\%',
#         '\n': '\\newline ' # \n\n will already be used as intended.
#     }
#     for pattern, replacement in escape_characters.items():
#         string = string.replace(pattern, replacement)

#     # Convert
#     return string

# def write_element(file_object, element):
#     # Escape all characters for each entry after the element type so they aren't compiled wrong - e.g. % starting a comment
#     escaped_values = map(parse_string, element['values'])
#     file_object.write(f'\\{element["type"]}'+'{'+'}{'.join(escaped_values)+'}\n')

def complile(data: list[dict]):
    """
    Takes a list of elements (point, visits etc) and compiles them into correct latex code which is
    written to latex/tmp.tex
    """
    config = json.load(open("cfg/config.json"))
    write_location, template_source = config["document"]["write-location"], config["document"]["template-source"]

    buckets = {name: [] for name in config["buckets"].keys()} # Initialise empty buckets

    for element in data:
        # Format element values into its function parameter
        print(f'{element['values']=}')

        func_env = Environment(loader=BaseLoader(), **jinja_env_params).from_string(element['compile-to'])
        formatted_function = func_env.render(element['values']) # Do string replacement using element values

        # Add to appropriate bucket
        buckets[element['bucket']].append(formatted_function)

    for bucket_name, bucket_elements in buckets.items():
        bconfig = config['buckets'][bucket_name] # Get config for only THIS bucket
        text = ""

        # Add begin and end values if values present or persistent (of course, persistent objects also with values will also get begin and end values)
        if bucket_elements or bconfig['persistent']: text += bconfig["begin"]

        # Add each element, joined by the joiner
        text += bconfig['joiner'].join(bucket_elements)

        if bucket_elements or bconfig['persistent']: text += bconfig["end"]

        buckets[bucket_name] = text

    # Finally, place buckets into document using Jinja string formatting
    bucket_env = Environment(loader=FileSystemLoader( searchpath="./" ), **jinja_env_params)
    template = bucket_env.get_template(template_source)

    # Render template and write to file of the same name (weird, I know but we want this as a file)
    with open(write_location, 'w') as file:
        file.write(template.render(buckets))
