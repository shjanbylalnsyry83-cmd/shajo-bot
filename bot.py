
import os
import random
import sqlite3
from datetime import datetime, timedelta
from telegram import Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# الإعدادات وقاعدة البيانات
# =========================
TOKEN = os.getenv(8849687037:AAGOnOMbLqC3BJW-b86w6jbgS7Whl_Eeyi0)
OWNER_ID =7316796900

db = sqlite3.connect("bot_data.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 0)"
)
db.commit()

إعدادات = {}
رسائل_سبام = {}
سجل_العمليات = []
قفل_الروابط = True
قفل_الصور = False

# =========================
# الدوال المساعدة
# =========================
async def هل_مشرف(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await context.bot.get_chat_member(
        update.effective_chat.id, update.effective_user.id
    )
    return member.status in ["administrator", "creator"]

async def مالك(update: Update):
    return update.effective_user.id == OWNER_ID

def حالة_المجموعة(chat_id):
    if chat_id not in إعدادات:
        إعدادات[chat_id] = {"ترحيب": True, "حماية": True}
    return إعدادات[chat_id]

async def تسجيل_عملية(نص):
    سجل_العمليات.append(نص)

# =========================
# قائمة الأوامر والمساعدة
# =========================
async def مساعدة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **أوامر بوت شاجو الاحترافية:**\n\n"
        "👑 **الإدارة:**\n"
        "/حظر - /طرد - /كتم - /فك_الكتم\n"
        "/كتم_مؤقت - /حظر_مؤقت - /تحذير - /الغاء_التحذير\n"
        "/حذف - /تثبيت - /المشرفين - /سجل_الادارة\n\n"
        "⚙️ **الإعدادات وقفل المجموعات:**\n"
        "/الاعدادات - /تفعيل_الترحيب - /تعطيل_الترحيب\n"
        "/تفعيل_الحماية - /تعطيل_الحماية - /قفل الروابط - /فتح الروابط\n\n"
        "🎮 **الألعاب والترفيه:**\n"
        "/نرد - /عملة - /حظ - /شخصية - /احزر - /سؤال - /اختيار\n"
        "/تحدي - /نسبة_الحب - /نكتة - /حقيقة - /حجر_ورقة_مقص - /دعاء - /اقتباس\n\n"
        "🏆 **النقاط والمستويات:**\n"
        "/نقاطي - /مستوى - /ترتيب\n\n"
        "ℹ️ **المعومات والخدمات:**\n"
        "/ايدي - /اسمي - /حالة - /الوقت - /عشوائي - /بنج\n"
        "/معلومات_المجموعة - /ايدي_المجموعة - /عدد_الاعضاء - /معلومات - /اذاعة"
    )

# =========================
# أوامر الإدارة والمشرفين
# =========================
async def حظر(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return await update.message.reply_text("❌ للمشرفين فقط")
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, uid)
        await update.message.reply_text("🚫 تم حظر العضو")
        await تسجيل_عملية(f"حظر المستخدم {uid}")

