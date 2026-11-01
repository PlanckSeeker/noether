import sys
import sympy as sp
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Simulating relative imports for the console environment
try:
    from ...apl.events import EpistemicEvent
except ImportError:
    from noether.apl.events import EpistemicEvent


class LaTeXViewport(QWidget):
    """
    A PySide6 widget that uses Matplotlib's mathtext engine to render
    SymPy AST snapshots as crisp LaTeX, flanked by event metadata labels.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Header Label (Action Name)
        self.header_label = QLabel("Select an event in the timeline.")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet("font-weight: bold; font-size: 14pt; color: #333;")
        self.layout.addWidget(self.header_label)

        # Matplotlib Canvas for LaTeX rendering
        self.figure = Figure(figsize=(5, 3), dpi=120)
        self.figure.patch.set_facecolor('#f8f9fa')  # Match UI background
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.layout.addWidget(self.canvas, stretch=1)

        # Add a single axis with no frames/ticks
        self.ax = self.figure.add_subplot(111)
        self.ax.axis('off')

        # Footer Label (Rationale)
        self.rationale_label = QLabel("")
        self.rationale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rationale_label.setWordWrap(True)
        self.rationale_label.setStyleSheet("font-style: italic; color: #555; padding: 10px;")
        self.layout.addWidget(self.rationale_label)

    def render_event(self, event: EpistemicEvent) -> None:
        """Updates the viewport to display the specific epistemic event."""
        self.header_label.setText(f"[{event.event_type.name}] {event.action_name}")
        self.rationale_label.setText(event.rationale)

        self.ax.clear()
        self.ax.axis('off')

        # Convert SymPy expression to LaTeX and render at the center of the axis
        latex_str = f"${sp.latex(event.ast_snapshot)}$"
        self.ax.text(
            0.5, 0.5, latex_str,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=24,
            color='black'
        )
        self.canvas.draw()


# --- Deterministic Verification Check ---
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from noether.apl.events import EventType

    app = QApplication.instance() or QApplication(sys.argv)

    viewport = LaTeXViewport()

    test_eq = sp.Eq(sp.Symbol('v_obs') ** 2, sp.Symbol('G') * sp.Symbol('M') / sp.Symbol('r'))
    test_event = EpistemicEvent(
        event_type=EventType.PASS,
        action_name="Keplerian Verification",
        ast_snapshot=test_eq,
        rationale="Equation is stable."
    )

    viewport.render_event(test_event)

    # Verify the UI components updated correctly
    assert "Keplerian Verification" in viewport.header_label.text(), "Header label failed to update."
    assert viewport.rationale_label.text() == "Equation is stable.", "Rationale label failed to update."

    # Verify Matplotlib axis contains the LaTeX text object
    assert len(viewport.ax.texts) == 1, "Matplotlib axis missing text object."
    assert "v_{obs}^{2} = \\frac{G M}{r}" in viewport.ax.texts[0].get_text(), "LaTeX conversion failed or mismatch."