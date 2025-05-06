from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# لیست دروس
subjects_list = [
    "ریاضی", "فیزیک", "شیمی", "زیست‌شناسی", "ادبیات فارسی", 
    "زبان انگلیسی", "عربی", "دین و زندگی", "تاریخ", "جغرافیا"
]

# توکن ربات شما
TOKEN = "7298813747:AAGi7qealqC4Shbl313aR7D-_OQySWp2K5U"  # جایگزین توکن واقعی خود کنید

# مراحل گفتگو
CHOICE_PROGRAMMING, CHOICE_IMPORTANT, CHOICE_SUBJECTS, CHOICE_GOAL, CHOICE_PHONE = range(5)

# تابع شروع
async def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        f"سلام {user.first_name}!\nدانش آموز عزیز به نمایشگاه کتاب قلم چی خوش آمدید (غرفه غرب دختر تهران)"
    )
    
    # سوال اول
    keyboard = [
        [KeyboardButton("بله")],
        [KeyboardButton("نه")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        "آیا می‌خواهید برنامه‌ریزی درسی شخصی‌سازی‌شده دریافت کنید؟",
        reply_markup=reply_markup
    )
    
    return CHOICE_PROGRAMMING

# دریافت پاسخ سوال اول
async def received_programming(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    context.user_data['programming'] = user_choice
    
    # سوال دوم
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

# دریافت پاسخ سوال دوم
async def received_important(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    context.user_data['important'] = user_choice
    
    # سوال سوم
    keyboard = [[KeyboardButton(subject)] for subject in subjects_list]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        "در کدام درس‌ها احساس ضعف می‌کنید؟",
        reply_markup=reply_markup
    )
    
    return CHOICE_SUBJECTS

# دریافت پاسخ سوال سوم
async def received_subjects(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    context.user_data['subjects'] = user_choice
    
    # سوال چهارم
    keyboard = [
        [KeyboardButton("آزمون برای سنجش خودم")],
        [KeyboardButton("آزمون برای برنامه‌ریزی درسی")],
        [KeyboardButton("آزمون برای تقویت دروس ")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        "آزمون یکی از مهم ترین ابزار ها برای برنامه ریزی درسی است. به نظر شما هدف از شرکت در آزمون های قلم چی چیست؟",
        reply_markup=reply_markup
    )
    
    return CHOICE_GOAL

# دریافت پاسخ سوال چهارم
async def received_goal(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    context.user_data['goal'] = user_choice
    
    # سوال پنجم
    keyboard = [
        [KeyboardButton("وارد کردن شماره تماس")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        "برای دریافت مشاوره با رتبه های برتر کنکور و دریافت برنامه تحصیلی شماره تماس خود را وارد کنید.",
        reply_markup=reply_markup
    )
    
    return CHOICE_PHONE

# دریافت شماره تماس     
async def received_phone(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    context.user_data['phone'] = user_choice
    
    # پیغام پایانی
    if context.user_data['phone'] == "بله، وارد می‌کنم":
        await update.message.reply_text(
               " مشاورین ما به زودی با شما تماس خواهند گرفت. موفق باشید"
        )
    else:
        await update.message.reply_text(
            "ممنون! مشاور ما به زودی با شما تماس خواهد گرفت. موفق باشید!"
        )
    
    return ConversationHandler.END

# ساخت و راه‌اندازی ربات
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # استفاده از ConversationHandler برای مدیریت مراحل مختلف
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE_PROGRAMMING: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_programming)],
            CHOICE_IMPORTANT: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_important)],
            CHOICE_SUBJECTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_subjects)],
            CHOICE_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_goal)],
            CHOICE_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_phone)],
        },
        fallbacks=[],
    )

    # اضافه کردن ConversationHandler به اپلیکیشن
    application.add_handler(conv_handler)

    # راه‌اندازی ربات
    application.run_polling()

if __name__ == '__main__':
    main()
