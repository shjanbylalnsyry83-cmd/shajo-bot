
import random
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8849687037:AAGVYH8sTkKwRQnzpnw2FNMURnyuZUga8Ho"

# --- القائمة الشاملة ---
async def الاوامر(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "✨ **قائمة أوامر بوت شاجو:**\n\n"
        "🛠 **الإدارة:** /حظر، /طرد، /كتم، /منشن\n"
        "🎲 **التسلية:** /نسبة_الحب، /نرد، /عملة، /تحدي، /اقتباس، /تسلية\n"
        "🔮 **أخرى:** /سحر، /ذكاء، /زمن، /قوة، /مبارزة، /زواج، /نكتة، /صورة، /حذف، /قفل، /فتح"
    )
    await update.message.reply_text(msg)

# --- الدوال البرمجية ---
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
    await update.message.reply_text(f"⚡ التحدي: {random.choice([ ارسل صورة ,  غير اسمك ,  غنّي ])}")

async def اقتباس(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💡 حكمة: {random.choice([ العلم نور ,  النجاح رحلة ])}")

# --- التشغيل ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # قائمة الأوامر
    cmds = [
        ("الاوامر", الاوامر), ("حظر", حظر), ("طرد", طرد), ("كتم", كتم), 
        ("منشن", منشن), ("نسبة_الحب", نسبة_الحب), ("نرد", نرد), 
        ("عملة", عملة), ("تحدي", تحدي), ("اقتباس", اقتباس)
    ]
    
    for name, func in cmds:
        app.add_handler(CommandHandler(name, func))
        
    app.run_polling()

if __name__ == "__main__":
    main()
