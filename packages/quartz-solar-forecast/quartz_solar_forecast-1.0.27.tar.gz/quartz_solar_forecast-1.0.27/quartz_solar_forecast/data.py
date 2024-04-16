""" Function to get NWP data and create fake PV dataset"""
import json
import ssl
from datetime import datetime
import os  # Add import for os module

import numpy as np
import pandas as pd
import requests
import xarray as xr

from quartz_solar_forecast.pydantic_models import PVSite
from quartz_solar_forecast.inverters.enphase import get_enphase_data # Added import for get_enphase_data from /inverters/enphase.py

ssl._create_default_https_context = ssl._create_unverified_context

# Load environment variables from .env file
from dotenv import load_dotenv

# Assigning secrets from the .env file
ENPHASE_API_KEY = os.getenv('ENPHASE_API_KEY')
ENPHASE_USER_ID = os.getenv('ENPHASE_USER_ID')

def get_nwp(site: PVSite, ts: datetime, nwp_source: str = "icon") -> xr.Dataset:
    """
    Get GFS NWP data for a point time space and time

    :param site: the PV site
    :param ts: the timestamp for when you want the forecast for
    :param nwp_source: the nwp data source. Either "gfs" or "icon". Defaults to "icon"
    :return: nwp forecast in xarray
    """

    variables = [
        "visibility",
        "windspeed_10m",
        "temperature_2m",
        "precipitation",
        "shortwave_radiation",
        "direct_radiation",
        "cloudcover_low",
        "cloudcover_mid",
        "cloudcover_high",
    ]

    start = ts.date()
    end = start + pd.Timedelta(days=7)

    # Getting NWP, from OPEN METEO
    url_nwp_source = None
    if nwp_source == "icon":
        url_nwp_source = "dwd-icon"
    elif nwp_source == "gfs":
        url_nwp_source = "gfs"
    else:
        raise Exception(f'Source ({nwp_source}) must be either "icon" or "gfs"')

    # Pull data from the nwp_source provided 
    url = (
        f"https://api.open-meteo.com/v1/{url_nwp_source}?"
        f"latitude={site.latitude}&longitude={site.longitude}"
        f"&hourly={','.join(variables)}"
        f"&start_date={start}&end_date={end}"
    )
    r = requests.get(url)
    d = json.loads(r.text)

    # If the nwp_source is ICON, get visibility data from GFS as its not available for icon on Open Meteo
    if nwp_source == "icon":
        url = (
            f"https://api.open-meteo.com/v1/gfs?"
            f"latitude={site.latitude}&longitude={site.longitude}"
            f"&hourly=visibility"
            f"&start_date={start}&end_date={end}"
        )
        r_gfs = requests.get(url)
        d_gfs = json.loads(r_gfs.text)

        # extract visibility data from gfs reponse
        gfs_visibility_data = d_gfs["hourly"]["visibility"]

        # add visibility to the icon reponse to make a complete json file 
        d["hourly"]["visibility"] = gfs_visibility_data

    # convert data into xarray
    df = pd.DataFrame(d["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    df = df.rename(
        columns={
            "visibility": "vis",
            "windspeed_10m": "si10",
            "temperature_2m": "t",
            "precipitation": "prate",
            "shortwave_radiation": "dswrf",
            "direct_radiation": "dlwrf",
            "cloudcover_low": "lcc",
            "cloudcover_mid": "mcc",
            "cloudcover_high": "hcc",
        }
    )
    df = df.set_index("time")
    data_xr = format_nwp_data(df, nwp_source, site)

    return data_xr


def format_nwp_data(df: pd.DataFrame, nwp_source:str, site: PVSite):
    data_xr = xr.DataArray(
        data=df.values,
        dims=["step", "variable"],
        coords=dict(
            step=("step", df.index - df.index[0]),
            variable=df.columns,
        ),
    )
    data_xr = data_xr.to_dataset(name=nwp_source)
    data_xr = data_xr.assign_coords(
        {"x": [site.longitude], "y": [site.latitude], "time": [df.index[0]]}
    )
    return data_xr

def make_pv_data(site: PVSite, ts: pd.Timestamp) -> xr.Dataset:
    """
    Make PV data by combining Enphase live data and fake PV data

    Later we could add PV history here

    :param site: the PV site
    :param ts: the timestamp of the site
    :return: The combined PV dataset in xarray form
    """

    # Check if the site has an inverter and use_enphase_data flag accordingly
    use_enphase_data = site.is_inverter

    if use_enphase_data:
        # Fetch live Enphase data and store it in live_generation_wh
        live_generation_wh = get_enphase_data(ENPHASE_USER_ID, ENPHASE_API_KEY)
    else:
        live_generation_wh = np.nan  # Default value if not using live Enphase data

    # Combine live Enphase data with fake PV data, this is where we could add history of a pv system
    generation_wh = [[live_generation_wh]]
    lon = [site.longitude]
    lat = [site.latitude]
    timestamp = [ts]
    pv_id = [1]

    da = xr.DataArray(
        data=generation_wh,
        dims=["pv_id", "timestamp"],
        coords=dict(
            longitude=(["pv_id"], lon),
            latitude=(["pv_id"], lat),
            timestamp=timestamp,
            pv_id=pv_id,
            kwp=(["pv_id"], [site.capacity_kwp]),
            tilt=(["pv_id"], [site.tilt]),
            orientation=(["pv_id"], [site.orientation]),
        ),
    )
    da = da.to_dataset(name="generation_wh")

    return da