import requests
import os

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


