from telegram.ext import ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

# لیست دروس
subjects_list = [
    "ریاضی", "فیزیک", "شیمی", "زیست‌شناسی", "ادبیات فارسی", 
    "زبان انگلیسی", "عربی", "دین و زندگی", "تاریخ", "جغرافیا"
]

# توکن ربات شما
TOKEN = "7298813747:AAGi7qealqC4Shbl313aR7D-_OQySWp2K5U"  # جایگزین توکن واقعی خود کنید

# تابع شروع
async def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        f"سلام {user.first_name}!\nمن ربات قلم‌چی هستم. چطور می‌توانم به شما کمک کنم؟"
    )
    
    # سوال اول
    await update.message.reply_text(
        "عالی! حالا لطفاً بگو در کدام درس‌ها احساس ضعف می‌کنی؟\n"
        "مثلاً: ریاضی، فیزیک، شیمی، زیست‌شناسی، ادبیات فارسی، زبان انگلیسی و ..."
    )
    
    # نمایش گزینه‌ها برای انتخاب
    keyboard = [[KeyboardButton(subject)] for subject in subjects_list]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text("لطفاً یک یا چند درس که در آن‌ها احساس ضعف دارید را انتخاب کنید:", reply_markup=reply_markup)
    
    return 1  # مرحله بعد

# دریافت پاسخ در مورد دروس
async def received_subjects(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    context.user_data['subjects'] = user_choice
    
    # ارسال پیام اطمینان
    await update.message.reply_text(
        "نگران نباش! ما کمکت می‌کنیم که در این درس‌ها هم پیشرفت کنی."
    )
    
    # سوال بعدی
    await asyncio.sleep(1)  # اضافه کردن تأخیر کوتاه برای جلوگیری از تداخل پیام‌ها
    await update.message.reply_text(
        "هدف شما از شرکت در آزمون‌های آزمایشی چیست؟\n"
        "1. آزمون برای سنجش خودم\n"
        "2. آزمون برای برنامه‌ریزی برای کنکور\n"
        "3. آزمون برای تقویت دروس خاص"
    )
    
    return 2  # مرحله بعد

# دریافت پاسخ سوال بعدی
async def received_goal(update: Update, context: CallbackContext) -> int:
    user_goal = update.message.text
    context.user_data['goal'] = user_goal
    
    # درخواست شماره تماس
    await update.message.reply_text(
        "برای دریافت برنامه اختصاصی، شماره تماس خود را وارد کن تا مشاور ما با شما در تماس باشد."
    )
    
    return 3  # مرحله بعد

# گرفتن شماره تماس
async def received_phone(update: Update, context: CallbackContext) -> int:
    user_phone = update.message.text
    context.user_data['phone'] = user_phone
    
    # تشکر و اعلام پایان پروسه
    await update.message.reply_text(
        "ممنون! مشاور ما به زودی با شما تماس خواهد گرفت. موفق باشید!"
    )
    
    return ConversationHandler.END  # پایان مکالمه

# ساخت و راه‌اندازی ربات
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # استفاده از ConversationHandler برای مدیریت مراحل مختلف
    from telegram.ext import ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_subjects)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_goal)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_phone)],
        },
        fallbacks=[],
    )

    # اضافه کردن ConversationHandler به اپلیکیشن
    application.add_handler(conv_handler)

    # راه‌اندازی ربات
    application.run_polling()

if __name__ == '__main__':
    main()
