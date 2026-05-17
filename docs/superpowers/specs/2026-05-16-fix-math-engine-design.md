# Fix Math Engine Integration

**Date:** 2026-05-16
**Status:** Implemented
**Scope:** Replace broken mathsteps bridge with unified mathsteps-primary solver pipeline

## Problem

The math animation system has a dual-solver architecture that is completely broken:

1. **`math_stepper.js` is missing** — The Node.js wrapper script that bridges the `mathsteps` npm package to Python was never committed to the repo. `math_bridge.py` raises `FileNotFoundError` when trying to use it.
2. **Animation renderer bypasses CAS solver** — `enhanced_animator.py` always uses `MathStepperBridge` (mathsteps), never the working SymPy CAS solver. Even when `main.py` solves an equation successfully via CAS, the animation path fails.
3. **Missing dependency** — `sympy` is not listed in `requirements.txt`, though `cas_solver.py` imports it.

## Solution

Three changes to create a unified CAS-first solving pipeline:

### 1. Create `math_stepper.js` (new file)

Node.js wrapper that calls the existing `mathsteps` npm package and outputs JSON to stdout.

- Accepts equation string as CLI argument
- Uses `mathsteps.solveEquation()` for equations (contains `=`)
- Uses `mathsteps.simplifyExpression()` for expressions (no `=`)
- Returns JSON: `{success, type, processedInput, stepCount, steps[{step, description, before, after, hasSubsteps, substepCount}]}`
- Handles errors gracefully with `{success: false, error: "..."}`

### 2. Refactor `enhanced_animator.py` to use CAS-first pipeline

Change `load_steps()` to mirror `main.py`'s solving strategy:

```
1. Try cas_solver.solve_with_steps(equation)
2. If CAS succeeds → normalize steps to animator format
3. If CAS fails → fall back to MathStepperBridge.get_info()
4. If both fail → show error
```

Step normalization maps CAS output `{step, before, after, desc, type}` to animator format `{step, description, before, after}`.

### 3. Update `requirements.txt`

Add `sympy` as an explicit dependency.

## Files Changed

| File | Action | Description |
|------|--------|-------------|
| `math_stepper.js` | Create | Node.js wrapper for mathsteps npm package |
| `enhanced_animator.py` | Modify | Refactor `load_steps()` to use CAS-first pipeline |
| `requirements.txt` | Modify | Add `sympy` |

## Data Flow (after fix)

```
User input (equation string)
        |
        v
  math_bridge.get_info()  ← PRIMARY (mathsteps)
        |
        +-- success? → flatten substeps, filter noise → animate
        |
        +-- fail? → cas_solver.solve_with_steps()  ← FALLBACK (SymPy)
                        |
                        +-- success? → normalize steps → animate
                        |
                        +-- fail? → show error in animation
```

## Step Format Contract

Both solvers must produce steps in this format for the animator:

```json
{
  "step": 1,
  "description": "Solve equation",
  "before": "5x + 3 = 0",
  "after": "x = -3/5"
}
```

CAS solver output mapping:
- `step` → `step` (already numbered)
- `desc` → `description`
- `before` → `before`
- `after` → `after`

mathsteps output: already uses `description`, `before`, `after` keys.

## Testing

Verify with equations from `equations.txt`:
- Linear: `5x+3=0`
- Quadratic: `x^2+2x+1=0`
- Square root: `sqrt(x+5)-2=sqrt(7-x)+3`

Test both paths:
1. `python main.py -e "5x+3=0"` (CAS solver)
2. `python main.py -e "5x+3=0" --animate` (animation with CAS)
3. `python enhanced_animator.py` standalone (should use CAS directly)
