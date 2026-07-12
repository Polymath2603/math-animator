# Math Animator 📐

> A lightweight Python tool that generates Manim-style math animation videos using a step-based API. No heavy Manim dependency required at the core — renders frames with Pillow and encodes with FFmpeg, with optional Manim integration for high-quality output.

Solves equations step-by-step using **mathsteps** (Node.js, primary) or **SymPy** (CAS, fallback), then produces animated video walkthroughs of each solution step.

## Status

Active development 🟢

## Features

- **Dual-solver pipeline** — mathsteps for detailed step-by-step solving, SymPy CAS as fallback
- **Step-based animation** — renders each solving step as a discrete animation frame
- **Video output** — MP4 via FFmpeg (Manim optional for richer animations)
- **Telegram bot** — solve and animate via Telegram messages
- **Batch processing** — solve or animate multiple equations from a file
- **Configurable** — animation styles, colors, timing, and quality presets
- **ASCII-to-LaTeX conversion** — automatically translates plain math notation to rendered math

## Architecture

```
math-animator/
├── main.py                — CLI entry point & pipeline orchestrator
├── enhanced_animator.py   — Manim-based animation scene
├── math_bridge.py         — Bridge to Node.js mathsteps solver
├── cas_solver.py          — SymPy CAS fallback solver
├── config.py              — Animation colors, timing, and behavior settings
├── telegram_bot.py        — Telegram bot interface
├── test_system.py         — Integration tests
├── docs/                  — Documentation
├── examples/              — Usage examples
└── CHANGELOG.md
```

## Quick Start

```bash
# Solve an equation
python main.py "5x+3=0"

# Solve and animate (requires manim)
python main.py "5x+3=0" -a

# Batch solve from file
python main.py -f equations.txt
```

## Requirements

- Python 3.8+
- Pillow, SymPy (core)
- Node.js + mathsteps (detailed step solving)
- Manim Community (optional, for video rendering)

## Support

If you find this useful, consider supporting development:

| Method | Address / ID |
|---|---|
| PayPal | `paypal.com/ncp/payment/W78F6W4TXZ4CS` |
| Binance | `1011264323` |
| Bybit | `467077834` |
| TRC20 (USDT) | `TMW5uSDN6sMUBNirMoqY1icpsfa7GhPZfK` |
| BEP20 / ERC20 | `0x7a8887c2ac3e596f6170c9e28b44e6b6d025c854` |
| LTC | `LVswXiD6Vd2dejXvGbZLa1R8jkvg748F4q` |
| TON | `UQAllRezWgHi3LPrSwyvAb4zazIph6j6goU7lMaqcFWFBxVH` |
| BTC | `1rSX6BDN1nqDMyBHqceySkZSs6PHUP23m` |
| SOL | `d8RonhC8oEHssrQjN1Y4UWHnd6MMP33XGCKtfNL4j59` |
