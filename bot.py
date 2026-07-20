
import random
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv(8849687037:AAF7U-0YOK3dhakr5JOm9SMUnPpOPkMSN_Y)

async def مساعدة(update, context):
    await update.message.reply_text("🤖 أوامر بوت شاجو:\n/حظر /طرد /كتم /نرد /عملة /وقت /نقاطي /عشوائي")

async def ردود(update, context):
    if not update.message or not update.message.text: return
    text = update.message.text.lower()
    if "سلام" in text: await update.message.reply_text("وعليكم السلام 🌹")
    elif "بوت" in text: await update.message.reply_text("🤖 أنا هنا!")

async def الوقت(update, context):
    await update.message.reply_text(f"🕒 الوقت: {datetime.now().strftime( %H:%M:%S )}")

async def عشوائي(update, context):
    await update.message.reply_text(f"🎲 رقم عشوائي: {random.randint(1, 100)}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("مساعدة", مساعدة))
    app.add_handler(CommandHandler("وقت", الوقت))
    app.add_handler(CommandHandler("عشوائي", عشوائي))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ردود))
    
    app.run_polling()

if __name__ == "__main__":
    main()
