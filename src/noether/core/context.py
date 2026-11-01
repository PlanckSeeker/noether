from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=True)
class ParadigmContext:
    """
    Defines the epistemic paradigm (Context), storing Fermi magnitude bounds
    and error tolerances to mathematically justify APL patches.
    """
    name: str
    bounds: dict[str, tuple[float, float]] = field(default_factory=dict)
    crisis_tolerance: float = 0.15  # 15% accumulated error threshold before Paradigm Shift

    def is_small(self, variable_name: str, threshold: float = 0.1) -> bool:
        """Evaluates if a variable is asymptotically small in this paradigm."""
        if variable_name not in self.bounds:
            return False
        _, max_val = self.bounds[variable_name]
        return max_val <= threshold

    def get_expected_magnitude(self, variable_name: str) -> float:
        """Calculates the geometric mean of the bounds as the characteristic scale."""
        if variable_name not in self.bounds:
            return 1.0
        min_val, max_val = self.bounds[variable_name]
        return (min_val * max_val) ** 0.5

    def magnitude_ratio(self, var_a: str, var_b: str) -> float:
        """Calculates expected scale ratios to justify asymptotic term dropping."""
        mag_a = self.get_expected_magnitude(var_a)
        mag_b = self.get_expected_magnitude(var_b)
        return float(mag_a / mag_b) if mag_b != 0 else float('inf')


@dataclass(frozen=True)
class WavePropagationContext(ParadigmContext):
    """
    Specialized ParadigmContext for wave physics, incorporating wave-specific
    diagnostics such as paraxial beam criteria and dispersion scales.
    """
    def is_paraxial(self, theta_var: str = "theta", threshold: float = 0.1) -> bool:
        """Evaluates if wave propagation satisfies the paraxial approximation (theta << 1)."""
        return self.is_small(theta_var, threshold)

    def dispersion_significance(self, omega_var: str = "omega", plasma_var: str = "omega_p") -> float:
        """Calculates the ratio of characteristic frequency to plasma/dispersion frequency."""
        return self.magnitude_ratio(omega_var, plasma_var)


# --- Central Paradigm Registry for Extensibility ---
class ParadigmRegistry:
    """
    Manages a global registry of physical paradigms, allowing new domains
    to be registered and retrieved dynamically by name.
    """
    _registry: Dict[str, ParadigmContext] = {}

    @classmethod
    def register(cls, context: ParadigmContext) -> ParadigmContext:
        """Registers a paradigm context instance."""
        cls._registry[context.name] = context
        return context

    @classmethod
    def get(cls, name: str) -> Optional[ParadigmContext]:
        """Retrieves a registered paradigm context by its name."""
        return cls._registry.get(name)

    @classmethod
    def list_paradigms(cls) -> list[str]:
        """Returns a list of all available paradigm names."""
        return list(cls._registry.keys())


# --- Standard Registered Paradigms ---

NEWTONIAN_ASTROPHYSICS = ParadigmRegistry.register(
    ParadigmContext(
        name="Newtonian Astrophysics",
        bounds={
            "v_obs": (1e3, 3e5),
            "c": (3e8, 3e8),
            "theta": (0.0, 0.05),
        },
        crisis_tolerance=0.15
    )
)

HIGH_FREQUENCY_WAVE_PARADIGM = ParadigmRegistry.register(
    WavePropagationContext(
        name="High-Frequency Wave Optics",
        bounds={
            "omega": (1e14, 1e16),         # Optical frequencies (rad/s)
            "omega_p": (1e10, 1e11),       # Plasma frequency scale
            "lambda_val": (400e-9, 700e-9), # Visible light wavelengths (m)
            "L_medium": (1e-3, 1.0),       # Scale of optical components (m)
            "theta": (0.0, 0.05)           # Paraxial beam divergence angle bound
        },
        crisis_tolerance=0.15
    )
)