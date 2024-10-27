import requests
from flask import Flask, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get-data/<latitude>/<longitude>')
def getData(latitude, longitude):
    # CALL WHATEVER NEEDS TO BE CALLED
    data = {}
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)