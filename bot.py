
import random
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8849687037:AAGVYH8sTkKwRQnzpnw2FNMURnyuZUga8Ho"

# --- الدوال ---
async def الاوامر(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "✨ بوت شاجو يعمل! الأوامر: /حظر /طرد /كتم /منشن /نسبة_الحب /نرد /عملة /تحدي /اقتباس"
    await update.message.reply_text(msg)

async def حظر(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await context.bot.ban_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🚫 تم الحظر.")

async def طرد(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, uid)
        await context.bot.unban_chat_member(update.effective_chat.id, uid)
        await update.message.reply_text("🚪 تم الطرد.")

async def كتم(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await context.bot.restrict_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False))
        await update.message.reply_text("🔇 تم الكتم.")

async def منشن(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📣 @everyone تنبيه للجميع!")

async def نسبة_الحب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"❤️ نسبة المحبة: {random.randint(0, 100)}%")

async def نرد(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_dice(update.effective_chat.id)

async def عملة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🪙 النتيجة: {random.choice([ ملك ,  كتابة ])}")

async def تحدي(update: Update, context: ContextTypes.DEFAULT_TYPE):
    خيارات = ["ارسل صورة سيلفي", "غير اسمك", "اكتب نكتة"]
    await update.message.reply_text(f"⚡ التحدي: {random.choice(خيارات)}")

async def اقتباس(update: Update, context: ContextTypes.DEFAULT_TYPE):
    حكم = ["العلم نور", "النجاح رحلة", "ابتسم للحياة"]
    await update.message.reply_text(f"💡 حكمة: {random.choice(حكم)}")

# --- التشغيل ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("الاوامر", الاوامر))
    app.add_handler(CommandHandler("حظر", حظر))
    app.add_handler(CommandHandler("طرد", طرد))
    app.add_handler(CommandHandler("كتم", كتم))
    app.add_handler(CommandHandler("منشن", منشن))
    app.add_handler(CommandHandler("نسبة_الحب", نسبة_الحب))
    app.add_handler(CommandHandler("نرد", نرد))
    app.add_handler(CommandHandler("عملة", عملة))
    app.add_handler(CommandHandler("تحدي", تحدي))
    app.add_handler(CommandHandler("اقتباس", اقتباس))
        
    app.run_polling()

if __name__ == "__main__":
    main()
