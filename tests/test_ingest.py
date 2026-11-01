import pytest
import tempfile
import os
import pandas as pd
import sympy as sp
from noether.core.context import ParadigmContext
from noether.data.ingest import bind_csv, validate_ingested_bounds

def test_bind_csv_and_validation() -> None:
    """Verify CSV binding and automated paradigm boundary validation."""
    v_obs = sp.Symbol('v_obs')
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as tmp:
        tmp.write("v_obs,radius\n220000,10\n230000,12")
        tmp_name = tmp.name

    try:
        df = bind_csv(tmp_name, {"v_obs": v_obs})
        assert "v_obs" in df.columns, "CSV binding failed to locate mapped column."
        assert len(df) == 2, "Row count mismatch."

        ctx = ParadigmContext(
            name="Newtonian Astrophysics",
            bounds={"v_obs": (1e3, 3e5)}
        )
        results = validate_ingested_bounds(df, ctx)
        assert results["v_obs"] is True, "Ingested v_obs values should comply with paradigm bounds."
    finally:
        os.remove(tmp_name)