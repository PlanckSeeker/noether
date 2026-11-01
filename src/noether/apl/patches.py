import sympy as sp
from typing import Callable
from dataclasses import dataclass
from ..core.context import ParadigmContext

@dataclass(frozen=True)
class Patch:
    name: str
    condition: Callable[[sp.Expr, ParadigmContext], bool]
    action: Callable[[sp.Expr, ParadigmContext], tuple[sp.Expr, float, str]]

# --- 1. Small-Angle / Taylor Patch ---
def condition_taylor(eq: sp.Expr, ctx: ParadigmContext) -> bool:
    """Triggers if the expression contains transcendental functions like sin()."""
    return any(isinstance(node, (sp.sin, sp.cos, sp.tan, sp.exp)) for node in eq.atoms(sp.Function))

def action_taylor(eq: sp.Expr, ctx: ParadigmContext) -> tuple[sp.Expr, float, str]:
    """Applies a first-order Maclaurin/Taylor expansion to transcendentals."""
    new_eq = eq.replace(sp.sin, lambda arg: arg)
    return new_eq, 0.05, "Replaced sin(x) with x via small-angle approximation."

taylor_patch = Patch("Small-Angle/Taylor", condition_taylor, action_taylor)


# --- 2. Asymptotic Drop Patch ---
def condition_asymptotic_drop(eq: sp.Expr, ctx: ParadigmContext) -> bool:
    """
    Triggers if an expression contains terms where expected velocity v_obs
    is orders of magnitude smaller than the speed of light c.
    """
    if "v_obs" in ctx.bounds and "c" in ctx.bounds:
        ratio = ctx.magnitude_ratio("v_obs", "c")
        return ratio < 0.01 and any(sym.name == 'c' for sym in eq.free_symbols)
    return False

def action_asymptotic_drop(eq: sp.Expr, ctx: ParadigmContext) -> tuple[sp.Expr, float, str]:
    """Drops higher-order relativistic correction terms based on scale bounds."""
    c = sp.Symbol('c')
    new_eq = eq.xreplace({term: 0 for term in eq.atoms(sp.Pow) if c in term.free_symbols})
    return new_eq, 0.03, "Dropped negligible high-order relativistic terms based on paradigm scale bounds."

asymptotic_drop_patch = Patch("Asymptotic Term Drop", condition_asymptotic_drop, action_asymptotic_drop)