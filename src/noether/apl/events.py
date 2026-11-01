import time
from enum import Enum, auto
from dataclasses import dataclass, field
import sympy as sp

class EventType(Enum):
    """Categorization of epistemic friction encountered during evaluation."""
    PASS = auto()      # Condition met, no action required.
    VETO = auto()      # Hard violation (e.g., evaluation error or dimension mismatch).
    ANOMALY = auto()   # Mathematical patch applied (e.g., Taylor expansion, term dropped).
    CRISIS = auto()    # Accumulated error exceeded paradigm tolerance.

@dataclass(frozen=True)
class EpistemicEvent:
    """Immutable snapshot of a mathematical state evaluated by the APL priority queue."""
    event_type: EventType
    action_name: str
    ast_snapshot: sp.Expr
    rationale: str
    delta_error: float = 0.0
    timestamp: float = field(default_factory=time.time)