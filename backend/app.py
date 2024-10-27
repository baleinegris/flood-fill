from flask import Flask, request, redirect
from flask_cors import CORS
from train import load_data, MODEL_PATH
from model import Model
from util import get_plot, get_expected_floods
import tensorflow as tf

app = Flask(__name__)
CORS(app)

model = Model()
model.load(MODEL_PATH)

@app.route('/get-data',  methods = ['POST'])
def getData():
    lat, lon, scenario, addr = [request.json[x] for x in ['lat', 'lon', 'scenario', 'addr']]
    expected_floods = get_expected_floods(lat, lon, scenario, model)
    plot_data = get_plot(addr, expected_floods)
    data = {'expected_floods': expected_floods, 'plot': plot_data}
    print(data)
    return data


@app.route('/ping')
def ping():
    return {'ping': 'ping'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)
