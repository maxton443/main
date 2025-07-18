from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import json
import os
from datetime import datetime

ADMIN_ID = 7734095649  # <-- এখানে নিজের টেলিগ্রাম আইডি বসাও

# ডেটা সেভ করার ফাংশন
def save_user(user_data):
    os.makedirs("data", exist_ok=True)
    file_path = "data/users.json"
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            users = json.load(f)
    else:
        users = {}

    user_id = str(user_data["id"])
    if user_id not in users:
        users[user_id] = user_data
        with open(file_path, "w") as f:
            json.dump(users, f, indent=2)

    return len(users)

# স্টার্ট কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.full_name
    username = f"@{user.username}" if user.username else "N/A"
    user_id = user.id
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total = save_user({
        "id": user_id,
        "name": name,
        "username": username,
        "joined": date
    })

    await update.message.reply_text("👋 হ্যালো! বটে স্বাগতম!")

    msg = f"""
🆕 New User Joined

👤 Name: {name}
🔗 Username: {username}
🆔 ID: {user_id}
📅 Join Date: {date}
📊 Total Users: {total}
""".strip()

    # অ্যাডমিনকে পাঠাও
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

# হ্যান্ডলার এক্সপোর্ট
start_handler = CommandHandler("start", start)
