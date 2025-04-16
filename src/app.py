import subprocess, shlex, os, json
from flask import Flask, render_template, request, send_file, Response
from latex.latex_compiler import complile_to_latex

from backend import assign_element_properties
from ui import build_elements
element_names = build_elements()

config = json.load(open("cfg/config.json"))
# Determine where final document will be location
document_location = ''
if config['document']['document-location']: document_location = config['document']['document-location']
else: document_location = config['document']['write-location']

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html', element_names=element_names)

# Handles data uploads from the JS frontend
@app.route("/data", methods=["POST"])
def data():
    json = request.get_json()
    print(f'Received JSON: {json}')
    json = assign_element_properties(json)
    print(f'Edited JSON to: {json}')
    complile_to_latex(json)

    # Compile the latex that compile_to_latex wrote,
    # setting the output directory to src/latex so that the log files do not clog the filesystem.
    p = subprocess.Popen(shlex.split(config['document']['compilation-command']))

    while (code:=p.poll()) is None: # Wait until the process has finished
        pass

    if p.poll() == 0: # The program exited succesfully
        return Response('Resouce created.', status=201) # Return that the resource was created.
    else:
        return Response(f'PDF creation failed due to pdflatex error. Error code: {code}', status=400) # Otherwise, return that it failed (e.g., the input was blank)


# Handles data download, requested by the frontend client.
@app.route("/download")
def download():
    if os.path.exists(document_location):
        return send_file(document_location.replace('src/', ''))
    else:
        return 'No PDF has been compiled yet.'

if __name__ == '__main__':
    # TODO: cleanup files so /download doens't download old file
    app.run(port=8080)
