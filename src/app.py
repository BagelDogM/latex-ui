import os
from flask import Flask, render_template, request, send_file
from latex.latex_compiler import complile_to_latex

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

# Handles data uploads from the JS frontend
@app.route("/data", methods=["POST"])
def data():
    json = request.get_json()
    if json != []:
        complile_to_latex(json)

        # Open a subshell that is in the latex/ directory so that all the log files end up there and aren't a nuisance.
        # Then run pdflatex tmp.tex to generate the PDF.
        # Direct to > null so that terminal output isn't spammed.
        os.system('(cd src/latex && pdflatex tmp.tex > null)')
    print(f'Received JSON: {json}')

    return '' # Dummy

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
