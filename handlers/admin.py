from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

ADMIN_ID = 7734095649  # <-- নিজের অ্যাডমিন আইডি বসাও

# বেসিক অ্যাডমিন মেনু
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    keyboard = [
        ["📊 Stats", "📋 User List"],
        ["🚫 Ban User", "✅ Unban User"],
        ["📝 Broadcast", "❌ Close"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🛠️ Admin Panel - Choose an option:", reply_markup=reply_markup)

admin_handler = CommandHandler("admin", admin_panel)
