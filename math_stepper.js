#!/usr/bin/env node

const mathsteps = require('mathsteps');

/**
 * Enhanced Math Stepper - Solves equations or simplifies expressions step-by-step
 * Handles both equations (with =) and expressions
 * 
 * GitHub: https://github.com/google/mathsteps
 */

/**
 * Preprocess input to handle various LaTeX and math notations
 */
function preprocessInput(input) {
    if (!input || typeof input !== 'string') {
        return input;
    }
    
    let processed = input.trim();
    
    // Convert LaTeX sqrt to proper format
    // \sqrt(x+5) or \sqrt{x+5} -> sqrt(x+5)
    processed = processed.replace(/\\sqrt\s*[\(\{]([^\)\}]+)[\)\}]/g, 'sqrt($1)');
    
    // Handle other common LaTeX commands
    processed = processed.replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, '($1)/($2)');
    processed = processed.replace(/\\cdot/g, '*');
    processed = processed.replace(/\\times/g, '*');
    processed = processed.replace(/\\div/g, '/');
    
    // Remove extra backslashes that might cause issues
    processed = processed.replace(/\\/g, '');
    
    return processed;
}

/**
 * Get expression as string from various mathsteps object types
 */
function getExpressionString(expr) {
    if (!expr) return '';
    
    try {
        // Try latex() method first (most reliable)
        if (typeof expr.latex === 'function') {
            const str = expr.latex();
            if (str && str !== '[object Object]') {
                return str;
            }
        }
        
        // Try toString() method
        if (expr.toString && typeof expr.toString === 'function') {
            const str = expr.toString();
            if (str && str !== '[object Object]') {
                return str;
            }
        }
        
        // Try accessing string properties
        if (expr.string) return expr.string;
        if (expr.ascii) return expr.ascii;
        
    } catch (e) {
        console.error('Error converting expression to string:', e.message);
    }
    
    // Fallback to string conversion
    return String(expr);
}

/**
 * Generate human-readable descriptions for each transformation
 */
function generateDescription(changeType, isEquation) {
    const descriptions = {
        'simplifyArithmetic': 'Simplify arithmetic operations',
        'addSubtractTerms': 'Combine like terms',
        'multiplyByInverse': 'Multiply both sides by inverse',
        'divideByCoefficient': 'Divide both sides by coefficient',
        'distributeMultiplication': 'Distribute multiplication',
        'factorQuadratic': 'Factor quadratic expression',
        'cancelTerms': 'Cancel equivalent terms',
        'simplifyFraction': 'Simplify fraction',
        'combineUnderRoot': 'Combine terms under root',
        'divideSquares': 'Divide squared terms',
        'rearrangeTerms': 'Rearrange terms',
        'collectLikeTerms': 'Collect like terms',
        'simplifyRadical': 'Simplify radical expression',
        'addRadicals': 'Add radical terms',
        'subtractRadicals': 'Subtract radical terms',
        'isolateVariable': 'Isolate the variable',
        'moveToOneSide': 'Move all terms to one side',
        'complex': 'Apply algebraic transformation'
    };

    return descriptions[changeType] || `Apply ${changeType || 'transformation'}`;
}

/**
 * Process mathematical input and return step-by-step solution
 */
function processMathInput(input) {
    try {
        if (!input || typeof input !== 'string') {
            throw new Error('Input must be a non-empty string');
        }

        // Preprocess the input to handle LaTeX and other formats
        const processedInput = preprocessInput(input);
        const isEquation = processedInput.includes('=');
        
        let steps = [];
        let processingError = null;
        
        try {
            if (isEquation) {
                steps = mathsteps.solveEquation(processedInput);
            } else {
                steps = mathsteps.simplifyExpression(processedInput);
            }
        } catch (mathError) {
            processingError = mathError.message;
            
            // Try alternative parsing if first attempt fails
            try {
                // Remove spaces and try again
                const noSpaces = processedInput.replace(/\s+/g, '');
                if (isEquation) {
                    steps = mathsteps.solveEquation(noSpaces);
                } else {
                    steps = mathsteps.simplifyExpression(noSpaces);
                }
                processingError = null; // Clear error if successful
            } catch (retryError) {
                // If both attempts fail, keep the original error
                processingError = mathError.message;
            }
        }

        if (processingError) {
            return {
                success: false,
                error: `Math processing error: ${processingError}`,
                input: input,
                processedInput: processedInput,
                type: isEquation ? 'equation' : 'expression',
                suggestion: 'Try simplifying the input or using standard notation (e.g., sqrt(x) instead of \\sqrt{x})'
            };
        }

        if (!steps || steps.length === 0) {
            return {
                success: false,
                error: 'No steps generated. The input may already be in simplest form.',
                input: input,
                processedInput: processedInput,
                type: isEquation ? 'equation' : 'expression',
                suggestion: 'The expression might already be simplified or in a form that cannot be further reduced.'
            };
        }

        // Format steps with enhanced details
        const formattedSteps = steps.map((step, index) => {
            return {
                step: index + 1,
                before: isEquation 
                    ? getExpressionString(step.oldEquation) 
                    : getExpressionString(step.oldNode),
                after: isEquation 
                    ? getExpressionString(step.newEquation) 
                    : getExpressionString(step.newNode),
                changeType: step.changeType || 'unknown',
                description: generateDescription(step.changeType, isEquation),
                hasSubsteps: step.substeps && step.substeps.length > 0,
                substepCount: step.substeps ? step.substeps.length : 0
            };
        });

        return {
            success: true,
            input: input,
            processedInput: processedInput,
            type: isEquation ? 'equation' : 'expression',
            stepCount: steps.length,
            steps: formattedSteps
        };
    } catch (error) {
        return {
            success: false,
            error: error.message,
            input: input,
            type: 'unknown',
            suggestion: 'Please check your input format and try again.'
        };
    }
}

// Handle both direct function call and command-line execution
if (require.main === module) {
    const input = process.argv[2] || '5x+3=0';
    const result = processMathInput(input);
    console.log(JSON.stringify(result, null, 2));
} else {
    module.exports = { processMathInput, preprocessInput };
}
