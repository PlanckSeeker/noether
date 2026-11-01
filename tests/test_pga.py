import pytest
import sympy as sp
from noether.core.algebra import SparseMultivector


def test_nilpotent_e0() -> None:
    """Verify that e0 * e0 = 0 (the dual nilpotent unit in G(3,0,1))."""
    e0 = SparseMultivector({1: 1})
    res = e0 * e0
    assert len(res.blades) == 0, "Nilpotent e0*e0 failed to vanish to zero."


def test_geometric_product_combination() -> None:
    """Verify symbolic blade combination and scalar scaling."""
    x = sp.Symbol('x')
    mv1 = SparseMultivector({2: x})  # e1 blade
    mv2 = SparseMultivector({4: 2})  # e2 blade

    res = mv1 * mv2
    assert res.blades.get(6) == 2 * x, f"Expected 2*x at blade mask 6, got {res.blades.get(6)}"