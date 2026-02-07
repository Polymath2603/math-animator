"""
Python bridge to connect with the math stepper JavaScript module.
Executes the JS math stepper and parses results for use in animations.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

class MathStepperBridge:
    """Bridge between Python and JavaScript math stepper"""
    
    def __init__(self, js_file: str = None):
        """
        Initialize the bridge with path to JS stepper
        
        Args:
            js_file: Path to math_stepper.js (auto-detected if None)
        """
        if js_file is None:
            # Auto-detect JS file in same directory as this script
            current_dir = Path(__file__).parent
            js_file = current_dir / 'math_stepper.js'
        
        self.js_file = Path(js_file)
        if not self.js_file.exists():
            raise FileNotFoundError(f"Math stepper JS file not found: {js_file}")
    
    def process_input(self, input_string: str) -> Dict[str, Any]:
        """
        Process math input (equation or expression) through math stepper
        
        Args:
            input_string: Mathematical equation or expression
            
        Returns:
            Dictionary with steps and metadata
        """
        if not input_string or not isinstance(input_string, str):
            return {
                'success': False,
                'error': 'Input must be a non-empty string',
                'input': input_string
            }
        
        try:
            # Execute Node.js script with input
            result = subprocess.run(
                ['node', str(self.js_file), input_string],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': result.stderr or 'Unknown error from math stepper',
                    'input': input_string
                }
            
            # Parse JSON output
            try:
                output = json.loads(result.stdout)
                return output
            except json.JSONDecodeError as e:
                return {
                    'success': False,
                    'error': f'Invalid JSON output from math stepper: {e}',
                    'input': input_string,
                    'raw_output': result.stdout
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Math stepper process timed out',
                'input': input_string
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'input': input_string
            }
    
    def get_steps(self, input_string: str) -> Optional[List[Dict[str, Any]]]:
        """Get steps if successful, None otherwise"""
        result = self.process_input(input_string)
        return result.get('steps') if result.get('success') else None
    
    def get_info(self, input_string: str) -> Dict[str, Any]:
        """Get full result information"""
        return self.process_input(input_string)


# Example usage and testing
if __name__ == '__main__':
    bridge = MathStepperBridge()
    
    # Test cases
    test_inputs = [
        '5x+3=0',
        'x^2+2x+1=0',
        '2x^2 + 4x + 2',
        '3(x+2) + 5x - 1'
    ]
    
    for test_input in test_inputs:
        print(f"\n{'='*60}")
        print(f"Input: {test_input}")
        print('='*60)
        
        result = bridge.get_info(test_input)
        
        if result.get('success'):
            print(f"Type: {result.get('type')}")
            print(f"Steps: {result.get('stepCount')}\n")
            
            for step in result.get('steps', []):
                print(f"Step {step['step']}: {step['description']}")
                print(f"  {step['before']} → {step['after']}")
        else:
            print(f"Error: {result.get('error')}")
