import shutil
import json

def parse_string(string):
    # Escape necessary characters and convert single linebreaks to \newline characters.
    escape_characters = {
        '\\': '\\textbackslash ',
        '{': '\\{',
        '}': '\\}',
        '%': '\\%',
        '\n': '\\newline ' # \n\n will already be used as intended.
    }
    for pattern, replacement in escape_characters.items():
        string = string.replace(pattern, replacement)

    # Convert
    return string

def write_element(file_object, element):
    # Escape all characters for each entry after the element type so they aren't compiled wrong - e.g. % starting a comment
    escaped_values = map(parse_string, element['values'])
    file_object.write(f'\\{element["type"]}'+'{'+'}{'.join(escaped_values)+'}\n')

def complile_to_latex(data: list[dict]):
    """
    Takes a list of elements (point, visits etc) and compiles them into correct latex code which is
    written to latex/tmp.tex
    """
    config = json.load(open("cfg/config.json"))

    write_location = config["document"]["write-location"]
    # Create a copy of the template to write to in order to create the final latex
    file_text = open(config["document"]["template-source"]).read()

    buckets = {name: [] for name in config["buckets"].keys()} # Initialise empty buckets

    for element in data:
        # Format element values into its function parameter
        formatted_function = element['function']
        print(element['values'])
        for name, value in element['values'].items():
            # TODO: refactor to Jinja
            print(name)
            formatted_function = formatted_function.replace(f'${name}', str(value))

        # Add to appropriate bucket
        buckets[element['bucket']].append(formatted_function)

    for bucket_name, bucket_elements in buckets.items():
        bconfig = config['buckets'][bucket_name]
        text = ""

        # Add begin and end values if values present or persistent
        if bucket_elements or bconfig['persistent']: text += bconfig["begin"]

        # Add each element, joined by the joiner
        text += bconfig['joiner'].join(bucket_elements)

        if bucket_elements or bconfig['persistent']: text += bconfig["end"]

        # Finally, once text is created, add to appropriate location in file.
        file_text = file_text.replace(f'${bucket_name}', text)

    # Add final text of all buckets.
    with open(write_location, 'w') as file:
        file.write(file_text)
