from __future__ import annotations
from typing import Tuple


try:
    from pyproj import Geod

    geod = Geod(ellps="WGS84")
except ImportError:

    class Geod: ...

    geod = None


def get_bounding_box(
    lat: float, lon: float, meters: float
) -> Tuple[float, float, float, float]:
    if geod is None:
        return _approx_get_bounding_box(lat, lon, meters)
    else:
        return _geod_get_bounding_box(geod, lat, lon, meters)


def _geod_get_bounding_box(
    geod: Geod, lat: float, lon: float, meters: float
) -> Tuple[float, float, float, float]:
    lon_top_left, lat_top_left, _ = geod.fwd(lon, lat, 315, meters)
    lon_bottom_right, lat_bottom_right, _ = geod.fwd(lon, lat, 135, meters)
    return lat_top_left, lon_top_left, lat_bottom_right, lon_bottom_right


KM_PER_DEGREE_ON_EARTH = 111.0


def _approx_get_bounding_box(
    lat: float, lon: float, meters: float
) -> Tuple[float, float, float, float]:
    lat_delta = meters / (KM_PER_DEGREE_ON_EARTH * 1000)
    lon_delta = meters / (KM_PER_DEGREE_ON_EARTH * 1000)
    return lat - lat_delta, lon - lon_delta, lat + lat_delta, lon + lon_delta
