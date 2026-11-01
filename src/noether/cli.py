import argparse
import sys
import sympy as sp

from noether.core.context import NEWTONIAN_ASTROPHYSICS, ParadigmContext
from noether.apl.priority_queue import EpistemicAPL
from noether.apl.patches import taylor_patch, asymptotic_drop_patch
from noether.data.ingest import bind_csv, validate_ingested_bounds


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Noether Headless CLI: Evaluate symbolic physics hypotheses against empirical datasets."
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="Path to observational CSV dataset file."
    )
    parser.add_argument(
        "--hypothesis",
        required=True,
        help="SymPy mathematical expression or equation to evaluate (e.g., 'v_obs - v_theo')"
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.15,
        help="Crisis tolerance accumulated error threshold (default: 0.15)."
    )

    args = parser.parse_args()

    print(f"\n[CLI] Ingesting dataset from '{args.csv}'...")
    try:
        # Parse expression to dynamically extract required variable symbols
        expr = sp.sympify(args.hypothesis)
        free_syms = {str(sym): sym for sym in expr.free_symbols}
        df = bind_csv(args.csv, free_syms)
    except Exception as e:
        print(f"[ERROR] Failed to parse hypothesis or bind CSV: {e}", file=sys.stderr)
        return 1

    print("[CLI] Cross-referencing ingested columns against paradigm bounds...")
    validation_results = validate_ingested_bounds(df, NEWTONIAN_ASTROPHYSICS)
    for var_name, is_compliant in validation_results.items():
        status = "COMPLIANT"
    else:
        "OUT OF BOUNDS"
        print(f"  -> {var_name}: {status}")

    # Build Paradigm Context and APL Engine
    ctx = ParadigmContext(
        name="CLI Evaluator Paradigm",
        bounds=NEWTONIAN_ASTROPHYSICS.bounds,
        crisis_tolerance=args.tolerance
    )
    apl = EpistemicAPL([taylor_patch, asymptotic_drop_patch])

    print(f"\n[ENGINE] Evaluating hypothesis '{args.hypothesis}' under '{ctx.name}'...")
    events = list(apl.evaluate(expr, ctx))

    print("\n[LOG] Epistemic Evaluation Timeline:")
    for event in events:
        print(f"  [{event.timestamp:.3f}] {event.event_type.name:<8} | {event.action_name:<24} | Err: +{event.delta_error:.2f}")
        print(f"       Rationale: {event.rationale}")
        print(f"       AST State: {event.ast_snapshot}")

    return 0


if __name__ == "__main__":
    sys.exit(main())