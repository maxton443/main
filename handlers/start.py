from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from datetime import datetime
import json
import os

# ⚙️ Admin Telegram ID
ADMIN_ID = 7734095649  # <-- নিজের অ্যাডমিন আইডি বসাও

# 📁 ইউজার ফাইলের পথ
USERS_FILE = "data/users.json"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)

    # নতুন ইউজার ডেটা
    new_user = {
        "id": user_id,
        "name": user.full_name,
        "username": f"@{user.username}" if user.username else "N/A",
        "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 📥 ইউজার সেভ
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)

    if user_id not in users:
        users[user_id] = new_user
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)

        # 🔔 Admin কে নোটিফিকেশন
        total = len(users)
        msg = (
            "🆕 *New user joined*\n"
            f"👤 *Name:* {new_user['name']}\n"
            f"🪪 *Username:* {new_user['username']}\n"
            f"🕐 *Join Date:* {new_user['join_date']}\n"
            f"👥 *Total users:* {total}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="Markdown")

    # 📨 ইউজারকে welcome মেসেজ
    await update.message.reply_text("👋 Welcome! Use the menu below to explore.")

# 🔧 হ্যান্ডলার রিটার্ন
start_handler = CommandHandler("start", start_command)
