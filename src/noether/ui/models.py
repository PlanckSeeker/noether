import sys
import sympy as sp
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from ..apl.events import EpistemicEvent, EventType


class EpistemicTimelineModel(QAbstractListModel):
    """
    Bridges the EpistemicEvent data stream into PySide6 item views.
    Provides the formatted string for display and the raw event for the AST viewport.
    """
    # Custom role to retrieve the raw dataclass from the Qt view index
    EventRole = Qt.ItemDataRole.UserRole + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self._events: list[EpistemicEvent] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._events)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._events)):
            return None

        event = self._events[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            # The text rendered in the timeline list
            return f"[{event.timestamp:.3f}] {event.event_type.name} - {event.action_name}"
        elif role == self.EventRole:
            # The raw dataclass passed to the AST renderer when clicked
            return event

        return None

    def add_event(self, event: EpistemicEvent) -> None:
        """Safely injects a new event and notifies attached UI views to update."""
        self.beginInsertRows(QModelIndex(), len(self._events), len(self._events))
        self._events.append(event)
        self.endInsertRows()


# --- Deterministic Verification Check ---
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    # A QApplication instance is required before instantiating any QObjects
    app = QApplication.instance() or QApplication(sys.argv)

    model = EpistemicTimelineModel()
    test_event = EpistemicEvent(
        event_type=EventType.ANOMALY,
        action_name="Asymptotic Drop",
        ast_snapshot=sp.Symbol('v_obs'),
        rationale="Term dropped."
    )

    model.add_event(test_event)

    # Verify Qt model indices and data retrieval
    assert model.rowCount() == 1, "Model row count failed to update after injection."
    idx = model.index(0, 0)

    display_text = model.data(idx, Qt.ItemDataRole.DisplayRole)
    assert "ANOMALY - Asymptotic Drop" in display_text, f"Display string formatting failed: {display_text}"

    raw_event = model.data(idx, EpistemicTimelineModel.EventRole)
    assert raw_event is test_event, "Failed to retrieve the exact EpistemicEvent pointer."