async def طرد(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return await update.message.reply_text("❌ للمشرفين فقط")
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(update.effective_chat.id, uid)
        await context.bot.unban_chat_member(update.effective_chat.id, uid)
        await update.message.reply_text("🚪 تم طرد العضو")
        await تسجيل_عملية(f"طرد المستخدم {uid}")

async def كتم(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return await update.message.reply_text("❌ للمشرفين فقط")
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        await context.bot.restrict_chat_member(
            update.effective_chat.id, uid, ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text("🔇 تم كتم العضو")

async def فك_الكتم(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return await update.message.reply_text("❌ للمشرفين فقط")
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            uid,
            ChatPermissions(can_send_messages=True, can_send_other_messages=True),
        )
        await update.message.reply_text("🔊 تم فك الكتم")

async def كتم_مؤقت(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return await update.message.reply_text("❌ للمشرفين فقط")
    if update.message.reply_to_message and context.args:
        دقائق = int(context.args[0])
        uid = update.message.reply_to_message.from_user.id
        وقت = datetime.now() + timedelta(minutes=دقائق)
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            uid,
            ChatPermissions(can_send_messages=False),
            until_date=وقت,
        )
        await update.message.reply_text(f"🔇 تم كتم العضو لمدة {دقائق} دقيقة")

async def حظر_مؤقت(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return await update.message.reply_text("❌ للمشرفين فقط")
    if update.message.reply_to_message and context.args:
        دقائق = int(context.args[0])
        uid = update.message.reply_to_message.from_user.id
        وقت = datetime.now() + timedelta(minutes=دقائق)
        await context.bot.ban_chat_member(
            update.effective_chat.id, uid, until_date=وقت
        )
        await update.message.reply_text(f"🚫 تم حظر العضو لمدة {دقائق} دقيقة")

async def تحذير(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return await update.message.reply_text("❌ للمشرفين فقط")
    if update.message.reply_to_message:
        العضو = update.message.reply_to_message.from_user.first_name
        await update.message.reply_text(f"⚠️ تم تحذير {العضو}")

async def الغاء_التحذير(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return await update.message.reply_text("❌ للمشرفين فقط")
    await update.message.reply_text("✅ تم إلغاء التحذير")

async def قائمة_المشرفين(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    نص = "👑 المشرفين:\n\n"
    for admin in admins:
        نص += f"• {admin.user.first_name}\n"
    await update.message.reply_text(نص)

async def تثبيت(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return await update.message.reply_text("❌ للمشرفين فقط")
    if update.message.reply_to_message:
        await context.bot.pin_chat_message(
            update.effective_chat.id, update.message.reply_to_message.message_id
        )
        await update.message.reply_text("📌 تم التثبيت")

async def حذف(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return await update.message.reply_text("❌ للمشرفين فقط")
    if update.message.reply_to_message:
        await context.bot.delete_message(
            update.effective_chat.id, update.message.reply_to_message.message_id
        )

async def سجل_الادارة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return await update.message.reply_text("❌ للمشرفين فقط")
    if not سجل_العمليات:
        return await update.message.reply_text("📋 لا يوجد سجل")
    نص = "📋 آخر العمليات:\n\n" + "\n".join([f"• {x}" for x in سجل_العمليات[-10:]])
    await update.message.reply_text(نص)

# =========================
# الإعدادات والقفل
# =========================
async def الاعدادات(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context):
        return
    حالة = حالة_المجموعة(update.effective_chat.id)
    await update.message.reply_text(
        f"⚙️ إعدادات المجموعة:\n\n"
        f"👋 الترحيب: { مفعل ✅  if حالة[ ترحيب ] else  متوقف ❌ }\n"
        f"🛡️ الحماية: { مفعلة ✅  if حالة[ حماية ] else  متوقفة ❌ }"
    )

async def تفعيل_الترحيب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context): return
    حالة_المجموعة(update.effective_chat.id)["ترحيب"] = True
    await update.message.reply_text("👋 تم تفعيل الترحيب")

async def تعطيل_الترحيب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context): return
    حالة_المجموعة(update.effective_chat.id)["ترحيب"] = False
    await update.message.reply_text("👋 تم تعطيل الترحيب")

async def تفعيل_الحماية(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context): return
    حالة_المجموعة(update.effective_chat.id)["حماية"] = True
    await update.message.reply_text("🛡️ تم تفعيل الحماية")

async def تعطيل_الحماية(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await هل_مشرف(update, context): return
    حالة_المجموعة(update.effective_chat.id)["حماية"] = False
    await update.message.reply_text("🛡️ تم تعطيل الحماية")

async def قفل(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global قفل_الروابط
    if not await هل_مشرف(update, context): return
    if context.args and context.args[0] == "الروابط":
        قفل_الروابط = True
        await update.message.reply_text("🔒 تم قفل الروابط")

async def فتح(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global قفل_الروابط
    if not await هل_مشرف(update, context): return
    if context.args and context.args[0] == "الروابط":
        قفل_الروابط = False
        await update.message.reply_text("🔓 تم فتح الروابط")

# =========================
# ألعاب وتسلية
# =========================
async def نرد(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_dice(update.effective_chat.id)

async def عملة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🪙 النتيجة: {random.choice([ ملك ,  كتابة ])}")

async def حظ(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🍀 نسبة حظك اليوم: {random.randint(0, 100)}%")

async def شخصية(update: Update, context: ContextTypes.DEFAULT_TYPE):
    شخصيات = ["👑 القائد", "🔥 المغامر", "🧠 العبقري", "😂 المرح"]
    await update.message.reply_text(f"🎭 شخصيتك: {random.choice(شخصيات)}")

async def احزر(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🎯 خمن رقم بين 1 و 10\n(الرقم السري كان: {random.randint(1, 10)})")

async def سؤال(update: Update, context: ContextTypes.DEFAULT_TYPE):
    اسئلة = ["🌍 ما أكبر قارة في العالم؟", "🦁 ما أسرع حيوان بري؟", "🌙 كم عدد أشهر السنة؟"]
    await update.message.reply_text(random.choice(اسئلة))

async def اختيار(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(["نعم ✅", "لا ❌", "ربما 🤔"]))

async def تحدي(update: Update, context: ContextTypes.DEFAULT_TYPE):
    تحديات = ["😂 اكتب نكتة", "📸 أرسل صورة", "🎤 أرسل تسجيل صوتي", "⭐ اكتب حكمة"]
    await update.message.reply_text(f"⚡ التحدي: {random.choice(تحديات)}")

async def نسبة_الحب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"❤️ نسبة المحبة: {random.randint(0, 100)}%")

async def نكتة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    نكت = [
        "😂 مرة واحد راح للدكتور قال له: كل ما أشرب شاي عيني توجعني... قال له طلع الملعقة من الكوب.",
        "🤣 بخيل دخل مطعم قال للنادل: عندك شوربة اليوم؟ قال نعم، قال ممتاز سخنها لبكرة."
    ]
    await update.message.reply_text(random.choice(نكت))

async def حقيقة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    حقائق = ["🌍 الأرض تدور حول الشمس.", "🐝 النحل يتواصل بالرقص.", "🌊 الماء يغطي أغلب سطح الأرض."]
    await update.message.reply_text(random.choice(حقائق))

async def حجر_ورقة_مقص(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🎮 اخترت لك: {random.choice([ 🪨 حجر ,  📄 ورقة ,  ✂️ مقص ])}")

async def دعاء(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ادعية = ["🤲 اللهم ارزقنا الخير والتوفيق.", "🤲 اللهم اجعل أيامنا فرحًا وسعادة."]
    await update.message.reply_text(random.choice(ادعية))

async def اقتباس(update: Update, context: ContextTypes.DEFAULT_TYPE):
    اقتباسات = ["العلم نور", "النجاح يحتاج صبر", "ابتسم للحياة", "كل بداية صعبة"]
    await update.message.reply_text(f"💡 {random.choice(اقتباسات)}")

# =========================
# نظام النقاط والمستويات
# =========================
async def نقاطي(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⭐ اجمع النقاط من التفاعل داخل المجموعة")

async def مستوى(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
    cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    res = cursor.fetchone()
    نقاط = res[0] if res else 0
    db.commit()
    lvl = (نقاط // 10) + 1
    await update.message.reply_text(f"🏆 معلوماتك:\n\n⭐ النقاط: {نقاط}\n🎖 المستوى: {lvl}")

async def ترتيب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT user_id, points FROM users ORDER BY points DESC LIMIT 10")
    النتائج = cursor.fetchall()
    نص = "🏆 أفضل الأعضاء:\n\n"
    for i, (user_id, points) in enumerate(النتائج, 1):
        نص += f"{i}- 🥇 {user_id} : {points} نقطة\n"
    await update.message.reply_text(نص)

# =========================
# معلومات وخدمات البوت
# =========================
async def ايدي(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 ايديك هو:\n{update.effective_user.id}")

async def اسمي(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👤 اسمك: {update.effective_user.first_name}")

async def حالة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 البوت يعمل بنجاح ✅")

async def الوقت(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🕒 الوقت الآن: {datetime.now().strftime( %H:%M:%S )}")

async def عشوائي(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🎲 رقمك العشوائي: {random.randint(1, 100)}")

async def بنج(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 البوت يعمل\n✅ Online")

async def معلومات_المجموعة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await update.message.reply_text(
        f"🏠 معلومات المجموعة:\n\nالاسم: {chat.title}\nالايدي: {chat.id}\nالنوع: {chat.type}"
    )

async def ايدي_المجموعة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 ايدي المجموعة:\n{update.effective_chat.id}")

async def عدد_الاعضاء(update: Update, context: ContextTypes.DEFAULT_TYPE):
    عدد = await context.bot.get_chat_member_count(update.effective_chat.id)
    await update.message.reply_text(f"👥 عدد الأعضاء: {عدد}")

async def معلومات(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await update.message.reply_text(
            f"👤 معلومات العضو:\n\nالاسم: {user.first_name}\nالمعرف: {user.id}\nاسم المستخدم: @{user.username}"
        )

async def اذاعة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await مالك(update):
        return await update.message.reply_text("❌ هذا الأمر للمالك فقط")
    if not context.args:
        return await update.message.reply_text("اكتب الرسالة بعد الأمر")
    الرسالة = " ".join(context.args)
    await update.message.reply_text(f"📢 تم طلب إرسال الإذاعة: {الرسالة}")

# =========================
# الأحداث والردود والتنظيف
# =========================
async def ترحيب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        for user in update.message.new_chat_members:
            await update.message.reply_text(
                f"🎉 أهلاً بك {user.first_name}\nنتمنى لك وقتًا ممتعًا معنا ❤️"
            )

async def منع_الروابط(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not قفل_الروابط: return
    if update.message.text:
        نص = update.message.text.lower()
        if "http" in نص or "t.me" in نص:
            try:
                await update.message.delete()
                await update.message.reply_text("🚫 ممنوع إرسال الروابط هنا")
            except:
                pass

async def منع_الصور(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if قفل_الصور and update.message.photo:
        try:
            await update.message.delete()
        except:
            pass

async def ردود(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    كلمة = update.message.text.lower()
    قاموس_الردود = {
        "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته 🌹",
        "مرحبا": "أهلاً وسهلاً بك ❤️",
        "بوت": "🤖 أنا بوت شاجو جاهز للخدمة",
        "شكرا": "العفو 🌹 تحت أمرك"
    }
    for سؤال, جواب in قاموس_الردود.items():
        if سؤال in كلمة:
            await update.message.reply_text(جواب)
            break

# =========================
# التشغيل الرئيسي
# =========================
def main():
    if not TOKEN:
        print("❌ لم يتم العثور على BOT_TOKEN في متغيرات البيئة!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # تسجيل الأوامر
    cmds = [
        ("مساعدة", مساعدة), ("الاوامر", مساعدة), ("بنج", بنج),
        ("حظر", حظر), ("طرد", طرد), ("كتم", كتم), ("فك_الكتم", فك_الكتم),
        ("كتم_مؤقت", كتم_مؤقت), ("حظر_مؤقت", حظر_مؤقت), ("تحذير", تحذير),
        ("الغاء_التحذير", الغاء_التحذير), ("المشرفين", قائمة_المشرفين),
        ("تثبيت", تثبيت), ("حذف", حذف), ("سجل_الادارة", سجل_الادارة),
        ("الاعدادات", الاعدادات), ("تفعيل_الترحيب", تفعيل_الترحيب),
        ("تعطيل_الترحيب", تعطيل_الترحيب), ("تفعيل_الحماية", تفعيل_الحماية),
        ("تعطيل_الحماية", تعطيل_الحماية), ("قفل", قفل), ("فتح", فتح),
        ("نرد", نرد), ("عملة", عملة), ("حظ", حظ), ("شخصية", شخصية),
        ("احزر", احزر), ("سؤال", سؤال), ("اختيار", اختيار), ("تحدي", تحدي),
        ("نسبة_الحب", نسبة_الحب), ("نكتة", نكتة), ("حقيقة", حقيقة),
        ("حجر_ورقة_مقص", حجر_ورقة_مقص), ("دعاء", دعاء), ("اقتباس", اقتباس),
        ("نقاطي", نقاطي), ("مستوى", مستوى), ("ترتيب", ترتيب),
        ("ايدي", ايدي), ("اسمي", اسمي), ("حالة", حالة), ("الوقت", الوقت),
        ("عشوائي", عشوائي), ("معلومات_المجموعة", معلومات_المجموعة),
        ("ايدي_المجموعة", ايدي_المجموعة), ("عدد_الاعضاء", عدد_الاعضاء),
        ("معلومات", معلومات), ("اذاعة", اذاعة)
    ]

    for name, func in cmds:
        app.add_handler(CommandHandler(name, func))

    # تسجيل المعالجات الفرعية
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, ترحيب))
    app.add_handler(MessageHandler(filters.PHOTO, منع_الصور))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, منع_الروابط))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ردود))

    print("✅ تم تشغيل البوت بنجاح بجميع الأوامر...")
    app.run_polling()

if __name__ == "__main__":
    main()
