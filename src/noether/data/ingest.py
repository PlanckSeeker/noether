import pandas as pd
import numpy as np
import sympy as sp
from typing import Mapping, Optional

try:
    from astropy.table import Table  # type: ignore
except ImportError:
    Table = None

# Simulating relative imports for the core context module
try:
    from ..core.context import ParadigmContext
except ImportError:
    from noether.core.context import ParadigmContext


def bind_csv(filepath: str, mapping: Mapping[str, sp.Symbol]) -> pd.DataFrame:
    """Ingests a CSV and maps its columns to Noether symbols."""
    df = pd.read_csv(filepath)
    missing = [col for col in mapping.keys() if col not in df.columns]
    if missing:
        raise ValueError(f"CSV missing required mapped columns: {missing}")
    return df


def bind_fits(filepath: str, hdu_index: int = 1) -> pd.DataFrame:
    """Ingests astronomical FITS/VOTable survey data into standard DataFrames."""
    if Table is None:
        raise ImportError("astropy is required for FITS ingestion.")
    astropy_table = Table.read(filepath, hdu=hdu_index)
    return astropy_table.to_pandas()


def validate_ingested_bounds(df: pd.DataFrame, ctx: ParadigmContext, tolerance_margin: float = 2.0) -> dict[str, bool]:
    """
    Cross-references ingested DataFrame columns against the ParadigmContext's
    defined Fermi magnitude bounds. Emits warnings or validation results if empirical
    values severely violate expected paradigm scales.

    Args:
        df: The pandas DataFrame containing ingested observational data.
        ctx: The ParadigmContext containing expected variable bounds {var_name: (min, max)}.
        tolerance_margin: Multiplier allowed beyond bounds before flagging an anomaly.

    Returns:
        A dictionary mapping variable names to boolean compliance status.
    """
    validation_results = {}

    for var_name, (min_bound, max_bound) in ctx.bounds.items():
        if var_name in df.columns:
            series = df[var_name].dropna()
            if series.empty:
                validation_results[var_name] = True
                continue

            observed_min = float(series.min())
            observed_max = float(series.max())

            # Check if values fall within allowable scale bounds with tolerance margin
            is_compliant = (
                    observed_min >= (min_bound / tolerance_margin) and
                    observed_max <= (max_bound * tolerance_margin)
            )
            validation_results[var_name] = is_compliant
        else:
            # If the bounded variable is not present in the empirical dataset, skip validation
            pass

    return validation_results