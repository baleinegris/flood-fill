import pandas as pd
import lzma
import pickle
from math import exp

DANGER_HIST_PATH = "data/danger_hist.pkl"

# Function to load training data from a pickle file
def load_training_data():
    # Load the data from the pickle file
    try:
        df = pd.read_pickle('data/training_data.pkl')
    except:
        df = pd.read_pickle(lzma.open('data/training_data.pkl.xz'))
    return df

def build_histogram(df):
    counts = dict(df['floods_per_year'].value_counts())
    counts = {n: counts[n].item() for n in counts}
    with open(DANGER_HIST_PATH, 'wb') as f:
        pickle.dump(counts, f)

def get_danger(num_floods):
    return 1 - exp(-num_floods)
#def get_danger(num_floods):
#    with open(DANGER_HIST_PATH, 'rb') as f:
#        counts = pickle.load(f)
#
#    total_below = sum(counts[n] for n in counts if n <= num_floods)
#    total = sum(counts[n] for n in counts)
#    return total_below / total


if __name__ == '__main__':
    df = load_training_data()
    build_histogram(df)
