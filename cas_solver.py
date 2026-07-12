#!/usr/bin/env python3
"""
CAS step-by-step equation solver using SymPy
"""

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import sympy.abc
import re
import json
import sys


def robust_parse(eq: str, show_parse=False):
    """Parse equation string into SymPy expression with proper transformations"""
    eq = eq.strip()
    
    # Split into left and right
    if '=' not in eq:
        return None, None
    
    left, right = eq.split('=', 1)
    left, right = left.strip(), right.strip()
    
    # Apply transformation rules
    def transform(s):
        s = s.strip()
        
        # Handle e^(ax) -> exp(a*x) FIRST (before other transformations)
        # e^(2x) -> exp(2*x)
        s = re.sub(r'e\^\((\d+)([x])\)', r'exp(\1*\2)', s)
        s = re.sub(r'e\^\(([^)]+)\)', r'exp(\1)', s)
        # e^2x or e^2*x without parens
        s = re.sub(r'e\*\*(\d+)([x])', r'exp(\1*\2)', s)
        s = re.sub(r'e\*\*([a-z])', r'exp(\1)', s)
        s = re.sub(r'e\*\*(.)', r'exp(\1)', s)
        
        # Handle implicit multiplication: 2x -> 2*x
        s = re.sub(r'(\d)(\w)', r'\1*\2', s)
        s = re.sub(r'(\d)(\()', r'\1*\2', s)
        
        # Replace ^ with **
        s = s.replace('^', '**')
        
        # Handle sqrt
        s = re.sub(r'sqrt\(([^)]+)\)', r'sqrt(\1)', s)
        
        return s
    
    left_t = transform(left)
    right_t = transform(right)
    
    if show_parse:
        print(f"Parsing: {left_t} - {right_t}")
    
    try:
        expr = parse_expr(f"({left_t}) - ({right_t})")
        return expr, left_t + " - " + right_t
    except Exception as e:
        return None, str(e)


def get_step_type(expr, x):
    """Determine the mathematical type and generate step-by-step reasoning"""
    steps = []
    
    # Degree check
    try:
        degree = sp.degree(expr, x)
    except:
        degree = None
    
    # Expand the expression
    expanded = sp.expand(expr)
    
    # Get variables
    free = expr.free_symbols
    
    # Check for specific forms
    expr_str = str(expr)
    
    # 1. RECIPROCAL form: x + a/x = c
    if re.search(r'x\s*\+\s*\d+\s*/\s*x|x\s*\*\s*\d+\s*/\s*x', expr_str):
        a = 1
        match = re.search(r'(\d+)/x', expr_str)
        if match:
            a = int(match.group(1))
        steps.append({"step": 1, "before": f"x + {a}/x = c", "after": "Multiply by x", "type": "RECIPROCAL", "desc": "x² + a = cx"})
        steps.append({"step": 2, "before": "x² - cx + a = 0", "after": "Standard quadratic form", "type": "REARRANGE", "desc": "ax² + bx + c = 0"})
        return "reciprocal", steps
    
    # 2. EXPONENTIAL: base^x form
    if '**' in expr_str or 'exp' in expr_str:
        steps.append({"step": 1, "before": "Exponential term detected", "after": "Identify base and exponent", "type": "EXP", "desc": "Take logarithm"})
        return "exponential", steps
    
    # 3. RADICAL: sqrt form
    if 'sqrt' in expr_str:
        steps.append({"step": 1, "before": "Square root detected", "after": "Square both sides", "type": "RADICAL", "desc": "Eliminate radical"})
        return "radical", steps
    
    # 4. POLYNOMIAL
    if degree and degree > 0:
        steps.append({"step": 1, "before": f"Degree {degree} polynomial", "after": "Identify coefficients", "type": "POLY", "desc": "Expand and collect terms"})
        return f"polynomial_{degree}", steps
    
    # Default - try to solve directly
    steps.append({"step": 1, "before": "General form", "after": "Solve directly", "type": "GENERAL", "desc": "Use SymPy solver"})
    return "general", steps


def solve_with_steps(eq: str):
    """Main solver with step-by-step reasoning"""
    x = sp.Symbol('x')
    
    expr, parse_info = robust_parse(eq)
    
    if expr is None:
        return {"success": False, "error": f"Parse error: {parse_info}", "input": eq}
    
    # Determine step type
    step_type, steps = get_step_type(expr, x)
    
    # Solve
    try:
        solutions = sp.solve(expr, x)
        
        if not solutions:
            return {"success": False, "error": "No solutions found", "input": eq, "steps": steps}
        
        # Add solution steps
        for i, sol in enumerate(solutions):
            steps.append({
                "step": len(steps) + 1,
                "before": "Solve equation",
                "after": f"x_{i+1} = {sp.nsimplify(sol)}",
                "type": "SOLUTION",
                "desc": f"Root {i+1}"
            })
        
        return {
            "success": True,
            "input": eq,
            "type": step_type,
            "steps": steps,
            "solutions": [str(sp.nsimplify(s)) for s in solutions]
        }
    
    except Exception as e:
        return {"success": False, "error": str(e), "input": eq, "steps": steps}


def show_solution(result):
    """Pretty print the solution"""
    if not result.get('success'):
        print(f"❌ Cannot solve: {result['input']}")
        print(f"   Error: {result.get('error', 'Unknown')}")
        return
    
    print(f"✓ Solving: {result['input']}")
    print(f"  Type: {result.get('type', 'unknown')}")
    print()
    
    for step in result.get('steps', []):
        print(f"  Step {step['step']}: {step['before']}")
        print(f"    → {step['after']}")
        if step.get('desc'):
            print(f"    [{step['desc']}]")
    
    print()
    for sol in result.get('solutions', []):
        print(f"  ══► x = {sol}")


if __name__ == '__main__':
    # Get equation from command line or use default
    eq = sys.argv[1] if len(sys.argv) > 1 else "x+1/x=5"
    
    if '--json' in sys.argv:
        result = solve_with_steps(eq)
        print(json.dumps(result, indent=2))
    else:
        result = solve_with_steps(eq)
        show_solution(result)