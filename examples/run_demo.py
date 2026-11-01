import sys
import sympy as sp
from PySide6.QtWidgets import QApplication

# Import core Noether engine components using professional package imports
from noether.core.context import ParadigmContext
from noether.apl.events import EpistemicEvent, EventType
from noether.apl.priority_queue import EpistemicAPL
from noether.apl.patches import taylor_patch, asymptotic_drop_patch
from noether.ui.models import EpistemicTimelineModel
from noether.ui.app import NoetherMainWindow


def main() -> int:
    """Master runner: Evaluates a multi-step wave/relativistic hypothesis and launches the PySide6 UI."""
    app = QApplication.instance() or QApplication(sys.argv)

    # 1. Define a Paradigm Context with tight crisis tolerance to watch health decay
    ctx = ParadigmContext(
        name="Relativistic Wave Mechanics",
        bounds={
            "v_obs": (10_000, 50_000),   # Moderate velocity scale (m/s)
            "c": (3e8, 3e8),             # Speed of light (m/s)
            "theta": (0.0, 0.04),        # Small angle paraxial bound
        },
        crisis_tolerance=0.10             # 10% maximum allowable epistemic health degradation
    )

    # 2. Pose a complex theoretical hypothesis requiring multiple successive patches:
    # Contains both a transcendental function (triggering Taylor) and a relativistic velocity ratio term (triggering Asymptotic Drop)
    x, v_obs, c = sp.symbols('x v_obs c')
    hypothesis = sp.sin(x) + 1 + (v_obs ** 2) / (c ** 2)

    print(f"\n[ENGINE] Evaluating multi-step hypothesis under '{ctx.name}' paradigm...")
    print(f" -> Initial Expression: {hypothesis}")

    # 3. Build and execute the APL priority queue with multiple patches
    apl = EpistemicAPL([taylor_patch, asymptotic_drop_patch])
    evaluation_events = list(apl.evaluate(hypothesis, ctx))

    # 4. Populate the UI Timeline Model
    model = EpistemicTimelineModel()
    for event in evaluation_events:
        model.add_event(event)
        print(f" -> Logged Event: [{event.event_type.name}] {event.action_name} | Penalty: {event.delta_error:.2f}")
        print(f"    Rationale: {event.rationale}")

    # 5. Launch the PySide6 Visualizer Window
    window = NoetherMainWindow(model, tolerance=ctx.crisis_tolerance)
    window.show()

    print("[UI] Multi-step epistemic log visualizer launched successfully.\n")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())