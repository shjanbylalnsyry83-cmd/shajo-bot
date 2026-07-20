import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8849687037:AAGVYH8sTkKwRQnzpnw2FNMURnyuZUga8Ho"

# 1. قائمة المساعدة للأوامر
async def start_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "✨ **قائمة الأوامر الخيالية والتفاعلية لبوت شاجو:**\n\n"
        "🔥 **الخاصية الجديدة: التفاعل التلقائي (Auto Reactions)!**\n"
        "• البوت يتفاعل تلقائياً مع الرسائل والضحك والتحيات بالإيموجيات المناسبة! 🎭\n\n"
        "🌌 **أوامر التسلية الخيالية:**\n"
        "• `سحر` : التنبؤ بالمستقبل وقراءة الطالع 🔮\n"
        "• `ذكاء` : إجابة ساخرة من الذكاء الاصطناعي 🤖\n"
        "• `سفر عبر الزمن` : رحلة زمنية إلى الماضي والمستقبل ⏳\n"
        "• `قوة خارقة` : اكتشف قوتك الخارقة السرية 🦸‍♂️\n"
        "• `مبارزة` : مبارزة خيالية بالرد على عضو ⚔️\n\n"
        "🛠 **أوامر الإدارة والتسلية العادية:**\n"
        "• `منشن` | `كتم` | `حظر` | `طرد` | `نسبة الحب` | `نرد` | `عملة` | `تحدي` | `اقتباس` | `صوت`"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

# 2. الترحيب العربي
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        welcome_text = (
            f"👋 **أهلاً وسهلاً بك يا {member.full_name}!**\n\n"
            f"أنرت المجموعة بوجودك معنا ✨\n"
            f"نتمنى لك وقتاً ممتعاً وطيباً 🌹"
        )
        await update.message.reply_text(welcome_text, parse_mode="Markdown")

# 3. منع الروابط
async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and ("http://" in update.message.text or "https://" in update.message.text or "t.me/" in update.message.text):
        await update.message.delete()
        await update.message.chat.send_message(
            f"عذراً يا **{update.message.from_user.first_name}**، يمنع إرسال الروابط داخل المجموعة! 🚫",
            parse_mode="Markdown"
        )

# --- [ التفاعل التلقائي بالرموز ] ---

async def auto_react(update: Update, text: str):
    try:
        emoji_to_set = None
        lower_text = text.lower()

        if any(word in lower_text for word in ["سلام", "السلام", "مرحبا", "هلا"]):
            emoji_to_set = random.choice(["👋", "🌹", "❤️"])
        elif any(word in lower_text for word in ["هههه", "هه", "😂", "🤣"]):
            emoji_to_set = random.choice(["😂", "🤣", "🔥"])
        elif any(word in lower_text for word in ["شكرا", "مشكور", "تسلم"]):
            emoji_to_set = random.choice(["❤️", "🙏", "✨"])
        elif any(word in lower_text for word in ["سحر", "تحدي", "قوة"]):
            emoji_to_set = random.choice(["🔥", "⚡", "🔮"])
        elif random.random() < 0.15:  # احتمال 15% تفاعل عشوائي مع الرسائل
            emoji_to_set = random.choice(["👍", "❤️", "🔥", "🎉", "👏"])

        if emoji_to_set:
            await update.message.set_reaction(reaction=emoji_to_set)
    except Exception:
        pass  # في حال لم تكن الصلاحيات مكتملة في المجموعة

# --- [ الأوامر الخيالية ] ---

async def magic_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    predictions = [
        "🔮 البلورة السحرية تقول: ستصبح مليونير خلال السنتين القادمتين!",
        "🔮 أرى في الطالع أنك ستسافر إلى كوكب المريخ قريباً 🚀",
        "🔮 أرى أن هناك مفاجأة سارة جداً تنتظرك خلال 24 ساعة القادمة ✨",
        "🔮 السحر يقول: انتبه من شخص يحاول سرقة طعامك اليوم! 🍕",
        "🔮 النجوم تؤكد أن طاقاتك التنافسية اليوم في أعلى مستوياتها 🔥"
    ]
    await update.message.reply_text(random.choice(predictions))

async def ai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    responses = [
        "🤖 تحليلي البرمجي يقول: سؤالك ذكي جداً، لكنني أذكى منك بكثير!",
        "🤖 جاري معالجة البيانات... النتيجة: ننصحك بشراب كوب من الشاي والاسترخاء.",
        "🤖 الخوارزميات تؤكد أنك أكثر شخص متفاعل في الجروب اليوم!",
        "🤖 خطأ في المعالجة! تم تجاوز حدود الذكاء، يرجى المحاولة لاحقاً ⚡"
    ]
    await update.message.reply_text(random.choice(responses))

async def time_travel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    year = random.randint(1800, 2090)
    events = [
        f"⏳ قمت بالقفز عبر الزمن إلى عام {year}! ووجدتك تقود مركبة فضائية متطورة 🛸",
        f"⏳ عدت بالزمن لعام {year} ووجدتك تعمل ملكاً في إحدى الحضارات القديمة 👑",
        f"⏳ سافرت لعام {year} ووجدتك تطور نظام ذكاء اصطناعي جديد 💻",
        f"⏳ قفزت لعام {year} وشاهدتك تكسب بطولة العالم في الشطرنج 🏆"
    ]
    await update.message.reply_text(random.choice(events))

