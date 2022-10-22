import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("../database/database.db")

@app.route('/data')
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