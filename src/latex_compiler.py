import shutil

def latex_escaped_string(string):
    escape_characters = {
        '\\': '\\textbackslash',
        '{': '\\{',
        '}': '\\}',
        '%': '\\%'}
    for pattern, replacement in escape_characters.items():
        string = string.replace(pattern, replacement)

    return string
    print(f'Esc as {string}')

def write_element(file_object, element):
    # Escape all characters for each entry after the element type so they aren't compiled wrong - e.g. % starting a comment
    escaped_values = map(latex_escaped_string, element['values'])
    file_object.write(f'\\{element["type"]}'+'{'+'}{'.join(escaped_values)+'}\n')

def complile_to_latex(data: list[dict]):
    # Create a copy of the template to write to in order to create the final latex
    shutil.copy('src/template.tex', 'src/tmp.tex')

    with open('src/tmp.tex', 'a') as file:
        # Add all trials, places and visits in order: visits, trials, places
        file.write('\\begin{offers}\n')

        types = ['visit', 'trial', 'place'] # Also the correct ordering
        relevant_elements = [e for e in data if e['type'] in types]
        relevant_elements.sort(key=lambda e: types.index(e['type'])) # Sort in the order the 'types' list is in.

        for element in relevant_elements:
            write_element(file, element)

        file.write('\\end{offers}\n')

        # Add all other points
        relevant_elements = [e for e in data if e['type'] == 'point']
        for element in relevant_elements:
            write_element(file, element)

        # End enumerate and document tags
        file.write('\\end{enumerate}\n\\end{document}')
