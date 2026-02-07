#!/bin/bash

# Math Animation System - Setup Script
# This script helps set up the environment for the math animation system

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Math Animation System - Setup${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python 3 found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 not found!${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Node.js
echo -e "\n${YELLOW}Checking Node.js...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js found: $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js not found!${NC}"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check npm
echo -e "\n${YELLOW}Checking npm...${NC}"
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ npm found: $NPM_VERSION${NC}"
else
    echo -e "${RED}✗ npm not found!${NC}"
    exit 1
fi

# Install Node.js dependencies
echo -e "\n${YELLOW}Installing Node.js dependencies...${NC}"
if [ -f "package.json" ]; then
    npm install
    echo -e "${GREEN}✓ Node.js dependencies installed${NC}"
else
    echo -e "${RED}✗ package.json not found!${NC}"
    exit 1
fi

# Install Python dependencies
echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo -e "${GREEN}✓ Python dependencies installed${NC}"
else
    echo -e "${RED}✗ requirements.txt not found!${NC}"
    exit 1
fi

# Check FFmpeg
echo -e "\n${YELLOW}Checking FFmpeg...${NC}"
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n1 | awk '{print $3}')
    echo -e "${GREEN}✓ FFmpeg found: $FFMPEG_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ FFmpeg not found!${NC}"
    echo "FFmpeg is required for video rendering."
    echo "Install it with:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org/"
fi

# Make scripts executable
echo -e "\n${YELLOW}Making scripts executable...${NC}"
chmod +x main.py
chmod +x test_system.py
chmod +x telegram_bot.py
echo -e "${GREEN}✓ Scripts are now executable${NC}"

# Run tests
echo -e "\n${YELLOW}Running system tests...${NC}"
python3 test_system.py

# Check test results
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Setup completed successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "\n${BLUE}Next steps:${NC}"
    echo "  1. Try solving an equation:"
    echo -e "     ${YELLOW}python3 main.py -e '5x+3=0'${NC}"
    echo ""
    echo "  2. Create an animation:"
    echo -e "     ${YELLOW}python3 main.py -e 'x^2+2x+1=0' --animate${NC}"
    echo ""
    echo "  3. Set up Telegram bot (optional):"
    echo -e "     ${YELLOW}export TELEGRAM_BOT_TOKEN='your_token'${NC}"
    echo -e "     ${YELLOW}python3 telegram_bot.py${NC}"
    echo ""
else
    echo -e "\n${RED}========================================${NC}"
    echo -e "${RED}⚠ Setup completed with warnings${NC}"
    echo -e "${RED}========================================${NC}"
    echo "Please check the test output above for details."
fi
