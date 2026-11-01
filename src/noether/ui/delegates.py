import sys
from PySide6.QtWidgets import QStyledItemDelegate, QStyle, QApplication
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtCore import Qt, QRect, QSize
import sympy as sp

# Simulating relative imports for the console environment
try:
    from .models import EpistemicTimelineModel
    from ..apl.events import EventType, EpistemicEvent
except ImportError:
    from noether.ui.models import EpistemicTimelineModel
    from noether.apl.events import EventType, EpistemicEvent


class EpistemicTimelineDelegate(QStyledItemDelegate):
    """
    Custom delegate to paint APL evaluation events in the QListView.
    Renders a color-coded left edge bar and structured typography based on EventType.
    """

    COLOR_MAP = {
        EventType.PASS: QColor("#27ae60"),  # Green
        EventType.VETO: QColor("#8e44ad"),  # Purple
        EventType.ANOMALY: QColor("#f39c12"),  # Orange/Yellow
        EventType.CRISIS: QColor("#e74c3c")  # Red
    }

    def paint(self, painter: QPainter, option, index) -> None:
        event: EpistemicEvent = index.data(EpistemicTimelineModel.EventRole)
        if not event:
            super().paint(painter, option, index)
            return

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Draw Background (Handles selection highlighting)
        rect = option.rect
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(rect, QColor("#e2e6ea"))
        else:
            painter.fillRect(rect, QColor("#ffffff"))

        # 2. Draw Color Bar (Left edge indicator)
        color = self.COLOR_MAP.get(event.event_type, QColor("#333333"))
        bar_rect = QRect(rect.left(), rect.top(), 6, rect.height())
        painter.fillRect(bar_rect, color)

        # 3. Draw Timestamp (Monospaced)
        painter.setPen(QPen(QColor("#7f8c8d")))
        font = painter.font()
        font.setFamily("monospace")
        font.setPointSize(9)
        painter.setFont(font)

        timestamp_str = f"[{event.timestamp:.3f}]"
        # 12px padding from left to clear the color bar
        painter.drawText(rect.adjusted(12, 0, -4, 0), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         timestamp_str)

        # 4. Draw Event Type & Action Name
        font.setFamily(option.font.family())
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(QPen(color))

        type_str = f"{event.event_type.name} "
        # 105px offset to clear the timestamp
        text_rect = rect.adjusted(105, 0, -4, 0)
        type_bounding_rect = painter.boundingRect(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                                                  type_str)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, type_str)

        # Action Name appended after Event Type
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#2c3e50")))
        painter.drawText(
            text_rect.adjusted(type_bounding_rect.width(), 0, 0, 0),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            f"| {event.action_name}"
        )

        # 5. Draw Bottom Separator Line
        painter.setPen(QPen(QColor("#ecf0f1")))
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())

        painter.restore()

    def sizeHint(self, option, index) -> QSize:
        """Forces a consistent, breathable row height of 32px."""
        return QSize(200, 32)


# --- Deterministic Verification Check ---
if __name__ == "__main__":
    from PySide6.QtWidgets import QListView

    app = QApplication.instance() or QApplication(sys.argv)

    model = EpistemicTimelineModel()
    delegate = EpistemicTimelineDelegate()

    # Push test data
    test_event = EpistemicEvent(
        event_type=EventType.CRISIS,
        action_name="Paradigm Shift Request",
        ast_snapshot=sp.Symbol('x'),
        rationale="Tolerance exceeded."
    )
    model.add_event(test_event)

    view = QListView()
    view.setModel(model)
    view.setItemDelegate(delegate)

    assert view.itemDelegate() is delegate, "Timeline view failed to bind the custom delegate."
    assert delegate.sizeHint(None, model.index(0, 0)).height() == 32, "Delegate row height invariant failed."