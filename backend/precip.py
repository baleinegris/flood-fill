from typing import Dict, List, Tuple

from netCDF4 import Dataset
import xarray
import numpy as np

PRECIP_DATA_DIR = "data/precip"

def get_dataframe() -> List[Tuple[float, float]]:
    filename = f'{PRECIP_DATA_DIR}/{_get_filename("historical")}'
    xr = xarray.open_dataset(filename)
    df = xr.to_dataframe()
    df.drop('spatial_ref', axis=1, inplace=True)
    df.reset_index(inplace=True)  # convert MultiIndex to columns
    df['year'] = [t.year for t in df['time']]
    df.drop('time', axis=1, inplace=True)
    df.rename(columns={'Precip': 'precip'}, inplace=True)
    return df


def project(lat: float, lon: float, scenario: str) -> Dict[int, float]:
    """Return the median total precipitation for the given location for the years 1950-2100.
    Combines historical data and predictions given by the scenario.
    Return a mapping from year to median total precipitation.

    Preconditions:
    - 41.0 <= lat <= 83.5
    - -140.9 <= lon <= 52.0
    - scenario.lower() in ['ssp126', 'ssp245', 'ssp585']
    """
    if not 41.0 <= lat <= 83.5: raise ValueError("Latitude out of range")
    if not -140.9 <= lon <= -52: raise ValueError("Longitude out of range")
    assert scenario.lower() in ['ssp126', 'ssp245', 'ssp585'], "Invalid scenario"

    historical = _project_from_dataset(lat, lon, 'historical')
    projected = _project_from_dataset(lat, lon, scenario)

    result = historical.copy()
    result.update(projected)

    return result


def _project_from_dataset(lat: float, lon: float, scenario: str) -> Dict[int, float]:
    """Return the median total precipitation for the given location for all years in the dataset.
    If the scenario is 'historical', return actual recorded values.
    Otherwise, return the predictions given by the scenario.
    Return a mapping from year to median total precipitation.

    Preconditions:
    - 41.0 <= lat <= 83.5
    - -140.9 <= lon <= 52.0
    - scenario.lower() in ['ssp126', 'ssp245', 'ssp585', 'historical']
    """
    if not 41.0 <= lat <= 83.5: raise ValueError("Latitude out of range")
    if not -140.9 <= lon <= -52: raise ValueError("Longitude out of range")
    assert scenario.lower() in ['ssp126', 'ssp245', 'ssp585', 'historical'], "Invalid scenario"

    filename = f'{PRECIP_DATA_DIR}/{_get_filename(scenario)}'
    nc = Dataset(filename, 'r')
    nc_lat_idx = _find_nearest_idx(nc.variables['lat'][:], lat)
    nc_lon_idx = _find_nearest_idx(nc.variables['lon'][:], lon)

    times = nc.variables['time']
    precips = nc.variables['Precip'][:, nc_lat_idx, nc_lon_idx]

    if any(x is np.ma.masked for x in precips): raise ValueError('Coordinates missing some data')

    return {int(np.round(times[i] / 365 + 1950, 0)): precips[i] for i in range(len(times))}


def _get_filename(scenario: str) -> str:
    """Return the filename of the netCFF file for the given scenario, or "historical".

    Preconditions:
    - scenario.lower() in ['ssp126', 'ssp245', 'ssp585', 'historical']
    """

    if scenario == 'historical':
        return '1950-2014_ECCC_CanDCSU6_Precip-Pct50_Sfc_LatLon0.86_P1Y.nc'
    else:
        return f'2015-2100_ECCC_CanDCSU6-{scenario.upper()}_Precip-Pct50_Sfc_LatLon0.86_P1Y.nc'


def _find_nearest_idx(array: np.array, value: float) -> float:
    """Return the index of the closest value in array to the given value

    Preconditions:
    - len(array) > 0
    """

    assert len(array) > 0, "_find_nearest_idx called on empty array"

    return np.abs(array - value).argmin()
