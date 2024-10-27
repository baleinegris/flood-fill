from model import Model
from precip import project
import pandas as pd
import lzma

MODEL_PATH = "models"

# Function to load training data from a pickle file
def load_data():
    # Load the data from the pickle file
    try:
        df = pd.read_pickle('data/training_data.pkl')
    except:
        df = pd.read_pickle(lzma.open('data/training_data.pkl.xz'))
    return df

# Load the training data
df = load_data()
# Initialize the model with the training data
model = Model(df)
model.save(MODEL_PATH)
print(get_expected_floods(50, -119, 'ssp245', model))
