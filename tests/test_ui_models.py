import pytest
import sympy as sp
from PySide6.QtCore import Qt
from noether.ui.models import EpistemicTimelineModel
from noether.apl.events import EpistemicEvent, EventType


def test_timeline_model_initialization() -> None:
    """Verify the model initializes with zero rows."""
    model = EpistemicTimelineModel()
    assert model.rowCount() == 0, "New timeline model must start empty."


def test_timeline_model_add_event(qtbot) -> None:
    """Verify adding events updates the model and triggers UI row insertion signals."""
    model = EpistemicTimelineModel()
    event = EpistemicEvent(
        event_type=EventType.ANOMALY,
        action_name="Test Patch",
        ast_snapshot=sp.Symbol('x'),
        rationale="Testing model integration.",
        delta_error=0.1
    )

    with qtbot.waitSignal(model.rowsInserted, timeout=1000):
        model.add_event(event)

    assert model.rowCount() == 1, "Model row count failed to update."
    idx = model.index(0, 0)
    raw_event = model.data(idx, EpistemicTimelineModel.EventRole)
    assert raw_event is event, "Model failed to return the exact raw EpistemicEvent pointer."