#!/usr/bin/env python3
"""
Automated Math Solver & Simplifier with Animation

Main entry point for the complete system with automatic Manim integration.

This project uses:
- Manim Community: https://github.com/ManimCommunity/manim
- mathsteps: https://github.com/google/mathsteps

Author: Your Name
License: MIT
"""

import argparse
import sys
import json
import subprocess
import os
from pathlib import Path
from typing import List, Dict, Optional
from math_bridge import MathStepperBridge


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class MathAnimationPipeline:
    """Orchestrates the complete math visualization pipeline"""
    
    def __init__(self, quiet: bool = False):
        self.bridge = MathStepperBridge()
        self.quiet = quiet
        self.script_dir = Path(__file__).parent.absolute()
    
    def log(self, message: str, color: str = ""):
        """Log message if not quiet mode"""
        if not self.quiet:
            print(f"{color}{message}{Colors.RESET}")
    
    def process_equation(self, equation: str, verbose: bool = True) -> dict:
        """
        Process a single equation/expression
        
        Args:
            equation: Math input
            verbose: Whether to print detailed output
            
        Returns:
            Results with steps and metadata
        """
        if verbose:
            self.log(f"\n{'='*70}", Colors.CYAN)
            self.log(f"Processing: {equation}", Colors.BOLD)
            self.log('='*70, Colors.CYAN)
        
        result = self.bridge.get_info(equation)
        
        if not result.get('success'):
            self.log(f"❌ Error: {result.get('error')}", Colors.RED)
            if result.get('suggestion'):
                self.log(f"💡 Suggestion: {result.get('suggestion')}", Colors.YELLOW)
            return result
        
        if verbose:
            self.log(f"✓ Type: {result.get('type')}", Colors.GREEN)
            self.log(f"✓ Total Steps: {result.get('stepCount')}", Colors.GREEN)
            
            if result.get('processedInput') != equation:
                self.log(f"📝 Processed as: {result.get('processedInput')}", Colors.YELLOW)
            
            self.log("")
            
            # Print each step
            for step in result.get('steps', []):
                self.log(f"Step {step['step']}: {step['description']}", Colors.BLUE)
                self.log(f"  {step['before']}")
                self.log(f"  ↓", Colors.YELLOW)
                self.log(f"  {step['after']}", Colors.GREEN)
                if step.get('hasSubsteps'):
                    self.log(f"  [Substeps: {step['substepCount']}]", Colors.MAGENTA)
                self.log("")
        
        return result
    
    def run_animation(self, equation: str, quality: str = 'l', preview: bool = True) -> bool:
        """
        Run Manim animation for the equation
        
        Args:
            equation: Math input
            quality: Quality level (l=low, m=medium, h=high, k=4k)
            preview: Whether to open preview after rendering
            
        Returns:
            True if successful, False otherwise
        """
        self.log(f"\n🎬 Creating animation for: {equation}", Colors.CYAN + Colors.BOLD)
        
        # First validate the equation
        result = self.process_equation(equation, verbose=False)
        if not result.get('success'):
            self.log(f"❌ Cannot create animation: {result.get('error')}", Colors.RED)
            return False
        
        # Build Manim command
        animator_path = self.script_dir / "enhanced_animator.py"
        
        if not animator_path.exists():
            self.log(f"❌ Animator script not found: {animator_path}", Colors.RED)
            return False
        
        # Quality flags
        quality_flag = f"-p{quality}" if preview else f"-{quality}"
        
        cmd = [
            "manim",
            quality_flag,
            str(animator_path),
            "MathStepsAnimator",
            "--",
            "--equation",
            equation
        ]
        
        self.log(f"🔧 Running: {' '.join(cmd[:4])} ... --equation \"{equation}\"", Colors.BLUE)
        self.log("⏳ This may take a moment...\n", Colors.YELLOW)
        
        try:
            # Run Manim
            result = subprocess.run(
                cmd,
                cwd=str(self.script_dir),
                capture_output=not preview,  # Show output if previewing
                text=True
            )
            
            if result.returncode == 0:
                self.log(f"\n✅ Animation created successfully!", Colors.GREEN + Colors.BOLD)
                
                # Find the output video
                media_dir = self.script_dir / "media" / "videos" / "enhanced_animator" / (
                    "1080p60" if quality == 'h' else 
                    "2160p60" if quality == 'k' else
                    "480p15" if quality == 'l' else
                    "720p30"
                )
                
                if media_dir.exists():
                    videos = list(media_dir.glob("*.mp4"))
                    if videos:
                        latest_video = max(videos, key=lambda p: p.stat().st_mtime)
                        self.log(f"📹 Video saved to: {latest_video}", Colors.CYAN)
                
                return True
            else:
                self.log(f"❌ Animation failed with error code: {result.returncode}", Colors.RED)
                if result.stderr:
                    self.log(f"Error output: {result.stderr}", Colors.RED)
                return False
                
        except FileNotFoundError:
            self.log("❌ Manim not found! Please install it:", Colors.RED)
            self.log("   pip install manim", Colors.YELLOW)
            return False
        except Exception as e:
            self.log(f"❌ Unexpected error: {str(e)}", Colors.RED)
            return False
    
    def batch_process(self, equations: List[str]) -> Dict[str, dict]:
        """
        Process multiple equations
        
        Args:
            equations: List of math inputs
            
        Returns:
            Dictionary with results for all equations
        """
        results = {}
        success_count = 0
        error_count = 0
        
        self.log(f"\n📦 Batch Processing {len(equations)} equations...\n", Colors.CYAN + Colors.BOLD)
        
        for i, eq in enumerate(equations, 1):
            self.log(f"[{i}/{len(equations)}]", Colors.BLUE)
            result = self.process_equation(eq)
            results[eq] = result
            
            if result.get('success'):
                success_count += 1
            else:
                error_count += 1
        
        # Summary
        self.log(f"\n{'='*70}", Colors.CYAN)
        self.log("BATCH SUMMARY", Colors.BOLD)
        self.log('='*70, Colors.CYAN)
        self.log(f"Total Processed: {len(equations)}")
        self.log(f"✓ Successful: {success_count}", Colors.GREEN)
        self.log(f"✗ Errors: {error_count}", Colors.RED)
        self.log('='*70, Colors.CYAN)
        
        return results
    
    def save_results(self, results: dict, output_file: str):
        """Save results to JSON file"""
        output_path = Path(output_file)
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.log(f"\n💾 Results saved to: {output_path}", Colors.GREEN)


