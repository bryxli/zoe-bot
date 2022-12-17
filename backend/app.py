from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/listofgames')
def master_output():
    #db = connect_db()
    #cursor = db.cursor()
    #cursor.execute("SELECT * FROM recent ORDER BY RAND()")
    #listofgames = cursor.fetchall()[:11]
    #data = {
    #    "games": 
    #    listofgames
    #}
    #cursor.close()
    #return jsonify(data)
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0')