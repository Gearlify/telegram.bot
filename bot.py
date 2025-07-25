from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import os
from dotenv import load_dotenv
import threading
import asyncio

os.environ.setdefault('PORT', '10000')
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create inline keyboard with your channels/links
    keyboard = [
        [
            InlineKeyboardButton("🔹 PAYOUT", url="https://chat.whatsapp.com/KvW5wtHgNRK8KkQrYO3MaI?mode=r_t"),
            InlineKeyboardButton("🔹 MUST JOIN", url="https://chat.whatsapp.com/KvW5wtHgNRK8KkQrYO3MaI?mode=r_t")
        ],
        [
            InlineKeyboardButton("🔹 MUST JOIN", url="https://chat.whatsapp.com/H6AJZ6VbaUv9cEObp7QrDq?mode=r_t"),
            InlineKeyboardButton("🔹 MUST JOIN", url="https://chat.whatsapp.com/J4G1P2NxySpDxHNIo7xSdu?mode=r_t")
        ],
        [
            InlineKeyboardButton("🔹 MUST JOIN", url="https://chat.whatsapp.com/LajUCqJmJ7sCP3A5Rs3HJv?mode=r_t")
        ],
        [
            InlineKeyboardButton("Proceed ✅", callback_data="proceed")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = """🎉 EARNING BOT LAUNCHED AND ACTIVE

JOIN OUR CHANNELS TO GET STARTED"""
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup
    )

# Handle button callbacks
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback
    
    if query.data == "proceed":
        # Show instructions or next steps (Fixed comment formatting)
        proceed_message = """✅ Welcome! You've joined our channels.

🎁 GIVEAWAY DETAILS:
• Airtime giveaway is now live
• Winners will be announced soon
• Stay active in our channels

📞 CONTACT: @emmzy for support

Thank you for joining! 🚀"""
        
        await query.edit_message_text(proceed_message)
    
    elif query.data == "check_membership":
        await query.edit_message_text("Checking your membership status...")
    
    elif query.data == "help":
        help_message = """❓ HOW TO PARTICIPATE:

1️⃣ Join all required channels
2️⃣ Click 'Proceed' button
3️⃣ Follow instructions in channels
4️⃣ Wait for giveaway results

🔄 Use /start to go back to main menu"""
        await query.edit_message_text(help_message)

# Handle general messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    
    if "help" in user_text:
        help_message = """❓ HELP & SUPPORT

🤖 Available Commands:
• /start - Main menu
• /help - Show this help

📞 Contact Support: @emmzy
🔄 Use /start to go back to main menu"""
        
        await update.message.reply_text(help_message)
    
    elif "status" in user_text:
        await update.message.reply_text("🔄 Giveaway is currently active! Use /start to participate.")
    
    else:
        # Default response
        await update.message.reply_text("👋 Welcome! Use /start to begin or type 'help' for assistance.")

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """❓ EARNING BOT HELP

🎁 ABOUT THIS BOT:
This bot helps you participate in earning and giveaways by joining channels and completing tasks.

📋 HOW TO USE:
1️⃣ Use /start to see the main menu
2️⃣ Join all required channels
3️⃣ Click "Proceed" to complete registration

🔧 COMMANDS:
• /start - Main menu
• /help - Show this help

📞 SUPPORT: @emmzy

🔄 Ready to start? Use /start"""
    
    await update.message.reply_text(help_text)

# HTTP Server for Render
def run_http_server():
    from flask import Flask
    
    flask_app = Flask(__name__)
    
    @flask_app.route('/')
    def index():
        return """
        <h1>🤖 Earning Bot Server</h1>
        <p>Bot Status: ✅ Running</p>
        <p>Server is active and ready!</p>
        """
    
    @flask_app.route('/health')
    def health():
        return {"status": "healthy", "bot": "active"}
    
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 HTTP Server starting on port {port}")
    flask_app.run(host='0.0.0.0', port=port, debug=False)

# Remove the async run_bot function since we don't need it anymore

# Main execution
def main():
    print("🚀 Starting Earning Bot Application...")
    
    # Start HTTP server in background thread
    http_thread = threading.Thread(target=run_http_server)
    http_thread.daemon = True
    http_thread.start()
    
    # Give HTTP server time to start
    import time
    time.sleep(2)
    
    # Create and start bot application
    print("🤖 Creating bot application...")
    
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN not found in environment variables!")
        return
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot handlers registered")
    print("🚀 Starting polling...")
    
    # Start polling (this handles the event loop internally)
    application.run_polling()

if __name__ == '__main__':
    main()
