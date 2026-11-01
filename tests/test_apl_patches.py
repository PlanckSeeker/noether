import pytest
import sympy as sp
from noether.core.context import ParadigmContext
from noether.apl.patches import taylor_patch, asymptotic_drop_patch


def test_taylor_patch_execution() -> None:
    """Verify the Small-Angle/Taylor patch correctly replaces sin(x) with x."""
    x = sp.Symbol('x')
    eq = sp.sin(x) + x ** 2
    ctx = ParadigmContext("TestContext")

    assert taylor_patch.condition(eq, ctx) is True, "Taylor condition failed to detect sin(x)."
    new_eq, err, rationale = taylor_patch.action(eq, ctx)
    assert new_eq == x + x ** 2, f"Expected x + x^2, got {new_eq}"
    assert err == 0.05, "Taylor patch error delta mismatch."


def test_asymptotic_drop_patch_execution() -> None:
    """Verify asymptotic drop removes high-order powers of c."""
    c = sp.Symbol('c')
    v_obs = sp.Symbol('v_obs')
    eq = 1 + v_obs ** 2 / c ** 2
    ctx = ParadigmContext("Test", bounds={"v_obs": (1e3, 3e5), "c": (3e8, 3e8)})

    assert asymptotic_drop_patch.condition(eq, ctx) is True, "Asymptotic drop condition should trigger."
    new_eq, err, rationale = asymptotic_drop_patch.action(eq, ctx)
    assert err == 0.03, "Asymptotic drop error delta mismatch."
    assert new_eq == 1, f"Expected relativistic term to drop to 1, got {new_eq}"