import subprocess, shlex, os
from flask import Flask, render_template, request, send_file, Response
from latex.latex_compiler import complile_to_latex

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

# Handles data uploads from the JS frontend
@app.route("/data", methods=["POST"])
def data():
    json = request.get_json()
    print(f'Received JSON: {json}')
    complile_to_latex(json)

    # Compile the latex that compile_to_latex wrote,
    # setting the output directory to src/latex so that the log files do not clog the filesystem.
    p = subprocess.Popen(shlex.split('pdflatex -interaction=nonstopmode -shell-escape -output-directory=src/latex src/latex/tmp.tex'))

    while p.poll() is None: # Wait until the process has finished
        pass

    if p.poll() == 0: # The program exited succesfully
        return Response('', status=201) # Return that the resource was created.
    else:
        return Response('', status=400) # Otherwise, return that it failed (e.g., the input was blank)


# Handles data download, requested by the frontend client.
@app.route("/download")
def download():
    if os.path.exists('src/latex/tmp.pdf'):
        return send_file('latex/tmp.pdf')
    else:
        return 'No PDF has been compiled yet.'

if __name__ == '__main__':
    # TODO: cleanup files so /download doens't download old file
    app.run(port=8080)
