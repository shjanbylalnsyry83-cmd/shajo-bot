
​​🌑🤎import random
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات ---
TOKEN = os.getenv(
    8849687037:AAF7U-0YOK3dhakr5JOm9SMUnPpOPkMSN_Y)

# --- قائمة الأوامر الاحترافية ---
async def مساعدة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🤖 أوامر بوت شاجو

👑 الإدارة:
 /حظر /طرد /كتم /فك_الكتم /كتم_مؤقت /حظر_مؤقت /تحذير /حذف /تثبيت /المشرفين

⚙️ الإعدادات:
 /الاعدادات /تفعيل_الترحيب /تعطيل_الترحيب /تفعيل_الحماية /تعطيل_الحماية

🎮 الألعاب:
 /نرد /عملة /حظ /شخصية /احزر /سؤال /تحدي

🏆 النقاط:
 /نقاط /مستوى /ترتيب

ℹ️ معلومات:
 /ايدي /اسمي /حالة /الوقت /نقاطي /عشوائي
""")

# --- الردود التلقائية ---
async def ردود(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text: return
    كلمة = update.message.text.lower()
    ردود_قاموس = {
        "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته 🌹",
        "مرحبا": "أهلاً وسهلاً بك ❤️",
        "بوت": "🤖 أنا بوت شاجو جاهز للخدمة",
        "شكرا": "العفو 🌹 تحت أمرك"
    }
    for سؤال, جواب in ردود_قاموس.items():
        if سؤال in كلمة:
            await update.message.reply_text(جواب)
            break

# --- الأوامر المضافة حديثاً ---
async def نقاطي(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⭐ اجمع النقاط من التفاعل داخل المجموعة")

async def الوقت(update: Update, context: ContextTypes.DEFAULT_TYPE):
    الآن = datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(f"🕒 الوقت الآن: {الآن}")

async def عشوائي(update: Update, context: ContextTypes.DEFAULT_TYPE):
    أرقام = random.randint(1, 100)
    await update.message.reply_text(f"🎲 رقمك العشوائي: {أرقام}")

# --- التشغيل ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # تسجيل الأوامر
    cmds = [
        ("مساعدة", مساعدة), ("نقاطي", نقاطي), 
        ("الوقت", الوقت), ("عشوائي", عشوائي)
    ]
    for name, func in cmds:
        app.add_handler(CommandHandler(name, func))

    # معالج النصوص
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ردود))

    print("✅ البوت يعمل")
    app.run_polling()

if __name__ == "__main__":
    main()

