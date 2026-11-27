"""CSV file reader and parser converting waterdrone logs into Sample containers."""

from typing import Optional
import numpy as np
import pandas as pd

from analysis_app.core import (
    COL_DEPTH,
    COL_LATITUDE,
    COL_LONGITUDE,
    COL_TIMESTAMP,
    Sample,
)
from .coordinates import choose_reference_origin, latlon_to_xy


def read_csv(path: str) -> tuple[list[str], np.ndarray]:
    """Read a waterdrone CSV file into a stripped header list and a 2D float64 numpy array."""
    df = pd.read_csv(path)
    header = [col.strip() for col in df.columns]
    table = df.to_numpy(dtype=np.float64)
    return header, table


def split_columns(header: list[str]) -> tuple[dict[str, int], dict[str, int]]:
    """Map fixed column names and parameter column names to their indices in the header."""
    fixed_names = {COL_TIMESTAMP, COL_LATITUDE, COL_LONGITUDE, COL_DEPTH}
    fixed_idx: dict[str, int] = {}
    param_idx: dict[str, int] = {}

    for idx, name in enumerate(header):
        if name in fixed_names:
            fixed_idx[name] = idx
        else:
            param_idx[name] = idx

    return fixed_idx, param_idx


def build_sample(
    table: np.ndarray,
    fixed_idx: dict[str, int],
    param_idx: dict[str, int],
    ref_origin: tuple[float, float],
) -> Sample:
    """Build an immutable Sample container from a 2D numeric table and column index maps."""
    t = table[:, fixed_idx[COL_TIMESTAMP]].astype(np.int64)
    lat_deg = table[:, fixed_idx[COL_LATITUDE]]
    lon_deg = table[:, fixed_idx[COL_LONGITUDE]]
    x, y = latlon_to_xy(lat_deg, lon_deg, ref_origin)

    depth: Optional[np.ndarray] = None
    if COL_DEPTH in fixed_idx:
        depth = table[:, fixed_idx[COL_DEPTH]].copy()

    values: dict[str, np.ndarray] = {
        name: table[:, idx].copy() for name, idx in param_idx.items()
    }

    return Sample(
        t=t,
        x=x,
        y=y,
        depth=depth,
        values=values,
        ref_origin=ref_origin,
    )


def parse_csv(
    path: str,
    ref_origin: Optional[tuple[float, float]] = None,
) -> Sample:
    """Parse a waterdrone CSV file into a Sample using a given or computed reference origin."""
    header, table = read_csv(path)
    fixed_idx, param_idx = split_columns(header)

    if ref_origin is None:
        lat_deg = table[:, fixed_idx[COL_LATITUDE]]
        lon_deg = table[:, fixed_idx[COL_LONGITUDE]]
        ref_origin = choose_reference_origin(lat_deg, lon_deg)

    return build_sample(table, fixed_idx, param_idx, ref_origin)
