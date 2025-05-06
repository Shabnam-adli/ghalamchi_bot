from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputFile
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, CallbackContext, ConversationHandler
)
import sqlite3
from datetime import datetime
import pandas as pd
import os

TOKEN = "7298813747:AAGi7qealqC4Shbl313aR7D-_OQySWp2K5U"
ADMIN_ID = 423848141

# مراحل گفتگو
CHOICE_PROGRAMMING, CHOICE_IMPORTANT, CHOICE_SUBJECTS, CHOICE_GOAL, CHOICE_PHONE, CHOICE_NAME, CHOICE_GRADE = range(7)

# لیست دروس
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

async def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        f"سلام {user.first_name}!\nدانش آموز عزیز به نمایشگاه کتاب قلم چی خوش آمدید (غرفه غرب دختر تهران)"
    )

    keyboard = [[KeyboardButton("بله")], [KeyboardButton("نه")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "آیا می‌خواهید برنامه‌ریزی درسی شخصی‌سازی‌شده دریافت کنید؟",
        reply_markup=reply_markup
    )

    return CHOICE_PROGRAMMING

async def received_programming(update: Update, context: CallbackContext) -> int:
    context.user_data['programming'] = update.message.text

    keyboard = [
        [KeyboardButton("بهبود روش مطالعه")],
        [KeyboardButton("برنامه‌ریزی دقیق درسی")],
        [KeyboardButton("پیدا کردن منابع آموزشی مناسب")],
        [KeyboardButton("تقویت انگیزه تحصیلی")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "کدام یک از موارد زیر بیشتر برای شما مهم است؟",
        reply_markup=reply_markup
    )
    return CHOICE_IMPORTANT

async def received_important(update: Update, context: CallbackContext) -> int:
    context.user_data['important'] = update.message.text

    keyboard = [[KeyboardButton(subject)] for subject in subjects_list]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "در کدام درس‌ها احساس ضعف می‌کنید؟",
        reply_markup=reply_markup
    )
    return CHOICE_SUBJECTS

async def received_subjects(update: Update, context: CallbackContext) -> int:
    context.user_data['subjects'] = update.message.text

    keyboard = [
        [KeyboardButton("آزمون برای سنجش خودم")],
        [KeyboardButton("آزمون برای برنامه‌ریزی درسی")],
        [KeyboardButton("آزمون برای تقویت دروس")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "آزمون یکی از مهم ترین ابزار ها برای برنامه ریزی درسی است. به نظر شما هدف از شرکت در آزمون های قلم چی چیست؟",
        reply_markup=reply_markup
    )
    return CHOICE_GOAL

async def received_goal(update: Update, context: CallbackContext) -> int:
    context.user_data['goal'] = update.message.text

    await update.message.reply_text("برای دریافت مشاوره با رتبه‌های برتر کنکور و دریافت برنامه تحصیلی، شماره تماس خود را وارد کنید:")
    return CHOICE_PHONE

async def received_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("نام و نام خانوادگی خود را وارد کنید:")
    return CHOICE_NAME

async def received_name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text("مقطع تحصیلی خود را وارد کنید (مثلاً: نهم، دهم، یازدهم، دوازدهم):")
    return CHOICE_GRADE

async def received_grade(update: Update, context: CallbackContext) -> int:
    context.user_data['grade'] = update.message.text
    user = update.message.from_user

    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO contacts (user_id, name, phone, grade, timestamp) VALUES (?, ?, ?, ?, ?)",
        (
            user.id,
            context.user_data['name'],
            context.user_data['phone'],
            context.user_data['grade'],
            datetime.now().isoformat()
        )
    )
    conn.commit()
    conn.close()

    await update.message.reply_text("ممنون 🌸 مشاورین ما به زودی با شما تماس خواهند گرفت. موفق باشید!")
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

async def export_excel(update: Update, context: CallbackContext):
    if update.message.from_user.id != ADMIN_ID:
        await context.bot.send_message(update.message.chat_id, text="شما اجازه دسترسی به این اطلاعات را ندارید.")
        return

    conn = sqlite3.connect("contacts.db")
    df = pd.read_sql_query("SELECT name AS 'نام و نام خانوادگی', phone AS 'شماره تماس', grade AS 'مقطع تحصیلی', timestamp AS 'زمان ثبت' FROM contacts", conn)
    conn.close()

    if df.empty:
        await context.bot.send_message(update.message.chat_id, text="هیچ داده‌ای برای خروجی وجود ندارد.")
        return

    file_path = "contacts.xlsx"
    df.to_excel(file_path, index=False)

    with open(file_path, 'rb') as file:
        await context.bot.send_document(chat_id=ADMIN_ID, document=InputFile(file, filename="contacts.xlsx"))

    os.remove(file_path)

async def get_id(update: Update, context: CallbackContext):
    user = update.message.from_user
    await update.message.reply_text(f"آیدی عددی شما: {user.id}")

def main():
    init_db()
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE_PROGRAMMING: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_programming)],
            CHOICE_IMPORTANT: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_important)],
            CHOICE_SUBJECTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_subjects)],
            CHOICE_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_goal)],
            CHOICE_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_phone)],
            CHOICE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_name)],
            CHOICE_GRADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_grade)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('get_contacts', get_contacts))
    application.add_handler(CommandHandler('export_excel', export_excel))
    application.add_handler(CommandHandler('id', get_id))

    application.run_polling()

if __name__ == '__main__':
    main()
