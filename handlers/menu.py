from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile
from telegram.ext import MessageHandler, CommandHandler, filters, ContextTypes, ConversationHandler
import json
import os

ADMIN_ID = 7734095649  # <-- তোমার আইডি বসাও

MENU_ADD, MENU_CONTENT = range(2)

def load_menus():
    if os.path.exists("data/config.json"):
        with open("data/config.json", "r") as f:
            return json.load(f)
    return {}

def save_menus(data):
    with open("data/config.json", "w") as f:
        json.dump(data, f, indent=2)

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    keyboard = [["➕ Add Menu"], ["📄 Show All Menus"]]
    await update.message.reply_text("🔧 Admin Panel", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def admin_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "➕ Add Menu":
        await update.message.reply_text("📝 Send new button name:", reply_markup=ReplyKeyboardRemove())
        return MENU_ADD
    elif text == "📄 Show All Menus":
        menus = load_menus()
        if not menus:
            await update.message.reply_text("❌ No menu buttons found.")
        else:
            msg = "\n".join(f"🔘 {k}" for k in menus)
            await update.message.reply_text(f"✅ Total {len(menus)} Menu Buttons:\n{msg}")
    else:
        menus = load_menus()
        if text in menus:
            content = menus[text]
            if content.get("type") == "text":
                await update.message.reply_text(content["data"])
            elif content.get("type") == "photo":
                await update.message.reply_photo(photo=InputFile(content["data"]))
            elif content.get("type") == "video":
                await update.message.reply_video(video=InputFile(content["data"]))
        else:
            await update.message.reply_text("❌ Unknown button.")
    return ConversationHandler.END

async def menu_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_menu"] = update.message.text
    await update.message.reply_text("📤 Now send the content (text/photo/video):")
    return MENU_CONTENT

async def menu_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content_type = None
    data = None

    if update.message.text:
        content_type = "text"
        data = update.message.text
    elif update.message.photo:
        content_type = "photo"
        file = await update.message.photo[-1].get_file()
        path = f"data/{context.user_data['new_menu']}_photo.jpg"
        await file.download_to_drive(path)
        data = path
    elif update.message.video:
        content_type = "video"
        file = await update.message.video.get_file()
        path = f"data/{context.user_data['new_menu']}_video.mp4"
        await file.download_to_drive(path)
        data = path

    if content_type:
        menus = load_menus()
        menus[context.user_data["new_menu"]] = {
            "type": content_type,
            "data": data
        }
        save_menus(menus)
        await update.message.reply_text(f"✅ Menu '{context.user_data['new_menu']}' added!")
    else:
        await update.message.reply_text("❌ Unsupported content.")
    return ConversationHandler.END

menu_handler = ConversationHandler(
    entry_points=[CommandHandler("menu", menu_command), MessageHandler(filters.TEXT, admin_menu_handler)],
    states={
        MENU_ADD: [MessageHandler(filters.TEXT, menu_add)],
        MENU_CONTENT: [MessageHandler(filters.ALL, menu_content)],
    },
    fallbacks=[],
  )
