from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/data", methods=["POST"])
def data():
    json = request.get_json()
    print(f'Received JSON: {json}')
    return '' # Dummy
if __name__ == '__main__':
    app.run()
