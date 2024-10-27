import fiona
import pandas as pd
import precip
import pickle
from util import get_elevation

PICKLE_PATH = 'data/training_data.pkl'
MAX_FLOODS = None  # to limit computation time. set to None to process whole dataset

def get_floods(filename: str) -> dict:
    with fiona.open(filename) as src:
        #print(src.schema)
        floods = []
        for feature in src:
            floods.append({'year': feature['properties']['year'], 'lon': feature['geometry']['coordinates'][0], 'lat': feature['geometry']['coordinates'][1]})
    return floods


def _get_closest_coords(lat, lon) -> pd.DataFrame:
    return (abs(df['lat']-lat) < 0.2) & (abs(df['lon']-lon) < 0.2)


if __name__ == '__main__':
    # Initialize dataframe with 0 floods
    print("Initializing dataframe from CanDCSU6 dataset")
    df = precip.get_dataframe()

    # df['elev'] = get_elevation(df['lat'], df['lon'])

    df['floods_per_year'] = 0

    print("Reading flood data")
    floods = get_floods('data/floods/historical_flood_events.gpkg')

    if MAX_FLOODS is not None:
        floods = floods[:MAX_FLOODS]

    print("Counting floods")
    for i, flood in enumerate(floods):
        print(f'\r{i}/{len(floods)}', end='')
        flooded_areas = _get_closest_coords(flood['lat'], flood['lon']) 
        df.loc[flooded_areas & (df['year'] == flood['year']), ['floods_per_year']] += 1
    print(f'\r{len(floods)}/{len(floods)}') # finalize count display

    # Remove data that won't be used in training
    df.dropna(inplace=True)
    df.drop('year', axis=1, inplace=True)

    print(f"Saving to {PICKLE_PATH}")
    df.to_pickle(PICKLE_PATH)

