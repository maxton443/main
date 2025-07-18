from telegram import Update, InputFile
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
import json
import os

ADMIN_ID = 7734095649  # তোমার আইডি বসাও
ASK_MESSAGE = range(1)

def load_users():
    if os.path.exists("data/users.json"):
        with open("data/users.json", "r") as f:
            return json.load(f)
    return []

async def broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("📨 What do you want to send to all members?")
    return ASK_MESSAGE

async def broadcast_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    success = 0
    fail = 0

    msg_type = None
    content = None

    if update.message.text:
        msg_type = "text"
        content = update.message.text
    elif update.message.photo:
        msg_type = "photo"
        file = await update.message.photo[-1].get_file()
        content = await file.download_as_bytearray()
    elif update.message.video:
        msg_type = "video"
        file = await update.message.video.get_file()
        content = await file.download_as_bytearray()

    for user in users:
        try:
            if msg_type == "text":
                await context.bot.send_message(chat_id=user, text=content)
            elif msg_type == "photo":
                await context.bot.send_photo(chat_id=user, photo=InputFile(content, filename="photo.jpg"))
            elif msg_type == "video":
                await context.bot.send_video(chat_id=user, video=InputFile(content, filename="video.mp4"))
            success += 1
        except:
            fail += 1

    await update.message.reply_text(f"✅ Message sent to {success} users. ❌ Failed: {fail}")
    return ConversationHandler.END

broadcast_handler = ConversationHandler(
    entry_points=[CommandHandler("broadcast", broadcast_start)],
    states={ASK_MESSAGE: [MessageHandler(filters.ALL, broadcast_send)]},
    fallbacks=[],
  )
