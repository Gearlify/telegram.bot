from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create inline keyboard with your channels/links
    keyboard = [
        [
            InlineKeyboardButton("🔹 PAYOUT", url="Nil"),
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
        # Show instructions or next steps
        proceed_message = """✅ Welcome! You've joined our channels.

# 🎁 GIVEAWAY DETAILS:
# • Airtime giveaway is now live
# • Winners will be announced soon
# • Stay active in our channels

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

# Alternative start with membership verification
async def start_with_verification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🎯 PAYOUT CHANNEL", url="Nil"),
        ],
        [
            InlineKeyboardButton("📢 Channel 1", url="https://chat.whatsapp.com/KvW5wtHgNRK8KkQrYO3MaI?mode=r_t"),
            InlineKeyboardButton("📢 Channel 2", url="https://chat.whatsapp.com/H6AJZ6VbaUv9cEObp7QrDq?mode=r_t")
        ],
        [
            InlineKeyboardButton("📢 Channel 3", url="https://chat.whatsapp.com/J4G1P2NxySpDxHNIo7xSdu?mode=r_t"),
            InlineKeyboardButton("📢 Channel 4", url="https://chat.whatsapp.com/LajUCqJmJ7sCP3A5Rs3HJv?mode=r_t")
        ],
        [
            InlineKeyboardButton("✅ Check Membership", callback_data="check_membership"),
            InlineKeyboardButton("❓ Help", callback_data="help")
        ],
        [
            InlineKeyboardButton("🚀 Proceed", callback_data="proceed")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """🎉 WELCOME TO EARNING BOT!

🎁 EARNING BOT LAUNCHED AND ACTIVE

📋 TO GET STARTED:
1️⃣ Join all our channels below
2️⃣ Click "Check Membership" to verify
3️⃣ Click "Proceed" to continue

👇 JOIN OUR CHANNELS TO GET STARTED"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )

# Function to check if user joined channels
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    # List of your channel usernames (without @)
    channels = ["your_payout_channel", "channel1", "channel2", "channel3", "channel4"]
    
    try:
        all_joined = True
        not_joined = []
        
        for channel in channels:
            try:
                member = await context.bot.get_chat_member(f"@{channel}", user_id)
                if member.status in ['left', 'kicked']:
                    all_joined = False
                    not_joined.append(channel)
            except Exception:
                # If can't check (bot not admin), assume not joined
                all_joined = False
                not_joined.append(channel)
        
        if all_joined:
            # Create a "proceed" button after verification
            keyboard = [[InlineKeyboardButton("🚀 Continue", callback_data="proceed")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "✅ VERIFIED! You've joined all required channels.\n\nClick Continue to proceed.",
                reply_markup=reply_markup
            )
        else:
            # Show which channels they haven't joined
            missing_channels = "\n".join([f"• @{ch}" for ch in not_joined])
            
            # Create back button
            keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"❌ Please join these channels:\n\n{missing_channels}\n\nThen try again.",
                reply_markup=reply_markup
            )
    
    except Exception as e:
        await query.edit_message_text("❌ Could not verify membership. Please ensure you've joined all channels and try again.")

# Handle back to menu
async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

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
    help_text = """❓ RECHARGE POINTS BOT HELP

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

# Main application setup
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    print("🤖 EARNING Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()