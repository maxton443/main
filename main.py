import os
import json
from datetime import datetime
from telegram.ext import ApplicationBuilder

from handlers.start import start_handler
from handlers.menu import menu_handler
from handlers.admin import admin_handler

# Bot Token (সরাসরি বসানো যাই, চাইলে ENV দিয়ে নিরাপদ করা যায়)
BOT_TOKEN = "7910847091:AAGCr1HgDFlDX_nm9e2YZ4zXa9aV3jmT4iU"  # <-- এখানে নিজের বট টোকেন বসাও

app = ApplicationBuilder().token(BOT_TOKEN).build()

# হ্যান্ডলার অ্যাড
app.add_handler(start_handler)
app.add_handler(menu_handler)
app.add_handler(admin_handler)

# লগ প্রিন্ট
print("✅ Bot is running...")
app.run_polling()
