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
