import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# 1. خادم ويب خفيف لإرضاء Render في الخطة المجانية
app = Flask(__name__)

@app.route('/')
def home():
    return "الموظف الخارق يعمل بنجاح 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# 2. إعدادات البوت والذكاء الاصطناعي
logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
أنت الموظف الخارق والمساعد التنفيذي لمدير ترويج الاستثمار بوزارة التجارة والصناعة وترويج الاستثمار بمحافظة ظفار.
مهامك ومبادئك:
1. التحدث حصرياً باللغة العربية الفصحى الرسمية والرصينة.
2. مساعدة المدير في صياغة الخطابات، المبادرات الاستراتيجية، وإعداد بطاقات الفرص.
3. الالتزام بالدقة وعدم تقديم معلومات دون التأكد من منطقيتها ووثوقيتها.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    user_message = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3
        )
        reply_text = response.choices[0].message.content
        await update.message.reply_text(reply_text)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء المعالجة: {str(e)}")

def run_bot():
    if not TELEGRAM_BOT_TOKEN:
        return
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    # تشغيل خادم الويب في مسار خلفي
    threading.Thread(target=run_flask).start()
    # تشغيل البوت
    run_bot()
