import os
import random
from telebot import TeleBot, types

TOKEN = os.environ.get("TOKEN")

CHANNEL_USERNAME = "@bodadraws"
ADMIN_ID = 2109926990          # 👑 انت
ADMIN_USERNAME = "abdallahmalhosseiny"  # من غير @

bot = TeleBot(TOKEN)

participants = {}
banned_users = set()
available_numbers = list(range(1, 1001))


# =========================
# ✅ فحص الاشتراك
# =========================
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# =========================
# ✅ رسالة الاشتراك
# =========================
def send_subscription_message(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔔 إشتراك",
            url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            "✅ تحقق من إشتراكي",
            callback_data="check_sub"
        )
    )

    bot.send_message(
        chat_id,
        "من فضلك إشترك في القناه لإستخدام البوت",
        reply_markup=markup
    )


# =========================
# 👑 القائمة الرئيسية
# =========================
def main_menu(chat_id, is_admin=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🎯 دخول السحب")
    markup.add("📊 عرض المشاركين")
    markup.add("ℹ️ معلومات السحب")
    markup.add("📞 تواصل مع الإدارة")

    if is_admin:
        markup.add("🏆 اختيار فائز")
        markup.add("📋 إدارة المشاركين")

    bot.send_message(chat_id, "اختر من القائمة 👇", reply_markup=markup)


# =========================
# /start
# =========================
@bot.message_handler(commands=['start'])
def start(message):
    if not check_subscription(message.from_user.id):
        send_subscription_message(message.chat.id)
        return

    is_admin = message.from_user.id == ADMIN_ID
    main_menu(message.chat.id, is_admin)


# =========================
# تحقق الاشتراك
# =========================
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_subscription(call):
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "تم التحقق بنجاح ✅")
        is_admin = call.from_user.id == ADMIN_ID
        main_menu(call.message.chat.id, is_admin)
    else:
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "❌ لم يتم الإشتراك بعد.")


# =========================
# 🎯 دخول السحب
# =========================
@bot.message_handler(func=lambda m: m.text == "🎯 دخول السحب")
def enter_draw(message):
    user_id = message.from_user.id

    if user_id in banned_users:
        bot.send_message(message.chat.id, "⛔ أنت محظور من السحب.")
        return

    if user_id in participants:
        bot.send_message(message.chat.id, "❌ لقد دخلت السحب بالفعل.")
        return

    bot.send_message(message.chat.id, "اكتب الاسم الذي تريد دخول السحب به 👇")
    bot.register_next_step_handler(message, save_name)


def save_name(message):
    user_id = message.from_user.id
    name = message.text.strip()

    if user_id in participants:
        return

    for data in participants.values():
        if data["name"].lower() == name.lower():
            bot.send_message(message.chat.id, "❌ الاسم مأخوذ بالفعل.")
            return

    if not available_numbers:
        bot.send_message(message.chat.id, "❌ انتهت أرقام السحب.")
        return

    number = random.choice(available_numbers)
    available_numbers.remove(number)

    participants[user_id] = {"name": name, "number": number}

    bot.send_message(
        message.chat.id,
        f"✅ تم التسجيل بإسم: {name}\n🎟 رقمك: {number}"
    )


# =========================
# 📊 عرض المشاركين
# =========================
@bot.message_handler(func=lambda m: m.text == "📊 عرض المشاركين")
def show_participants(message):
    if not participants:
        bot.send_message(message.chat.id, "لا يوجد مشاركين حالياً.")
        return

    text = f"📊 عدد المشتركين: {len(participants)}\n\n"
    for data in participants.values():
        text += f"👤 {data['name']} - 🎟 {data['number']}\n"

    bot.send_message(message.chat.id, text)


# =========================
# ℹ️ معلومات السحب
# =========================
@bot.message_handler(func=lambda m: m.text == "ℹ️ معلومات السحب")
def draw_info(message):
    bot.send_message(
        message.chat.id,
        "🔥 السحب على 660 شدة ببجي\n"
        "🎟 كل شخص يحصل على رقم عشوائي\n"
        "🏆 سيتم اختيار فائز واحد عشوائياً"
    )


# =========================
# 🏆 اختيار فائز (أدمن فقط)
# =========================
@bot.message_handler(func=lambda m: m.text == "🏆 اختيار فائز")
def pick_winner(message):
    if message.from_user.id != ADMIN_ID:
        return

    if not participants:
        bot.send_message(message.chat.id, "لا يوجد مشاركين.")
        return

    winner = random.choice(list(participants.values()))

    bot.send_message(
        message.chat.id,
        f"🏆 الفائز هو:\n\n"
        f"👤 {winner['name']}\n"
        f"🎟 رقم: {winner['number']}"
    )


# =========================
# 📋 إدارة المشاركين (أدمن)
# =========================
@bot.message_handler(func=lambda m: m.text == "📋 إدارة المشاركين")
def manage_participants(message):
    if message.from_user.id != ADMIN_ID:
        return

    if not participants:
        bot.send_message(message.chat.id, "❌ لا يوجد مشاركين.")
        return

    for user_id, data in participants.items():
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                "🚫 إقصاء من السحب",
                callback_data=f"remove_{user_id}"
            )
        )

        bot.send_message(
            message.chat.id,
            f"👤 {data['name']} - 🎟 {data['number']}",
            reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_"))
def remove_user_callback(call):
    if call.from_user.id != ADMIN_ID:
        return

    user_id = int(call.data.split("_")[1])

    if user_id in participants:
        available_numbers.append(participants[user_id]["number"])
        del participants[user_id]

        bot.edit_message_text(
            "✅ تم إقصاء المستخدم من السحب.",
            call.message.chat.id,
            call.message.message_id
        )
    else:
        bot.answer_callback_query(call.id, "المستخدم غير موجود.")


# =========================
# 📞 تواصل مع الإدارة
# =========================
@bot.message_handler(func=lambda m: m.text == "📞 تواصل مع الإدارة")
def contact_admin(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "✉️ إرسال رسالة للإدارة",
            callback_data="contact_admin"
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            "🔗 فتح حساب الإدارة",
            url=f"https://t.me/{ADMIN_USERNAME}"
        )
    )

    bot.send_message(
        message.chat.id,
        "اختر طريقة التواصل 👇",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "contact_admin")
def contact_step(call):
    bot.send_message(call.message.chat.id, "اكتب رسالتك للإدارة 👇")
    bot.register_next_step_handler(call.message, forward_to_admin)


def forward_to_admin(message):
    text = (
        f"📩 رسالة جديدة من مستخدم\n\n"
        f"👤 الاسم: {message.from_user.first_name}\n"
        f"🆔 ID: {message.from_user.id}\n\n"
        f"📝 الرسالة:\n{message.text}"
    )

    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ تم إرسال رسالتك للإدارة.")


bot.infinity_polling()
