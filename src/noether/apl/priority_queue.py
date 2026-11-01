import sympy as sp
from typing import Generator
from .events import EpistemicEvent, EventType
from .patches import Patch
from ..core.context import ParadigmContext


class EpistemicAPL:
    """
    The Kuhnian state machine evaluating an equation against patches
    using non-linear multiplicative error propagation and epistemic health decay.
    """

    def __init__(self, patches: list[Patch]):
        self.patches = patches

    def evaluate(self, eq: sp.Expr, ctx: ParadigmContext) -> Generator[EpistemicEvent, None, None]:
        current_eq = eq
        # Model epistemic health starts at 1.0 (100% valid, zero friction)
        epistemic_health = 1.0

        # Crisis tolerance now represents the minimum health threshold (e.g., 0.85 = 15% max degradation)
        # If context crisis_tolerance is set low (e.g. 0.15), treat it as max allowable health drop (1.0 - tolerance)
        min_health_threshold = max(0.0, 1.0 - ctx.crisis_tolerance)

        try:
            for patch in self.patches:
                if patch.condition(current_eq, ctx):
                    current_eq, penalty, rationale = patch.action(current_eq, ctx)

                    # Multiplicative health decay: each patch reduces remaining health proportionally
                    # penalty is treated as a fractional degradation factor in (0, 1)
                    epistemic_health *= max(0.0, 1.0 - penalty)

                    yield EpistemicEvent(
                        EventType.ANOMALY,
                        patch.name,
                        current_eq,
                        rationale,
                        delta_error=penalty
                    )

                # Trigger crisis immediately if model health drops below the paradigm threshold
                if epistemic_health <= min_health_threshold:
                    total_degradation = 1.0 - epistemic_health
                    yield EpistemicEvent(
                        EventType.CRISIS,
                        "Declare Crisis",
                        current_eq,
                        f"Model epistemic health dropped to {epistemic_health:.2f} (degradation {total_degradation:.2f}), breaching paradigm safety threshold ({ctx.crisis_tolerance}).",
                        total_degradation
                    )
                    return

            if epistemic_health > min_health_threshold:
                yield EpistemicEvent(
                    EventType.PASS,
                    "Stable",
                    current_eq,
                    f"Model retained stable epistemic health ({epistemic_health:.2f}).",
                    0.0
                )

        except Exception as e:
            yield EpistemicEvent(
                EventType.VETO,
                "Evaluation Veto",
                current_eq,
                f"Engine encountered critical evaluation exception: {str(e)}",
                1.0
            )