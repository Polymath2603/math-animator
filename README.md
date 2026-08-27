# Math Animator 📐

Lightweight Python tool that generates Manim-style math animation videos
using a step-based API. Renders frames with Pillow and encodes with FFmpeg
(optional Manim for higher quality). Solves equations step-by-step via
**mathsteps** (Node.js) or **SymPy** (fallback), then animates each step.

> 🛠️ **Vibe-coded.** Built with AI assistance; no formal review. Works for the
> documented commands.

## Status

Archived — feature-complete for the core pipeline; kept as a reference.

## Quick start

```bash
pip install pillow numpy ffmpeg-python sympy
# optional: node + mathsteps for richer step solving
python main.py "5x+3=0"              # solve
python main.py "5x+3=0" -a           # solve + animate (needs manim)
python main.py -f equations.txt      # batch
```

## Architecture

```
main.py           CLI entry + pipeline orchestrator
enhanced_animator.py  Manim scene
math_bridge.py    Node.js mathsteps bridge
cas_solver.py     SymPy CAS fallback
telegram_bot.py   solve/animate via Telegram
```

## Known issues / Limitations

- mathsteps requires Node; without it, SymPy fallback is used.
- Manim is optional but needed for the `-a` animation path.

## License

MIT (see LICENSE)
