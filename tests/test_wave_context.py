import pytest
from noether.core.context import (
    ParadigmContext,
    WavePropagationContext,
    ParadigmRegistry,
    HIGH_FREQUENCY_WAVE_PARADIGM,
)


def test_paradigm_registry_storage_and_retrieval() -> None:
    """Verify that the ParadigmRegistry correctly registers, retrieves, and lists contexts."""
    # 1. Verify pre-registered wave paradigm
    retrieved_wave = ParadigmRegistry.get("High-Frequency Wave Optics")
    assert retrieved_wave is not None, "Failed to retrieve pre-registered wave paradigm."
    assert isinstance(retrieved_wave, WavePropagationContext), "Retrieved context must be a WavePropagationContext."
    assert retrieved_wave.is_paraxial("theta") is True, "Paraxial check failed."
    assert retrieved_wave.dispersion_significance("omega", "omega_p") > 1000.0, "Dispersion scale ratio failed."

    # 2. Register a custom dynamic paradigm
    custom_ctx = ParadigmContext(
        name="Quantum Mechanics Sandbox",
        bounds={"hbar": (1.054e-34, 1.054e-34), "mass": (9.109e-31, 9.109e-31)},
        crisis_tolerance=0.10
    )
    ParadigmRegistry.register(custom_ctx)

    # 3. Retrieve and verify the custom paradigm
    retrieved_custom = ParadigmRegistry.get("Quantum Mechanics Sandbox")
    assert retrieved_custom is not None, "Failed to retrieve newly registered custom paradigm."
    assert retrieved_custom.crisis_tolerance == 0.10, "Custom crisis tolerance mismatch."

    # 4. Verify list_paradigms includes both standard and custom contexts
    all_paradigms = ParadigmRegistry.list_paradigms()
    assert "High-Frequency Wave Optics" in all_paradigms
    assert "Quantum Mechanics Sandbox" in all_paradigms
    assert "Newtonian Astrophysics" in all_paradigms


# --- Deterministic Verification Check ---
if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(["-v", __file__]))