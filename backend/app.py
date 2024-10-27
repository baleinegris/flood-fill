from flask import Flask, request, redirect
from flask_cors import CORS
from main import get_expected_floods, get_plot

app = Flask(__name__)
CORS(app)

@app.route('/get-data?lat=<latitude>&lat=<longitude>&addr=<address>&scenario=<scenario>')
def getData(latitude, longitude, address):
    # CALL WHATEVER NEEDS TO BE CALLED
    print(latitude, longitude, addr)
    (lat, lon, scenario, addr) = [request.args.get(x) for x in ['lat', 'lon', 'scenario', 'addr']]
    expected_floods = get_expected_floods(lat, lon, scenario)
    plot_data = get_plot(address, expected_floods)
    data = {'expected_floods': expected_floods, 'plot': plot_data}
    return data


@app.route('/ping')
def ping():
    return {'ping': 'ping'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)
