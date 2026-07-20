import random
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8849687037:AAGVYH8sTkKwRQnzpnw2FNMURnyuZUga8Ho"

# --- الدوال البرمجية ---

async def start_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "✨ **قائمة أوامر بوت شاجو المتكاملة:**\n\n"
        "🌌 **أوامر التسلية:** /magic, /ai, /time, /power, /duel\n"
        "💍 **أوامر جديدة:** /marriage, /joke, /avatar, /del\n"
        "🔒 **أوامر المجموعة:** /lock, /unlock\n"
        "🛠 **أوامر الإدارة:** /mute, /ban, /kick, /mention"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"👋 أهلاً بك يا {member.full_name} في مجموعتنا!")

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and ("http://" in update.message.text or "https://" in update.message.text or "t.me/" in update.message.text):
        await update.message.delete()

# --- الدوال الخيالية والجديدة ---

async def marriage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    partners = ["أحمد", "سارة", "محمد", "نور", "علي", "ليلى"]
    await update.message.reply_text(f"💍 مبروك! لقد تزوجت من {random.choice(partners)}")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jokes = ["مرة واحد راح للبقالة قال له عندك خبز؟ قال له لا.. قال له طيب عندك خبز؟", "محشش سألوه ليش الثلج يذوب؟ قال عشان خايف من الصيف!"]
    await update.message.reply_text(random.choice(jokes))

async def avatar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photos = await user.get_profile_photos()
    if photos.total_count > 0:
        await update.message.reply_photo(photos.photos[0][0].file_id)
    else:
        await update.message.reply_text("ليس لديك صورة شخصية.")

async def delete_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()

# --- أوامر القفل والفتح ---
async def lock_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.set_chat_permissions(chat_id=update.effective_chat.id, permissions=ChatPermissions(can_send_messages=False))
    await update.message.reply_text("🔒 تم قفل المجموعة.")

async def unlock_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.set_chat_permissions(chat_id=update.effective_chat.id, permissions=ChatPermissions(can_send_messages=True))
    await update.message.reply_text("🔓 تم فتح المجموعة.")

# --- أوامر الإدارة ---
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(f"🚫 تم حظر {target.first_name}")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        await context.bot.unban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(f"🚪 تم طرد {target.first_name}")

# --- دالة التشغيل الرئيسية ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # تسجيل جميع الأوامر
    app.add_handler(CommandHandler(["start", "help"], start_help))
    app.add_handler(CommandHandler("marriage", marriage))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("avatar", avatar))
    app.add_handler(CommandHandler("del", delete_msg))
    app.add_handler(CommandHandler("lock", lock_group))
    app.add_handler(CommandHandler("unlock", unlock_group))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("kick", kick_user))

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_links))

    print("🚀 شاجو بوت المتفاعل يعمل بكامل أوامره!")
    app.run_polling()

if __name__ == "__main__":
    main()
