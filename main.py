import os
from telegram.ext import ApplicationBuilder

from handlers.start import start_handler
from handlers.menu import menu_handler
from handlers.admin import admin_handler

BOT_TOKEN = "7910847091:AAGCr1HgDFlDX_nm9e2YZ4zXa9aV3jmT4iU"  # <-- নিজের টোকেন বসা

app = ApplicationBuilder().token(BOT_TOKEN).build()

# হ্যান্ডলার অ্যাড করা হচ্ছে
app.add_handler(start_handler)
app.add_handler(menu_handler)
app.add_handler(admin_handler)

print("✅ Bot is running...")
app.run_polling()
