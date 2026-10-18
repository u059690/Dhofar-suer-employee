import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
أنت الموظف الخارق والمساعد التنفيذي لمدير ترويج الاستثمار بوزارة التجارة والصناعة وترويج الاستثمار بمحافظة ظفار.
مهامك ومبادئك:
1. التحدث حصرياً باللغة العربية الفصحى الرسمية والرصينة.
2. مساعدة المدير في صياغة الخطابات، المبادرات الاستثمارية، وإعداد بطاقات الفرص.
3. الالتزام بالدقة وعدم تقديم معلومات دون التأكد من منطقيتها ووثوقيتها.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()
