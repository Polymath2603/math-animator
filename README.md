# Math Animation System

Step-by-step math equation solver with animations, powered by Manim and mathsteps.

## Features

- Step-by-step equation solving
- Beautiful animations with Manim
- Telegram bot interface
- LaTeX support
- Batch processing
- JSON export

## What Can It Solve?

- Linear equations: `5x + 3 = 0`
- Quadratic equations: `x^2 + 2x + 1 = 0`
- Equations with radicals: `sqrt(x+5) = 3`
- Complex expressions: `2x^2 + 4x + 2`
- LaTeX notation: `\sqrt{x+5} - 2 = \sqrt{7-x} + 3`

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js (for mathsteps)
- FFmpeg

### Installation

```bash
git clone https://github.com/yourusername/math-animator.git
cd math-animator
pip install -r requirements.txt
npm install mathsteps
```

### Usage

**Solve an equation:**
```bash
python main.py -e "5x+3=0"
```

**Create an animation:**
```bash
python main.py -e "x^2+2x+1=0" --animate
```

**Batch process:**
```bash
python main.py -f equations.txt --batch
```

**High quality:**
```bash
python main.py -e "2x-6=0" --animate -q h
```

## Telegram Bot

1. Get token from @BotFather
2. Set token: `export TELEGRAM_BOT_TOKEN="your_token"`
3. Run: `python telegram_bot.py`
4. Use: `/solve 5x+3=0` or `/animate 2x-6=0`

## Quality Levels

- `l` - Low (480p15) - Fast
- `m` - Medium (720p30) - Balanced
- `h` - High (1080p60) - Best
- `k` - 4K (2160p60) - Production

## Troubleshooting

**"Math stepper JS file not found"**
```bash
npm install mathsteps
```

**"No steps generated"**
- Equation might already be simplified
- Try standard notation instead of LaTeX

**Animation fails**
```bash
pip install manim
ffmpeg -version  # Check FFmpeg is installed
```

## License

MIT License

## Acknowledgments

Built with:
- [Manim Community](https://github.com/ManimCommunity/manim) - MIT License
- [mathsteps](https://github.com/google/mathsteps) - Apache 2.0 License

---

## Support This Project

If you find this useful, consider supporting:

### 💰 Cryptocurrency

<img src="https://img.shields.io/badge/Bitcoin-000000?style=for-the-badge&logo=bitcoin&logoColor=white" alt="Bitcoin"/>

```
15kPSKNLEgVH6Jy3RtNaT2mPsxTMS6MAEp
```

<img src="https://img.shields.io/badge/Ethereum-3C3C3D?style=for-the-badge&logo=ethereum&logoColor=white" alt="Ethereum"/>

```
0xc4f7076dd25a38f2256b5c23b8ca859cc42924cf
```

<img src="https://img.shields.io/badge/BNB-F3BA2F?style=for-the-badge&logo=binance&logoColor=white" alt="BNB"/>

```
0xc4f7076dd25a38f2256b5c23b8ca859cc42924cf
```

<img src="https://img.shields.io/badge/Solana-9945FF?style=for-the-badge&logo=solana&logoColor=white" alt="Solana"/>

```
EWcxGVtbohy8CdFLb2HNUqSHdecRiWKLywgMLwsXByhn
```

### 🏦 Exchange Platforms

<img src="https://img.shields.io/badge/Binance-FCD535?style=for-the-badge&logo=binance&logoColor=white" alt="Binance"/>

- **URL:** https://app.binance.com/uni-qr/Uzof5Lrq
- **ID:** `1011264323`

<img src="https://img.shields.io/badge/Bybit-F7A600?style=for-the-badge&logo=bybit&logoColor=white" alt="Bybit"/>

- **URL:** https://i.bybit.com/W2abUWF
- **ID:** `467077834`

### 💳 Traditional

<img src="https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white" alt="PayPal"/>

https://www.paypal.com/ncp/payment/W78F6W4TXZ4CS
