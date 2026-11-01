from .core.dimensions import (
    Q8Lattice,
    Length,
    Mass,
    Time,
    Current,
    Temperature,
    Amount,
    LuminousIntensity,
    SolidAngle,
)
from .core.context import (
    ParadigmContext,
    NEWTONIAN_ASTROPHYSICS,
    WavePropagationContext,
    HIGH_FREQUENCY_WAVE_PARADIGM,
    ParadigmRegistry,
)
from .core.algebra import SparseMultivector
from .apl.events import EventType, EpistemicEvent
from .apl.patches import Patch, taylor_patch, asymptotic_drop_patch
from .apl.priority_queue import EpistemicAPL
from .data.ingest import bind_csv, bind_fits, validate_ingested_bounds

__version__ = "0.1.0"

__all__ = [
    "Q8Lattice",
    "Length",
    "Mass",
    "Time",
    "Current",
    "Temperature",
    "Amount",
    "LuminousIntensity",
    "SolidAngle",
    "ParadigmContext",
    "NEWTONIAN_ASTROPHYSICS",
    "WavePropagationContext",
    "HIGH_FREQUENCY_WAVE_PARADIGM",
    "ParadigmRegistry",
    "SparseMultivector",
    "EventType",
    "EpistemicEvent",
    "Patch",
    "taylor_patch",
    "asymptotic_drop_patch",
    "EpistemicAPL",
    "bind_csv",
    "bind_fits",
    "validate_ingested_bounds",
]