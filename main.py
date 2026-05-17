#!/usr/bin/env python3
"""
Math Solver & Animator - Step-by-step equation solving with Manim animations.

Solver priority: mathsteps (detailed) → CAS/SymPy (fallback)
"""

import argparse
import sys
import json
import subprocess
import os
from pathlib import Path
from typing import List, Dict

try:
    from math_bridge import MathStepperBridge
    HAS_BRIDGE = True
except ImportError:
    HAS_BRIDGE = False

try:
    from cas_solver import solve_with_steps as cas_solve
    HAS_CAS = True
except ImportError:
    HAS_CAS = False


class C:
    """ANSI colors"""
    G = '\033[92m'  # green
    R = '\033[91m'  # red
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    M = '\033[95m'  # magenta
    C = '\033[96m'  # cyan
    X = '\033[0m'   # reset
    BOLD = '\033[1m'


class Pipeline:
    """Math solving pipeline: mathsteps primary, CAS fallback"""

    def __init__(self, quiet=False):
        self.quiet = quiet
        self.dir = Path(__file__).parent.absolute()
        self.bridge = None
        if HAS_BRIDGE:
            try:
                self.bridge = MathStepperBridge()
            except FileNotFoundError:
                pass

    def log(self, msg, color=""):
        if not self.quiet:
            print(f"{color}{msg}{C.X}")

    def solve(self, equation: str) -> dict:
        """Solve equation using mathsteps first, CAS fallback"""
        # mathsteps (primary - detailed steps)
        if self.bridge:
            try:
                result = self.bridge.get_info(equation)
                if result.get('success'):
                    result['solver'] = 'mathsteps'
                    return result
            except Exception:
                pass

        # CAS fallback
        if HAS_CAS:
            try:
                result = cas_solve(equation)
                if result.get('success'):
                    return {
                        'success': True,
                        'type': result.get('type', 'equation'),
                        'stepCount': len(result.get('steps', [])),
                        'steps': [
                            {'step': i+1, 'description': s.get('desc', 'Solve'),
                             'before': s.get('before', ''), 'after': s.get('after', '')}
                            for i, s in enumerate(result.get('steps', []))
                        ],
                        'solutions': result.get('solutions', []),
                        'input': equation,
                        'solver': 'cas'
                    }
            except Exception:
                pass

        return {'success': False, 'error': 'No solver available', 'input': equation}

    def print_result(self, equation: str, result: dict):
        """Print solving result to terminal"""
        if self.quiet:
            return

        self.log(f"\n{'─'*60}")
        self.log(f"  {equation}", C.BOLD)
        self.log(f"{'─'*60}")

        if not result.get('success'):
            self.log(f"  Error: {result.get('error')}", C.R)
            return

        solver = result.get('solver', 'unknown')
        steps = result.get('steps', [])
        self.log(f"  Solver: {solver}  |  Steps: {result.get('stepCount', len(steps))}", C.C)

        for step in steps:
            phase = step.get('phase', '')
            prefix = f"  [{phase}] " if phase else "  "
            self.log(f"{prefix}{step['description']}", C.B)
            if step.get('before') and step.get('after'):
                self.log(f"    {step['before']}")
                self.log(f"    ↓", C.Y)
                self.log(f"    {step['after']}", C.G)

        for sol in result.get('solutions', []):
            self.log(f"  ══► x = {sol}", C.G + C.BOLD)

    def animate(self, equation: str, quality: str = 'l', output: str = None) -> bool:
        """Render Manim animation. If output is given, copy the video there."""
        self.log(f"\n  Rendering animation ({quality} quality)...", C.C)

        result = self.solve(equation)
        if not result.get('success'):
            self.log(f"  Cannot animate: {result.get('error')}", C.R)
            return False

        animator = self.dir / "enhanced_animator.py"
        if not animator.exists():
            self.log(f"  Animator not found: {animator}", C.R)
            return False

        env = os.environ.copy()
        env["MATH_EQUATION"] = equation

        cmd = ["python", "-m", "manim", "render", f"-q{quality}",
               str(animator), "MathStepsAnimator", "--disable_caching"]

        try:
            r = subprocess.run(cmd, cwd=str(self.dir), env=env)
            if r.returncode == 0:
                media = self.dir / "media" / "videos" / "enhanced_animator"
                src = None
                if media.exists():
                    for mp4 in media.rglob("MathStepsAnimator.mp4"):
                        if src is None or mp4.stat().st_mtime > src.stat().st_mtime:
                            src = mp4
                if src and src.exists():
                    if output:
                        import shutil
                        dest = Path(output)
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src, dest)
                        self.log(f"  Saved: {dest.resolve()}", C.G)
                    else:
                        self.log(f"  Saved: {src}", C.G)
                return True
            else:
                self.log(f"  Manim failed (code {r.returncode})", C.R)
                return False
        except FileNotFoundError:
            self.log("  Manim not installed: pip install manim", C.R)
            return False

    def batch(self, equations: List[str]) -> Dict[str, dict]:
        """Process multiple equations"""
        results = {}
        ok = 0
        for i, eq in enumerate(equations, 1):
            self.log(f"[{i}/{len(equations)}]", C.B)
            r = self.solve(eq)
            self.print_result(eq, r)
            results[eq] = r
            if r.get('success'):
                ok += 1
        self.log(f"\n  {ok}/{len(equations)} solved", C.G)
        return results