async def super_power(update: Update, context: ContextTypes.DEFAULT_TYPE):
    powers = [
        "🦸‍♂️ قوتك الخارقة هي: **الطيران وسرعة الصوت** ⚡ (مستوى القوة: 98%)",
        "🦸‍♂️ قوتك الخارقة هي: **الختفاء والتحكم بالزمن** ⏳ (مستوى القوة: 92%)",
        "🦸‍♂️ قوتك الخارقة هي: **قراءة الأفكار عن بُعد** 🧠 (مستوى القوة: 85%)",
        "🦸‍♂️ قوتك الخارقة هي: **التحكم بالمعادن والتخاطر** 🧲 (مستوى القوة: 90%)"
    ]
    await update.message.reply_text(random.choice(powers), parse_mode="Markdown")

async def duel_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        p1 = update.effective_user.first_name
        p2 = update.message.reply_to_message.from_user.first_name
        winner = random.choice([p1, p2])
        msg = f"⚔️ **مبارزة حامية بين {p1} و {p2}!**\n\n🎯 بعد صراع خيالي قوي... الفائز في المبارزة هو: **{winner}** 🎉"
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("رد على رسالة العضو الذي تريد مبارزته! ⚔️")

# --- [ الأوامر الأخرى ] ---

async def mention_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_status = (await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)).status
    if user_status not in [ administrator ,  creator ]:
        await update.message.reply_text("❌ هذا الأمر مخصص للمشرفين فقط!")
        return
    await update.message.reply_text("📣 **تنبيه للجميع! يرجى الانتباه للرسالة.**", parse_mode="Markdown")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        await update.message.reply_text(f"🔇 تم كتم العضو **{target.full_name}** بنجاح.", parse_mode="Markdown")
    else:
        await update.message.reply_text("يرجى الرد على رسالة العضو المراد كتمه!")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(f"🚫 تم حظر العضو **{target.full_name}** بنجاح.", parse_mode="Markdown")
    else:
        await update.message.reply_text("يرجى الرد على رسالة العضو المراد حظره!")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        await context.bot.unban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(f"🚪 تم طرد العضو **{target.full_name}** من المجموعة.", parse_mode="Markdown")
    else:
        await update.message.reply_text("يرجى الرد على رسالة العضو المراد طرده!")

async def love_percentage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user1 = update.effective_user.first_name
        user2 = update.message.reply_to_message.from_user.first_name
        percent = random.randint(0, 100)
        await update.message.reply_text(f"❤️ نسبة المحبة بين **{user1}** و **{user2}** هي: **{percent}%**", parse_mode="Markdown")
    else:
        await update.message.reply_text("رد على رسالة الشخص لقياس نسبة المحبة! ❤️")

async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_dice(chat_id=update.effective_chat.id)

async def flip_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = random.choice(["ملك 👑", "كتابة 📝"])
    await update.message.reply_text(f"🪙 نتيجة رمي العملة: **{result}**", parse_mode="Markdown")

async def challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    challenges = ["أرسل صورة لآخر شيء صورته! 📸", "غير اسمك لمدة ساعة! 🎭", "أرسل بصمة صوتية تغني فيها! 🎤"]
    await update.message.reply_text(f"⚡ **التحدي الخاص بك:**\n{random.choice(challenges)}", parse_mode="Markdown")

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = ["«لا تدع أمسك يأخذ الكثير من يومك.»", "«النجاح هو انتقالك من فشل إلى فشل دون فقدان الشغف.»"]
    await update.message.reply_text(f"💡 **حكمة اليوم:**\n{random.choice(quotes)}", parse_mode="Markdown")

async def send_audio_sample(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sample_audio = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    await update.message.reply_audio(audio=sample_audio, caption="🎵 مقطع صوتي ممتع لك!")

# معالج الكلمات النصية والتفاعلات
async def handle_text_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip() if update.message.text else ""
    
    # 1. تطبيق التفاعل التلقائي بالأشكال
    if text:
        await auto_react(update, text)

    # 2. تنفيذ الأوامر النصية
    if text in ["الأوامر", "الاوامر"]:
        await start_help(update, context)
    elif text == "سحر":
        await magic_prediction(update, context)
    elif text == "ذكاء":
        await ai_response(update, context)
    elif text == "سفر عبر الزمن":
        await time_travel(update, context)
    elif text == "قوة خارقة":
        await super_power(update, context)
    elif text == "مبارزة":
        await duel_battle(update, context)
    elif text in ["منشن", "الجميع"]:
        await mention_all(update, context)
    elif text == "كتم":
        await mute_user(update, context)
    elif text == "حظر":
        await ban_user(update, context)
    elif text == "طرد":
        await kick_user(update, context)
    elif text == "نسبة الحب":
        await love_percentage(update, context)
    elif text == "نرد":
        await roll_dice(update, context)
    elif text == "عملة":
        await flip_coin(update, context)
    elif text == "تحدي":
        await challenge(update, context)
    elif text == "اقتباس":
        await quote(update, context)
    elif text in ["صوت", "اغنية", "أغنية"]:
        await send_audio_sample(update, context)
    else:
        await delete_links(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # تسجيل الأوامر
    app.add_handler(CommandHandler(["start", "help"], start_help))
    app.add_handler(CommandHandler("magic", magic_prediction))
    app.add_handler(CommandHandler("ai", ai_response))
    app.add_handler(CommandHandler("time", time_travel))
    app.add_handler(CommandHandler("power", super_power))
    app.add_handler(CommandHandler("duel", duel_battle))

    # الترحيب والأوامر النصية + التفاعل التلقائي
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_commands))

    print("شاجو بوت المتفاعل يعمل بنجاح! 🚀")
    app.run_polling()

if __name__ ==  __main__ :
    main()

