#!/usr/bin/env node
'use strict';

const mathsteps = require('mathsteps');
const print = require('mathsteps/lib/util/print');

const input = process.argv[2];

if (!input) {
  console.log(JSON.stringify({ success: false, error: 'No input provided' }));
  process.exit(0);
}

const isEquation = input.includes('=');

function formatStep(step, index, phase) {
  const before = step.oldNode ? print.ascii(step.oldNode)
    : step.oldEquation ? step.oldEquation.ascii()
    : '';
  const after = step.newNode ? print.ascii(step.newNode)
    : step.newEquation ? step.newEquation.ascii()
    : '';

  const result = {
    step: index + 1,
    phase: phase,
    description: step.changeType.replace(/_/g, ' ').toLowerCase(),
    before: before,
    after: after,
  };

  if (step.substeps && step.substeps.length > 0) {
    result.substeps = step.substeps.map((sub, i) => formatStep(sub, i, phase));
  }

  return result;
}

function countSteps(steps) {
  let count = 0;
  for (const s of steps) {
    count++;
    if (s.substeps) count += countSteps(s.substeps);
  }
  return count;
}

try {
  if (!isEquation) {
    const steps = mathsteps.simplifyExpression(input);
    if (!steps || steps.length === 0) {
      console.log(JSON.stringify({ success: false, error: 'No steps found', input }));
      process.exit(0);
    }
    const formatted = steps.map((s, i) => formatStep(s, i, 'simplify'));
    console.log(JSON.stringify({
      success: true, type: 'expression', processedInput: input,
      stepCount: formatted.length, totalSteps: countSteps(formatted), steps: formatted
    }));
    process.exit(0);
  }

  // Equation: multi-phase pipeline
  const comparators = ['<=', '>=', '=', '<', '>'];
  let comparator = '=';
  let leftSide = '', rightSide = '';

  for (const comp of comparators) {
    const parts = input.split(comp);
    if (parts.length === 2) {
      comparator = comp;
      leftSide = parts[0].trim();
      rightSide = parts[1].trim();
      break;
    }
  }

  if (!leftSide || !rightSide) {
    console.log(JSON.stringify({ success: false, error: 'Invalid equation', input }));
    process.exit(0);
  }

  const allSteps = [];
  let stepNum = 0;

  // Phase 1: Simplify left side
  const leftSteps = mathsteps.simplifyExpression(leftSide);
  for (const s of leftSteps) {
    allSteps.push(formatStep(s, stepNum++, 'simplify-left'));
  }

  // Phase 2: Simplify right side
  const rightSteps = mathsteps.simplifyExpression(rightSide);
  for (const s of rightSteps) {
    allSteps.push(formatStep(s, stepNum++, 'simplify-right'));
  }

  // Get final simplified forms
  const finalLeft = leftSteps.length > 0
    ? print.ascii(leftSteps[leftSteps.length - 1].newNode)
    : leftSide;
  const finalRight = rightSteps.length > 0
    ? print.ascii(rightSteps[rightSteps.length - 1].newNode)
    : rightSide;

  // Phase 3: Solve the simplified equation
  const simplifiedEq = finalLeft + ' ' + comparator + ' ' + finalRight;
  const solveSteps = mathsteps.solveEquation(simplifiedEq);
  for (const s of solveSteps) {
    allSteps.push(formatStep(s, stepNum++, 'solve'));
  }

  if (allSteps.length === 0) {
    console.log(JSON.stringify({ success: false, error: 'No steps found', input }));
    process.exit(0);
  }

  console.log(JSON.stringify({
    success: true,
    type: 'equation',
    processedInput: input,
    simplifiedInput: simplifiedEq,
    stepCount: allSteps.length,
    totalSteps: countSteps(allSteps),
    steps: allSteps
  }));
} catch (err) {
  console.log(JSON.stringify({
    success: false,
    error: err.message,
    input: input
  }));
}
