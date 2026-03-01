import os
import random
from telebot import TeleBot, types

TOKEN = os.environ.get("TOKEN")

CHANNEL_USERNAME = "@bodadraws"
ADMIN_ID = 2109926990  # ده انت 👑

bot = TeleBot(TOKEN)

participants = {}
banned_users = set()
available_numbers = list(range(1, 1001))


# ✅ فحص الاشتراك
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ✅ رسالة الاشتراك
def send_subscription_message(chat_id):
    markup = types.InlineKeyboardMarkup()

    join_btn = types.InlineKeyboardButton(
        "إشتراك",
        url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
    )

    check_btn = types.InlineKeyboardButton(
        "تحقق من إشتراكي",
        callback_data="check_sub"
    )

    markup.add(join_btn)
    markup.add(check_btn)

    bot.send_message(
        chat_id,
        "من فضلك إشترك في القناه لإستخدام البوت",
        reply_markup=markup
    )


# ✅ /start
@bot.message_handler(commands=['start'])
def start(message):
    if not check_subscription(message.from_user.id):
        send_subscription_message(message.chat.id)
        return

    bot.send_message(
        message.chat.id,
        "🔥 سحب على 660 شدة ببجي 🔥\n\n"
        "🎯 للدخول اكتب:\n"
        "/entering_the_draw\n\n"
        "📊 لعرض المشاركين:\n"
        "/participants"
    )


# ✅ تحقق الاشتراك
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_subscription(call):
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "تم التحقق بنجاح ✅")
        bot.send_message(call.message.chat.id, "🔥 يمكنك الآن استخدام البوت")
    else:
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "❌ عذراً لم يتم الإشتراك في القناه"
        )


# ✅ دخول السحب
@bot.message_handler(commands=['entering_the_draw'])
def enter_draw(message):
    user_id = message.from_user.id

    if user_id in banned_users:
        bot.send_message(message.chat.id, "⛔ أنت محظور من المشاركة في السحب.")
        return

    if not check_subscription(user_id):
        send_subscription_message(message.chat.id)
        return

    if user_id in participants:
        bot.send_message(message.chat.id, "❌ لقد دخلت السحب بالفعل.")
        return

    bot.send_message(
        message.chat.id,
        "برجاء إدخال الإسم الذي تريد دخول السحب به 👇"
    )

    bot.register_next_step_handler(message, save_name)


def save_name(message):
    user_id = message.from_user.id
    entered_name = message.text.strip()

    if user_id in participants:
        return

    for data in participants.values():
        if data["name"].lower() == entered_name.lower():
            bot.send_message(
                message.chat.id,
                "❌ عذراً هذا الإسم مأخوذ بالفعل\nبرجاء إختيار اسم آخر"
            )
            return

    if not available_numbers:
        bot.send_message(message.chat.id, "❌ انتهت أرقام السحب.")
        return

    number = random.choice(available_numbers)
    available_numbers.remove(number)

    participants[user_id] = {
        "name": entered_name,
        "number": number
    }

    bot.send_message(
        message.chat.id,
        f"✅ تم دخول السحب بإسم: {entered_name}\n🎟 رقمك في السحب: {number}"
    )


# ✅ عرض المشاركين
@bot.message_handler(commands=['participants'])
def show_participants(message):

    if not participants:
        bot.send_message(message.chat.id, "❌ لا يوجد مشاركين حالياً.")
        return

    text = f"📊 عدد المشتركين: {len(participants)}\n\n"
    text += "📋 قائمة المشاركين:\n\n"

    for data in participants.values():
        text += f"👤 {data['name']} - 🎟 {data['number']}\n"

    bot.send_message(message.chat.id, text)


# ✅ حظر مستخدم (أمر للأدمن فقط)
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text.split()[1])
        banned_users.add(user_id)

        if user_id in participants:
            del participants[user_id]

        bot.send_message(message.chat.id, "✅ تم حظر المستخدم من السحب.")
    except:
        bot.send_message(message.chat.id, "اكتب بالشكل ده:\n/ban 123456789")


# ✅ فك حظر
@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text.split()[1])
        banned_users.discard(user_id)
        bot.send_message(message.chat.id, "✅ تم فك الحظر.")
    except:
        bot.send_message(message.chat.id, "اكتب بالشكل ده:\n/unban 123456789")


bot.infinity_polling()
