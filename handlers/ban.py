from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import json
import os

BANNED_FILE = "data/banned.json"
ADMIN_ID = 7734095649  # তোমার ID

def load_banned_users():
    if os.path.exists(BANNED_FILE):
        with open(BANNED_FILE, "r") as f:
            return json.load(f)
    return []

def save_banned_users(users):
    with open(BANNED_FILE, "w") as f:
        json.dump(users, f)

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) != 1:
        await update.message.reply_text("⚠️ Usage: /ban USER_ID")
        return

    user_id = context.args[0]
    banned_users = load_banned_users()
    if user_id not in banned_users:
        banned_users.append(user_id)
        save_banned_users(banned_users)
        await update.message.reply_text(f"✅ User {user_id} banned.")
    else:
        await update.message.reply_text("❗ Already banned.")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) != 1:
        await update.message.reply_text("⚠️ Usage: /unban USER_ID")
        return

    user_id = context.args[0]
    banned_users = load_banned_users()
    if user_id in banned_users:
        banned_users.remove(user_id)
        save_banned_users(banned_users)
        await update.message.reply_text(f"✅ User {user_id} unbanned.")
    else:
        await update.message.reply_text("❗ Not banned.")

ban_handler = CommandHandler("ban", ban)
unban_handler = CommandHandler("unban", unban)
