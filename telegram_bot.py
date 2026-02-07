#!/usr/bin/env python3
"""
Math Animation Telegram Bot

A Telegram bot interface for the Math Animation System.
Allows users to solve equations and create animations directly from Telegram.

Setup:
1. Create a bot with @BotFather on Telegram
2. Get your bot token
3. Set environment variable: export TELEGRAM_BOT_TOKEN="your_token_here"
4. Run: python telegram_bot.py

Dependencies:
    pip install python-telegram-bot
"""

import os
import sys
import logging
import asyncio
from pathlib import Path
from typing import Optional

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        CallbackQueryHandler,
        ContextTypes,
        filters
    )
except ImportError:
    print("❌ python-telegram-bot not installed!")
    print("Install it with: pip install python-telegram-bot")
    sys.exit(1)

# Import our math animation system
from main import MathAnimationPipeline, Colors

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
DONATION_LINKS = {
    'paypal': 'https://paypal.me/yourpaypal',
    'binance': 'your_binance_pay_id',
    'bitcoin': 'your_bitcoin_address'
}

SOURCE_CODE_URL = 'https://github.com/yourusername/math-animator'

HELP_TEXT = """
🧮 *Math Animation Bot* 🎬

I can solve equations and create beautiful step-by-step animations!

*Commands:*
/start - Start the bot
/help - Show this help message
/solve <equation> - Solve an equation
/animate <equation> - Create animation (may take time)
/donate - Support this project
/source - View source code

*Examples:*
• `/solve 5x+3=0`
• `/solve x^2+2x+1=0`
• `/animate 2x-6=0`
• `/solve sqrt(x+5)=3`

*Supported:*
✓ Linear equations
✓ Quadratic equations
✓ Expressions with square roots
✓ LaTeX notation

*Note:* Animations take time to render. Please be patient! ⏳
"""

ABOUT_TEXT = """
🔬 *About Math Animation Bot*

This bot uses:
• *Manim Community* - Beautiful math animations
  https://github.com/ManimCommunity/manim
  
• *mathsteps* - Step-by-step equation solver
  https://github.com/google/mathsteps

*Open Source Project*
All code is available on GitHub!
{source_url}

*Support Development* 💝
If you find this useful, consider donating:
/donate
"""


