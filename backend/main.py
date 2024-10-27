from model import Model
from precip import project
import pandas as pd
import lzma

MODEL_PATH = "models/small.keras"

# Function to get expected floods for a given latitude, longitude, year, and scenario
def get_expected_floods(lat, lon, scenario, model):
    # Define the range of years for the prediction
    years = range(2024, 2034)
    expected_floods = {}

    precips = project(lat, lon, scenario)
    predictions = model.predict_floods(lat, lon, [precips[yr] for yr in years])

    for i, yr in enumerate(years):
        expected_floods[yr] = [predictions[i], precips[yr]]
    return expected_floods

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
