# Fix Math Engine Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the broken math engine by creating the missing `math_stepper.js` wrapper, wiring the CAS solver into the animation renderer, and adding `sympy` to requirements.

**Architecture:** mathsteps (Node.js) is primary (detailed step-by-step with substeps), CAS solver (SymPy) is fallback. The animation renderer uses the same mathsteps-primary pipeline as `main.py`.

**Tech Stack:** Python (SymPy, Manim), Node.js (mathsteps npm package)

---

### Task 1: Create `math_stepper.js`

**Files:**
- Create: `math_stepper.js`

- [ ] **Step 1: Create `math_stepper.js` with equation solving**

```javascript
#!/usr/bin/env node
'use strict';

const mathsteps = require('mathsteps');

const input = process.argv[2];

if (!input) {
  console.log(JSON.stringify({ success: false, error: 'No input provided' }));
  process.exit(0);
}

const isEquation = input.includes('=');

try {
  let steps;
  if (isEquation) {
    steps = mathsteps.solveEquation(input);
  } else {
    steps = mathsteps.simplifyExpression(input);
  }

  if (!steps || steps.length === 0) {
    console.log(JSON.stringify({
      success: false,
      error: 'No steps found',
      input: input
    }));
    process.exit(0);
  }

  const formattedSteps = steps.map((step, index) => ({
    step: index + 1,
    description: step.changeType.replace(/_/g, ' ').toLowerCase(),
    before: step.oldEquation ? step.oldEquation.ascii() : input,
    after: step.newEquation.ascii(),
    hasSubsteps: step.substeps && step.substeps.length > 0,
    substepCount: step.substeps ? step.substeps.length : 0
  }));

  console.log(JSON.stringify({
    success: true,
    type: isEquation ? 'equation' : 'expression',
    processedInput: input,
    stepCount: formattedSteps.length,
    steps: formattedSteps
  }));
} catch (err) {
  console.log(JSON.stringify({
    success: false,
    error: err.message,
    input: input
  }));
}
```

- [ ] **Step 2: Test the script directly**

Run: `node math_stepper.js "5x+3=0"`
Expected: JSON output with `success: true` and steps array

- [ ] **Step 3: Test with a quadratic equation**

Run: `node math_stepper.js "x^2+2x+1=0"`
Expected: JSON output with steps for solving the quadratic

- [ ] **Step 4: Test error handling with invalid input**

Run: `node math_stepper.js ""`
Expected: JSON output with `success: false` and error message

- [ ] **Step 5: Commit**

```bash
git add math_stepper.js
git commit -m "feat: add missing math_stepper.js wrapper for mathsteps"
```

---

### Task 2: Refactor `enhanced_animator.py` to use CAS-first pipeline

**Files:**
- Modify: `enhanced_animator.py:1-60` (imports and `__init__`/`load_steps`)

- [ ] **Step 1: Update imports to include CAS solver**

Replace the imports section at the top of `enhanced_animator.py`:

```python
from manim import *
from typing import Dict, Any
import sys
import os

# Try CAS solver first (primary)
try:
    from cas_solver import solve_with_steps as cas_solve
    HAS_CAS = True
except ImportError:
    HAS_CAS = False

# Fallback to mathsteps bridge
try:
    from math_bridge import MathStepperBridge
    HAS_BRIDGE = True
except ImportError:
    HAS_BRIDGE = False
```

- [ ] **Step 2: Replace `__init__` to remove direct bridge dependency**

```python
def __init__(self, equation: str = "5x+3=0", *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.equation = equation
    self.steps_data = None
    self.current_equation = None
    self.load_steps()
```

- [ ] **Step 3: Replace `load_steps` with CAS-first logic**

