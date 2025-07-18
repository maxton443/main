from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 হ্যালো {user.first_name}!\n\nআমি আপনার Telegram বট 🤖\n\n/start কমান্ড সফলভাবে কাজ করছে!",
    )

start_handler = CommandHandler("start", start)
