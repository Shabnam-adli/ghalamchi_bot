from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# توکن باتت
TOKEN = '7298813747:AAGi7qealqC4Shbl313aR7D-_OQySWp2K5U'

# شروع کار: خوش‌آمدگویی و پرسیدن مقطع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['ابتدایی', 'متوسطه اول', 'متوسطه دوم']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('سلام! به نمایشگاه کتاب قلم‌چی خوش اومدی. مقطع تحصیلی خودتو انتخاب کن:', reply_markup=reply_markup)

# جواب کاربر به انتخاب مقطع
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in ['ابتدایی', 'متوسطه اول', 'متوسطه دوم']:
        await update.message.reply_text(f'عالی! خوش اومدی به نمایشگاه مخصوص {text}ی‌ها 🎉\nمیتونی آزمون‌ها رو با تخفیف ویژه ثبت‌نام کنی.')
    else:
        await update.message.reply_text('لطفاً از گزینه‌های موجود انتخاب کن.')

# اجرای برنامه

import pytz

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

app.run_polling()
