import requests
import os
import base64
from io import BytesIO

import matplotlib.pyplot as plt

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def get_elevation(lat, lon):
    api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
    url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={lat}%2C{lon}&key={GOOGLE_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0].get('elevation')
    return None

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
    plt.grid(True)
    bio = BytesIO()
    plt.savefig(bio, format='png')
    bio.seek(0)
    return base64.b64encode(bio.read()).decode('utf-8')
