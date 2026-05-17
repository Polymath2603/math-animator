# Math Animation System

Step-by-step math equation solver with animated visualizations.

## Features

- **mathsteps** as primary solver (detailed step-by-step with substeps)
- **SymPy CAS** as fallback for equations mathsteps can't handle
- Manim animations with permanent progress bar and LaTeX rendering
- Telegram bot interface
- Batch processing and JSON export

## Quick Start

```bash
pip install -r requirements.txt
npm install

# Solve
python main.py "5x+3=0"

# Solve + animate
python main.py "5x+3=0" -a

# Save animation to file
python main.py "5x+3=0" -a output.mp4

# High quality
python main.py "5x+3=0" -a -q h

# Batch
python main.py -f equations.txt

# JSON export
python main.py "5x+3=0" -o results.json
```

## CLI Reference

```
python main.py [equation] [options]

positional:
  equation              equation to solve

options:
  -f FILE, --file FILE  equations file (one per line)
  -a, --animate [FILE]  render animation (optionally specify output .mp4)
  -q {l,m,h,k}         animation quality (default: l)
  -o FILE, --output     save results as JSON
  -s, --silent          quiet output

quality: l=480p15  m=720p30  h=1080p60  k=2160p60
```

## How It Works

The solver uses a multi-phase pipeline:

1. **mathsteps** (Node.js) — primary solver, produces detailed step-by-step solutions
   - Phase 1: Simplify left side (expand, distribute, collect)
   - Phase 2: Simplify right side
   - Phase 3: Solve the simplified equation
2. **SymPy CAS** (Python) — fallback for equations mathsteps can't handle

## Supported Equations

- Linear: `5x + 3 = 0`
- Quadratic: `x^2 + 2x + 1 = 0`
- Polynomial: `(x+2)^3 - (x-2)^3 = (2x+1)^3 - (2x-1)^3`
- Exponential: `e^(2x) = 4`
- Trigonometric: `sin(x) = 0`
- Radicals: `sqrt(x+5) = x - 3`
- Rational: `(x^2+1)/(x-1) = 3`
- Complex roots, reciprocal, polynomial traps

## Telegram Bot

```bash
export TELEGRAM_BOT_TOKEN="your_token"
python telegram_bot.py
```

Commands: `/solve 5x+3=0` or `/animate 2x-6=0`

## Dependencies

**Python**: manim, sympy, python-telegram-bot, numpy, scipy
**Node.js**: mathsteps

## Credits

- [Manim Community](https://github.com/ManimCommunity/manim) — animation engine
- [mathsteps](https://github.com/google/mathsteps) — equation solver

## Support

| | |
|---|---|
| PayPal | `paypal.com/ncp/payment/W78F6W4TXZ4CS` |
| Binance | `1011264323` |
| Bybit | `467077834` |
| TRC20 | `TMW5uSDN6sMUBNirMoqY1icpsfa7GhPZfK` |
| BEP20/ERC20 | `0x7a8887c2ac3e596f6170c9e28b44e6b6d025c854` |
| LTC | `LVswXiD6Vd2dejXvGbZLa1R8jkvg748F4q` |
| TON | `UQAllRezWgHi3LPrSwyvAb4zazIph6j6goU7lMaqcFWFBxVH` |
| BTC | `1rSX6BDN1nqDMyBHqceySkZSs6PHUP23m` |
| SOL | `d8RonhC8oEHssrQjN1Y4UWHnd6MMP33XGCKtfNL4j59` |
