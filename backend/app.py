import mysql.connector
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def connect_db():
    return mysql.connector.connect(host = 'data', user = 'root', password = '123', port = 3306)

@app.route('/listofgames')
def master_output():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM recent ORDER BY RANDOM()")
    listofgames = cursor.fetchall()[:11]
    data = {
        "games": 
        listofgames
    }
    cursor.close()
    return jsonify(data)

@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)