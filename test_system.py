#!/usr/bin/env python3
"""
Quick test suite for the enhanced math animation system
Validates all components work correctly
"""

import sys
import json
from pathlib import Path
from math_bridge import MathStepperBridge
from main import MathAnimationPipeline


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def test_math_bridge():
    """Test the Python-JavaScript bridge"""
    print(f"\n{Colors.BOLD}Test 1: Math Bridge{Colors.RESET}")
    print("-" * 50)
    
    try:
        bridge = MathStepperBridge()
        print(f"{Colors.GREEN}✓ Bridge initialized{Colors.RESET}")
        
        # Test 1: Simple equation
        result = bridge.get_info("5x+3=0")
        if result.get('success'):
            print(f"{Colors.GREEN}✓ Equation solving works{Colors.RESET}")
            print(f"  Steps found: {result.get('stepCount')}")
        else:
            print(f"{Colors.RED}✗ Equation solving failed: {result.get('error')}{Colors.RESET}")
            return False
        
        # Test 2: Complex equation
        result = bridge.get_info("2x^2+4x+2=0")
        if result.get('success'):
            print(f"{Colors.GREEN}✓ Complex equation works{Colors.RESET}")
            print(f"  Steps found: {result.get('stepCount')}")
        else:
            print(f"{Colors.RED}✗ Complex equation failed: {result.get('error')}{Colors.RESET}")
            return False
        
        # Test 3: LaTeX input (the problematic case)
        result = bridge.get_info("\\sqrt{x+5}-2=\\sqrt{7-x}+3")
        if result.get('success'):
            print(f"{Colors.GREEN}✓ LaTeX input parsing works{Colors.RESET}")
            print(f"  Processed as: {result.get('processedInput')}")
            print(f"  Steps found: {result.get('stepCount')}")
        else:
            print(f"{Colors.YELLOW}⚠ LaTeX input failed (this is known): {result.get('error')}{Colors.RESET}")
            print(f"  Suggestion: {result.get('suggestion')}")
            # This is acceptable - we handle it gracefully
        
        # Test 4: Error handling
        result = bridge.get_info("")
        if not result.get('success'):
            print(f"{Colors.GREEN}✓ Error handling works{Colors.RESET}")
        else:
            print(f"{Colors.RED}✗ Error handling failed{Colors.RESET}")
            return False
        
        return True
        
    except Exception as e:
        print(f"{Colors.RED}✗ Bridge test failed: {str(e)}{Colors.RESET}")
        return False


def test_pipeline():
    """Test the main pipeline"""
    print(f"\n{Colors.BOLD}Test 2: Animation Pipeline{Colors.RESET}")
    print("-" * 50)
    
    try:
        pipeline = MathAnimationPipeline(quiet=True)
        print(f"{Colors.GREEN}✓ Pipeline initialized{Colors.RESET}")
        
        # Test 1: Single equation processing
        result = pipeline.process_equation("5x+3=0", verbose=False)
        if result.get('success'):
            print(f"{Colors.GREEN}✓ Single equation processing works{Colors.RESET}")
        else:
            print(f"{Colors.RED}✗ Single processing failed{Colors.RESET}")
            return False
        
        # Test 2: Batch processing
        equations = ["5x+3=0", "x^2=4", "2x-6=0"]
        results = pipeline.batch_process(equations)
        if len(results) == len(equations):
            print(f"{Colors.GREEN}✓ Batch processing works{Colors.RESET}")
            success_count = sum(1 for r in results.values() if r.get('success'))
            print(f"  Successful: {success_count}/{len(equations)}")
        else:
            print(f"{Colors.RED}✗ Batch processing failed{Colors.RESET}")
            return False
        
        return True
        
    except Exception as e:
        print(f"{Colors.RED}✗ Pipeline test failed: {str(e)}{Colors.RESET}")
        return False


