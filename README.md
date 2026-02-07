# 🧮 Math Animation System

Beautiful step-by-step math equation solver with animations, powered by **Manim** and **mathsteps**.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Manim](https://img.shields.io/badge/manim-community-orange.svg)

## ✨ Features

- 📊 **Step-by-step equation solving** with detailed explanations
- 🎬 **Beautiful animations** created with Manim Community
- 🤖 **Telegram bot interface** for easy access
- 📝 **LaTeX support** for mathematical notation
- 🔄 **Batch processing** for multiple equations
- 💾 **JSON export** of solutions

## 🎯 What Can It Solve?

- ✅ Linear equations: `5x + 3 = 0`
- ✅ Quadratic equations: `x^2 + 2x + 1 = 0`
- ✅ Equations with radicals: `sqrt(x+5) = 3`
- ✅ Complex expressions: `2x^2 + 4x + 2`
- ✅ LaTeX notation: `\sqrt{x+5} - 2 = \sqrt{7-x} + 3`

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js (for mathsteps)
- FFmpeg (for video generation)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/math-animator.git
cd math-animator
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Node.js dependencies**
```bash
npm install mathsteps
```

4. **Install Manim Community**
```bash
# On Ubuntu/Debian
sudo apt-get install ffmpeg
pip install manim

# On macOS
brew install ffmpeg
pip install manim

# On Windows
# Download FFmpeg from https://ffmpeg.org/
pip install manim
```

### Usage

#### Command Line

**Solve an equation:**
```bash
python main.py -e "5x+3=0"
```

**Create an animation:**
```bash
python main.py -e "x^2+2x+1=0" --animate
```

**Batch process from file:**
```bash
python main.py -f equations.txt --batch
```

**High quality animation:**
```bash
python main.py -e "2x-6=0" --animate -q h
```

#### Telegram Bot

1. **Get a bot token from @BotFather**

2. **Set your token:**
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
```

3. **Run the bot:**
```bash
python telegram_bot.py
```

4. **Start chatting!**
   - `/solve 5x+3=0` - Get step-by-step solution
   - `/animate 2x-6=0` - Create and receive animation video

## 📖 Documentation

### Command Line Options

```
python main.py [OPTIONS]

Options:
  -e, --equation TEXT    Single equation to process
  -f, --file PATH        File with equations (one per line)
  --batch               Process multiple equations
  --animate             Create animation with Manim
  -q, --quality LEVEL   Animation quality: l/m/h/k (default: l)
  --no-preview          Don't open preview after rendering
  --save FILE           Save results to JSON
  --quiet               Suppress output
```

### Quality Levels

- `l` - Low (480p15) - Fast preview
- `m` - Medium (720p30) - Balanced
- `h` - High (1080p60) - Best for sharing
- `k` - 4K (2160p60) - Production quality

### Example Equations File

Create a file `equations.txt`:
```
5x + 3 = 0
x^2 + 2x + 1 = 0
2x - 6 = 0
sqrt(x) = 4
```

Then run:
```bash
python main.py -f equations.txt --batch
```

## 🎨 Animation Preview

The system creates beautiful step-by-step animations showing:

1. **Title slide** with the equation
2. **Initial state** of the equation
3. **Each transformation step** with description
4. **Progress indicator** showing current step
5. **Final result** with celebration effect

## 🔧 Configuration

Edit `config.py` to customize:

- Animation timings
- Color schemes
- Font sizes
- Quality presets

Example presets:
```python
# Fast preview
python main.py -e "5x+3=0" --animate --preset fast

# Educational mode (more detailed)
python main.py -e "x^2=4" --animate --preset educational
```

## 🐛 Troubleshooting

### Common Issues

**"Math stepper JS file not found"**
- Make sure `math_stepper.js` is in the same directory
- Install mathsteps: `npm install mathsteps`

**"No steps generated"**
- The equation might already be in simplest form
- Try using standard notation instead of LaTeX
- Check for parsing errors in the input

**LaTeX equations not working**
- Use `\sqrt{x}` instead of `\sqrt(x)`
- Enclose in quotes: `python main.py -e "\sqrt{x+5}=3"`

**Animation fails**
- Make sure FFmpeg is installed and in PATH
- Try lower quality: `--quality l`
- Check Manim installation: `manim --version`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This project is built on top of amazing open-source projects:

- **[Manim Community](https://github.com/ManimCommunity/manim)** - Mathematical animation engine
  - Documentation: https://docs.manim.community/
  - License: MIT
  
- **[mathsteps](https://github.com/google/mathsteps)** - Step-by-step math solver
  - By Google
  - License: Apache 2.0

## 💝 Support This Project

If you find this project useful, please consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs and issues
- 💡 Suggesting new features
- 🔀 Contributing code

### Donations

Support development of this free, open-source project:

**PayPal:** https://paypal.me/yourpaypal

**Binance Pay ID:** `your_binance_pay_id`

**Bitcoin:** `your_bitcoin_address`

## 📞 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Telegram: [@yourusername](https://t.me/yourusername)

## ⚠️ Disclaimer

This software is provided "as is", without warranty of any kind. The mathematical solutions are generated by the mathsteps library and should be verified for accuracy in critical applications.

---

Made with ❤️ and Python

**Star this repo if you find it useful!** ⭐
