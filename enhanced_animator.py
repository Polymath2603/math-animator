"""
Enhanced Math Steps Animator - Creates beautiful step-by-step math animations

This uses the Manim Community library for animations.
GitHub: https://github.com/ManimCommunity/manim
Documentation: https://docs.manim.community/

Math processing powered by mathsteps:
GitHub: https://github.com/google/mathsteps
"""

from manim import *
from math_bridge import MathStepperBridge
from typing import Dict, Any
import sys


class MathStepsAnimator(Scene):
    """Main scene for animating math steps with enhanced UI"""
    
    # Configuration
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    
    # Enhanced color scheme for better visual hierarchy
    COLOR_TITLE = "#4A90E2"        # Professional blue
    COLOR_EQUATION = "#FFFFFF"     # White
    COLOR_DESCRIPTION = "#F5A623"  # Warm orange
    COLOR_RESULT = "#7ED321"       # Success green
    COLOR_HIGHLIGHT = "#FF6B6B"    # Attention red
    COLOR_STEP_BG = "#2C3E50"      # Dark blue-gray
    COLOR_ACCENT = "#9B59B6"       # Purple accent
    
    def __init__(self, equation: str = "5x+3=0", *args, **kwargs):
        """
        Initialize with an equation or expression
        
        Args:
            equation: The math input to process
        """
        super().__init__(*args, **kwargs)
        self.equation = equation
        self.bridge = MathStepperBridge()
        self.steps_data = None
        self.current_equation = None
        self.load_steps()
    
    def load_steps(self):
        """Load and validate steps from math stepper"""
        result = self.bridge.get_info(self.equation)
        
        if not result.get('success'):
            print(f"❌ Error loading steps: {result.get('error')}")
            if result.get('suggestion'):
                print(f"💡 Suggestion: {result.get('suggestion')}")
            self.steps_data = []
        else:
            self.steps_data = result.get('steps', [])
            print(f"✓ Loaded {len(self.steps_data)} steps for: {self.equation}")
    
    def construct(self):
        """Main animation construction"""
        if not self.steps_data:
            self.show_error("Failed to process input", self.equation)
            return
        
        # Set background color
        self.camera.background_color = "#1a1a2e"
        
        # Create title with animation
        self.create_title()
        self.wait(1)
        
        # Show initial equation/expression
        self.show_initial_equation()
        self.wait(1.5)
        
        # Animate through each step with progress indicator
        for step_index, step in enumerate(self.steps_data):
            self.animate_step(step_index, step)
            self.wait(1.5)
        
        # Show final result with celebration
        self.show_final_result()
        self.wait(2)
    
    def create_title(self):
        """Create and animate the title with improved styling"""
        problem_type = "Equation Solver" if '=' in self.equation else "Expression Simplifier"
        
        # Main title
        title = Text(
            problem_type,
            font_size=52,
            color=self.COLOR_TITLE,
            weight=BOLD
        ).move_to(UP * 3.5)
        
        # Subtitle with the problem
        subtitle = MathTex(
            self.equation,
            font_size=38,
            color=self.COLOR_EQUATION
        ).next_to(title, DOWN, buff=0.4)
        
        # Background decoration
        title_underline = Line(
            start=title.get_left() + LEFT * 0.5,
            end=title.get_right() + RIGHT * 0.5,
            color=self.COLOR_TITLE,
            stroke_width=3
        ).next_to(title, DOWN, buff=0.15)
        
        # Animate title appearance
        self.play(
            Write(title, run_time=1.2),
            Create(title_underline, run_time=1.2)
        )
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        
        self.title_group = VGroup(title, subtitle, title_underline)
    
    def show_initial_equation(self):
        """Display the initial equation/expression with styling"""
        first_step = self.steps_data[0]
        
        # Create equation with border
        equation_tex = MathTex(
            first_step['before'],
            font_size=44,
            color=self.COLOR_EQUATION
        ).move_to(ORIGIN)
        
        # Add subtle background box
        equation_box = SurroundingRectangle(
            equation_tex,
            color=self.COLOR_STEP_BG,
            buff=0.3,
            stroke_width=2,
            corner_radius=0.1,
            fill_opacity=0.1,
            fill_color=self.COLOR_STEP_BG
        )
        
        self.current_equation = equation_tex
        self.current_box = equation_box
        
        # Animate appearance
        self.play(
            Create(equation_box, run_time=0.8),
            Write(equation_tex, run_time=1.2)
        )
    
    def animate_step(self, step_index: int, step: Dict[str, Any]):
        """
        Animate a single step with enhanced visuals
        
        Args:
            step_index: Index of current step (0-based)
            step: Step data from math stepper
        """
        total_steps = len(self.steps_data)
        
        # Create step indicator
        step_indicator = Text(
            f"Step {step['step']} of {total_steps}",
            font_size=20,
            color=self.COLOR_DESCRIPTION,
            weight=BOLD
        ).to_edge(UP, buff=2.2).to_edge(LEFT, buff=0.5)
        
        # Progress bar
        progress = step_index / total_steps
        progress_bar = Rectangle(
            width=progress * 6,
            height=0.15,
            fill_color=self.COLOR_ACCENT,
            fill_opacity=1,
            stroke_width=0
        ).next_to(step_indicator, DOWN, buff=0.2).align_to(step_indicator, LEFT)
        
        progress_bg = Rectangle(
            width=6,
            height=0.15,
            fill_color=self.COLOR_STEP_BG,
            fill_opacity=0.3,
            stroke_width=1,
            stroke_color=self.COLOR_STEP_BG
        ).move_to(progress_bar, aligned_edge=LEFT)
        
        # Description box with improved styling
        description = Text(
            step['description'],
            font_size=26,
            color=self.COLOR_DESCRIPTION
        ).next_to(progress_bg, DOWN, buff=0.4).align_to(step_indicator, LEFT)
        
        description_box = SurroundingRectangle(
            description,
            color=self.COLOR_DESCRIPTION,
            buff=0.2,
            stroke_width=2,
            corner_radius=0.08,
            fill_opacity=0.05,
            fill_color=self.COLOR_DESCRIPTION
        )
        
        # Show step info with animation
        self.play(
            FadeIn(step_indicator, shift=RIGHT * 0.3),
            Create(progress_bg),
            Create(progress_bar),
            run_time=0.5
        )
        self.play(
            Write(description, run_time=0.7),
            Create(description_box, run_time=0.7)
        )
        
        # Create new equation
        new_equation = MathTex(
            step['after'],
            font_size=44,
            color=self.COLOR_RESULT
        ).move_to(ORIGIN)
        
        new_box = SurroundingRectangle(
            new_equation,
            color=self.COLOR_RESULT,
            buff=0.3,
            stroke_width=2,
            corner_radius=0.1,
            fill_opacity=0.1,
            fill_color=self.COLOR_STEP_BG
        )
        
        # Animate transformation with smooth transition
        self.play(
            ReplacementTransform(self.current_equation, new_equation),
            ReplacementTransform(self.current_box, new_box),
            run_time=1.5
        )
        
        # Update references
        self.current_equation = new_equation
        self.current_box = new_box
        
        # Remove step info after showing
        self.play(
            FadeOut(step_indicator),
            FadeOut(description_box),
            FadeOut(description),
            FadeOut(progress_bar),
            FadeOut(progress_bg),
            run_time=0.6
        )
    
    def show_final_result(self):
        """Highlight and celebrate the final result"""
        # Final label
        final_label = Text(
            "✓ Solution Complete!",
            font_size=36,
            color=self.COLOR_RESULT,
            weight=BOLD
        ).to_edge(DOWN, buff=1.5)
        
        # Create glowing effect
        glow_circle = Circle(
            radius=2.5,
            stroke_color=self.COLOR_RESULT,
            stroke_width=4,
            fill_opacity=0,
        ).move_to(self.current_equation)
        
        # Sparkle effect
        stars = VGroup(*[
            Star(n=5, outer_radius=0.15, color=self.COLOR_RESULT, fill_opacity=1)
            .move_to(self.current_equation.get_corner(corner) + corner * 0.5)
            for corner in [UL, UR, DL, DR]
        ])
        
        # Animate celebration
        self.play(
            Create(glow_circle, run_time=1),
            FadeIn(final_label, shift=UP * 0.3, run_time=1)
        )
        self.play(
            glow_circle.animate.scale(1.15).set_stroke(opacity=0.5),
            FadeIn(stars, lag_ratio=0.3),
            run_time=1
        )
        self.play(
            glow_circle.animate.scale(0.95).set_stroke(opacity=1),
            stars.animate.scale(1.2).set_opacity(0.7),
            run_time=0.5
        )
    
    def show_error(self, message: str, details: str = ""):
        """Show error message with helpful information"""
        # Error icon
        error_icon = Text("⚠", font_size=80, color=RED).move_to(UP * 1)
        
        # Error message
        error_text = Text(
            message,
            font_size=32,
            color=RED,
            weight=BOLD
        ).next_to(error_icon, DOWN, buff=0.5)
        
        # Details
        if details:
            details_text = Text(
                details,
                font_size=20,
                color=GRAY,
                slant=ITALIC
            ).next_to(error_text, DOWN, buff=0.3)
        
        # Background box
        error_group = VGroup(error_icon, error_text)
        if details:
            error_group.add(details_text)
        
        error_box = SurroundingRectangle(
            error_group,
            color=RED,
            buff=0.5,
            stroke_width=3,
            corner_radius=0.2,
            fill_opacity=0.1,
            fill_color=RED
        )
        
        # Animate error display
        self.play(
            Create(error_box, run_time=1),
            FadeIn(error_icon, scale=1.5, run_time=1)
        )
        self.play(Write(error_text, run_time=1))
        if details:
            self.play(FadeIn(details_text, run_time=0.8))
        
        self.wait(3)


# CLI argument parsing for Manim
if __name__ == "__main__":
    # Handle custom equation argument
    equation = "5x+3=0"  # Default
    
    # Parse custom arguments
    if "--equation" in sys.argv:
        try:
            eq_index = sys.argv.index("--equation")
            if eq_index + 1 < len(sys.argv):
                equation = sys.argv[eq_index + 1]
        except (ValueError, IndexError):
            pass
    
    # Set equation for scene
    MathStepsAnimator.equation_to_solve = equation
