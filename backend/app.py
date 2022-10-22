from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/data')
def master_output():
    listofgames = ["output1","output2"]
    data = {
        "games": listofgames
    }
    return jsonify(data)