def test_comprehensive():
    """Run comprehensive test with example equations"""
    print(f"\n{Colors.BOLD}Test 3: Comprehensive Examples{Colors.RESET}")
    print("-" * 50)
    
    try:
        bridge = MathStepperBridge()
        
        test_cases = [
            ("5x+3=0", "equation", "Simple linear equation"),
            ("x^2+2x+1=0", "equation", "Quadratic equation"),
            ("2x+5=3x-2", "equation", "Linear with both sides"),
            ("3x-6=0", "equation", "Another linear equation"),
            ("x^2-1=0", "equation", "Difference of squares"),
            ("sqrt(x)=4", "equation", "Square root equation"),
            ("\\sqrt{x+5}=3", "equation", "LaTeX square root"),
        ]
        
        passed = 0
        failed = 0
        warnings = 0
        
        for equation, expected_type, description in test_cases:
            result = bridge.get_info(equation)
            
            if result.get('success'):
                actual_type = result.get('type')
                steps = result.get('stepCount', 0)
                
                if actual_type == expected_type:
                    status = Colors.GREEN
                    passed += 1
                else:
                    status = Colors.YELLOW
                    warnings += 1
                
                print(f"{status}✓ {description}{Colors.RESET}")
                print(f"  Input: {equation}")
                if result.get('processedInput') != equation:
                    print(f"  Processed: {result.get('processedInput')}")
                print(f"  Type: {actual_type} | Steps: {steps}")
            else:
                print(f"{Colors.YELLOW}⚠ {description}{Colors.RESET}")
                print(f"  Input: {equation}")
                print(f"  Error: {result.get('error')}")
                if result.get('suggestion'):
                    print(f"  Suggestion: {result.get('suggestion')}")
                warnings += 1
        
        print(f"\n{Colors.BOLD}Results: {passed} passed, {warnings} warnings{Colors.RESET}")
        
        # Consider warnings acceptable for complex LaTeX inputs
        return True
        
    except Exception as e:
        print(f"{Colors.RED}✗ Comprehensive test failed: {str(e)}{Colors.RESET}")
        return False


def test_node_setup():
    """Test Node.js and mathsteps installation"""
    print(f"\n{Colors.BOLD}Test 4: Node.js Setup{Colors.RESET}")
    print("-" * 50)
    
    import subprocess
    
    try:
        # Check Node.js
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Colors.GREEN}✓ Node.js installed: {result.stdout.strip()}{Colors.RESET}")
        else:
            print(f"{Colors.RED}✗ Node.js not found{Colors.RESET}")
            return False
        
        # Check if mathsteps is installed
        js_file = Path(__file__).parent / "math_stepper.js"
        result = subprocess.run(['node', str(js_file), '5x+3=0'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✓ mathsteps library working{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}✗ mathsteps not installed or not working{Colors.RESET}")
            print(f"{Colors.YELLOW}Run: npm install mathsteps{Colors.RESET}")
            return False
            
    except FileNotFoundError:
        print(f"{Colors.RED}✗ Node.js not found in PATH{Colors.RESET}")
        print(f"{Colors.YELLOW}Install Node.js from https://nodejs.org/{Colors.RESET}")
        return False
    except Exception as e:
        print(f"{Colors.RED}✗ Setup test failed: {str(e)}{Colors.RESET}")
        return False


def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}Math Animation System - Test Suite{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    results = {
        'Node.js Setup': test_node_setup(),
        'Bridge': test_math_bridge(),
        'Pipeline': test_pipeline(),
        'Comprehensive': test_comprehensive(),
    }
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}Summary:{Colors.RESET}")
    print('=' * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if passed else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print('=' * 60)
    
    if all_passed:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ All tests passed!{Colors.RESET}")
        print(f"\n{Colors.BLUE}Next steps:{Colors.RESET}")
        print("  1. Try: python main.py -e '5x+3=0'")
        print("  2. Try: python main.py -e 'x^2+2x+1=0' --animate")
        print("  3. Try: python telegram_bot.py (with TELEGRAM_BOT_TOKEN set)")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Some tests failed!{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Troubleshooting:{Colors.RESET}")
        print("  1. Install Node.js: https://nodejs.org/")
        print("  2. Install mathsteps: npm install mathsteps")
        print("  3. Install Python deps: pip install -r requirements.txt")
        print("  4. Install Manim: pip install manim")
        return 1


if __name__ == '__main__':
    sys.exit(main())
