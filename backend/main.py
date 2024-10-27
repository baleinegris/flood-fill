import base64
from io import BytesIO
import matplotlib.pyplot as plt
from model import Model
from precip import project
import pandas as pd
import lzma

MODEL_PATH = "models/small.keras"

def _get_expected_floods_year(lat, lon, yr, scenario, model):
    # Initialize the model with the training data
    # Project precipitation data for the given coordinates and scenario
    precip = project(lat, lon, scenario)[yr]
    # Predict floods using the model
    return [model.predict_floods({'lat': [lat], 'lon': [lon], 'precip': [precip]}), precip]

# Function to get expected floods for a given latitude, longitude, year, and scenario
def get_expected_floods(lat, lon, scenario, model):
    # Define the range of years for the prediction
    years = range(2024, 2101)
    expected_floods = {}
    # Get expected floods for each year in the range
    for yr in years:
        expected_floods[yr] = _get_expected_floods_year(lat, lon, yr, scenario, model)
    return expected_floods

# Function to generate and save a plot of expected floods for a given address
def get_plot(address, expected_floods) -> str:
    # Create a plot of expected floods over the years
    plt.figure(figsize=(10, 5))
    plt.plot(expected_floods, marker='o')
    plt.title(f'Expected Floods per Year for {address}')
    plt.xlabel('Year')
    plt.ylabel('Expected Floods')
    plt.grid(True)
    bio = BytesIO()
    plt.savefig(bio, format='png')
    return base64.b64encode(bio.read()).decode('utf-8')

# Function to load training data from a pickle file
def load_data():
    # Load the data from the pickle file
    try:
        df = pd.read_pickle('data/training_data.pkl')
    except:
        df = pd.read_pickle(lzma.open('data/training_data.pkl.xz'))
    return df

if __name__ == '__main__':
    # Load the training data
    df = load_data()
    # Initialize the model with the training data
    model = Model(df)
    model.model.save(MODEL_PATH)
    print(get_expected_floods(50, -119, 'ssp245', model))
