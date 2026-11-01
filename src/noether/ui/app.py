import sys
import sympy as sp
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QListView, QSplitter
)
from PySide6.QtCore import Qt, QModelIndex

# Simulating relative imports for the console environment structure
try:
    from .models import EpistemicTimelineModel
    from .delegates import EpistemicTimelineDelegate
    from .widgets.viewport import LaTeXViewport
    from .widgets.meter import CrisisMeter
    from ..apl.events import EpistemicEvent, EventType
except ImportError:
    from noether.ui.models import EpistemicTimelineModel
    from noether.ui.delegates import EpistemicTimelineDelegate
    from noether.ui.widgets.viewport import LaTeXViewport
    from noether.ui.widgets.meter import CrisisMeter
    from noether.apl.events import EpistemicEvent, EventType


class NoetherMainWindow(QMainWindow):
    """The main PySide6 window for the Noether Epistemic Log Visualizer."""

    def __init__(self, timeline_model: EpistemicTimelineModel, tolerance: float = 0.15):
        super().__init__()
        self.setWindowTitle("Noether - Epistemic Plausibility Engine")
        self.resize(1100, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left Pane: Crisis Meter + Timeline Scrubber
        left_pane = QWidget()
        left_layout = QVBoxLayout(left_pane)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        self.crisis_meter = CrisisMeter(tolerance=tolerance)
        left_layout.addWidget(self.crisis_meter)

        self.timeline_view = QListView()
        self.timeline_view.setModel(timeline_model)
        self.timeline_delegate = EpistemicTimelineDelegate(self.timeline_view)
        self.timeline_view.setItemDelegate(self.timeline_delegate)
        self.timeline_view.setFrameShape(QListView.Shape.NoFrame)
        left_layout.addWidget(self.timeline_view)

        splitter.addWidget(left_pane)

        # Right Pane: AST Math Viewport (Matplotlib LaTeX renderer)
        self.ast_viewport = LaTeXViewport()
        splitter.addWidget(self.ast_viewport)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        self.timeline_view.selectionModel().currentChanged.connect(self._on_event_selected)

    def _on_event_selected(self, current: QModelIndex, previous: QModelIndex) -> None:
        """Handles timeline selection, extracting the raw event and updating UI panels."""
        if not current.isValid():
            return

        model = self.timeline_view.model()
        event: EpistemicEvent = current.data(EpistemicTimelineModel.EventRole)

        if event:
            self.ast_viewport.render_event(event)

        # Compute compounding health attenuation up to the currently selected timeline step
        current_health = 1.0
        for i in range(current.row() + 1):
            row_event = model.data(model.index(i, 0), EpistemicTimelineModel.EventRole)
            if row_event and row_event.delta_error > 0:
                current_health *= max(0.0, 1.0 - row_event.delta_error)

        total_degradation = 1.0 - current_health
        self.crisis_meter.update_error(total_degradation)


def main() -> int:
    """Application entry point."""
    app = QApplication.instance() or QApplication(sys.argv)
    model = EpistemicTimelineModel()
    window = NoetherMainWindow(model)
    window.show()
    return app.exec()


# --- Deterministic Verification Check ---
if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)

    test_model = EpistemicTimelineModel()
    e1 = EpistemicEvent(EventType.ANOMALY, "Patch 1", sp.Symbol('x'), "Err 0.05", delta_error=0.05)
    e2 = EpistemicEvent(EventType.ANOMALY, "Patch 2", sp.Symbol('y'), "Err 0.08", delta_error=0.08)
    test_model.add_event(e1)
    test_model.add_event(e2)

    window = NoetherMainWindow(test_model, tolerance=0.15)

    # Simulate a selection event of the 2nd row to test error accumulation
    window.timeline_view.selectionModel().setCurrentIndex(
        test_model.index(1, 0),
        window.timeline_view.selectionModel().SelectionFlag.ClearAndSelect
    )

    # Multiplicative health degradation calculation
    expected_health = (1.0 - 0.05) * (1.0 - 0.08)
    expected_degradation = 1.0 - expected_health
    expected_ratio = expected_degradation / 0.15
    assert window.crisis_meter.bar.value() == int(
        expected_ratio * 1000), "Crisis meter failed to accumulate error correctly on selection."
    print("[TEST] NoetherMainWindow multi-step selection and crisis meter update passed successfully!")