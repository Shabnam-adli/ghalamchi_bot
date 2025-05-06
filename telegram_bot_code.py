from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputFile
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, CallbackContext, ConversationHandler
)
import sqlite3
from datetime import datetime
import pandas as pd
import os
import re

# ✅ توکن واقعی ربات
TOKEN = "7949641234:AAEBsEKqGwwzDdzPxA2c4Wwt_Gf-XFbTWVE"
ADMIN_ID = 423848141  # آیدی عددی خودت

CHOICE_PROGRAMMING, CHOICE_IMPORTANT, CHOICE_SUBJECTS, CHOICE_GOAL, CHOICE_PHONE, CHOICE_NAME, CHOICE_GRADE = range(7)

subjects_list = [
    "ریاضی", "فیزیک", "شیمی", "زیست‌شناسی", "ادبیات فارسی",
    "زبان انگلیسی", "عربی", "دین و زندگی", "تاریخ", "جغرافیا"
]

def init_db():
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        phone TEXT,
        grade TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def is_valid_phone(phone):
    return re.match(r"^09\d{9}$", phone)

async def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        f"سلام {user.first_name}!\nدانش‌آموز عزیز به نمایشگاه کتاب قلم‌چی خوش آمدید (غرفه غرب دختر تهران)"
    )

    keyboard = [[KeyboardButton("بله")], [KeyboardButton("نه")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "آیا می‌خواهید برنامه‌ریزی درسی شخصی‌سازی‌شده دریافت کنید؟",
        reply_markup=reply_markup
    )

    return CHOICE_PROGRAMMING

# توابع دیگر مانند received_important و غیره باید تعریف شوند...

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("مکالمه لغو شد.")
    return ConversationHandler.END

async def get_contacts(update: Update, context: CallbackContext):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("شما اجازه دسترسی به این اطلاعات را ندارید.")
        return

    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("SELECT name, phone, grade, timestamp FROM contacts")
    rows = c.fetchall()
    conn.close()

    if not rows:
        await update.message.reply_text("هنوز هیچ اطلاعاتی ثبت نشده است.")
        return

    msg = "📋 لیست ثبت‌شده:\n\n"
    for name, phone, grade, time in rows:
        msg += f"👤 {name}\n📞 {phone}\n🎓 {grade}\n🕒 {time}\n\n"

    await update.message.reply_text(msg)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE_PROGRAMMING: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_programming)],
            # سایر states باید اضافه شوند...
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('get_contacts', get_contacts))
    application.add_handler(CommandHandler('export_excel', export_excel))
    application.add_handler(CommandHandler('id', get_id))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
