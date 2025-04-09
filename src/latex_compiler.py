import shutil

def complile_to_latex(data: list[dict]):
    # Create a copy of the template to write to in order to create the final latex
    shutil.copy('src/template.txt', 'src/tmp.txt')

    with open('src/tmp.txt', 'a') as file:
        # Add all trials, places and visits in order: visits, trials, places
        file.write('\\begin{offers}\n')

        types = ['visit', 'trial', 'place'] # Also the correct ordering
        relevant_elements = [e for e in data if e['type'] in types]
        relevant_elements.sort(key=lambda e: types.index(e['type'])) # Sort in the order the 'types' list is in.

        for element in relevant_elements:
            file.write(f'\\{element["type"]}'+'{'+'}{'.join(element['values'])+'}\n')

        file.write('\\end{offers}\n')

        # Add all other points
        relevant_elements = [e for e in data if e['type'] == 'point']
        for element in relevant_elements:
            file.write(f'\\{element["type"]}'+'{'+'}{'.join(element['values'])+'}\n')

        # End enumerate and document tags
        file.write('\\end{enumerate}\n\\end{document}')
