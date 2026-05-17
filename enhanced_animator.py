"""
Enhanced Math Steps Animator - Creates beautiful step-by-step math animations

This uses the Manim Community library for animations.
GitHub: https://github.com/ManimCommunity/manim
Documentation: https://docs.manim.community/

Math processing powered by mathsteps (primary) and SymPy (fallback).
"""

from manim import *
from typing import Dict, Any
import sys
import os
import re

# Try mathsteps bridge first (primary - detailed steps)
try:
    from math_bridge import MathStepperBridge
    HAS_BRIDGE = True
except ImportError:
    HAS_BRIDGE = False

# Fallback to CAS solver (SymPy)
try:
    from cas_solver import solve_with_steps as cas_solve
    HAS_CAS = True
except ImportError:
    HAS_CAS = False

# Steps that add no value to the animation
SKIP_DESCRIPTIONS = {
    'remove adding zero',
    'remove multiplying by one',
    'multiply by zero',
    'multiply by one',
    'remove multiplying by zero',
}


def ascii_to_latex(expr: str) -> str:
    """Convert ASCII math from mathsteps to LaTeX for MathTex"""
    if not expr:
        return ''

    s = expr.strip()

    # Fractions: a/b -> \frac{a}{b}
    # Match: (expr)/(expr) or number/number or var/var
    def replace_frac(m):
        num = m.group(1).strip()
        den = m.group(2).strip()
        # Wrap in braces if contains + or -
        if re.search(r'[+\-]', num) and not (num.startswith('(') and num.endswith(')')):
            num = f'({num})'
        if re.search(r'[+\-]', den) and not (den.startswith('(') and den.endswith(')')):
            den = f'({den})'
        return f'\\frac{{{num}}}{{{den}}}'

    # Handle nested fractions by repeatedly applying
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r'\(([^()]+)\)\s*/\s*\(([^()]+)\)', replace_frac, s)

    # Simple fractions without parens: 3/5, x/2, -14/-12
    s = re.sub(r'(-?\w+)\s*/\s*(-?\w+)', replace_frac, s)

    # Exponents: x^2 -> x^{2}, (x+1)^3 -> (x+1)^{3}
    s = re.sub(r'\^(\w)', r'^{\1}', s)
    s = re.sub(r'\^(\([^)]+\))', r'^{\1}', s)

    # Multiplication: * -> \cdot
    s = s.replace('*', r' \cdot ')

    # Square root: sqrt(x) -> \sqrt{x}
    s = re.sub(r'sqrt\(([^)]+)\)', r'\\sqrt{\1}', s)

    # Comparison operators
    s = s.replace('<=', r' \leq ')
    s = s.replace('>=', r' \geq ')

    # Clean up spacing
    s = re.sub(r'\s+', ' ', s).strip()

    return s


def get_equation_from_env() -> str:
    """Read equation from environment variable"""
    return os.environ.get('MATH_EQUATION', '5x+3=0')


