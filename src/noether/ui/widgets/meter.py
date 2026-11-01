import sys
from PySide6.QtWidgets import QProgressBar, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt


class CrisisMeter(QWidget):
    """
    Visualizes accumulated epistemic error against the paradigm's crisis tolerance.
    Transitions from safe (green) to warning (yellow) to crisis (red).
    """

    def __init__(self, parent: QWidget | None = None, tolerance: float = 0.15) -> None:
        super().__init__(parent)
        self.tolerance = tolerance

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 5)

        self.label = QLabel("Paradigm Stability (0.0% to Crisis)")
        self.label.setStyleSheet("font-weight: bold; font-size: 10pt; color: #2c3e50;")
        self.layout.addWidget(self.label)

        self.bar = QProgressBar()
        self.bar.setRange(0, 1000)  # 0.0 to 1.0 mapped to 0-1000 for precision
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(12)
        self.layout.addWidget(self.bar)

        self.update_error(0.0)

    def update_error(self, accumulated_error: float) -> None:
        """Updates the progress bar fill and dynamic color based on the error ratio."""
        ratio = min(accumulated_error / self.tolerance, 1.0) if self.tolerance > 0 else 1.0

        # Color mapping: < 50% Safe (Green), < 100% Warn (Yellow), >= 100% Crisis (Red)
        color = "#27ae60" if ratio < 0.5 else "#f39c12" if ratio < 1.0 else "#e74c3c"

        self.bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ecf0f1;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)

        self.bar.setValue(int(ratio * 1000))
        self.label.setText(f"Paradigm Stability ({min(ratio * 100.0, 100.0):.1f}% to Crisis)")


# --- Deterministic Verification Check ---
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(sys.argv)

    meter = CrisisMeter(tolerance=0.15)

    # Test safe threshold
    meter.update_error(0.05)
    assert meter.bar.value() == int((0.05 / 0.15) * 1000), "Meter fill calculation failed."
    assert "27ae60" in meter.bar.styleSheet(), "Meter failed to assign safe (green) color."

    # Test crisis threshold
    meter.update_error(0.16)
    assert meter.bar.value() == 1000, "Meter failed to clamp at 100% capacity."
    assert "e74c3c" in meter.bar.styleSheet(), "Meter failed to assign crisis (red) color."