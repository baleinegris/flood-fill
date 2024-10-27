import requests
import os
import base64
from io import BytesIO

import matplotlib.pyplot as plt

# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# def get_elevation(lat, lon):
#     api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
#     url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={lat}%2C{lon}&key={
#     GOOGLE_API_KEY}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         results = response.json().get('results')
#         if results:
#             return results[0].get('elevation')
#     return None

# Function to generate and save a plot of expected floods for a given address
def get_plot(address, expected_floods) -> str:
    # Create a plot of expected floods over the years
    plt.figure(figsize=(10, 5))
    x = [yr for yr in expected_floods]
    y = [expected_floods[yr][0] for yr in expected_floods]
    plt.plot(x, y, marker='o')
    plt.title(f'Expected Floods per Year for {address}')
    plt.xlabel('Year')
    plt.ylabel('Expected Floods')
    plt.ylim(0, max(y) * 1.3)
    plt.grid(True)
    bio = BytesIO()
    plt.savefig(bio, format='png')
    bio.seek(0)
    return base64.b64encode(bio.read()).decode('utf-8')

# Function to get expected floods for a given latitude, longitude, year, and scenario
def get_expected_floods(lat, lon, scenario, model):
    # Define the range of years for the prediction
    years = range(2024, 2100 + 1)
    expected_floods = {}

    precips = project(lat, lon, scenario)
    predictions = model.predict_floods(lat, lon, [precips[yr] for yr in years])

    for i, yr in enumerate(years):
        expected_floods[yr] = [predictions[i][0].item(), precips[yr].item()]
    return expected_floods