class MathBot:
    """Telegram bot for math animations"""
    
    def __init__(self, token: str):
        self.token = token
        self.pipeline = MathAnimationPipeline(quiet=True)
        self.app = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_text = """
👋 *Welcome to Math Animation Bot!*

I can help you solve equations step-by-step and create beautiful animations.

Try: `/solve 5x+3=0`

For more info, use /help
"""
        
        keyboard = [
            [
                InlineKeyboardButton("📖 Help", callback_data='help'),
                InlineKeyboardButton("💝 Donate", callback_data='donate')
            ],
            [
                InlineKeyboardButton("💻 Source Code", url=SOURCE_CODE_URL)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await update.message.reply_text(HELP_TEXT, parse_mode='Markdown')
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
        about = ABOUT_TEXT.format(source_url=SOURCE_CODE_URL)
        await update.message.reply_text(about, parse_mode='Markdown')
    
    async def donate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /donate command"""
        donate_text = f"""
💝 *Support This Project*

If you find this bot useful, consider supporting its development:

*PayPal*
{DONATION_LINKS['paypal']}

*Binance Pay*
ID: `{DONATION_LINKS['binance']}`

*Bitcoin*
`{DONATION_LINKS['bitcoin']}`

Your support helps keep this project free and open source! 🙏

*Other ways to help:*
⭐ Star the project on GitHub
🔄 Share with friends
🐛 Report bugs and suggest features
"""
        
        keyboard = [
            [InlineKeyboardButton("💻 View Source Code", url=SOURCE_CODE_URL)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            donate_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def source_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /source command"""
        source_text = f"""
💻 *Source Code*

This bot is fully open source!

*GitHub Repository:*
{SOURCE_CODE_URL}

*Technologies:*
• Python 3.8+
• Manim Community
• mathsteps (Node.js)
• python-telegram-bot

*Features:*
✓ Equation solving
✓ Expression simplification
✓ Step-by-step animations
✓ LaTeX support

Feel free to contribute, report issues, or fork the project!
"""
        
        keyboard = [
            [InlineKeyboardButton("📖 View on GitHub", url=SOURCE_CODE_URL)],
            [InlineKeyboardButton("💝 Donate", callback_data='donate')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            source_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def solve_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /solve command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Please provide an equation!\n\n"
                "Example: `/solve 5x+3=0`",
                parse_mode='Markdown'
            )
            return
        
        equation = ' '.join(context.args)
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"🔄 Solving: `{equation}`\n\nPlease wait...",
            parse_mode='Markdown'
        )
        
        try:
            # Process equation
            result = self.pipeline.process_equation(equation, verbose=False)
            
            if not result.get('success'):
                error_msg = f"❌ *Error:* {result.get('error')}\n\n"
                if result.get('suggestion'):
                    error_msg += f"💡 *Suggestion:* {result.get('suggestion')}"
                
                await processing_msg.edit_text(error_msg, parse_mode='Markdown')
                return
            
            # Format solution
            solution_text = f"✅ *Solved:* `{equation}`\n\n"
            solution_text += f"*Type:* {result.get('type')}\n"
            solution_text += f"*Steps:* {result.get('stepCount')}\n\n"
            
            # Add steps
            for step in result.get('steps', [])[:10]:  # Limit to 10 steps for Telegram
                solution_text += f"*Step {step['step']}:* {step['description']}\n"
                solution_text += f"`{step['before']}`\n"
                solution_text += f"↓\n"
                solution_text += f"`{step['after']}`\n\n"
            
            if len(result.get('steps', [])) > 10:
                solution_text += f"... and {len(result.get('steps', [])) - 10} more steps\n\n"
            
            solution_text += "Use `/animate {equation}` to create a video!"
            
            await processing_msg.edit_text(solution_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error solving equation: {e}")
            await processing_msg.edit_text(
                f"❌ An error occurred: {str(e)}\n\n"
                "Please try again or use /help for examples."
            )
    
    async def animate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /animate command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Please provide an equation!\n\n"
                "Example: `/animate 5x+3=0`",
                parse_mode='Markdown'
            )
            return
        
        equation = ' '.join(context.args)
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"🎬 Creating animation for: `{equation}`\n\n"
            "⏳ This may take 30-60 seconds...\n"
            "Please be patient!",
            parse_mode='Markdown'
        )
        
        try:
            # Verify equation is valid first
            result = self.pipeline.process_equation(equation, verbose=False)
            
            if not result.get('success'):
                error_msg = f"❌ Cannot create animation:\n{result.get('error')}\n\n"
                if result.get('suggestion'):
                    error_msg += f"💡 {result.get('suggestion')}"
                
                await processing_msg.edit_text(error_msg, parse_mode='Markdown')
                return
            
            # Create animation
            success = self.pipeline.run_animation(
                equation,
                quality='l',  # Low quality for faster rendering
                preview=False
            )
            
            if success:
                # Find the video file
                media_dir = Path(__file__).parent / "media" / "videos" / "enhanced_animator"
                video_dirs = list(media_dir.glob("*"))
                
                if video_dirs:
                    latest_dir = max(video_dirs, key=lambda p: p.stat().st_mtime)
                    videos = list(latest_dir.glob("*.mp4"))
                    
                    if videos:
                        latest_video = max(videos, key=lambda p: p.stat().st_mtime)
                        
                        # Send video
                        await processing_msg.edit_text(
                            "📤 Uploading video...",
                            parse_mode='Markdown'
                        )
                        
                        with open(latest_video, 'rb') as video_file:
                            await update.message.reply_video(
                                video=video_file,
                                caption=f"🎬 Animation for: `{equation}`\n\n"
                                       f"Steps: {result.get('stepCount')}",
                                parse_mode='Markdown'
                            )
                        
                        await processing_msg.delete()
                        return
            
            # If we get here, something went wrong
            await processing_msg.edit_text(
                "❌ Failed to create animation.\n\n"
                "Try using `/solve {equation}` instead for step-by-step solution."
            )
            
        except Exception as e:
            logger.error(f"Error creating animation: {e}")
            await processing_msg.edit_text(
                f"❌ An error occurred during animation:\n{str(e)}\n\n"
                "Try using `/solve {equation}` for text solution."
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        text = update.message.text.strip()
        
        # If message looks like an equation, solve it
        if any(char in text for char in ['=', 'x', 'X']) or 'sqrt' in text.lower():
            await update.message.reply_text(
                f"💡 Did you want to solve this?\n"
                f"Use: `/solve {text}`\n\n"
                f"Or create animation:\n"
                f"`/animate {text}`",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "👋 Hi! I'm a math solver bot.\n\n"
                "Use /help to see what I can do!"
            )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'help':
            await query.message.reply_text(HELP_TEXT, parse_mode='Markdown')
        elif query.data == 'donate':
            await self.donate_command(update, context)
        elif query.data == 'about':
            await self.about_command(update, context)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.message:
            await update.message.reply_text(
                "❌ An unexpected error occurred.\n"
                "Please try again or contact support."
            )
    
    def run(self):
        """Run the bot"""
        # Create application
        self.app = Application.builder().token(self.token).build()
        
        # Add handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("about", self.about_command))
        self.app.add_handler(CommandHandler("donate", self.donate_command))
        self.app.add_handler(CommandHandler("source", self.source_command))
        self.app.add_handler(CommandHandler("solve", self.solve_command))
        self.app.add_handler(CommandHandler("animate", self.animate_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        self.app.add_error_handler(self.error_handler)
        
        # Start bot
        logger.info("🤖 Bot is starting...")
        logger.info(f"🔗 Bot username will be displayed after first message")
        logger.info("Press Ctrl+C to stop")
        
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point"""
    # Get token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print(f"{Colors.RED}❌ TELEGRAM_BOT_TOKEN environment variable not set!{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Setup instructions:{Colors.RESET}")
        print("1. Create a bot with @BotFather on Telegram")
        print("2. Copy your bot token")
        print("3. Set environment variable:")
        print(f"   {Colors.CYAN}export TELEGRAM_BOT_TOKEN=\"your_token_here\"{Colors.RESET}")
        print("4. Run this script again")
        print(f"\n{Colors.BLUE}Or run with token directly:{Colors.RESET}")
        print(f"   {Colors.CYAN}TELEGRAM_BOT_TOKEN=\"your_token\" python telegram_bot.py{Colors.RESET}")
        sys.exit(1)
    
    # Create and run bot
    bot = MathBot(token)
    
    try:
        bot.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ Bot stopped by user{Colors.RESET}")
        sys.exit(0)


if __name__ == '__main__':
    main()