def print_banner():
    """Print application banner"""
    banner = f"""
{Colors.CYAN}{'='*70}
{Colors.BOLD}  Math Animation System - Step-by-Step Solver & Animator
{Colors.CYAN}{'='*70}{Colors.RESET}
  Powered by: {Colors.BLUE}Manim Community{Colors.RESET} & {Colors.BLUE}mathsteps{Colors.RESET}
  
  GitHub: 
    - https://github.com/ManimCommunity/manim
    - https://github.com/google/mathsteps
{Colors.CYAN}{'='*70}{Colors.RESET}
"""
    print(banner)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Automated Math Solver & Simplifier with Step-by-Step Animation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.BOLD}Examples:{Colors.RESET}
  {Colors.GREEN}# Solve and animate an equation{Colors.RESET}
  python main.py -e "5x+3=0" --animate
  
  {Colors.GREEN}# Process without animation{Colors.RESET}
  python main.py -e "x^2+2x+1=0"
  
  {Colors.GREEN}# Batch process from file{Colors.RESET}
  python main.py -f equations.txt --batch
  
  {Colors.GREEN}# Save results to JSON{Colors.RESET}
  python main.py -e "2x^2+4x+2=0" --save results.json
  
  {Colors.GREEN}# High quality animation{Colors.RESET}
  python main.py -e "sqrt(x+5)-2=sqrt(7-x)+3" --animate -q h

{Colors.BOLD}Quality Options:{Colors.RESET}
  l = Low quality (480p15) - Fast preview
  m = Medium quality (720p30) - Balanced
  h = High quality (1080p60) - Best for sharing
  k = 4K quality (2160p60) - Production quality

{Colors.BOLD}Supported Formats:{Colors.RESET}
  - Equations: 5x+3=0, x^2+2x+1=0
  - Expressions: 2x^2+4x+2, sqrt(x+5)
  - LaTeX: \\sqrt{{x+5}}-2=\\sqrt{{7-x}}+3
        """
    )
    
    parser.add_argument(
        '-e', '--equation',
        type=str,
        help='Single equation or expression to process'
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='File containing equations (one per line)'
    )
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Process multiple equations from file'
    )
    
    parser.add_argument(
        '--animate',
        action='store_true',
        help='Create animation with Manim'
    )
    
    parser.add_argument(
        '-q', '--quality',
        choices=['l', 'm', 'h', 'k'],
        default='l',
        help='Animation quality (default: l=low for fast preview)'
    )
    
    parser.add_argument(
        '--no-preview',
        action='store_true',
        help='Do not open preview after rendering'
    )
    
    parser.add_argument(
        '--save',
        type=str,
        metavar='FILE',
        help='Save results to JSON file'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress output'
    )
    
    args = parser.parse_args()
    
    # Print banner unless quiet
    if not args.quiet:
        print_banner()
    
    # Validate arguments
    if not args.equation and not args.file:
        parser.print_help()
        sys.exit(1)
    
    pipeline = MathAnimationPipeline(quiet=args.quiet)
    results = {}
    
    # Process equation(s)
    if args.equation:
        result = pipeline.process_equation(args.equation)
        results[args.equation] = result
        
        # Create animation if requested
        if args.animate and result.get('success'):
            success = pipeline.run_animation(
                args.equation,
                quality=args.quality,
                preview=not args.no_preview
            )
            if not success:
                sys.exit(1)
    
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"{Colors.RED}❌ File not found: {args.file}{Colors.RESET}")
            sys.exit(1)
        
        # Read equations from file
        with open(file_path, 'r') as f:
            equations = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not equations:
            print(f"{Colors.RED}❌ No equations found in: {args.file}{Colors.RESET}")
            sys.exit(1)
        
        if args.batch:
            results = pipeline.batch_process(equations)
        else:
            for eq in equations:
                results[eq] = pipeline.process_equation(eq)
    
    # Save results if requested
    if args.save:
        pipeline.save_results(results, args.save)
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠ Interrupted by user{Colors.RESET}")
        sys.exit(130)
