import fiona
import pandas as pd
import precip
import pickle
from util import get_elevation

DEFAULT_HISTORICAL_SCENARIO = 'ssp126'  # scenario doesn't matter for years <2015

def get_floods(filename: str) -> dict:
    with fiona.open(filename) as src:
        print(src.schema)
        floods = []
        for feature in src:
            floods.append({'year': feature['properties']['year'], 'lon': feature['geometry']['coordinates'][0], 'lat': feature['geometry']['coordinates'][1]})
    return floods

if __name__ == '__main__':
    # Initialize dataframe with 0 floods
    df = pd.DataFrame(columns=['lat', 'lon', 'elev', 'precip', 'floods_per_year'])

    floods = get_floods('data/floods/historical_flood_events.gpkg')

    for flood in floods:
        lat, lon = get_closest_coords(flood['lat'], flood['lon'])
        elev = get_elevation(lat, lon)
        recorded_precip = precip.project(flood['lat'], flood['lon'], DEFAULT_HISTORICAL_SCENARIO)

        df.loc[['lat'==lat, 'lon'==lon, 'elev'==elev, 'precip'=recorded_precip]] += 1

    df.to_pickle('data/training_data.pkl')
