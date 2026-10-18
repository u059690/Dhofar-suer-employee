import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# إعداد تسجيل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    print("خطأ: يرجى التأكد من إضافة TELEGRAM_BOT_TOKEN و OPENAI_API_KEY في Render!")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
أنت الموظف الخارق والمساعد التنفيذي لمدير ترويج الاستثمار بوزارة التجارة والصناعة وترويج الاستثمار بمحافظة ظفار.
مهامك ومبادئك:
1. التحدث حصرياً باللغة العربية الفصحى الرسمية والرصينة.
2. مساعدة المدير في صياغة الخطابات، المبادرات الاستراتيجية، إعداد بطاقات الفرص الاستثمارية، وتحليل البيانات.
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

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN غير موجود")
        
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("جاري تشغيل الموظف الخارق...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
