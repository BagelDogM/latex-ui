import subprocess, shlex, os, json
from flask import Flask, render_template, request, send_file, Response
from compile.compiler import complile

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

    complile(json) # Invoke compilation layer

    # Compile the code that the compile() function wrote,
    if (ccom := config['document'].get('compilation-command')):
        p = subprocess.Popen(shlex.split(ccom))

        while (code:=p.poll()) is None: # Wait until the process has finished
            pass

        if p.poll() == 0: # The program exited succesfully
            return Response('Resouce created.', status=201) # No error, so successful creation
        else:
            return Response(f'File creation failed due to compilation error. Error code: {code}', status=400) # Otherwise, return that it failed (e.g., the input was blank)
    else:
        return Response('Resouce created.', status=201)

# Handles data download, requested by the frontend client.
@app.route("/download")
def download():
    if os.path.exists(document_location):
        return send_file(document_location.replace('src/', '')) # Remove src because this is in a different context. TODO: make this better
    else:
        return 'No document has been compiled yet.'

if __name__ == '__main__':
    app.run(port=8080)