class MathStepsAnimator(Scene):
    """Main scene for animating math steps with enhanced UI"""

    # Color scheme
    COLOR_TITLE = "#4A90E2"
    COLOR_EQUATION = "#FFFFFF"
    COLOR_DESCRIPTION = "#F5A623"
    COLOR_RESULT = "#7ED321"
    COLOR_HIGHLIGHT = "#FF6B6B"
    COLOR_STEP_BG = "#2C3E50"
    COLOR_ACCENT = "#9B59B6"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.equation = get_equation_from_env()
        self.steps_data = None
        self.current_equation = None
        self.load_steps()

    def load_steps(self):
        """Load steps using mathsteps first, CAS as fallback"""
        if HAS_BRIDGE:
            try:
                bridge = MathStepperBridge()
                result = bridge.get_info(self.equation)
                if result.get('success'):
                    raw = result.get('steps', [])
                    self.steps_data = self._flatten_and_filter(raw)
                    print(f"✓ mathsteps: {len(self.steps_data)} steps for: {self.equation}")
                    return
            except Exception as e:
                print(f"mathsteps failed: {e}")

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

        print(f"❌ No solver available for: {self.equation}")
        self.steps_data = []

    def _flatten_and_filter(self, steps):
        """Flatten substeps and filter out noise steps"""
        flat = []
        for step in steps:
            desc = step.get('description', '')
            if desc.lower().strip() in SKIP_DESCRIPTIONS:
                continue
            flat.append({
                'step': len(flat) + 1,
                'description': desc,
                'before': step.get('before', ''),
                'after': step.get('after', ''),
                'phase': step.get('phase', '')
            })
            for sub in step.get('substeps', []):
                sub_desc = sub.get('description', '')
                if sub_desc.lower().strip() in SKIP_DESCRIPTIONS:
                    continue
                flat.append({
                    'step': len(flat) + 1,
                    'description': '  ↳ ' + sub_desc,
                    'before': sub.get('before', ''),
                    'after': sub.get('after', ''),
                    'phase': sub.get('phase', '')
                })
        return flat

    def construct(self):
        """Main animation construction"""
        if not self.steps_data:
            self.show_error("Failed to process input", self.equation)
            return

        self.camera.background_color = "#1a1a2e"

        self.create_title()
        self.wait(1)

        self.show_initial_equation()
        self.wait(1.5)

        for step_index, step in enumerate(self.steps_data):
            self.animate_step(step_index, step)
            self.wait(1)

        self.show_final_result()
        self.wait(2)

    def create_title(self):
        """Create and animate the title"""
        problem_type = "Equation Solver" if '=' in self.equation else "Expression Simplifier"

        title = Text(
            problem_type,
            font_size=48,
            color=self.COLOR_TITLE,
            weight=BOLD
        ).to_edge(UP, buff=0.4)

        subtitle = MathTex(
            ascii_to_latex(self.equation),
            font_size=36,
            color=self.COLOR_EQUATION
        ).next_to(title, DOWN, buff=0.3)

        title_underline = Line(
            start=title.get_left() + LEFT * 0.3,
            end=title.get_right() + RIGHT * 0.3,
            color=self.COLOR_TITLE,
            stroke_width=2
        ).next_to(title, DOWN, buff=0.1)

        self.play(Write(title, run_time=1), Create(title_underline, run_time=1))
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.6)

        self.title_group = VGroup(title, subtitle, title_underline)

    def show_initial_equation(self):
        """Display the initial equation"""
        first = self.steps_data[0]
        tex = MathTex(
            ascii_to_latex(first['before']),
            font_size=42,
            color=self.COLOR_EQUATION
        ).move_to(DOWN * 0.5)

        box = SurroundingRectangle(
            tex, color=self.COLOR_STEP_BG, buff=0.25,
            stroke_width=2, corner_radius=0.1,
            fill_opacity=0.08, fill_color=self.COLOR_STEP_BG
        )

        self.current_equation = tex
        self.current_box = box

        self.play(Create(box, run_time=0.6), Write(tex, run_time=1))

    def animate_step(self, step_index: int, step: Dict[str, Any]):
        """Animate a single step"""
        total = len(self.steps_data)

        # Step label (top-left, compact)
        label = Text(
            f"Step {step['step']}/{total}",
            font_size=18,
            color=self.COLOR_DESCRIPTION,
            weight=BOLD
        ).to_corner(UL, buff=0.3).shift(DOWN * 1.2)

        # Progress bar
        frac = (step_index + 1) / total
        bar_bg = Rectangle(width=4, height=0.1, fill_color=GRAY,
                           fill_opacity=0.2, stroke_width=0)
        bar_fg = Rectangle(width=4 * frac, height=0.1, fill_color=self.COLOR_ACCENT,
                           fill_opacity=1, stroke_width=0)
        bar = VGroup(bar_bg, bar_fg).next_to(label, DOWN, buff=0.15).align_to(label, LEFT)

        # Description
        desc = Text(
            step['description'],
            font_size=22,
            color=self.COLOR_DESCRIPTION
        ).next_to(bar, DOWN, buff=0.3).align_to(label, LEFT)

        # Phase tag if present
        phase_tag = None
        if step.get('phase'):
            phase_tag = Text(
                step['phase'],
                font_size=14,
                color=self.COLOR_ACCENT
            ).next_to(desc, RIGHT, buff=0.3)

        # New equation
        new_tex = MathTex(
            ascii_to_latex(step['after']),
            font_size=42,
            color=self.COLOR_RESULT
        ).move_to(DOWN * 0.5)

        new_box = SurroundingRectangle(
            new_tex, color=self.COLOR_RESULT, buff=0.25,
            stroke_width=2, corner_radius=0.1,
            fill_opacity=0.08, fill_color=self.COLOR_STEP_BG
        )

        # Show step info
        anims = [
            FadeIn(label, shift=RIGHT * 0.2),
            Create(bar_bg), Create(bar_fg),
            Write(desc, run_time=0.5),
        ]
        if phase_tag:
            anims.append(FadeIn(phase_tag))
        self.play(*anims, run_time=0.6)

        # Transform equation
        self.play(
            ReplacementTransform(self.current_equation, new_tex),
            ReplacementTransform(self.current_box, new_box),
            run_time=1.2
        )

        self.current_equation = new_tex
        self.current_box = new_box

        # Clean up step info
        outs = [FadeOut(label), FadeOut(bar_bg), FadeOut(bar_fg), FadeOut(desc)]
        if phase_tag:
            outs.append(FadeOut(phase_tag))
        self.play(*outs, run_time=0.4)

    def show_final_result(self):
        """Celebrate the final result"""
        final_label = Text(
            "Solution Complete!",
            font_size=32,
            color=self.COLOR_RESULT,
            weight=BOLD
        ).to_edge(DOWN, buff=1.2)

        glow = Circle(
            radius=2, stroke_color=self.COLOR_RESULT,
            stroke_width=3, fill_opacity=0
        ).move_to(self.current_equation)

        stars = VGroup(*[
            Star(n=5, outer_radius=0.12, color=self.COLOR_RESULT, fill_opacity=1)
            .move_to(self.current_equation.get_corner(c) + c * 0.4)
            for c in [UL, UR, DL, DR]
        ])

        self.play(Create(glow, run_time=0.8), FadeIn(final_label, shift=UP * 0.2))
        self.play(
            glow.animate.scale(1.1).set_stroke(opacity=0.5),
            FadeIn(stars, lag_ratio=0.3),
            run_time=0.8
        )
        self.play(
            glow.animate.scale(0.9).set_stroke(opacity=1),
            stars.animate.scale(1.1).set_opacity(0.7),
            run_time=0.4
        )

    def show_error(self, message: str, details: str = ""):
        """Show error message"""
        icon = Text("!", font_size=60, color=RED).move_to(UP * 0.5)
        text = Text(message, font_size=28, color=RED, weight=BOLD).next_to(icon, DOWN, buff=0.4)

        group = VGroup(icon, text)
        if details:
            det = Text(details, font_size=18, color=GRAY).next_to(text, DOWN, buff=0.2)
            group.add(det)

        box = SurroundingRectangle(
            group, color=RED, buff=0.4, stroke_width=2,
            corner_radius=0.15, fill_opacity=0.08, fill_color=RED
        )

        self.play(Create(box), FadeIn(icon, scale=1.3))
        self.play(Write(text))
        if details:
            self.play(FadeIn(det))
        self.wait(2)


if __name__ == "__main__":
    pass
