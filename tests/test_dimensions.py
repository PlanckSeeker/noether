import pytest
import random
from fractions import Fraction
from noether.core.dimensions import Q8Lattice, Length, Mass, Time


def test_q8_valid_arithmetic() -> None:
    """Verify standard dimensional arithmetic tracks rational exponents correctly."""
    Velocity = Length / Time
    Acceleration = Velocity / Time
    Force = Mass * Acceleration
    Energy = Force * Length
    expected = (Fraction(2), Fraction(1), Fraction(-2), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    assert Energy.exponents == expected, f"Energy dimensional derivation failed. Got {Energy.exponents}"


def test_q8_fuzz_inverses() -> None:
    """Fuzz inverse operations over 100 random Q8 lattice states to ensure stability."""
    for _ in range(100):
        e1 = tuple(Fraction(random.randint(-5, 5)) for _ in range(8))
        e2 = tuple(Fraction(random.randint(-5, 5)) for _ in range(8))
        q1 = Q8Lattice(e1)  # type: ignore
        q2 = Q8Lattice(e2)  # type: ignore

        restored = (q1 * q2) / q1
        assert restored.exponents == q2.exponents, "Rational exponent tracking failed on cyclic inversion."
        assert (q1 / q1).is_dimensionless(), "Self-division must yield a dimensionless Q8Lattice."


def test_dimensional_veto_condition() -> None:
    """Simulate APL Priority 1 check: dimensional mismatch between LHS and RHS."""
    lhs = Mass * (Length / Time) ** 2  # Energy
    rhs = Mass * (Length / Time)  # Momentum
    is_vetoed = lhs != rhs
    assert is_vetoed is True, "Dimensional veto failed to flag Mass*Velocity vs Energy."