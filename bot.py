
import random
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8849687037:AAGVYH8sTkKwRQnzpnw2FNMURnyuZUga8Ho"

# --- القائمة الشاملة ---
async def الاوامر(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "✨ **قائمة أوامر بوت شاجو المتكاملة:**\n\n"
        "🛠 **أوامر الإدارة:**\n"
        "• /حظر : حظر عضو\n• /طرد : طرد عضو\n• /كتم : كتم عضو\n• /منشن : تنبيه الجميع\n\n"
        "🎲 **أوامر التسلية والترفيه:**\n"
        "• /نسبة_الحب : قياس الحب\n• /نرد : رمي النرد\n• /عملة : رمي العملة\n• /تحدي : تحدي عشوائي\n"
        "• /اقتباس : حكمة اليوم\n• /تسلية : نصيحة ترفيهية\n\n"
        "🔮 **أوامر خيالية:**\n"
        "• /سحر /ذكاء /زمن /قوة /مبارزة /زواج /نكتة /صورة /حذف /قفل /فتح"
    )
    await update.message.reply_text(msg)

# --- دوال الإدارة ---
async def حظر(update, context):
    if update.message.reply_to_message:
        await context.bot.ban_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🚫 تم الحظر.")

async def طرد(update, context):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, uid)
        await context.bot.unban_chat_member(update.effective_chat.id, uid)
        await update.message.reply_text("🚪 تم الطرد.")

async def كتم(update, context):
    if update.message.reply_to_message:
        await context.bot.restrict_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False))
        await update.message.reply_text("🔇 تم الكتم.")

async def منشن(update, context):
    await update.message.reply_text("📣 @everyone تنبيه للجميع!")

# --- دوال التسلية ---
async def نسبة_الحب(update, context):
    percent = random.randint(0, 100)
    await update.message.reply_text(f"❤️ نسبة المحبة: {percent}%")

async def نرد(update, context): await context.bot.send_dice(update.effective_chat.id)
async def عملة(update, context): await update.message.reply_text(f"🪙 النتيجة: {random.choice([ ملك ,  كتابة ])}")
async def تحدي(update, context): await update.message.reply_text(f"⚡ التحدي: {random.choice([ ارسل صورة ,  غير اسمك ,  غنّي ])}")
async def اقتباس(update, context): await update.message.reply_text(f"💡 حكمة: {random.choice([ العلم نور ,  النجاح رحلة ])}")
async def تسلية(update, context): await update.message.reply_text("🌟 ابتسم، الحياة جميلة!")

# --- التشغيل ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    handlers = [
        ("الاوامر", الاوامر), ("حظر", حظر), ("طرد", طرد), ("كتم", كتم), ("منشن", منشن),
        ("نسبة_الحب", نسبة_الحب), ("نرد", نرد), ("عملة", عملة), ("تحدي", تحدي),
        ("اقتباس", اقتباس), ("تسلية", تسلية)
    ]
    for cmd, func in handlers: app.add_handler(CommandHandler(cmd, func))
    app.run_polling()

if __name__ == "__main__":
    main()