def main():
    p = argparse.ArgumentParser(
        description='Math solver & animator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  %(prog)s "5x+3=0"                    solve equation
  %(prog)s "5x+3=0" -a                 solve and animate
  %(prog)s "5x+3=0" -a out.mp4         animate, save to out.mp4
  %(prog)s "5x+3=0" -a -q h            high quality animation
  %(prog)s -f equations.txt             batch solve from file
  %(prog)s -f equations.txt -a          batch animate
  %(prog)s "5x+3=0" -o results.json    save to JSON

quality: l=480p15  m=720p30  h=1080p60  k=2160p60
""")

    p.add_argument('equation', nargs='?', help='equation to solve')
    p.add_argument('-f', '--file', help='equations file (one per line)')
    p.add_argument('-a', '--animate', nargs='?', const=True, metavar='FILE', help='render animation (optionally specify output .mp4)')
    p.add_argument('-q', '--quality', choices='lmhk', default='l', help='animation quality (default: l)')
    p.add_argument('-o', '--output', metavar='FILE', help='save results as JSON')
    p.add_argument('-n', '--no-preview', action='store_true', help='skip video preview')
    p.add_argument('-s', '--silent', action='store_true', help='quiet output')

    args = p.parse_args()

    if not args.equation and not args.file:
        p.print_help()
        sys.exit(1)

    pipe = Pipeline(quiet=args.silent)
    results = {}

    # Determine animate output path
    animate_out = None
    if args.animate:
        if isinstance(args.animate, str):
            animate_out = args.animate
            if not animate_out.endswith('.mp4'):
                animate_out += '.mp4'

    if args.equation:
        result = pipe.solve(args.equation)
        results[args.equation] = result
        pipe.print_result(args.equation, result)

        if args.animate and result.get('success'):
            if not pipe.animate(args.equation, args.quality, output=animate_out):
                sys.exit(1)

    elif args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"{C.R}File not found: {args.file}{C.X}")
            sys.exit(1)

        equations = [l.strip() for l in path.read_text().splitlines()
                     if l.strip() and not l.startswith('#')]

        if not equations:
            print(f"{C.R}No equations in: {args.file}{C.X}")
            sys.exit(1)

        results = pipe.batch(equations)

        if args.animate:
            for eq in results:
                if results[eq].get('success'):
                    pipe.animate(eq, args.quality, output=animate_out)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(results, indent=2))
        pipe.log(f"  Saved: {args.output}", C.G)

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{C.Y}Interrupted{C.X}")
        sys.exit(130)
