from netCDF4 import Dataset
import numpy as np

PRECIP_DATA_DIR = "data/precip"

def project(lat: float, lon: float, year: int, scenario: str = None) -> float:
    """Return the median total precipitation for the given location in the given year.
    If the year is 2015 or before, return the actual recorded precipiation.
    If the year is after 2014, project based on the given SSP scenario.
    If no scenario is given, the year must be before 2015.

    Preconditions:
    - 41.0 <= lat <= 83.5
    - -140.9 <= lon <= 52.0
    - 1950 <= year <= 2100
    - year < 2015 or scenario.lower() in ['ssp126', 'ssp245', 'ssp585']
    """
    assert 41.0 <= lat <= 83.5, "Latitude out of range"
    assert -140.9 <= lon <= -52, "Longitude out of range"
    assert 1950 <= year <= 2100, "Year out of range"
    assert scenario is None or scenario.lower() in ['ssp126', 'ssp245', 'ssp585'], \
            "Invalid scenario"
    assert year < 2015 or scenario is not None, "Must specify scenario for 2015 or after"

    if year < 2015:
        scenario = 'historical'

    filename = f'{PRECIP_DATA_DIR}/{_get_filename(scenario)}'
    nc = Dataset(filename, 'r')
    nc_lat_idx = _find_nearest_idx(nc.variables['lat'][:], lat)
    nc_lon_idx = _find_nearest_idx(nc.variables['lon'][:], lon)
    nc_time_idx = _find_nearest_idx(nc.variables['time'][:], (year - 1950) * 365)

    return float(nc.variables['Precip'][nc_time_idx][nc_lat_idx][nc_lon_idx])


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

    assert len(array) > 0, "_find_nearest_idk called on empty array"

    return np.abs(array - value).argmin()