```python
def load_steps(self):
    """Load steps using CAS solver first, mathsteps as fallback"""
    # Try CAS solver first
    if HAS_CAS:
        try:
            result = cas_solve(self.equation)
            if result.get('success'):
                self.steps_data = [
                    {
                        'step': i + 1,
                        'description': s.get('desc', 'Solve'),
                        'before': s.get('before', ''),
                        'after': s.get('after', '')
                    }
                    for i, s in enumerate(result.get('steps', []))
                ]
                print(f"✓ CAS solver: {len(self.steps_data)} steps for: {self.equation}")
                return
        except Exception as e:
            print(f"CAS solver failed: {e}")

    # Fallback to mathsteps bridge
    if HAS_BRIDGE:
        try:
            bridge = MathStepperBridge()
            result = bridge.get_info(self.equation)
            if result.get('success'):
                self.steps_data = result.get('steps', [])
                print(f"✓ mathsteps: {len(self.steps_data)} steps for: {self.equation}")
                return
        except Exception as e:
            print(f"mathsteps bridge failed: {e}")

    # Both failed
    print(f"❌ No solver available for: {self.equation}")
    self.steps_data = []
```

- [ ] **Step 4: Update the module docstring**

Replace the docstring at the top of the file:

```python
"""
Enhanced Math Steps Animator - Creates beautiful step-by-step math animations

This uses the Manim Community library for animations.
GitHub: https://github.com/ManimCommunity/manim
Documentation: https://docs.manim.community/

Math processing powered by SymPy (primary) and mathsteps (fallback).
"""
```

- [ ] **Step 5: Remove `MATH_EQUATION` env var handling from `__main__` block**

The `__main__` block at the bottom sets `MathStepsAnimator.equation_to_solve` but this attribute is never used. Remove it and keep only the env var / arg parsing:

```python
if __name__ == "__main__":
    equation = "5x+3=0"

    if "MATH_EQUATION" in os.environ:
        equation = os.environ["MATH_EQUATION"]
    elif "--equation" in sys.argv:
        try:
            eq_index = sys.argv.index("--equation")
            if eq_index + 1 < len(sys.argv):
                equation = sys.argv[eq_index + 1]
        except (ValueError, IndexError):
            pass
```

- [ ] **Step 6: Test standalone animation**

Run: `MATH_EQUATION="5x+3=0" python enhanced_animator.py`
Expected: Should load steps via CAS solver (no FileNotFoundError)

- [ ] **Step 7: Commit**

```bash
git add enhanced_animator.py
git commit -m "feat: wire CAS solver into animation renderer as primary solver"
```

---

### Task 3: Update `requirements.txt`

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Add `sympy` to requirements.txt**

Add `sympy>=1.12` after the existing dependencies:

```
# Core dependencies
manim>=0.18.0
python-telegram-bot>=20.0
sympy>=1.12

# Optional but recommended
numpy>=1.24.0
scipy>=1.10.0
```

- [ ] **Step 2: Verify sympy is installed**

Run: `python -c "import sympy; print(sympy.__version__)"`
Expected: Version number output (e.g., `1.12.1`)

- [ ] **Step 3: Commit**

```bash
git add requirements.txt
git commit -m "chore: add sympy as explicit dependency"
```

---

### Task 4: End-to-end verification

- [ ] **Step 1: Test CAS solver directly**

Run: `python main.py -e "5x+3=0"`
Expected: Successful output with steps and solution

- [ ] **Step 2: Test mathsteps fallback via Node.js**

Run: `node math_stepper.js "5x+3=0"`
Expected: JSON output with `success: true`

- [ ] **Step 3: Test animation pipeline (CAS path)**

Run: `python main.py -e "5x+3=0" --animate -q l`
Expected: Animation renders using CAS solver

- [ ] **Step 4: Test animation pipeline (mathsteps fallback)**

Temporarily rename `cas_solver.py` to test the fallback path, then restore it.

- [ ] **Step 5: Test with equations from `equations.txt`**

Run: `python main.py -f equations.txt`
Expected: All equations solve successfully

- [ ] **Step 6: Final commit with all files**

```bash
git add -A
git status
git commit -m "fix: complete math engine integration - CAS primary, mathsteps fallback"
```
