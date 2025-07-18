from telegram.ext import ApplicationBuilder
from handlers.start import start_handler
from handlers.menu import menu_handler, content_handler
from handlers.admin import admin_handler, message_all_handler
import json
import os

# টোকেন এখানে বসাও
BOT_TOKEN = "7910847091:AAGCr1HgDFlDX_nm9e2YZ4zXa9aV3jmT4iU"

# বট চালু
async def on_startup(app):
    print("🤖 Bot is running...")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()

    # হ্যান্ডলার যুক্ত করা
    app.add_handler(start_handler)
    app.add_handler(menu_handler)
    app.add_handler(content_handler)
    app.add_handler(admin_handler)
    app.add_handler(message_all_handler)

    app.run_polling()
