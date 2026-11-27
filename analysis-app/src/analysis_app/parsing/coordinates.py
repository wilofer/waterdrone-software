"""Conversion between geographic coordinates (degrees) and local Cartesian coordinates (metres)."""

import numpy as np

EARTH_RADIUS_M = 6_371_000.0


def choose_reference_origin(
    lat_deg: np.ndarray,
    lon_deg: np.ndarray,
) -> tuple[float, float]:
    """Compute the mean latitude and mean longitude in degrees as a reference origin."""
    return (float(np.mean(lat_deg)), float(np.mean(lon_deg)))


def latlon_to_xy(
    lat_deg: np.ndarray,
    lon_deg: np.ndarray,
    ref_origin: tuple[float, float],
) -> tuple[np.ndarray, np.ndarray]:
    """Convert latitude and longitude arrays in degrees to local (x, y) coordinates in metres."""
    lat0_rad = np.radians(ref_origin[0])
    lon0_rad = np.radians(ref_origin[1])
    lat_rad = np.radians(lat_deg)
    lon_rad = np.radians(lon_deg)

    x = EARTH_RADIUS_M * np.cos(lat0_rad) * (lon_rad - lon0_rad)
    y = EARTH_RADIUS_M * (lat_rad - lat0_rad)
    return x, y


def xy_to_latlon(
    x: np.ndarray,
    y: np.ndarray,
    ref_origin: tuple[float, float],
) -> tuple[np.ndarray, np.ndarray]:
    """Convert local (x, y) coordinates in metres back to latitude and longitude in degrees."""
    lat0_rad = np.radians(ref_origin[0])
    lon0_rad = np.radians(ref_origin[1])

    lon_rad = lon0_rad + x / (EARTH_RADIUS_M * np.cos(lat0_rad))
    lat_rad = lat0_rad + y / EARTH_RADIUS_M

    return np.degrees(lat_rad), np.degrees(lon_rad)
