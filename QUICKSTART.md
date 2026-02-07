# 🚀 Quick Start Guide

Get started with Math Animation System in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 14+
- FFmpeg (for video rendering)

## Installation

### Option 1: Automatic Setup (Recommended)

```bash
./setup.sh
```

This will:
- Check all dependencies
- Install required packages
- Run system tests
- Verify everything works

### Option 2: Manual Setup

1. **Install Node.js dependencies:**
```bash
npm install
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install Manim:**
```bash
pip install manim
```

4. **Install FFmpeg:**
- **Ubuntu/Debian:** `sudo apt-get install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Windows:** Download from https://ffmpeg.org/

## First Steps

### 1. Solve Your First Equation

```bash
python main.py -e "5x+3=0"
```

Expected output:
```
Processing: 5x+3=0
✓ Type: equation
✓ Total Steps: 2

Step 1: Add/subtract terms
  5x+3=0
  ↓
  5x=-3

Step 2: Divide by coefficient
  5x=-3
  ↓
  x=-3/5
```

### 2. Create Your First Animation

```bash
python main.py -e "2x-6=0" --animate
```

This will:
- Process the equation
- Generate a beautiful animation
- Open the video automatically (if `-p` flag used)
- Save video to `media/videos/` folder

### 3. Test the System

```bash
python test_system.py
```

This runs comprehensive tests to verify everything is working correctly.

## Common Use Cases

### Solve Multiple Equations

Create a file `my_equations.txt`:
```
5x+3=0
x^2+2x+1=0
2x-6=0
```

Then run:
```bash
python main.py -f my_equations.txt --batch
```

### High Quality Animation

```bash
python main.py -e "x^2-4=0" --animate -q h
```

Quality options:
- `l` - Low (480p15) - Fast preview
- `m` - Medium (720p30) - Balanced
- `h` - High (1080p60) - Best for sharing
- `k` - 4K (2160p60) - Production quality

### Save Results

```bash
python main.py -e "3x+7=2x-1" --save results.json
```

### LaTeX Support

```bash
python main.py -e "sqrt(x+5)=3"
# or
python main.py -e "\sqrt{x+5}=3"
```

## Telegram Bot Setup

### 1. Create a Bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow instructions to get your token

### 2. Set Your Token

```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
```

Or create a `.env` file:
```
TELEGRAM_BOT_TOKEN=your_token_here
```

### 3. Run the Bot

```bash
python telegram_bot.py
```

### 4. Use the Bot

In Telegram, send these commands to your bot:
- `/start` - Welcome message
- `/solve 5x+3=0` - Solve equation
- `/animate 2x-6=0` - Create animation
- `/help` - Show help

## Troubleshooting

### "Math stepper JS file not found"

```bash
# Make sure you're in the correct directory
cd math_animator

# Install mathsteps
npm install mathsteps
```

### "No steps generated"

This usually means the equation is already in simplest form, or there's a parsing issue.

Try:
- Using standard notation: `sqrt(x)` instead of `\sqrt{x}`
- Simplifying the input
- Checking for typos

### "Manim not found"

```bash
pip install manim

# Verify installation
manim --version
```

### Animation Fails

1. Check FFmpeg is installed:
```bash
ffmpeg -version
```

2. Try lower quality:
```bash
python main.py -e "5x+3=0" --animate -q l
```

3. Check Manim installation:
```bash
manim --version
```

## Examples

### Linear Equations
```bash
python main.py -e "5x+3=0"
python main.py -e "2x-6=0"
python main.py -e "3x+7=2x-1"
```

### Quadratic Equations
```bash
python main.py -e "x^2+2x+1=0"
python main.py -e "x^2-4=0"
python main.py -e "2x^2+4x+2=0"
```

### Square Roots
```bash
python main.py -e "sqrt(x)=4"
python main.py -e "sqrt(x+5)=3"
```

### With Animations
```bash
python main.py -e "x^2-1=0" --animate
python main.py -e "3(x+2)=17" --animate -q h
```

## Next Steps

- Read the full [README.md](README.md)
- Check out [examples](equations.txt)
- Explore [configuration options](config.py)
- Contribute on [GitHub](https://github.com/yourusername/math-animator)

## Support

- 🐛 **Found a bug?** [Open an issue](https://github.com/yourusername/math-animator/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/yourusername/math-animator/discussions)
- 💝 **Want to help?** Check out [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Made with ❤️ and Python**

Star this repo if you find it useful! ⭐
