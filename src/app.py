from flask import Flask, render_template, request
from latex_compiler import complile_to_latex

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/data", methods=["POST"])
def data():
    json = request.get_json()
    complile_to_latex(json)
    print(f'Received JSON: {json}')

    return '' # Dummy

if __name__ == '__main__':
    app.run(port=8080)
