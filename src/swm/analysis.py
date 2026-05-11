import logging
import esda
import pandas as pd

logger = logging.getLogger(__name__)


def compute_global_morans(gdf, w, variable: str) -> esda.Moran:
    """
    Computes Global Moran's I for a given variable and W object.

    Args:
        gdf:      GeoDataFrame containing the variable.
        w:        A libpysal W object.
        variable: Column name in gdf to analyze.

    Returns:
        An esda.Moran object with .I, .p_sim, and .z_sim attributes.
    """
    logger.info("Computing Global Moran's I — variable: %s", variable)
    y = gdf[variable].values
    return esda.Moran(y, w)


def build_morans_table(gdf, weights_dict: dict, variable: str) -> pd.DataFrame:
    """
    Runs Global Moran's I for each W in weights_dict and returns
    a comparison table as a DataFrame.

    Args:
        gdf:          GeoDataFrame containing the variable.
        weights_dict: Dict mapping W name (str) to libpysal W object.
                      Example: {"Rook": w_rook, "Queen": w_queen}
        variable:     Column name in gdf to analyze.

    Returns:
        A pandas DataFrame with one row per W type.
    """
    logger.info("Building Moran's I comparison table — variable: %s", variable)
    results = []

    for name, w in weights_dict.items():
        mi = compute_global_morans(gdf, w, variable)
        results.append(
            {
                "W Type": name,
                "Moran's I": round(mi.I, 4),
                "p-value": round(mi.p_sim, 4),
                "z-score": round(mi.z_sim, 4),
                "Significant": "yes" if mi.p_sim < 0.05 else "no",
            }
        )

    return pd.DataFrame(results)


def compute_local_morans(gdf, w, variable: str) -> esda.Moran_Local:
    """
    Computes Local Moran's I (LISA) for a given variable and W object.

    Args:
        gdf:      GeoDataFrame containing the variable.
        w:        A libpysal W object.
        variable: Column name in gdf to analyze.

    Returns:
        An esda.Moran_Local object for use in LISA cluster maps.
    """
    logger.info("Computing Local Moran's I — variable: %s", variable)
    y = gdf[variable].values
    return esda.Moran_Local(y, w)
