"""Core data containers and CSV column name constants."""

from typing import NamedTuple, Optional
import numpy as np

COL_TIMESTAMP = "TIMESTAMP"
COL_LATITUDE = "LATITUDE"
COL_LONGITUDE = "LONGITUDE"
COL_DEPTH = "Z"


class Sample(NamedTuple):
    """Immutable container holding a single parsed waterdrone CSV sample."""

    t: np.ndarray  # (n,) int64 timestamps
    x: np.ndarray  # (n,) float64, metres
    y: np.ndarray  # (n,) float64, metres
    depth: Optional[np.ndarray]  # (n,) float64, or None
    values: dict[str, np.ndarray]  # name -> (n,) float64
    ref_origin: tuple[float, float]  # (lat0, lon0), degrees