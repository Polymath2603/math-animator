# Changelog

All notable changes to Math Animation System will be documented in this file.

## [2.0.0] - 2026-05-17

### Added
- **mathsteps as primary solver**: Detailed step-by-step solutions with substeps
- **Multi-phase pipeline**: Simplify LHS → Simplify RHS → Solve (40+ steps for complex equations)
- **LaTeX rendering**: Fractions, exponents, square roots render properly in animations
- **Permanent progress bar**: Stays on screen, only description updates per step
- **Noise step filtering**: Skip 11 types of unhelpful steps (remove adding zero, simplify left side, etc.)
- **`math_stepper.js`**: Node.js wrapper for mathsteps (was missing from repo)
- **Simpler CLI**: Positional equation arg, `-a [file.mp4]`, `-q`, `-o`, `-s`
- **`-a` accepts output filename**: `python main.py "eq" -a out.mp4`
- **sympy** added as explicit dependency in requirements.txt

### Changed
- **Solver priority**: mathsteps (primary) → SymPy CAS (fallback)
- **Animation renderer**: Uses same CAS-first pipeline as main.py
- **CLI rewrite**: Removed `-e`/`--equation` flag, positional arg instead
- **Timeout**: math_bridge timeout increased from 10s to 30s for complex equations

### Fixed
- Animation renderer was always using broken mathsteps bridge, never CAS
- Equation not passed correctly to Manim scene (read from env in `__init__`)
- Quality flags (`-q l/m/h/k`) now work (removed hardcoded 1080p60)
- Overlap between step info and equation (repositioned to upper-left)
- LaTeX conversion: sqrt before fractions, proper exponent bracing

## [1.1.0] - 2026-05-02

### Changed
- Rewrote README with simpler format

## [1.1.0] - 2026-04-11

### Added

#### TRUE CAS SOLVER (SymPy Integration)
- **Full algebraic solver**: Handles ALL equation types including:
  - Reciprocal equations: x + 1/x = c
  - Exponential: e^(2x), 4^x = 8
  - Trigonometric: sin(x)=0, tan(x)=1
  - Complex numbers: x²+x+1=0
  - Radicals: sqrt(x+5)=x-3
  - Rational: 1/x + 1/(x+1) = 1/2
- **Proper parsing**: Uses sympy.parsing.sympy_parser
- **Real step-by-step reasoning**: Shows every transformation

#### System Integration
- **Unified solver**: main.py now uses CAS + mathsteps fallback
- **Animation support**: Generate videos for ALL solvable equations
- **More equation types**: 26/30 terrifying equations now solvable

### Breaking Changes
- Animation command now requires `python main.py` (not just `manim`)

### Files Added
- `cas_solver.py` - TRUE CAS step-by-step solver
- `sympy_stepper.py` - SymPy step generator

### Test Results
- Basic equations: 100% (linear, quadratic, exponential)
- Complex equations: 87% (reciprocal, trig, radical)
- Animation generation: Working for all valid solutions

---

## [1.0.0] - 2026-01-29

### Added

#### Core Features
- **Equation Solver**: Step-by-step solving for linear and quadratic equations
- **Expression Simplifier**: Simplification of mathematical expressions
- **Beautiful Animations**: Manim-powered visualizations with:
  - Title slides
  - Step indicators
  - Progress bars
  - Celebration effects
  - Smooth transitions
- **LaTeX Support**: Parse and process LaTeX mathematical notation
- **Batch Processing**: Process multiple equations from files

#### Interfaces
- **Command-line interface** with comprehensive options
- **Telegram Bot** for easy mobile access with commands:
  - `/solve` - Solve equations
  - `/animate` - Create animations
  - `/help` - Show help
  - `/donate` - Support the project

#### Quality & Performance
- **Multiple quality presets**: Low, Medium, High, 4K
- **Configuration presets**: Fast, Presentation, Educational, Minimal
- **Optimized rendering**: Efficient video generation
- **Error handling**: Graceful failure with helpful suggestions

#### Developer Experience
- **Comprehensive testing suite**: Automated system tests
- **Setup automation**: One-command setup script
- **Documentation**: README, QUICKSTART, CONTRIBUTING guides
- **Examples**: Sample equations file included

### Technical Details

#### Improvements
- **Enhanced LaTeX parsing**: Better handling of square roots and complex notation
- **Improved error messages**: Clear, actionable error reporting
- **Better UI/UX**: Professional color scheme and typography
- **Progress indicators**: Visual feedback during long operations

#### Bug Fixes
- Fixed parsing issues with LaTeX `\sqrt{}` notation
- Improved handling of equations with no simplification steps
- Better error recovery in Node.js bridge
- Fixed animation timing inconsistencies

### Dependencies

#### Python
- manim >= 0.18.0
- python-telegram-bot >= 20.0
- numpy >= 1.24.0
- scipy >= 1.10.0

#### Node.js
- mathsteps ^0.2.0

### Known Issues

- Some complex LaTeX expressions may require preprocessing
- Very long equations might exceed Telegram message limits
- 4K rendering can be slow on older hardware

### Credits

Built with:
- [Manim Community](https://github.com/ManimCommunity/manim) - Animation engine
- [mathsteps](https://github.com/google/mathsteps) - Equation solver

For the full commit history, see: https://github.com/yourusername/math-animator/commits/main
