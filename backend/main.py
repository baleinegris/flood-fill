import matplotlib.pyplot as plt
import numpy as np
from model import Model
import requests
import os
from dotenv import load_dotenv
from precip import project
import fiona

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

sample_data = {
    'latitude': np.random.uniform(-90, 90, 1000),
    'longitude': np.random.uniform(-180, 180, 1000),
    'elevation': np.random.uniform(0, 5000, 1000),
    'precipitation': np.random.uniform(0, 500, 1000),
    'floods_per_year': np.random.poisson(2, 1000)
}

def get_expected_floods(address, yr, scenario):
    lat, lon = get_lat_long(address)
    elev = get_elevation(lat, lon)
    precip = project(lat, lon, scenario)[yr]
    return model.predict_floods({'latitude': [lat], 'longitude': [lon], 'elevation': [elev], 'precipitation': [precip]})

def get_plot(address):
    years = range(2024, 2101)
    expected_floods = [get_expected_floods(address, yr) for yr in years]

    plt.figure(figsize=(10, 5))
    plt.plot(years, expected_floods, marker='o')
    plt.title(f'Expected Floods per Year for {address}')
    plt.xlabel('Year')
    plt.ylabel('Expected Floods')
    plt.grid(True)
    plt.savefig("expected_floods.png")

def get_elevation(lat, lon):
    api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
    url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={lat}%2C{lon}&key={GOOGLE_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0].get('elevation')
    return None

def get_lat_long(address):
    return 50, -119

if __name__ == '__main__':
    # model = Model(sample_data)
    # get_expected_floods('Vancouver', 2025, 'ssp126')
    with fiona.open('historical_flood_events.gpkg') as src:
        print(src.schema)
        for feature in src:
            print(feature['properties'])
            print(feature['geometry']['coordinates'])